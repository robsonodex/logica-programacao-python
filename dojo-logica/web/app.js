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
    modalConceitoId: null,
  };

  const $ = (sel) => document.querySelector(sel);
  const $$ = (sel) => Array.from(document.querySelectorAll(sel));

  // ==================== UTILITÁRIOS DE API & HTML ====================
  async function api(url, opcoes = {}) {
    if (window.DojoBridge && window.DojoBridge.isStatic()) {
      return await window.DojoBridge.request(url, opcoes);
    }
    const cfg = {
      headers: { "Content-Type": "application/json" },
      ...opcoes,
    };
    const resp = await fetch(url, cfg);
    const dados = await resp.json();
    if (!resp.ok || dados.falha) {
      throw new Error(dados.falha || `Erro HTTP ${resp.status}`);
    }
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
    const blocos = String(texto).replace(/\r\n/g, "\n").split(/```(?:python)?\n?([\s\S]*?)```/g);
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
          html += "<ul>" + linhas.filter((l) => l.trim()).map((l) => `<li>${formatarInline(l.replace(/^\s*[-*]\s+/, ""))}</li>`).join("") + "</ul>";
        } else {
          // Pode conter texto seguido de lista sem linha em branco
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
  }

  // ==================== EDITOR DE CÓDIGO ====================
  function atualizarLinhas(textarea, preLinhas) {
    const n = Math.max(1, textarea.value.split("\n").length);
    const arr = [];
    for (let i = 1; i <= n; i++) arr.push(i);
    preLinhas.textContent = arr.join("\n");
  }

  function vincularEditor(textarea, preLinhas, aoMudar) {
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
          // Indentar ou desindentar bloco selecionado
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
        toast(`🏅 Nova conquista: <strong>${escaparHtml(c.icone)} ${escaparHtml(c.nome)}</strong> — ${escaparHtml(c.desc)}`, "ouro");
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
    $("#info-revisoes").textContent = `🔄 ${est.fila_revisao} ${est.fila_revisao === 1 ? "revisão na fila" : "revisões na fila"}`;
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
      opt.textContent = idx === 0 ? `Treino Principal (${ok}/${c.length})` : `Treino Extra #${idx} (${ok}/${c.length})`;
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
      btn.className = "q-pill";
      if (item.status === "resolvido") btn.classList.add("resolvido");
      if (item.status === "solucao") btn.classList.add("solucao");
      if (idx === state.questaoIdx) btn.classList.add("ativa");
      btn.dataset.origem = item.origem;
      btn.textContent = String(item.n);
      const origemNome = { aquecimento: "Aquecimento", revisao: "Revisão espaçada", novo: `Estágio ${item.estagio}`, desafio: "Desafio" }[item.origem] || "";
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
      stEl.textContent = `✓ Resolvida (+${q.xp_ganho || 0} XP)`;
      stEl.className = "badge badge-status ok";
    } else if (q.status === "solucao") {
      stEl.textContent = "🔓 Gabarito visto";
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
      b.className = "chip-conceito";
      b.textContent = `📖 ${c.nome}`;
      b.title = c.resumo || "Clique para abrir a mini-lição";
      b.addEventListener("click", () => abrirModalConceito(c.id));
      chips.appendChild(b);
    }

    $("#q-enunciado").innerHTML = renderMiniMarkdown(q.enunciado);

    // Dicas
    renderDicas(q.dicas_reveladas, q.dicas_total);

    // Gabarito se já resolvido ou visto
    if (q.solucao) {
      mostrarGabarito(q.solucao, q.explicacao, q.saida_correta);
    } else {
      $("#area-gabarito").classList.add("hidden");
      $("#area-gabarito").innerHTML = "";
    }

    $("#btn-ver-solucao").classList.toggle("hidden", Boolean(q.solucao));
    $("#area-resultado").classList.add("hidden");
    $("#area-resultado").innerHTML = "";
    $("#status-rascunho").textContent = "";

    // Alternar modo código vs prever
    if (q.tipo === "prever") {
      $("#box-editor-codigo").classList.add("hidden");
      $("#box-resposta-prever").classList.remove("hidden");
      $("#q-trecho-prever").classList.remove("hidden");
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
    } else {
      $("#box-editor-codigo").classList.remove("hidden");
      $("#box-resposta-prever").classList.add("hidden");
      $("#q-trecho-prever").classList.add("hidden");

      const exBox = $("#q-exemplos");
      exBox.innerHTML = `<div class="bloco-header"><span>🧪 Exemplo de validação (total de ${q.n_testes} teste${q.n_testes > 1 ? "s" : ""})</span></div>`;
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
    btn.textContent = `💡 Pedir dica (${reveladas.length}/${total})`;
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

  function mostrarGabarito(solucao, explicacao, saidaCorreta = null) {
    const area = $("#area-gabarito");
    area.classList.remove("hidden");
    const ehPrever = state.questao && state.questao.tipo === "prever";
    const titulo = ehPrever ? "✅ Resposta correta e explicação" : "✅ Gabarito comentado";
    let corpo = `<h4><span>${titulo}</span>`;
    if (!ehPrever) {
      corpo += `<button class="btn btn-sec btn-xs" id="btn-lab-gabarito">🔬 Rastrear gabarito</button>`;
    }
    corpo += `</h4>`;
    if (ehPrever && saidaCorreta !== null && saidaCorreta !== undefined) {
      corpo += `<div class="mb-sm"><strong>Saída exata:</strong><pre class="codigo-bloco">${escaparHtml(saidaCorreta)}</pre></div>`;
    } else {
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
      let html = `<div class="res-banner info"><span>▶️ Execução de teste</span><span>⏱️ ${r.tempo}s</span></div>`;
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
        <div class="erro-titulo">❌ ${escaparHtml(erro.tipo)}${lin}</div>
        <div class="erro-msg">${escaparHtml(erro.mensagem || "")}${erro.texto ? `\n→ ${escaparHtml(erro.texto)}` : ""}</div>
        <div class="erro-explicacao">${renderMiniMarkdown(erro.explicacao || "")}</div>
      </div>`;
  }

  async function verificarAtual() {
    const q = state.questao;
    if (!q) return;
    const ehPrever = q.tipo === "prever";
    const payload = ehPrever
      ? { id: q.id, resposta: $("#resposta-prever").value }
      : { id: q.id, codigo: $("#editor-codigo").value };

    const resEl = $("#area-resultado");
    resEl.classList.remove("hidden");
    resEl.innerHTML = `<p class="texto-suave">Rodando todos os casos de teste...</p>`;

    try {
      const r = await api("/api/verificar", {
        method: "POST",
        body: JSON.stringify(payload),
      });

      const lista = state.estado.conjuntos[state.conjuntoAtual];
      const temProxima = state.questaoIdx < lista.length - 1;

      let html = "";
      if (r.passou) {
        const xpMsg = r.xp > 0 ? `+${r.xp} XP ganhos!` : "Questão validada!";
        html += `<div class="res-banner ok">
          <span>🎉 Excelente! ${xpMsg}</span>
          ${temProxima ? `<button class="btn btn-primario btn-sm" id="btn-proxima-questao">Próxima questão →</button>` : ""}
        </div>`;
        if (r.solucao) {
          mostrarGabarito(r.solucao, r.explicacao, r.saida_correta);
        }
        $("#btn-ver-solucao").classList.add("hidden");
        if (ehPrever) $("#btn-rastrear-prever").classList.remove("hidden");
      } else {
        html += `<div class="res-banner falha"><span>❌ Ainda não bateu com o esperado (tentativa ${r.tentativas})</span></div>`;
      }

      for (const t of r.resultados) {
        const ok = t.status === "exato" || t.status === "quase";
        const tag = {
          exato: "✅ Exato",
          quase: "✅ Aceito (atenção a espaços/maiúsculas)",
          diferente: "❌ Saída diferente",
          erro: "💥 Erro na execução",
        }[t.status];

        html += `<div class="teste-item ${ok ? "ok" : "falha"}">
          <div class="teste-topo"><span>Caso de teste #${t.n}</span><span>${tag}</span></div>`;
        if (t.entrada || t.chamada) {
          html += `<div class="texto-suave" style="margin:0 0 6px;">${t.chamada ? `Chamada: <code>${escaparHtml(t.chamada)}</code>` : `Entrada: <code>${escaparHtml(t.entrada.replace(/\n/g, " ↵ "))}</code>`}</div>`;
        }
        if (t.erro) {
          html += renderCardErro(t.erro);
        } else if (!ok || t.status === "quase") {
          const esp = t.esperado !== null && t.esperado !== undefined ? `<pre>${escaparHtml(t.esperado)}</pre>` : `<pre>(tente novamente ou use uma dica)</pre>`;
          html += `<div class="teste-cols">
            <div><strong>Sua saída:</strong><pre>${escaparHtml(t.obtido || "(vazio)")}</pre></div>
            <div><strong>Saída esperada:</strong>${esp}</div>
          </div>`;
        }
        html += `</div>`;
      }

      resEl.innerHTML = html;

      if (r.passou) {
        if (r.desbloqueou) {
          const estNovo = state.estado.estagios.find((e) => e.n === r.desbloqueou);
          toast(`🔓 <strong>Estágio ${r.desbloqueou} desbloqueado!</strong> ${estNovo ? escaparHtml(estNovo.nome) : ""}`, "verde");
        }
        if (r.concluiu_basico) {
          toast("🏆 <strong>Você concluiu todos os 13 estágios do nível básico!</strong> Confira a aba Evolução.", "ouro");
        }
        const btnProx = $("#btn-proxima-questao");
        if (btnProx) {
          btnProx.addEventListener("click", async () => {
            state.questaoIdx += 1;
            renderRegua();
            await abrirQuestao(lista[state.questaoIdx].id);
          });
        }
        // Atualiza contadores e régua sem perder a questão atual
        await carregarEstado(state.dataAtual, true);
        // Reexibe o banner na área de resultado após recarregar o estado
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
    if (!state.questao || state.questao.tipo === "prever") return;
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

    $("#modal-c-dica").innerHTML = `💡 <strong>Dica de ouro:</strong> ${formatarInline(c.dica_de_ouro || "")}`;
    $("#modal-conceito").classList.remove("hidden");
  }

  function fecharModalConceito() {
    $("#modal-conceito").classList.add("hidden");
  }

  // ==================== TRILHA & BIBLIOTECA ====================
  function renderTrilha() {
    const est = state.estado;
    if (!est) return;
    const grid = $("#grid-estagios");
    grid.innerHTML = "";

    for (const e of est.estagios) {
      const card = document.createElement("div");
      card.className = "card-estagio";
      if (e.n === est.estagio_atual) card.classList.add("atual");
      if (!e.liberado) card.classList.add("bloqueado");

      const pct = Math.min(100, Math.round((e.acertos / Math.max(1, e.meta)) * 100));
      const chips = (e.conceitos_info || [])
        .map((c) => `<button class="chip-conceito" data-cid="${c.id}">📖 ${escaparHtml(c.nome)}</button>`)
        .join("");

      let acaoHtml = "";
      if (e.n === est.estagio_atual) {
        acaoHtml = `<span class="badge badge-status ok">Estágio Atual</span>`;
      } else if (e.liberado) {
        acaoHtml = `<button class="btn btn-sec btn-sm btn-trocar-est" data-est="${e.n}">Estudar este estágio</button>`;
      } else {
        acaoHtml = `<span class="badge">🔒 Bloqueado</span>`;
      }

      card.innerHTML = `
        <div>
          <div class="est-topo">
            <span class="est-icone">${e.icone}</span>
            <div>
              <div class="est-titulo">Estágio ${e.n}: ${escaparHtml(e.nome)}</div>
              <div class="est-sub">${e.modelos} modelos de questões</div>
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
            toast(`Estágio alterado para <strong>${e.n}: ${escaparHtml(e.nome)}</strong> e plano de hoje atualizado!`, "verde");
            irParaAba("treino");
          } else {
            toast(`Estágio padrão alterado para <strong>${e.n}: ${escaparHtml(e.nome)}</strong>. Como você já começou o plano de hoje, ele valerá no Treino Extra ou amanhã.`);
            renderTrilha();
          }
        });
      }
      grid.appendChild(card);
    }

    // Biblioteca de 22 conceitos
    const gridC = $("#grid-conceitos");
    gridC.innerHTML = "";
    for (const [cid, c] of Object.entries(state.conceitos)) {
      const div = document.createElement("div");
      div.className = "card-conceito-bib";
      div.innerHTML = `<h4>📖 ${escaparHtml(c.nome)}</h4><p>${escaparHtml(c.resumo)}</p>`;
      div.addEventListener("click", () => abrirModalConceito(cid));
      gridC.appendChild(div);
    }
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
          msg += `<div class="erro-titulo" style="margin-top:6px;">⏱️ Limite de 600 passos atingido (possível loop muito longo ou infinito).</div>`;
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
    $("#lab-pilha").innerHTML = (passo.pilha || []).map((f) => `<span class="pilha-item">📌 ${escaparHtml(f)}</span>`).join("");

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
      $("#lab-retorno").textContent = `↩ return ${passo.retorno[0]} (${passo.retorno[1]})`;
    } else {
      $("#lab-retorno").classList.add("hidden");
    }

    $("#lab-saida").textContent = passo.saida ? passo.saida : "(vazia)";
  }

  // ==================== EVOLUÇÃO & CONQUISTAS ====================
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
        <div class="kpi-valor">🔥 ${est.sequencia}</div>
        <div class="kpi-sub">Recorde: ${est.melhor_sequencia} dia(s)</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Nível &amp; XP</div>
        <div class="kpi-valor">⚡ Nv. ${est.nivel.nivel}</div>
        <div class="kpi-sub">${est.xp} XP total (${est.nivel.no_nivel}/${est.nivel.para_proximo} p/ próximo)</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Estágio liberado</div>
        <div class="kpi-valor">${est.estagio_max} / ${est.estagios.length}</div>
        <div class="kpi-sub">${est.fila_revisao} item(ns) para revisão espaçada</div>
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
      concEl.innerHTML = `<p class="texto-suave">Resolva suas primeiras questões para ver seu desempenho por conceito!</p>`;
    } else {
      concEl.innerHTML = est.conceitos
        .map((c) => `
          <div class="term-item">
            <span>${escaparHtml(c.nome)}</span>
            <div class="barra-progresso"><div style="width:${c.taxa}%"></div></div>
            <span>${c.taxa}% (${c.acertos})</span>
          </div>`)
        .join("");
    }

    // Card Nível Intermediário
    const estDom = est.estagios.filter((e) => e.acertos >= e.meta).length;
    $("#card-intermediario").className = "card mt-lg card-intermediario-destaque";
    $("#card-intermediario").innerHTML = est.basico_concluido
      ? `<h3>🎓 Nível Básico Dominado!</h3>
         <p>Você completou todos os 13 estágios fundamentais (${estDom}/13 dominados). Quando sentir que está pronto, volte na conversa e peça a evolução para o <strong>Nível Intermediário</strong> escolhendo os novos tópicos (dicionários, tuplas, conjuntos, compreensão de listas, arquivos, tratamento de exceções, módulos e POO).</p>`
      : `<h3>🚀 Próxima Etapa: Nível Intermediário</h3>
         <p>Progresso no Nível Básico: <strong>${estDom} de ${est.estagios.length} estágios dominados</strong> (cada estágio pede ${est.meta_estagio} acertos).</p>
         <p class="texto-suave" style="margin-bottom:0;">Concentre-se em entender o raciocínio de cada questão hoje. Quando sentir domínio do básico, você poderá solicitar a abertura da trilha Intermediária com os novos conteúdos que desejar.</p>`;

    // Conquistas
    $("#evo-conquistas").innerHTML = est.conquistas
      .map((c) => `
        <div class="conquista-card ${c.ok ? "desbloqueada" : "bloqueada"}">
          <span class="conq-icone">${escaparHtml(c.icone)}</span>
          <div>
            <div class="conq-nome">${escaparHtml(c.nome)}</div>
            <div class="conq-desc">${escaparHtml(c.desc)}</div>
          </div>
        </div>`)
      .join("");
  }

  // ==================== EVENTOS INICIAIS ====================
  function registrarEventos() {
    $$(".aba").forEach((b) => b.addEventListener("click", () => irParaAba(b.dataset.aba)));
    $("#btn-logo").addEventListener("click", () => irParaAba("treino"));
    $("#pill-estagio").addEventListener("click", () => irParaAba("trilha"));

    vincularEditor($("#editor-codigo"), $("#editor-linhas"), agendarRascunho);
    vincularEditor($("#lab-codigo"), $("#lab-linhas"));

    // Atalhos no editor da questão
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
      toast("✨ Novo conjunto de <strong>20 questões extras</strong> gerado para hoje!", "verde");
    });

    $("#btn-restaurar").addEventListener("click", () => {
      if (!state.questao) return;
      $("#editor-codigo").value = state.questao.codigo_inicial || "";
      atualizarLinhas($("#editor-codigo"), $("#editor-linhas"));
      agendarRascunho();
    });

    $("#btn-executar").addEventListener("click", executarCodigoAtual);
    $("#btn-verificar").addEventListener("click", verificarAtual);
    $("#btn-verificar-prever").addEventListener("click", verificarAtual);

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
      mostrarGabarito(r.solucao, r.explicacao, r.saida_correta);
      $("#btn-ver-solucao").classList.add("hidden");
      if (state.questao.tipo === "prever") $("#btn-rastrear-prever").classList.remove("hidden");
      await carregarEstado(state.dataAtual, true);
    });

    // Modal
    $("#modal-c-fechar").addEventListener("click", fecharModalConceito);
    $("#modal-conceito").addEventListener("click", (e) => {
      if (e.target === $("#modal-conceito")) fecharModalConceito();
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") fecharModalConceito();
    });
    $("#modal-c-testar-lab").addEventListener("click", () => {
      const c = state.conceitos[state.modalConceitoId];
      fecharModalConceito();
      if (c && c.exemplo) abrirNoLaboratorio(c.exemplo, "");
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
      $("#lab-auto").textContent = "⏸ Pausar";
      state.lab.timerAuto = setInterval(() => {
        if (state.lab.indice >= state.lab.passos.length - 1) {
          pararAutoLab();
          return;
        }
        state.lab.indice++;
        renderPassoLab();
      }, 650);
    });

    // Backup e portabilidade do progresso
    const btnExportar = $("#btn-exportar-progresso");
    const btnImportar = $("#btn-importar-progresso");
    const inputImportar = $("#input-importar-progresso");
    if (btnExportar) {
      btnExportar.addEventListener("click", exportarProgresso);
    }
    if (btnImportar && inputImportar) {
      btnImportar.addEventListener("click", () => inputImportar.click());
      inputImportar.addEventListener("change", async (e) => {
        const arquivo = e.target.files && e.target.files[0];
        inputImportar.value = "";
        if (arquivo) await importarProgresso(arquivo);
      });
    }

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
    await carregarEstado();
    atualizarLinhas($("#lab-codigo"), $("#lab-linhas"));
  }

  async function iniciar() {
    registrarEventos();
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
