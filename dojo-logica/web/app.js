(() => {
  "use strict";

  const state = {
    estado: null,
    conceitos: {},
    dataAtual: null,
    conjuntoAtual: 0,
    questaoIdx: 0,
    questao: null,
    timerRascunho: null,
    lab: {
      codigo: "",
      passos: [],
      indice: 0,
      timerAuto: null,
    },
    simulado: {
      ativo: null,
      indice: 0,
      respostas: {},
      restanteSeg: 0,
      inicioTs: 0,
      timer: null,
    },
    contaModo: "entrar",
    modalConceitoId: null,
  };

  const $ = (sel) => document.querySelector(sel);
  const $$ = (sel) => Array.from(document.querySelectorAll(sel));

  // ==================== UTILITÁRIOS DE API & HTML ====================
  async function api(url, opcoes = {}) {
    const metodo = (opcoes.method || "GET").toUpperCase();
    let dados;
    if (window.DojoBridge && window.DojoBridge.isStatic()) {
      dados = await window.DojoBridge.request(url, opcoes);
    } else {
      const cfg = {
        headers: { "Content-Type": "application/json" },
        ...opcoes,
      };
      const resp = await fetch(url, cfg);
      dados = await resp.json();
      if (!resp.ok || dados.falha) {
        throw new Error(dados.falha || `Erro HTTP ${resp.status}`);
      }
    }

    // Dispara sync em nuvem após mutações de estado (sem bloquear UI)
    const ehMutacao =
      metodo === "POST" &&
      !url.startsWith("/api/executar") &&
      !url.startsWith("/api/rastrear");
    if (ehMutacao && window.DojoCloud && window.DojoCloud.isLoggedIn()) {
      window.DojoCloud.schedulePush(apiSemSync);
    }
    return dados;
  }

  async function apiSemSync(url, opcoes = {}) {
    if (window.DojoBridge && window.DojoBridge.isStatic()) {
      return await window.DojoBridge.request(url, opcoes);
    }
    const cfg = { headers: { "Content-Type": "application/json" }, ...opcoes };
    const resp = await fetch(url, cfg);
    const dados = await resp.json();
    if (!resp.ok || dados.falha) throw new Error(dados.falha || `Erro HTTP ${resp.status}`);
    return dados;
  }

  function escaparHtml(txt) {
    return String(txt ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function formatarInline(txt) {
    const partes = String(txt).split(/(`[^`]+`)/g);
    return partes
      .map((p) => {
        if (p.startsWith("`") && p.endsWith("`") && p.length >= 2) {
          return `<code>${escaparHtml(p.slice(1, -1))}</code>`;
        }
        return escaparHtml(p).replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
      })
      .join("");
  }

  function renderMiniMarkdown(texto) {
    if (!texto) return "";
    const blocos = String(texto).replace(/\r\n/g, "\n").split(/```(?:python|json)?\n?([\s\S]*?)```/g);
    let html = "";
    for (let i = 0; i < blocos.length; i++) {
      if (i % 2 === 1) {
        html += `<pre>${escaparHtml(blocos[i].replace(/\n$/, ""))}</pre>`;
        continue;
      }
      const paragrafos = blocos[i].trim().split(/\n\s*\n/);
      for (const p of paragrafos) {
        if (!p.trim()) continue;
        const linhas = p.split("\n");
        const ehLista = linhas.every((l) => /^\s*[-*]\s+/.test(l) || !l.trim());
        if (ehLista) {
          html +=
            "<ul>" +
            linhas
              .filter((l) => l.trim())
              .map((l) => `<li>${formatarInline(l.replace(/^\s*[-*]\s+/, ""))}</li>`)
              .join("") +
            "</ul>";
        } else {
          let emLista = false;
          let bufP = [];
          const fecharP = () => {
            if (bufP.length) {
              html += `<p>${bufP.map(formatarInline).join("<br>")}</p>`;
              bufP = [];
            }
          };
          for (const l of linhas) {
            if (/^\s*[-*]\s+/.test(l)) {
              fecharP();
              if (!emLista) {
                html += "<ul>";
                emLista = true;
              }
              html += `<li>${formatarInline(l.replace(/^\s*[-*]\s+/, ""))}</li>`;
            } else {
              if (emLista) {
                html += "</ul>";
                emLista = false;
              }
              bufP.push(l);
            }
          }
          if (emLista) html += "</ul>";
          fecharP();
        }
      }
    }
    return html;
  }

  function renderCodigoNumerado(codigo, linhaAtiva = null) {
    const linhas = String(codigo || "").replace(/\r\n/g, "\n").replace(/\n$/, "").split("\n");
    return linhas
      .map((l, idx) => {
        const num = idx + 1;
        const ativa = linhaAtiva === num ? " linha-ativa" : "";
        const seta = linhaAtiva === num ? "▶ " : "";
        return `<div class="codigo-linha${ativa}" data-linha="${num}"><span class="ln">${seta}${num}</span><span>${escaparHtml(l) || " "}</span></div>`;
      })
      .join("");
  }

  function toast(msg, tipo = "") {
    const el = document.createElement("div");
    el.className = `toast ${tipo}`;
    el.innerHTML = msg;
    $("#toasts").appendChild(el);
    setTimeout(() => el.remove(), 4600);
  }

  // ==================== NAVEGAÇÃO POR ABAS ====================
  function irParaAba(nome) {
    pararAutoLab();
    $$(".aba").forEach((b) => b.classList.toggle("ativa", b.dataset.aba === nome));
    $$(".painel-aba").forEach((s) => s.classList.toggle("ativo", s.id === `aba-${nome}`));
    if (nome === "trilha") renderTrilha();
    if (nome === "evolucao") renderEvolucao();
    if (nome === "entrevista") renderHistoricoSimulados();
  }

  // ==================== EDITOR DE CÓDIGO ====================
  function atualizarLinhas(textarea, preLinhas) {
    if (!textarea || !preLinhas) return;
    const n = Math.max(1, textarea.value.split("\n").length);
    const arr = [];
    for (let i = 1; i <= n; i++) arr.push(i);
    preLinhas.textContent = arr.join("\n");
  }

  function vincularEditor(textarea, preLinhas, aoMudar) {
    if (!textarea || !preLinhas) return;
    const sync = () => {
      atualizarLinhas(textarea, preLinhas);
      preLinhas.scrollTop = textarea.scrollTop;
    };
    textarea.addEventListener("input", () => {
      sync();
      if (aoMudar) aoMudar();
    });
    textarea.addEventListener("scroll", () => {
      preLinhas.scrollTop = textarea.scrollTop;
    });
    textarea.addEventListener("keydown", (e) => {
      if (e.key === "Tab") {
        e.preventDefault();
        const start = textarea.selectionStart;
        const end = textarea.selectionEnd;
        const val = textarea.value;
        if (start === end && !e.shiftKey) {
          textarea.value = val.slice(0, start) + "    " + val.slice(end);
          textarea.selectionStart = textarea.selectionEnd = start + 4;
        } else {
          const linIni = val.lastIndexOf("\n", start - 1) + 1;
          const linFimIdx = val.indexOf("\n", end);
          const linFim = linFimIdx === -1 ? val.length : linFimIdx;
          const bloco = val.slice(linIni, linFim).split("\n");
          const novo = bloco.map((l) => (e.shiftKey ? l.replace(/^ {1,4}/, "") : "    " + l)).join("\n");
          textarea.value = val.slice(0, linIni) + novo + val.slice(linFim);
          textarea.selectionStart = linIni;
          textarea.selectionEnd = linIni + novo.length;
        }
        sync();
        if (aoMudar) aoMudar();
      } else if (e.key === "Enter") {
        e.preventDefault();
        const start = textarea.selectionStart;
        const val = textarea.value;
        const linIni = val.lastIndexOf("\n", start - 1) + 1;
        const linhaAntes = val.slice(linIni, start);
        const espacos = (linhaAntes.match(/^ */) || [""])[0];
        const extra = linhaAntes.trimEnd().endsWith(":") ? "    " : "";
        const ins = "\n" + espacos + extra;
        textarea.value = val.slice(0, start) + ins + val.slice(textarea.selectionEnd);
        textarea.selectionStart = textarea.selectionEnd = start + ins.length;
        sync();
        if (aoMudar) aoMudar();
      }
    });
    sync();
  }

  // ==================== CARREGAMENTO DE ESTADO & PLANO ====================
  async function carregarEstado(data = null, manterIndice = false) {
    const q = data ? `?data=${encodeURIComponent(data)}` : "";
    const est = await api(`/api/estado${q}`);
    state.estado = est;
    state.dataAtual = est.data;
    if (state.conjuntoAtual >= est.conjuntos.length) state.conjuntoAtual = 0;

    if (est.novas_conquistas && est.novas_conquistas.length) {
      for (const c of est.novas_conquistas) {
        toast(`Nova conquista: <strong>${escaparHtml(c.nome)}</strong> — ${escaparHtml(c.desc)}`, "ouro");
      }
    }

    atualizarCabecalho();
    preencherSeletoresDia();
    renderRegua();

    const lista = est.conjuntos[state.conjuntoAtual] || [];
    if (!manterIndice) {
      const pendente = lista.findIndex((item) => item.status === "pendente");
      state.questaoIdx = pendente >= 0 ? pendente : 0;
    } else if (state.questaoIdx >= lista.length) {
      state.questaoIdx = 0;
    }

    if (lista.length > 0) {
      await abrirQuestao(lista[state.questaoIdx].id);
    }
  }

  function atualizarCabecalho() {
    const est = state.estado;
    if (!est) return;
    const estInfo = est.estagios.find((e) => e.n === est.estagio_atual) || est.estagios[0];
    $("#hdr-estagio-icone").textContent = estInfo.icone;
    $("#hdr-estagio-txt").textContent = `Estágio ${estInfo.n}: ${estInfo.nome}`;
    $("#hdr-streak").textContent = `${est.sequencia} ${est.sequencia === 1 ? "dia" : "dias"}`;
    $("#hdr-nivel").textContent = `Nv. ${est.nivel.nivel}`;
    $("#hdr-xp").textContent = `${est.xp} XP`;
    const pct = Math.min(100, Math.round((est.nivel.no_nivel / Math.max(1, est.nivel.para_proximo)) * 100));
    $("#hdr-xp-barra").style.width = `${pct}%`;

    const conj = est.conjuntos[state.conjuntoAtual] || [];
    const ok = conj.filter((x) => x.status === "resolvido").length;
    $("#hdr-hoje").textContent = `${ok}/${conj.length}`;
    $("#info-progresso-dia").textContent = `${ok} de ${conj.length} resolvidas`;
    $("#info-revisoes").textContent = `${est.fila_revisao} ${est.fila_revisao === 1 ? "revisão na fila" : "revisões na fila"}`;
  }

  function preencherSeletoresDia() {
    const est = state.estado;
    const selData = $("#seletor-data");
    selData.innerHTML = "";
    const dias = [...est.dias_com_plano].reverse();
    for (const d of dias) {
      const opt = document.createElement("option");
      opt.value = d;
      opt.textContent = d === est.hoje ? `Hoje (${d})` : d;
      if (d === est.data) opt.selected = true;
      selData.appendChild(opt);
    }

    const selConj = $("#seletor-conjunto");
    selConj.innerHTML = "";
    est.conjuntos.forEach((c, idx) => {
      const ok = c.filter((x) => x.status === "resolvido").length;
      const opt = document.createElement("option");
      opt.value = String(idx);
      const label =
        idx === 0
          ? `Treino Principal (${ok}/${c.length})`
          : c.length === 10
            ? `Treino Cirúrgico #${idx} (${ok}/${c.length})`
            : `Treino Extra #${idx} (${ok}/${c.length})`;
      opt.textContent = label;
      if (idx === state.conjuntoAtual) opt.selected = true;
      selConj.appendChild(opt);
    });
  }

  function renderRegua() {
    const est = state.estado;
    const lista = est.conjuntos[state.conjuntoAtual] || [];
    const wrap = $("#regua-questoes");
    wrap.innerHTML = "";
    lista.forEach((item, idx) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "q-pill";
      if (item.status === "resolvido") btn.classList.add("resolvido");
      if (item.status === "solucao") btn.classList.add("solucao");
      if (idx === state.questaoIdx) btn.classList.add("ativa");
      btn.dataset.origem = item.origem;
      btn.textContent = String(item.n);
      const origemNome =
        { aquecimento: "Aquecimento", revisao: "Revisão espaçada", novo: `Estágio ${item.estagio}`, desafio: "Desafio" }[
          item.origem
        ] || "";
      btn.title = `#${item.n} · ${item.titulo} (${item.tipo_nome} · ${origemNome} · Dif ${item.dificuldade}/5)`;
      btn.addEventListener("click", async () => {
        state.questaoIdx = idx;
        renderRegua();
        await abrirQuestao(item.id);
      });
      wrap.appendChild(btn);
    });
  }

  // ==================== QUESTÃO ATUAL ====================
  async function abrirQuestao(instId) {
    const q = await api(`/api/questao?id=${encodeURIComponent(instId)}`);
    state.questao = q;

    $("#q-num").textContent = `#${q.n}`;
    const mapaOrigem = {
      aquecimento: `Aquecimento (Est. ${q.estagio})`,
      revisao: `Revisão Espaçada (Est. ${q.estagio})`,
      novo: `Estágio ${q.estagio}`,
      desafio: `Desafio (Est. ${q.estagio})`,
    };
    const origEl = $("#q-origem");
    origEl.textContent = mapaOrigem[q.origem] || `Estágio ${q.estagio}`;
    origEl.className = `badge badge-origem ${q.origem}`;

    $("#q-tipo").textContent = q.tipo_nome;
    $("#q-dificuldade").textContent = "★".repeat(q.dificuldade) + "☆".repeat(5 - q.dificuldade);

    const stEl = $("#q-status");
    if (q.status === "resolvido") {
      stEl.textContent = `Resolvida (+${q.xp_ganho || 0} XP)`;
      stEl.className = "badge badge-status ok";
    } else if (q.status === "solucao") {
      stEl.textContent = "Gabarito visto";
      stEl.className = "badge badge-status sol";
    } else {
      stEl.textContent = "";
      stEl.className = "badge badge-status hidden";
    }

    $("#q-titulo").textContent = q.titulo;

    // Conceitos clicáveis
    const chips = $("#q-conceitos-chips");
    chips.innerHTML = "";
    for (const c of q.conceitos) {
      const b = document.createElement("button");
      b.type = "button";
      b.className = "chip-conceito";
      b.textContent = c.nome;
      b.title = c.resumo || "Clique para abrir a mini-lição";
      b.addEventListener("click", () => abrirModalConceito(c.id));
      chips.appendChild(b);
    }

    $("#q-enunciado").innerHTML = renderMiniMarkdown(q.enunciado);

    // Pensar Antes de Codar + Feynman
    const padrao = q.padrao || {};
    $("#pensar-contrato").value = padrao.contrato || "";
    $("#pensar-edges").value = padrao.edge_cases || "";
    $("#pensar-plano").value = padrao.plano || "";
    $("#input-feynman").value = padrao.feynman || "";
    $("#box-feynman").classList.toggle("hidden", q.status !== "resolvido");

    const mostrarPensar = q.tipo !== "prever";
    $("#box-pensar-primeiro").classList.toggle("hidden", !mostrarPensar);
    const temPlano = Boolean(padrao.contrato || padrao.edge_cases || padrao.plano);
    $("#pensar-corpo").classList.toggle("hidden", !temPlano);
    $("#btn-toggle-pensar").textContent = temPlano ? "Recolher" : "Expandir";

    // Dicas
    renderDicas(q.dicas_reveladas, q.dicas_total);

    // Gabarito se já resolvido ou visto
    if (q.solucao) {
      mostrarGabarito(q.solucao, q.explicacao, q.saida_correta, q.entrada_quebrar_exemplo);
    } else {
      $("#area-gabarito").classList.add("hidden");
      $("#area-gabarito").innerHTML = "";
    }

    $("#btn-ver-solucao").classList.toggle("hidden", Boolean(q.solucao));
    $("#area-resultado").classList.add("hidden");
    $("#area-resultado").innerHTML = "";
    $("#status-rascunho").textContent = "";

    // Alternar entre Código / Prever / Quebrar
    $("#box-editor-codigo").classList.add("hidden");
    $("#box-resposta-prever").classList.add("hidden");
    $("#box-resposta-quebrar").classList.add("hidden");
    $("#q-trecho-prever").classList.add("hidden");

    if (q.tipo === "prever") {
      $("#box-resposta-prever").classList.remove("hidden");
      $("#q-trecho-prever").classList.remove("hidden");
      $("#prever-bloco-titulo").textContent = "Leia e faça o teste de mesa do código abaixo:";
      $("#q-exemplos").innerHTML = "";
      $("#prever-codigo-linhas").innerHTML = renderCodigoNumerado(q.trecho);

      if (q.entrada_prever) {
        $("#prever-entrada-box").classList.remove("hidden");
        $("#prever-entrada-txt").textContent = q.entrada_prever;
      } else {
        $("#prever-entrada-box").classList.add("hidden");
      }

      $("#resposta-prever").value = q.codigo_salvo || "";
      $("#btn-rastrear-prever").classList.toggle("hidden", q.status === "pendente");
    } else if (q.tipo === "quebrar") {
      $("#box-resposta-quebrar").classList.remove("hidden");
      $("#q-trecho-prever").classList.remove("hidden");
      $("#prever-bloco-titulo").textContent = "Código com bug sutil — descubra qual entrada o quebra:";
      $("#prever-entrada-box").classList.add("hidden");
      $("#q-exemplos").innerHTML = "";
      $("#prever-codigo-linhas").innerHTML = renderCodigoNumerado(q.trecho);
      $("#resposta-quebrar").value = q.codigo_salvo || "";
      $("#resposta-quebrar").placeholder = q.placeholder_quebrar || "Digite a entrada que quebra o código...";
      $("#quebrar-instrucao").textContent =
        q.modo_quebrar === "args"
          ? `Digite os argumentos Python literais para ${q.funcao_quebrar}(...) que fazem o código bugado falhar ou divergir do esperado:`
          : "Digite as linhas de entrada (input) que fazem o código bugado ao lado falhar:";
    } else {
      $("#box-editor-codigo").classList.remove("hidden");

      const exBox = $("#q-exemplos");
      const metaBench = q.tem_benchmark ? " · Inclui medidor de Big-O" : "";
      exBox.innerHTML = `<div class="bloco-header"><span>Exemplo de validação (total de ${q.n_testes} teste${q.n_testes > 1 ? "s" : ""}${metaBench})</span></div>`;
      for (const ex of q.exemplos) {
        const div = document.createElement("div");
        div.className = "exemplo-card";
        const temIn = ex.entrada !== "";
        const temCham = Boolean(ex.chamada);
        let top = "";
        if (temIn || temCham) {
          top = `<div class="exemplo-grade">
            <div><strong>${temCham ? "Chamada" : "Entrada"}:</strong><pre>${escaparHtml(temCham ? ex.chamada : ex.entrada)}</pre></div>
            <div><strong>Saída esperada:</strong><pre>${escaparHtml(ex.saida)}</pre></div>
          </div>`;
        } else {
          top = `<div><strong>Saída esperada:</strong><pre>${escaparHtml(ex.saida)}</pre></div>`;
        }
        div.innerHTML = top;
        exBox.appendChild(div);
      }

      const editor = $("#editor-codigo");
      editor.value = q.codigo_salvo !== null && q.codigo_salvo !== undefined ? q.codigo_salvo : q.codigo_inicial || "";
      atualizarLinhas(editor, $("#editor-linhas"));

      const primeiraEntrada = q.exemplos[0]?.entrada || "";
      $("#entrada-teste").value = primeiraEntrada;
    }
  }

  function renderDicas(reveladas, total) {
    const btn = $("#btn-pedir-dica");
    btn.textContent = `Pedir dica (${reveladas.length}/${total})`;
    btn.disabled = reveladas.length >= total;
    const area = $("#area-dicas");
    if (!reveladas.length) {
      area.classList.add("hidden");
      area.innerHTML = "";
      return;
    }
    area.classList.remove("hidden");
    area.innerHTML = reveladas
      .map((d, i) => `<div class="dica-item"><strong>Dica ${i + 1}:</strong> ${formatarInline(d)}</div>`)
      .join("");
  }

  function mostrarGabarito(solucao, explicacao, saidaCorreta = null, exemploQuebrar = null) {
    const area = $("#area-gabarito");
    area.classList.remove("hidden");
    const ehPrever = state.questao && state.questao.tipo === "prever";
    const ehQuebrar = state.questao && state.questao.tipo === "quebrar";
    const titulo = ehPrever
      ? "Resposta correta e explicação"
      : ehQuebrar
        ? "Solução corrigida e caso que quebra o código"
        : "Gabarito comentado";

    let corpo = `<h4><span>${titulo}</span>`;
    if (!ehPrever && !ehQuebrar) {
      corpo += `<button class="btn btn-sec btn-xs" id="btn-lab-gabarito" type="button">Rastrear gabarito</button>`;
    }
    corpo += `</h4>`;

    if (ehPrever && saidaCorreta !== null && saidaCorreta !== undefined) {
      corpo += `<div class="mb-sm"><strong>Saída exata:</strong><pre class="codigo-bloco">${escaparHtml(saidaCorreta)}</pre></div>`;
    } else {
      if (ehQuebrar && exemploQuebrar) {
        corpo += `<div class="mb-sm"><strong>Exemplo de entrada que quebra o bug:</strong><pre class="codigo-bloco">${escaparHtml(exemploQuebrar)}</pre></div>`;
      }
      corpo += `<pre class="codigo-bloco">${escaparHtml(solucao)}</pre>`;
    }
    corpo += `<div>${renderMiniMarkdown(explicacao)}</div>`;
    area.innerHTML = corpo;

    const btnLab = $("#btn-lab-gabarito");
    if (btnLab) {
      btnLab.addEventListener("click", () => {
        const entrada = state.questao.exemplos?.[0]?.entrada || "";
        abrirNoLaboratorio(solucao, entrada);
      });
    }
  }

  function renderRaioX(raioX) {
    if (!raioX) return "";
    const q = raioX.qualidade || {};
    const ef = raioX.eficiencia || {};
    const met = q.metricas || {};
    const obsHtml = (q.observacoes || [])
      .map(
        (o) =>
          `<li class="${escaparHtml(o.severidade || "ok")}"><strong>${escaparHtml(o.titulo)}:</strong> ${formatarInline(o.detalhe)}</li>`
      )
      .join("");

    let benchBadge = "";
    if (ef.tem_benchmark) {
      const cls = ef.otimo ? "ok" : "sol";
      benchBadge = `<span class="badge badge-status ${cls}">Big-O empírico: ${escaparHtml(ef.classe)} (meta: ${escaparHtml(ef.esperado)})</span>`;
    } else if (ef.passos) {
      benchBadge = `<span class="badge">${ef.passos} passos executados</span>`;
    }

    const efFeedback = ef.feedback ? `<p class="texto-suave" style="margin:6px 0 0;">${escaparHtml(ef.feedback)}</p>` : "";

    return `
      <div class="raiox-card">
        <div class="raiox-topo">
          <strong>Raio-X do Engenheiro (Code Review AST &amp; Eficiência)</strong>
          <div class="raiox-badges">
            <span class="badge badge-status ${q.nota >= 85 ? "ok" : "sol"}">Qualidade: ${q.nota}/100 (${escaparHtml(q.nivel || "")})</span>
            <span class="badge">${met.linhas || 0} linhas · aninhamento ${met.aninhamento || 0}</span>
            ${benchBadge}
          </div>
        </div>
        ${efFeedback}
        <ul class="raiox-lista">${obsHtml}</ul>
      </div>
    `;
  }

  // ==================== EXECUÇÃO E VERIFICAÇÃO ====================
  async function executarCodigoAtual() {
    const codigo = $("#editor-codigo").value;
    const entrada = $("#entrada-teste").value;
    const resEl = $("#area-resultado");
    resEl.classList.remove("hidden");
    resEl.innerHTML = `<p class="texto-suave">Executando...</p>`;

    try {
      const r = await api("/api/executar", {
        method: "POST",
        body: JSON.stringify({ codigo, entrada }),
      });
      let html = `<div class="res-banner info"><span>Execução de teste</span><span>${r.tempo}s</span></div>`;
      if (r.saida) {
        html += `<pre class="saida-terminal">${escaparHtml(r.saida)}</pre>`;
      } else if (!r.erro) {
        html += `<p class="texto-suave">(O programa terminou sem imprimir nada na tela.)</p>`;
      }
      if (r.erro) {
        html += renderCardErro(r.erro);
      }
      resEl.innerHTML = html;
    } catch (err) {
      resEl.innerHTML = `<div class="erro-card">${escaparHtml(err.message)}</div>`;
    }
  }

  function renderCardErro(erro) {
    const lin = erro.linha ? ` (linha ${erro.linha})` : "";
    return `
      <div class="erro-card">
        <div class="erro-titulo">${escaparHtml(erro.tipo)}${lin}</div>
        <div class="erro-msg">${escaparHtml(erro.mensagem || "")}${erro.texto ? `\n→ ${escaparHtml(erro.texto)}` : ""}</div>
        <div class="erro-explicacao">${renderMiniMarkdown(erro.explicacao || "")}</div>
      </div>`;
  }

  async function verificarAtual() {
    const q = state.questao;
    if (!q) return;
    const ehPrever = q.tipo === "prever";
    const ehQuebrar = q.tipo === "quebrar";
    const payload = ehPrever
      ? { id: q.id, resposta: $("#resposta-prever").value }
      : ehQuebrar
        ? { id: q.id, resposta: $("#resposta-quebrar").value }
        : { id: q.id, codigo: $("#editor-codigo").value };

    const resEl = $("#area-resultado");
    resEl.classList.remove("hidden");
    resEl.innerHTML = `<p class="texto-suave">Rodando validação completa e Raio-X...</p>`;

    try {
      const r = await api("/api/verificar", {
        method: "POST",
        body: JSON.stringify(payload),
      });

      if (r.bug && window.DojoCloud && window.DojoCloud.isLoggedIn()) {
        window.DojoCloud.syncBug(r.bug);
      }

      const lista = state.estado.conjuntos[state.conjuntoAtual];
      const temProxima = state.questaoIdx < lista.length - 1;

      let html = "";
      if (r.passou) {
        const xpMsg = r.xp > 0 ? `+${r.xp} XP ganhos` : "Questão validada";
        const tituloOk = ehQuebrar ? `Código quebrado com sucesso! ${xpMsg}` : `Excelente! ${xpMsg}`;
        html += `<div class="res-banner ok">
          <span>${tituloOk}</span>
          ${temProxima ? `<button class="btn btn-primario btn-sm" id="btn-proxima-questao" type="button">Próxima questão →</button>` : ""}
        </div>`;
        if (r.solucao) {
          mostrarGabarito(r.solucao, r.explicacao, r.saida_correta, r.entrada_quebrar_exemplo);
        }
        $("#btn-ver-solucao").classList.add("hidden");
        if (ehPrever) $("#btn-rastrear-prever").classList.remove("hidden");
        $("#box-feynman").classList.remove("hidden");
      } else {
        const msgFalha = ehQuebrar
          ? `O código bugado sobreviveu a essa entrada (tentativa ${r.tentativas})`
          : `Ainda não bateu com o esperado (tentativa ${r.tentativas})`;
        html += `<div class="res-banner falha"><span>${msgFalha}</span></div>`;
      }

      for (const t of r.resultados) {
        const ok = t.status === "exato" || t.status === "quase";
        const tag = t.quebrar_modo
          ? ok
            ? "Bug exposto!"
            : "Saídas iguais (tente outra borda)"
          : {
              exato: "Exato",
              quase: "Aceito (atenção a espaços/maiúsculas)",
              diferente: "Saída diferente",
              erro: "Erro na execução",
            }[t.status];

        html += `<div class="teste-item ${ok ? "ok" : "falha"}">
          <div class="teste-topo"><span>${t.quebrar_modo ? "Teste de ataque" : `Caso de teste #${t.n}`}</span><span>${tag}</span></div>`;
        if (t.entrada || t.chamada) {
          html += `<div class="texto-suave" style="margin:0 0 6px;">${t.chamada ? `Chamada: <code>${escaparHtml(t.chamada)}</code>` : `Entrada: <code>${escaparHtml(t.entrada.replace(/\n/g, " ↵ "))}</code>`}</div>`;
        }
        if (t.erro) {
          html += renderCardErro(t.erro);
        } else if (t.quebrar_modo) {
          html += `<div class="teste-cols">
            <div><strong>Código bugado retornou:</strong><pre>${escaparHtml(t.obtido || "(vazio)")}</pre></div>
            <div><strong>Referência correta:</strong><pre>${escaparHtml(t.esperado || "(vazio)")}</pre></div>
          </div>`;
        } else if (!ok || t.status === "quase") {
          const esp =
            t.esperado !== null && t.esperado !== undefined
              ? `<pre>${escaparHtml(t.esperado)}</pre>`
              : `<pre>(tente novamente ou use uma dica)</pre>`;
          html += `<div class="teste-cols">
            <div><strong>Sua saída:</strong><pre>${escaparHtml(t.obtido || "(vazio)")}</pre></div>
            <div><strong>Saída esperada:</strong>${esp}</div>
          </div>`;
        }
        html += `</div>`;
      }

      if (r.raio_x) {
        html += renderRaioX(r.raio_x);
      }

      resEl.innerHTML = html;

      if (r.passou) {
        if (r.desbloqueou) {
          const estNovo = state.estado.estagios.find((e) => e.n === r.desbloqueou);
          toast(`<strong>Estágio ${r.desbloqueou} desbloqueado!</strong> ${estNovo ? escaparHtml(estNovo.nome) : ""}`, "verde");
        }
        if (r.concluiu_basico) {
          toast("<strong>Você concluiu os 13 estágios de Fundamentos!</strong> Avance para a Trilha de Entrevistas (Estágio 14+).", "ouro");
        }
        await carregarEstado(state.dataAtual, true);
        $("#area-resultado").classList.remove("hidden");
        $("#area-resultado").innerHTML = html;
        const btnProx2 = $("#btn-proxima-questao");
        if (btnProx2) {
          btnProx2.addEventListener("click", async () => {
            state.questaoIdx += 1;
            renderRegua();
            await abrirQuestao(state.estado.conjuntos[state.conjuntoAtual][state.questaoIdx].id);
          });
        }
      }
    } catch (err) {
      resEl.innerHTML = `<div class="erro-card">${escaparHtml(err.message)}</div>`;
    }
  }

  function agendarRascunho() {
    if (!state.questao || state.questao.tipo === "prever" || state.questao.tipo === "quebrar") return;
    $("#status-rascunho").textContent = "Salvando...";
    clearTimeout(state.timerRascunho);
    const id = state.questao.id;
    const codigo = $("#editor-codigo").value;
    state.timerRascunho = setTimeout(async () => {
      try {
        await api("/api/rascunho", {
          method: "POST",
          body: JSON.stringify({ id, codigo }),
        });
        $("#status-rascunho").textContent = "Rascunho salvo";
      } catch {
        $("#status-rascunho").textContent = "";
      }
    }, 650);
  }

  async function salvarPadraoAtual(notificarTexto = "Plano salvo no Caderno Mental.") {
    if (!state.questao) return;
    const payload = {
      id: state.questao.id,
      contrato: $("#pensar-contrato").value,
      edge_cases: $("#pensar-edges").value,
      plano: $("#pensar-plano").value,
      feynman: $("#input-feynman").value,
    };
    const r = await api("/api/padrao", { method: "POST", body: JSON.stringify(payload) });
    if (r.padrao && window.DojoCloud && window.DojoCloud.isLoggedIn()) {
      window.DojoCloud.syncPadrao(r.padrao);
    }
    toast(notificarTexto, "verde");
  }

  // ==================== MODAL DE MINI-LIÇÃO ====================
  function abrirModalConceito(cid) {
    const c = state.conceitos[cid];
    if (!c) return;
    state.modalConceitoId = cid;
    $("#modal-c-titulo").textContent = c.nome;
    $("#modal-c-resumo").textContent = c.resumo;
    $("#modal-c-explicacao").innerHTML = renderMiniMarkdown(c.explicacao);
    $("#modal-c-exemplo").textContent = c.exemplo;

    const ul = $("#modal-c-erros");
    ul.innerHTML = (c.erros_comuns || []).map((e) => `<li>${formatarInline(e)}</li>`).join("");
    $("#modal-c-erros-wrap").classList.toggle("hidden", !(c.erros_comuns && c.erros_comuns.length));

    $("#modal-c-dica").innerHTML = `<strong>Dica de ouro:</strong> ${formatarInline(c.dica_de_ouro || "")}`;
    $("#modal-conceito").classList.remove("hidden");
  }

  function fecharModalConceito() {
    $("#modal-conceito").classList.add("hidden");
  }

  // ==================== TRILHA & BIBLIOTECA ====================
  function renderTrilha() {
    const est = state.estado;
    if (!est) return;
    const container = $("#trilhas-container");
    container.innerHTML = "";

    const trilhas = est.trilhas || [{ id: "basico", nome: "Fundamentos", resumo: "", estagios: [1, 22] }];
    for (const tr of trilhas) {
      const bloco = document.createElement("div");
      bloco.className = "trilha-bloco";
      bloco.innerHTML = `
        <div class="trilha-bloco-header">
          <div>
            <h3>${escaparHtml(tr.nome)} (Estágios ${tr.estagios[0]} a ${tr.estagios[1]})</h3>
            <p class="texto-suave" style="margin:2px 0 0;">${escaparHtml(tr.resumo)}</p>
          </div>
        </div>
        <div class="grid-estagios"></div>
      `;
      const grid = bloco.querySelector(".grid-estagios");
      const listaEst = est.estagios.filter((e) => e.n >= tr.estagios[0] && e.n <= tr.estagios[1]);

      for (const e of listaEst) {
        const card = document.createElement("div");
        card.className = "card-estagio";
        if (e.n === est.estagio_atual) card.classList.add("atual");
        if (!e.liberado) card.classList.add("bloqueado");

        const pct = Math.min(100, Math.round((e.acertos / Math.max(1, e.meta)) * 100));
        const chips = (e.conceitos_info || [])
          .map((c) => `<button class="chip-conceito" type="button" data-cid="${c.id}">${escaparHtml(c.nome)}</button>`)
          .join("");

        let acaoHtml = "";
        if (e.n === est.estagio_atual) {
          acaoHtml = `<span class="badge badge-status ok">Estágio Atual</span>`;
        } else if (e.liberado) {
          acaoHtml = `<button class="btn btn-sec btn-sm btn-trocar-est" type="button" data-est="${e.n}">Estudar este estágio</button>`;
        } else {
          acaoHtml = `<span class="badge">Bloqueado</span>`;
        }

        card.innerHTML = `
          <div>
            <div class="est-topo">
              <span class="est-icone">${escaparHtml(e.icone)}</span>
              <div>
                <div class="est-titulo">Estágio ${e.n}: ${escaparHtml(e.nome)}</div>
                <div class="est-sub">${e.modelos} modelos paramétricos</div>
              </div>
            </div>
            <p class="est-resumo" style="margin-top:8px;">${escaparHtml(e.resumo)}</p>
          </div>
          <div>
            <div class="conceitos-chips" style="margin-bottom:10px;">${chips}</div>
            <div class="barra-progresso"><div style="width:${pct}%"></div></div>
            <div class="est-rodape" style="margin-top:8px;">
              <span>Domínio: ${e.acertos}/${e.meta} acertos</span>
              ${acaoHtml}
            </div>
          </div>
        `;

        card.querySelectorAll(".chip-conceito").forEach((b) => {
          b.addEventListener("click", () => abrirModalConceito(b.dataset.cid));
        });
        const btnEst = card.querySelector(".btn-trocar-est");
        if (btnEst) {
          btnEst.addEventListener("click", async () => {
            await api("/api/estagio", { method: "POST", body: JSON.stringify({ estagio: e.n }) });
            const reg = await api("/api/regenerar", { method: "POST", body: "{}" });
            await carregarEstado(est.hoje);
            if (reg.ok) {
              toast(`Estágio alterado para <strong>${e.n}: ${escaparHtml(e.nome)}</strong> e plano de hoje atualizado.`, "verde");
              irParaAba("treino");
            } else {
              toast(`Estágio alterado para <strong>${e.n}: ${escaparHtml(e.nome)}</strong>. Como você já começou o plano de hoje, clique em "+20 Questões Extras" para gerar um plano desse estágio agora.`);
              renderTrilha();
            }
          });
        }
        grid.appendChild(card);
      }

      container.appendChild(bloco);
    }

    renderBibliotecaConceitos();
  }

  function renderBibliotecaConceitos() {
    const termo = ($("#filtro-conceitos")?.value || "").trim().toLowerCase();
    const gridC = $("#grid-conceitos");
    gridC.innerHTML = "";
    let count = 0;
    for (const [cid, c] of Object.entries(state.conceitos)) {
      const alvo = `${c.nome} ${c.resumo} ${cid}`.toLowerCase();
      if (termo && !alvo.includes(termo)) continue;
      count++;
      const div = document.createElement("div");
      div.className = "card-conceito-bib";
      div.innerHTML = `<h4>${escaparHtml(c.nome)}</h4><p>${escaparHtml(c.resumo)}</p>`;
      div.addEventListener("click", () => abrirModalConceito(cid));
      gridC.appendChild(div);
    }
    if (!count) {
      gridC.innerHTML = `<p class="texto-suave">Nenhum conceito encontrado para "${escaparHtml(termo)}".</p>`;
    }
  }

  // ==================== SIMULADO DE ENTREVISTA ====================
  function formatarRelogio(seg) {
    const m = Math.floor(Math.max(0, seg) / 60);
    const s = Math.max(0, seg) % 60;
    return `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
  }

  function pararRelogioSimulado() {
    if (state.simulado.timer) {
      clearInterval(state.simulado.timer);
      state.simulado.timer = null;
    }
  }

  function salvarRascunhoSimuladoAtual() {
    const sim = state.simulado.ativo;
    if (!sim) return;
    const q = sim.questoes[state.simulado.indice];
    if (!q) return;
    state.simulado.respostas[q.n] = {
      n: q.n,
      codigo: $("#sim-editor").value,
      raciocinio: $("#sim-raciocinio").value,
    };
  }

  function renderQuestaoSimulado(idx) {
    const sim = state.simulado.ativo;
    if (!sim) return;
    salvarRascunhoSimuladoAtual();
    state.simulado.indice = idx;
    const q = sim.questoes[idx];

    const nav = $("#sim-nav-problemas");
    nav.innerHTML = sim.questoes
      .map(
        (item, i) =>
          `<button class="btn ${i === idx ? "btn-primario" : "btn-sec"} btn-sm" type="button" data-sim-idx="${i}">Problema ${item.n}</button>`
      )
      .join("");
    nav.querySelectorAll("button").forEach((b) => {
      b.addEventListener("click", () => renderQuestaoSimulado(Number(b.dataset.simIdx)));
    });

    $("#sim-q-num").textContent = `Problema ${q.n} de ${sim.questoes.length}`;
    $("#sim-q-tipo").textContent = q.tipo_nome;
    $("#sim-q-estagio").textContent = `Estágio ${q.estagio}`;
    $("#sim-q-titulo").textContent = q.titulo;
    $("#sim-q-enunciado").innerHTML = renderMiniMarkdown(q.enunciado);

    if (q.tipo === "quebrar") {
      $("#sim-q-trecho-wrap").classList.remove("hidden");
      $("#sim-q-trecho").innerHTML = renderCodigoNumerado(q.trecho || q.codigo_inicial);
      $("#sim-q-exemplos").innerHTML = "";
      $("#sim-editor-label").textContent = `Entrada de ataque (${q.funcao_quebrar || "input"})`;
      $("#sim-entrada-wrap").classList.add("hidden");
      $("#btn-sim-executar").classList.add("hidden");
    } else {
      $("#sim-q-trecho-wrap").classList.add("hidden");
      $("#sim-editor-label").textContent = "solucao_entrevista.py";
      $("#sim-entrada-wrap").classList.remove("hidden");
      $("#btn-sim-executar").classList.remove("hidden");
      const exHtml = (q.exemplos || [])
        .map(
          (ex) => `
          <div class="exemplo-card">
            <div class="exemplo-grade">
              <div><strong>${ex.chamada ? "Chamada" : "Entrada"}:</strong><pre>${escaparHtml(ex.chamada || ex.entrada || "(sem entrada)")}</pre></div>
              <div><strong>Saída esperada:</strong><pre>${escaparHtml(ex.saida)}</pre></div>
            </div>
          </div>`
        )
        .join("");
      $("#sim-q-exemplos").innerHTML = `<div class="bloco-header"><span>Exemplo visível (mais ${Math.max(0, q.n_testes - 1)} caso(s) oculto(s) na avaliação)</span></div>${exHtml}`;
    }

    const salvo = state.simulado.respostas[q.n];
    $("#sim-raciocinio").value = salvo ? salvo.raciocinio : "";
    $("#sim-editor").value = salvo ? salvo.codigo : q.tipo === "quebrar" ? "" : q.codigo_inicial || "";
    $("#sim-editor").placeholder =
      q.tipo === "quebrar" ? q.placeholder_quebrar || "Digite a entrada que quebra o código..." : "# Escreva sua solução limpa aqui...";
    atualizarLinhas($("#sim-editor"), $("#sim-linhas"));
    $("#sim-saida-rapida").classList.add("hidden");
    $("#sim-saida-rapida").innerHTML = "";
  }

  async function iniciarSimulado() {
    const trilha = $("#sim-trilha").value;
    const duracao = Number($("#sim-duracao").value);
    const btn = $("#btn-iniciar-simulado");
    btn.disabled = true;
    try {
      const sim = await api("/api/simulado/iniciar", {
        method: "POST",
        body: JSON.stringify({ trilha, duracao_min: duracao }),
      });
      state.simulado.ativo = sim;
      state.simulado.indice = 0;
      state.simulado.respostas = {};
      state.simulado.restanteSeg = sim.duracao_min * 60;
      state.simulado.inicioTs = Date.now();

      $("#sim-config").classList.add("hidden");
      $("#sim-resultado").classList.add("hidden");
      $("#sim-ativo").classList.remove("hidden");

      const rel = $("#sim-relogio");
      rel.textContent = formatarRelogio(state.simulado.restanteSeg);
      rel.classList.remove("urgente");
      pararRelogioSimulado();
      state.simulado.timer = setInterval(() => {
        state.simulado.restanteSeg -= 1;
        rel.textContent = formatarRelogio(state.simulado.restanteSeg);
        if (state.simulado.restanteSeg <= 300) rel.classList.add("urgente");
        if (state.simulado.restanteSeg <= 0) {
          pararRelogioSimulado();
          toast("Tempo esgotado! Avaliando sua entrega automaticamente...");
          encerrarSimulado(true);
        }
      }, 1000);

      renderQuestaoSimulado(0);
    } catch (err) {
      toast(`Erro ao iniciar simulado: ${escaparHtml(err.message)}`);
    } finally {
      btn.disabled = false;
    }
  }

  async function encerrarSimulado(automatico = false) {
    const sim = state.simulado.ativo;
    if (!sim) return;
    if (!automatico) {
      const ok = window.confirm("Deseja encerrar o simulado agora e avaliar todas as suas respostas contra os casos ocultos?");
      if (!ok) return;
    }
    salvarRascunhoSimuladoAtual();
    pararRelogioSimulado();

    const btn = $("#btn-encerrar-simulado");
    btn.disabled = true;
    try {
      const duracaoUsada = Math.round((Date.now() - state.simulado.inicioTs) / 1000);
      const respostas = sim.questoes.map((q) => state.simulado.respostas[q.n] || { n: q.n, codigo: "", raciocinio: "" });
      const boletim = await api("/api/simulado/avaliar", {
        method: "POST",
        body: JSON.stringify({ id: sim.id, respostas, duracao_usada_seg: duracaoUsada }),
      });

      if (window.DojoCloud && window.DojoCloud.isLoggedIn()) {
        window.DojoCloud.syncSimulado(boletim);
      }

      state.simulado.ativo = null;
      $("#sim-ativo").classList.add("hidden");
      renderBoletimSimulado(boletim);
      await carregarEstado(state.dataAtual, true);
    } catch (err) {
      toast(`Erro ao avaliar simulado: ${escaparHtml(err.message)}`);
    } finally {
      btn.disabled = false;
    }
  }

  function renderBoletimSimulado(b) {
    const el = $("#sim-resultado");
    el.classList.remove("hidden");
    const cls = b.nota_geral >= 70 ? "ok" : "falha";
    const detHtml = (b.detalhes || [])
      .map(
        (d) => `
        <div class="card mt-md">
          <div class="res-banner ${d.passou ? "ok" : "falha"}">
            <span>Problema ${d.n}: ${escaparHtml(d.titulo)} (Estágio ${d.estagio})</span>
            <span>${d.passou ? "Aprovado" : "Falhou"}</span>
          </div>
          ${d.raio_x ? renderRaioX(d.raio_x) : ""}
          <div class="mt-md">
            <strong>Solução de referência:</strong>
            ${d.entrada_quebrar_exemplo ? `<p class="texto-suave">Entrada exemplo que quebra: <code>${escaparHtml(d.entrada_quebrar_exemplo)}</code></p>` : ""}
            <pre class="codigo-bloco">${escaparHtml(d.solucao)}</pre>
            <div>${renderMiniMarkdown(d.explicacao)}</div>
          </div>
        </div>`
      )
      .join("");

    el.innerHTML = `
      <div class="card">
        <div class="res-banner ${cls}">
          <span>Boletim da Entrevista — Nota Geral: ${b.nota_geral}/100</span>
          <span>${b.resolvidas}/${b.total} resolvidos · ${formatarRelogio(b.duracao_seg)}</span>
        </div>
        <p><strong>Veredito:</strong> ${escaparHtml(b.veredito)}</p>
        <div class="kpis-grid mt-md">
          <div class="kpi-card"><div class="kpi-label">Correção</div><div class="kpi-valor">${b.nota_correcao}</div><div class="kpi-sub">Testes totais</div></div>
          <div class="kpi-card"><div class="kpi-label">Casos de borda</div><div class="kpi-valor">${b.nota_edge_cases}</div><div class="kpi-sub">Testes ocultos</div></div>
          <div class="kpi-card"><div class="kpi-label">Qualidade AST</div><div class="kpi-valor">${b.nota_qualidade}</div><div class="kpi-sub">Clareza e estrutura</div></div>
          <div class="kpi-card"><div class="kpi-label">Eficiência</div><div class="kpi-valor">${b.nota_eficiencia}</div><div class="kpi-sub">Complexidade Big-O</div></div>
        </div>
        <div class="acoes-pratica">
          <button class="btn btn-primario" id="btn-novo-simulado" type="button">Voltar / Novo Simulado</button>
        </div>
      </div>
      ${detHtml}
    `;

    $("#btn-novo-simulado").addEventListener("click", () => {
      $("#sim-resultado").classList.add("hidden");
      $("#sim-config").classList.remove("hidden");
      renderHistoricoSimulados();
    });
  }

  function renderHistoricoSimulados() {
    const est = state.estado;
    const wrap = $("#sim-historico");
    if (!est || !wrap) return;
    const lista = est.simulados || [];
    if (!lista.length) {
      wrap.innerHTML = `<p class="texto-suave">Nenhum simulado concluído ainda. Inicie seu primeiro simulado para medir sua prontidão para entrevistas.</p>`;
      return;
    }
    wrap.innerHTML = lista
      .map(
        (s) => `
        <div class="sim-hist-item">
          <div>
            <strong>Nota ${s.nota_geral}/100 · Trilha: ${escaparHtml(s.trilha)}</strong>
            <div class="padrao-meta">${escaparHtml((s.criado_em || "").replace("T", " "))} · ${s.resolvidas || 0}/${s.total || 3} resolvidos · ${formatarRelogio(s.duracao_seg || 0)}</div>
            <div class="texto-suave" style="margin:2px 0 0;">${escaparHtml(s.veredito || "")}</div>
          </div>
          <div class="sim-hist-notas">
            <span class="badge">Correção ${s.nota_correcao}</span>
            <span class="badge">Bordas ${s.nota_edge_cases}</span>
            <span class="badge">AST ${s.nota_qualidade}</span>
            <span class="badge">Big-O ${s.nota_eficiencia}</span>
          </div>
        </div>`
      )
      .join("");
  }

  // ==================== LABORATÓRIO (TESTE DE MESA VISUAL) ====================
  function pararAutoLab() {
    if (state.lab.timerAuto) {
      clearInterval(state.lab.timerAuto);
      state.lab.timerAuto = null;
      $("#lab-auto").textContent = "⏯ Auto";
    }
  }

  function preencherExemplosLab() {
    const sel = $("#lab-seletor-exemplo");
    sel.innerHTML = `<option value="">Carregar exemplo no Laboratório...</option>`;
    for (const [cid, c] of Object.entries(state.conceitos)) {
      if (!c.exemplo) continue;
      const opt = document.createElement("option");
      opt.value = cid;
      opt.textContent = `Conceito: ${c.nome}`;
      sel.appendChild(opt);
    }
  }

  async function abrirNoLaboratorio(codigo, entrada = "") {
    irParaAba("laboratorio");
    $("#lab-codigo").value = codigo;
    $("#lab-entrada").value = entrada;
    atualizarLinhas($("#lab-codigo"), $("#lab-linhas"));
    await rastrearLaboratorio();
  }

  async function rastrearLaboratorio() {
    pararAutoLab();
    const codigo = $("#lab-codigo").value;
    const entrada = $("#lab-entrada").value;
    state.lab.codigo = codigo;

    $("#lab-erro").classList.add("hidden");
    $("#lab-contador-passo").textContent = "Rastreando...";

    try {
      const r = await api("/api/rastrear", {
        method: "POST",
        body: JSON.stringify({ codigo, entrada }),
      });
      state.lab.passos = r.passos || [];
      state.lab.indice = 0;

      if (r.erro || r.limite) {
        $("#lab-erro").classList.remove("hidden");
        let msg = r.erro ? renderCardErro(r.erro) : "";
        if (r.limite) {
          msg += `<div class="erro-titulo" style="margin-top:6px;">Limite de 600 passos atingido (possível loop muito longo ou infinito).</div>`;
        }
        $("#lab-erro").innerHTML = msg;
      }

      const slider = $("#lab-slider");
      slider.min = 0;
      slider.max = Math.max(0, state.lab.passos.length - 1);
      slider.value = 0;
      renderPassoLab();
    } catch (err) {
      $("#lab-erro").classList.remove("hidden");
      $("#lab-erro").textContent = err.message;
    }
  }

  function renderPassoLab() {
    const passos = state.lab.passos;
    if (!passos.length) {
      $("#lab-codigo-trace").innerHTML = renderCodigoNumerado(state.lab.codigo || $("#lab-codigo").value);
      $("#lab-contador-passo").textContent = "0 passos";
      $("#lab-vars-tabela").innerHTML = `<p class="texto-suave">Nenhum passo registrado.</p>`;
      $("#lab-saida").textContent = "(vazia)";
      $("#lab-retorno").classList.add("hidden");
      return;
    }

    const idx = Math.max(0, Math.min(state.lab.indice, passos.length - 1));
    state.lab.indice = idx;
    $("#lab-slider").value = idx;
    $("#lab-contador-passo").textContent = `Passo ${idx + 1} de ${passos.length}`;

    const passo = passos[idx];
    const anterior = idx > 0 ? passos[idx - 1] : null;
    const varsAnt = anterior && anterior.escopo === passo.escopo ? anterior.vars : {};

    $("#lab-codigo-trace").innerHTML = renderCodigoNumerado(state.lab.codigo, passo.linha);
    const linAtiva = $("#lab-codigo-trace .linha-ativa");
    if (linAtiva) linAtiva.scrollIntoView({ block: "nearest" });

    $("#lab-escopo").textContent = `Escopo: ${passo.escopo}${passo.evento === "fim" ? " (fim)" : ""}`;
    $("#lab-pilha").innerHTML = (passo.pilha || []).map((f) => `<span class="pilha-item">${escaparHtml(f)}</span>`).join("");

    const entradas = Object.entries(passo.vars || {});
    if (!entradas.length) {
      $("#lab-vars-tabela").innerHTML = `<p class="texto-suave">Nenhuma variável local criada ainda.</p>`;
    } else {
      let tbl = `<table class="tabela-vars"><thead><tr><th>Variável</th><th>Valor</th><th>Tipo</th></tr></thead><tbody>`;
      for (const [nome, [repr, tipo]] of entradas) {
        const mudou = !varsAnt[nome] || varsAnt[nome][0] !== repr || varsAnt[nome][1] !== tipo;
        tbl += `<tr class="${mudou ? "var-alterada" : ""}">
          <td>${escaparHtml(nome)}</td>
          <td>${escaparHtml(repr)}</td>
          <td><span class="tipo-tag">${escaparHtml(tipo)}</span></td>
        </tr>`;
      }
      tbl += `</tbody></table>`;
      $("#lab-vars-tabela").innerHTML = tbl;
    }

    if (passo.evento === "return" && passo.retorno) {
      $("#lab-retorno").classList.remove("hidden");
      $("#lab-retorno").textContent = `return ${passo.retorno[0]} (${passo.retorno[1]})`;
    } else {
      $("#lab-retorno").classList.add("hidden");
    }

    $("#lab-saida").textContent = passo.saida ? passo.saida : "(vazia)";
  }

  // ==================== EVOLUÇÃO, BUGS & CADERNO MENTAL ====================
  function renderEvolucao() {
    const est = state.estado;
    if (!est) return;

    $("#evo-kpis").innerHTML = `
      <div class="kpi-card">
        <div class="kpi-label">Questões resolvidas</div>
        <div class="kpi-valor">${est.total_resolvidos}</div>
        <div class="kpi-sub">Meta sugerida: 20 por dia</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Sequência atual</div>
        <div class="kpi-valor">${est.sequencia}</div>
        <div class="kpi-sub">Recorde: ${est.melhor_sequencia} dia(s)</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Nível &amp; XP</div>
        <div class="kpi-valor">Nv. ${est.nivel.nivel}</div>
        <div class="kpi-sub">${est.xp} XP total (${est.nivel.no_nivel}/${est.nivel.para_proximo} p/ próximo)</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Estágios liberados</div>
        <div class="kpi-valor">${est.estagio_max} / ${est.estagios.length}</div>
        <div class="kpi-sub">${est.fila_revisao} item(ns) na fila de revisão</div>
      </div>
    `;

    // Calendário últimos 30 dias
    const cal = $("#evo-calendario");
    cal.innerHTML = "";
    const hoje = new Date(`${est.hoje}T12:00:00`);
    for (let d = 29; d >= 0; d--) {
      const dt = new Date(hoje);
      dt.setDate(hoje.getDate() - d);
      const iso = dt.toISOString().slice(0, 10);
      const qtd = est.calendario[iso] || 0;
      const cell = document.createElement("div");
      cell.className = "cal-dia";
      if (qtd >= 20) cell.classList.add("lv3");
      else if (qtd >= 10) cell.classList.add("lv2");
      else if (qtd >= 1) cell.classList.add("lv1");
      cell.title = `${iso}: ${qtd} resolvida(s)`;
      cell.innerHTML = `<span>${iso.slice(8)}</span>`;
      cal.appendChild(cell);
    }

    // Termômetro de conceitos
    const concEl = $("#evo-conceitos");
    if (!est.conceitos.length) {
      concEl.innerHTML = `<p class="texto-suave">Resolva suas primeiras questões para ver seu desempenho por conceito.</p>`;
    } else {
      concEl.innerHTML = est.conceitos
        .map(
          (c) => `
          <div class="term-item">
            <span>${escaparHtml(c.nome)}</span>
            <div class="barra-progresso"><div style="width:${c.taxa}%"></div></div>
            <span>${c.taxa}% (${c.acertos})</span>
          </div>`
        )
        .join("");
    }

    // Museu dos Meus Bugs
    const bugsWrap = $("#lista-museu-bugs");
    const bugs = est.museu_bugs || [];
    if (!bugs.length) {
      bugsWrap.innerHTML = `<p class="texto-suave">Nenhum bug registrado ainda. Conforme você praticar, seus pontos cegos aparecerão aqui com diagnóstico automático.</p>`;
    } else {
      bugsWrap.innerHTML = bugs
        .map(
          (b) => `
          <div class="bug-card">
            <div class="bug-card-topo">
              <strong>${escaparHtml(b.nome)}</strong>
              <span class="badge badge-origem desafio">${b.total}x</span>
            </div>
            <p>${formatarInline(b.cura)}</p>
          </div>`
        )
        .join("");
    }

    // Caderno de Padrões Mentais
    renderCadernoPadroes();

    // Resumo das 3 Trilhas
    const estDom = est.estagios.filter((e) => e.acertos >= e.meta).length;
    $("#card-intermediario").className = "card mt-lg";
    $("#card-intermediario").innerHTML = `
      <h3>Jornada 2027 — Fundamentos, Entrevistas e IA &amp; Automação</h3>
      <p>Progresso global: <strong>${estDom} de ${est.estagios.length} estágios dominados</strong> (meta: ${est.meta_estagio} acertos por estágio).
      Você já tem acesso às trilhas de <strong>Entrevista Técnica (14–18)</strong>, <strong>IA &amp; Automação (19–22)</strong> e ao <strong>Simulador de Entrevista</strong>.</p>
    `;

    // Conquistas
    $("#evo-conquistas").innerHTML = est.conquistas
      .map(
        (c) => `
        <div class="conquista-card ${c.ok ? "desbloqueada" : "bloqueada"}">
          <span class="conq-icone">${escaparHtml(c.icone)}</span>
          <div>
            <div class="conq-nome">${escaparHtml(c.nome)}</div>
            <div class="conq-desc">${escaparHtml(c.desc)}</div>
          </div>
        </div>`
      )
      .join("");
  }

  function renderCadernoPadroes() {
    const est = state.estado;
    const wrap = $("#lista-caderno-padroes");
    if (!est || !wrap) return;
    const termo = ($("#filtro-padroes")?.value || "").trim().toLowerCase();
    const lista = (est.padroes || []).filter((p) => {
      if (!termo) return true;
      return `${p.titulo} ${p.contrato} ${p.edge_cases} ${p.plano} ${p.feynman}`.toLowerCase().includes(termo);
    });

    if (!lista.length) {
      wrap.innerHTML = `<p class="texto-suave">Nenhuma anotação no Caderno Mental ainda. Use "Pensar Antes de Codar" ou o "Fechamento Feynman" ao resolver questões.</p>`;
      return;
    }

    wrap.innerHTML = "";
    for (const p of lista) {
      const div = document.createElement("div");
      div.className = "padrao-item";
      div.innerHTML = `
        <div class="padrao-topo">
          <div>
            <strong>${escaparHtml(p.titulo)}</strong>
            <span class="badge" style="margin-left:6px;">Estágio ${p.estagio}</span>
          </div>
          <button class="btn btn-ghost btn-xs btn-excluir-padrao" type="button">Excluir</button>
        </div>
        ${p.contrato ? `<div class="padrao-meta"><strong>Contrato:</strong> ${escaparHtml(p.contrato)}</div>` : ""}
        ${p.edge_cases ? `<div class="padrao-meta"><strong>Edge cases:</strong> ${escaparHtml(p.edge_cases)}</div>` : ""}
        ${p.plano ? `<div class="padrao-meta"><strong>Plano:</strong> ${escaparHtml(p.plano)}</div>` : ""}
        ${p.feynman ? `<div class="padrao-feynman"><strong>Sacada Feynman:</strong> ${escaparHtml(p.feynman)}</div>` : ""}
      `;
      div.querySelector(".btn-excluir-padrao").addEventListener("click", async () => {
        const ok = window.confirm(`Tem certeza que deseja excluir "${p.titulo}" do Caderno Mental? Esta ação não pode ser desfeita.`);
        if (!ok) return;
        await api("/api/padrao/excluir", { method: "POST", body: JSON.stringify({ id: p.questao_id }) });
        if (window.DojoCloud && window.DojoCloud.isLoggedIn()) {
          window.DojoCloud.deletePadrao(p.questao_id);
        }
        await carregarEstado(state.dataAtual, true);
        renderEvolucao();
        toast("Registro removido do Caderno Mental.");
      });
      wrap.appendChild(div);
    }
  }

  // ==================== CONTA SUPABASE & SINCRONIZAÇÃO ====================
  function atualizarUiNuvem(st) {
    const dot = $("#hdr-nuvem-dot");
    const txt = $("#hdr-nuvem-txt");
    const det = $("#status-nuvem-detalhe");
    const btnSync = $("#btn-sync-agora");
    const btnAbrir = $("#btn-abrir-conta-backup");
    if (!dot || !txt) return;

    dot.className = "status-dot";
    if (!st.configured) {
      txt.textContent = "Local";
      if (det) det.textContent = "Modo local ativo (progresso salvo neste navegador). Configure as variáveis do Supabase na Vercel para ativar nuvem.";
      if (btnSync) btnSync.classList.add("hidden");
    } else if (st.loggedIn) {
      dot.classList.add(st.status === "syncing" ? "syncing" : st.status === "error" ? "erro" : "online");
      txt.textContent = st.email.split("@")[0].slice(0, 14) || "Conta";
      if (det) det.textContent = `Conectado como ${st.email} · ${st.detail || "Sincronização automática ativa"}`;
      if (btnSync) btnSync.classList.remove("hidden");
      if (btnAbrir) btnAbrir.textContent = "Gerenciar conta";
    } else {
      txt.textContent = "Entrar";
      if (det) det.textContent = "Entre com sua conta Supabase para sincronizar progresso entre computador e celular.";
      if (btnSync) btnSync.classList.add("hidden");
      if (btnAbrir) btnAbrir.textContent = "Entrar / Criar conta";
    }

    // Atualiza conteúdo do modal se estiver aberto
    $("#conta-nao-configurada").classList.toggle("hidden", st.configured);
    $("#conta-logada").classList.toggle("hidden", !st.configured || !st.loggedIn);
    $("#conta-form-wrap").classList.toggle("hidden", !st.configured || st.loggedIn);
    if (st.loggedIn) {
      $("#conta-email-atual").textContent = st.email;
      const badge = $("#conta-sync-badge");
      badge.textContent = st.status === "syncing" ? "Sincronizando..." : st.status === "error" ? "Atenção" : "Sincronizado";
      badge.className = `badge badge-status ${st.status === "error" ? "sol" : "ok"}`;
      $("#conta-sync-msg").textContent = st.detail || "Seu progresso é sincronizado automaticamente a cada atividade.";
    }
  }

  function abrirModalConta() {
    if (window.DojoCloud) atualizarUiNuvem(window.DojoCloud.getState());
    $("#conta-feedback").classList.add("hidden");
    $("#modal-conta").classList.remove("hidden");
  }

  function fecharModalConta() {
    $("#modal-conta").classList.add("hidden");
  }

  function definirModoConta(modo) {
    state.contaModo = modo;
    $$(".conta-tab").forEach((b) => b.classList.toggle("ativa", b.dataset.modo === modo));
    $("#wrap-conta-nome").classList.toggle("hidden", modo !== "cadastrar");
    $("#wrap-conta-senha").classList.toggle("hidden", modo === "recuperar");
    $("#conta-senha").required = modo !== "recuperar";
    $("#btn-conta-submit").textContent =
      modo === "cadastrar" ? "Criar conta gratuita" : modo === "recuperar" ? "Enviar link de recuperação" : "Entrar na conta";
    $("#conta-feedback").classList.add("hidden");
  }

  function mostrarFeedbackConta(msg, tipo = "") {
    const el = $("#conta-feedback");
    el.textContent = msg;
    el.className = `conta-feedback ${tipo}`;
    el.classList.remove("hidden");
  }

  async function sincronizarComNuvem(mostrarToast = true) {
    if (!window.DojoCloud || !window.DojoCloud.isLoggedIn()) return;
    try {
      const res = await window.DojoCloud.pullAndMerge(apiSemSync);
      if (res.changed) {
        await carregarEstado();
        renderEvolucao();
      }
      if (mostrarToast) {
        toast(
          res.direction === "downloaded"
            ? "Progresso carregado da nuvem com sucesso."
            : "Progresso sincronizado com a nuvem.",
          "verde"
        );
      }
    } catch (err) {
      if (mostrarToast) toast(`Sincronização: ${escaparHtml(err.message)}`);
    }
  }

  // ==================== EVENTOS INICIAIS ====================
  function registrarEventos() {
    $$(".aba").forEach((b) => b.addEventListener("click", () => irParaAba(b.dataset.aba)));
    $("#btn-logo").addEventListener("click", () => irParaAba("treino"));
    $("#pill-estagio").addEventListener("click", () => irParaAba("trilha"));
    $("#btn-conta-nuvem").addEventListener("click", abrirModalConta);
    $("#btn-abrir-conta-backup").addEventListener("click", abrirModalConta);

    vincularEditor($("#editor-codigo"), $("#editor-linhas"), agendarRascunho);
    vincularEditor($("#lab-codigo"), $("#lab-linhas"));
    vincularEditor($("#sim-editor"), $("#sim-linhas"));

    $("#editor-codigo").addEventListener("keydown", (e) => {
      if (e.ctrlKey && e.shiftKey && e.key === "Enter") {
        e.preventDefault();
        verificarAtual();
      } else if (e.ctrlKey && e.key === "Enter") {
        e.preventDefault();
        executarCodigoAtual();
      }
    });

    $("#seletor-data").addEventListener("change", async (e) => {
      state.conjuntoAtual = 0;
      await carregarEstado(e.target.value);
    });

    $("#seletor-conjunto").addEventListener("change", async (e) => {
      state.conjuntoAtual = Number(e.target.value);
      const lista = state.estado.conjuntos[state.conjuntoAtual] || [];
      const pendente = lista.findIndex((x) => x.status === "pendente");
      state.questaoIdx = pendente >= 0 ? pendente : 0;
      atualizarCabecalho();
      renderRegua();
      if (lista[state.questaoIdx]) await abrirQuestao(lista[state.questaoIdx].id);
    });

    $("#btn-treino-extra").addEventListener("click", async () => {
      const res = await api("/api/treino-extra", { method: "POST", body: "{}" });
      state.conjuntoAtual = res.conjunto;
      await carregarEstado(state.estado.hoje);
      toast("Novo conjunto de <strong>20 questões extras</strong> gerado para hoje.", "verde");
    });

    $("#btn-treino-bugs").addEventListener("click", async () => {
      const res = await api("/api/treino-bugs", { method: "POST", body: "{}" });
      state.conjuntoAtual = res.conjunto;
      await carregarEstado(state.estado.hoje);
      irParaAba("treino");
      toast(`Treino cirúrgico de <strong>${res.total} questões</strong> gerado com base nos seus pontos fracos.`, "verde");
    });

    $("#btn-restaurar").addEventListener("click", () => {
      if (!state.questao) return;
      const ok = window.confirm("Deseja restaurar o código inicial desta questão?");
      if (!ok) return;
      $("#editor-codigo").value = state.questao.codigo_inicial || "";
      atualizarLinhas($("#editor-codigo"), $("#editor-linhas"));
      agendarRascunho();
    });

    $("#btn-executar").addEventListener("click", executarCodigoAtual);
    $("#btn-verificar").addEventListener("click", verificarAtual);
    $("#btn-verificar-prever").addEventListener("click", verificarAtual);
    $("#btn-verificar-quebrar").addEventListener("click", verificarAtual);

    // Pensar Antes de Codar & Feynman
    $("#btn-toggle-pensar").addEventListener("click", () => {
      const corpo = $("#pensar-corpo");
      const oculto = corpo.classList.toggle("hidden");
      $("#btn-toggle-pensar").textContent = oculto ? "Expandir" : "Recolher";
    });
    $("#btn-salvar-pensar").addEventListener("click", () => salvarPadraoAtual("Plano lógico salvo (+4 XP de bônus ao acertar)."));
    $("#btn-limpar-pensar").addEventListener("click", () => {
      if (!window.confirm("Deseja limpar todos os campos do planejamento?")) return;
      $("#pensar-contrato").value = "";
      $("#pensar-edges").value = "";
      $("#pensar-plano").value = "";
    });
    $("#btn-salvar-feynman").addEventListener("click", () => salvarPadraoAtual("Sacada Feynman salva no Caderno Mental."));

    // Trilhas desbloqueio rápido
    $("#btn-liberar-entrevista").addEventListener("click", async () => {
      await api("/api/desbloquear", { method: "POST", body: JSON.stringify({ estagio: 18 }) });
      await carregarEstado(state.dataAtual, true);
      renderTrilha();
      toast("Trilha de Entrevista Técnica (Estágios 14 a 18) liberada.", "verde");
    });
    $("#btn-liberar-ia").addEventListener("click", async () => {
      await api("/api/desbloquear", { method: "POST", body: JSON.stringify({ estagio: 22 }) });
      await carregarEstado(state.dataAtual, true);
      renderTrilha();
      toast("Trilha de IA, APIs & Automação (Estágios 19 a 22) liberada.", "verde");
    });
    $("#btn-liberar-todos").addEventListener("click", async () => {
      const ok = window.confirm("Deseja ativar o Modo Autônomo e liberar todos os 22 estágios para navegar livremente?");
      if (!ok) return;
      await api("/api/desbloquear", { method: "POST", body: JSON.stringify({ modo_livre: true }) });
      await carregarEstado(state.dataAtual, true);
      renderTrilha();
      toast("Modo Autônomo ativado: todos os 22 estágios liberados.", "verde");
    });
    $("#filtro-conceitos").addEventListener("input", renderBibliotecaConceitos);
    $("#filtro-padroes").addEventListener("input", renderCadernoPadroes);

    // Simulado de Entrevista
    $("#btn-iniciar-simulado").addEventListener("click", iniciarSimulado);
    $("#btn-encerrar-simulado").addEventListener("click", () => encerrarSimulado(false));
    $("#btn-sim-executar").addEventListener("click", async () => {
      const resEl = $("#sim-saida-rapida");
      resEl.classList.remove("hidden");
      resEl.innerHTML = `<p class="texto-suave">Executando teste rápido...</p>`;
      try {
        const r = await api("/api/executar", {
          method: "POST",
          body: JSON.stringify({ codigo: $("#sim-editor").value, entrada: $("#sim-entrada").value }),
        });
        let html = `<div class="res-banner info"><span>Saída de teste</span><span>${r.tempo}s</span></div>`;
        if (r.saida) html += `<pre class="saida-terminal">${escaparHtml(r.saida)}</pre>`;
        if (r.erro) html += renderCardErro(r.erro);
        resEl.innerHTML = html;
      } catch (err) {
        resEl.innerHTML = `<div class="erro-card">${escaparHtml(err.message)}</div>`;
      }
    });

    $("#btn-rastrear-questao").addEventListener("click", () => {
      abrirNoLaboratorio($("#editor-codigo").value, $("#entrada-teste").value);
    });
    $("#btn-rastrear-prever").addEventListener("click", () => {
      if (!state.questao) return;
      abrirNoLaboratorio(state.questao.trecho || "", state.questao.entrada_prever || "");
    });

    $("#btn-pedir-dica").addEventListener("click", async () => {
      if (!state.questao) return;
      const r = await api("/api/dica", { method: "POST", body: JSON.stringify({ id: state.questao.id }) });
      renderDicas(r.dicas_reveladas, state.questao.dicas_total);
    });

    $("#btn-ver-solucao").addEventListener("click", async () => {
      if (!state.questao) return;
      if (state.questao.status === "pendente") {
        const ok = window.confirm("Ver o gabarito antes de resolver marca esta questão para revisão espaçada. Deseja revelar?");
        if (!ok) return;
      }
      const r = await api("/api/solucao", { method: "POST", body: JSON.stringify({ id: state.questao.id }) });
      mostrarGabarito(r.solucao, r.explicacao, r.saida_correta, r.entrada_quebrar_exemplo);
      $("#btn-ver-solucao").classList.add("hidden");
      if (state.questao.tipo === "prever") $("#btn-rastrear-prever").classList.remove("hidden");
      await carregarEstado(state.dataAtual, true);
    });

    // Modais
    $("#modal-c-fechar").addEventListener("click", fecharModalConceito);
    $("#modal-conceito").addEventListener("click", (e) => {
      if (e.target === $("#modal-conceito")) fecharModalConceito();
    });
    $("#modal-conta-fechar").addEventListener("click", fecharModalConta);
    $("#modal-conta").addEventListener("click", (e) => {
      if (e.target === $("#modal-conta")) fecharModalConta();
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
        fecharModalConceito();
        fecharModalConta();
      }
    });
    $("#modal-c-testar-lab").addEventListener("click", () => {
      const c = state.conceitos[state.modalConceitoId];
      fecharModalConceito();
      if (c && c.exemplo) abrirNoLaboratorio(c.exemplo, "");
    });

    // Modal Conta Supabase
    $$(".conta-tab").forEach((b) => b.addEventListener("click", () => definirModoConta(b.dataset.modo)));
    $("#form-conta").addEventListener("submit", async (e) => {
      e.preventDefault();
      if (!window.DojoCloud) return;
      const email = $("#conta-email").value.trim();
      const senha = $("#conta-senha").value;
      const nome = $("#conta-nome").value.trim();
      const btn = $("#btn-conta-submit");
      btn.disabled = true;
      try {
        if (state.contaModo === "entrar") {
          await window.DojoCloud.signIn(email, senha);
          mostrarFeedbackConta("Login realizado! Sincronizando seu progresso...", "ok");
          await sincronizarComNuvem(true);
          fecharModalConta();
        } else if (state.contaModo === "cadastrar") {
          const r = await window.DojoCloud.signUp(email, senha, nome);
          if (r.needsConfirmation) {
            mostrarFeedbackConta("Conta criada! Confira seu e-mail para confirmar o cadastro e depois faça login.", "ok");
          } else {
            mostrarFeedbackConta("Conta criada e conectada! Sincronizando progresso...", "ok");
            await sincronizarComNuvem(true);
            fecharModalConta();
          }
        } else {
          await window.DojoCloud.sendPasswordReset(email);
          mostrarFeedbackConta("Link de recuperação enviado para o seu e-mail.", "ok");
        }
      } catch (err) {
        mostrarFeedbackConta(err.message || "Falha na autenticação.", "erro");
      } finally {
        btn.disabled = false;
      }
    });

    $("#btn-conta-sync").addEventListener("click", () => sincronizarComNuvem(true));
    $("#btn-sync-agora").addEventListener("click", () => sincronizarComNuvem(true));
    $("#btn-conta-sair").addEventListener("click", async () => {
      if (!window.confirm("Deseja sair da sua conta na nuvem neste aparelho?")) return;
      await window.DojoCloud.signOut();
      toast("Você saiu da conta na nuvem. O modo local continua ativo.");
      fecharModalConta();
    });

    // Laboratório controles
    $("#btn-lab-rastrear").addEventListener("click", rastrearLaboratorio);
    $("#lab-seletor-exemplo").addEventListener("change", (e) => {
      const c = state.conceitos[e.target.value];
      if (!c) return;
      $("#lab-codigo").value = c.exemplo;
      $("#lab-entrada").value = "";
      atualizarLinhas($("#lab-codigo"), $("#lab-linhas"));
      rastrearLaboratorio();
    });
    $("#lab-inicio").addEventListener("click", () => { pararAutoLab(); state.lab.indice = 0; renderPassoLab(); });
    $("#lab-ant").addEventListener("click", () => { pararAutoLab(); state.lab.indice--; renderPassoLab(); });
    $("#lab-prox").addEventListener("click", () => { pararAutoLab(); state.lab.indice++; renderPassoLab(); });
    $("#lab-fim").addEventListener("click", () => { pararAutoLab(); state.lab.indice = state.lab.passos.length - 1; renderPassoLab(); });
    $("#lab-slider").addEventListener("input", (e) => {
      pararAutoLab();
      state.lab.indice = Number(e.target.value);
      renderPassoLab();
    });
    $("#lab-auto").addEventListener("click", () => {
      if (state.lab.timerAuto) {
        pararAutoLab();
        return;
      }
      if (!state.lab.passos.length) return;
      if (state.lab.indice >= state.lab.passos.length - 1) state.lab.indice = 0;
      $("#lab-auto").textContent = "Pausar";
      state.lab.timerAuto = setInterval(() => {
        if (state.lab.indice >= state.lab.passos.length - 1) {
          pararAutoLab();
          return;
        }
        state.lab.indice++;
        renderPassoLab();
      }, 650);
    });

    // Backup JSON
    $("#btn-exportar-progresso").addEventListener("click", exportarProgresso);
    const inputImportar = $("#input-importar-progresso");
    $("#btn-importar-progresso").addEventListener("click", () => inputImportar.click());
    inputImportar.addEventListener("change", async (e) => {
      const arquivo = e.target.files && e.target.files[0];
      inputImportar.value = "";
      if (arquivo) await importarProgresso(arquivo);
    });

    const btnTentarMotor = $("#btn-motor-tentar");
    if (btnTentarMotor) {
      btnTentarMotor.addEventListener("click", async () => {
        btnTentarMotor.disabled = true;
        try {
          if (window.DojoBridge && window.DojoBridge.isStatic()) {
            await window.DojoBridge.retryInit();
          }
          await carregarDadosIniciais();
        } catch (err) {
          toast(`Erro ao carregar ambiente Python: ${escaparHtml(err.message)}`);
        } finally {
          btnTentarMotor.disabled = false;
        }
      });
    }
  }

  async function exportarProgresso() {
    const btn = $("#btn-exportar-progresso");
    if (btn) btn.disabled = true;
    try {
      const dados = await api("/api/progresso");
      const blob = new Blob([JSON.stringify(dados, null, 2)], { type: "application/json;charset=utf-8" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "progresso_dojo.json";
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
      toast("Progresso exportado com sucesso.", "verde");
    } catch (err) {
      toast(`Falha ao exportar progresso: ${escaparHtml(err.message)}`);
    } finally {
      if (btn) btn.disabled = false;
    }
  }

  async function importarProgresso(arquivo) {
    const btn = $("#btn-importar-progresso");
    let dados;
    try {
      const txt = await arquivo.text();
      dados = JSON.parse(txt);
    } catch {
      toast("Arquivo JSON inválido. Verifique o arquivo selecionado.");
      return;
    }

    const confirmado = window.confirm(
      "Tem certeza que deseja substituir seu progresso atual pelos dados deste arquivo? Esta ação não pode ser desfeita."
    );
    if (!confirmado) return;

    if (btn) btn.disabled = true;
    try {
      await api("/api/progresso", {
        method: "POST",
        body: JSON.stringify(dados),
      });
      await carregarEstado();
      renderEvolucao();
      toast("Progresso importado com sucesso.", "verde");
    } catch (err) {
      toast(`Falha ao importar progresso: ${escaparHtml(err.message)}`);
    } finally {
      if (btn) btn.disabled = false;
    }
  }

  function atualizarBannerMotor(status) {
    const banner = $("#banner-motor-web");
    const texto = $("#banner-motor-texto");
    const btnTentar = $("#btn-motor-tentar");
    if (!banner || !texto || !btnTentar) return;

    if (!status || status.stage === "idle" || status.stage === "ready") {
      banner.classList.add("hidden");
      banner.classList.remove("erro");
      btnTentar.classList.add("hidden");
      return;
    }
    banner.classList.remove("hidden");
    texto.textContent = status.message || "Preparando ambiente Python no navegador...";
    if (status.stage === "error") {
      banner.classList.add("erro");
      btnTentar.classList.remove("hidden");
    } else {
      banner.classList.remove("erro");
      btnTentar.classList.add("hidden");
    }
  }

  async function carregarDadosIniciais() {
    if (window.DojoBridge && window.DojoBridge.isStatic()) {
      await window.DojoBridge.init();
    }
    state.conceitos = await api("/api/conceitos");
    preencherExemplosLab();
    if (window.DojoCloud && window.DojoCloud.isLoggedIn()) {
      try {
        await window.DojoCloud.pullAndMerge(apiSemSync);
      } catch {
        // Segue com dados locais caso offline ou tabelas ainda não criadas
      }
    }
    await carregarEstado();
    atualizarLinhas($("#lab-codigo"), $("#lab-linhas"));
  }

  async function iniciar() {
    registrarEventos();
    if (window.DojoCloud) {
      window.DojoCloud.onChange(atualizarUiNuvem);
    }
    if (window.DojoBridge && window.DojoBridge.isStatic()) {
      window.DojoBridge.onStatus(atualizarBannerMotor);
    }
    try {
      await carregarDadosIniciais();
    } catch (err) {
      atualizarBannerMotor({
        stage: "error",
        message: `Não foi possível iniciar o ambiente Python: ${err.message}`,
      });
      toast(`Erro ao carregar sistema: ${escaparHtml(err.message)}`);
    }
  }

  document.addEventListener("DOMContentLoaded", iniciar);
})();
