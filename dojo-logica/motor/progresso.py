"""Plano diário, progresso do aluno, XP, revisão espaçada e conquistas."""

from __future__ import annotations

import json
import os
import random
import threading
from collections import Counter
from datetime import date, datetime, timedelta

from banco import REGISTRO, TIPOS, executar_referencia, modelos_do_estagio
from . import executor
from .conceitos import CONCEITOS
from .estagios import ESTAGIOS, TOTAL_ESTAGIOS, estagio

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_DADOS = os.path.join(RAIZ, "dados")
ARQ_PROGRESSO = os.path.join(PASTA_DADOS, "progresso.json")

QUESTOES_POR_DIA = 20
META_ESTAGIO = 20          # acertos no estágio atual para desbloquear o próximo
INTERVALOS_REVISAO = [1, 3, 7]  # dias até rever um modelo em que você teve dificuldade

_trava = threading.RLock()
_cache_esperado: dict = {}


def hoje() -> str:
    return date.today().isoformat()


def _agora() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _somar_dias(d: str, n: int) -> str:
    return (date.fromisoformat(d) + timedelta(days=n)).isoformat()


# ---------------------------------------------------------------------------
# Persistência
# ---------------------------------------------------------------------------

def _novo_progresso() -> dict:
    return {
        "versao": 1,
        "criado_em": _agora(),
        "estagio_atual": 1,
        "estagio_max": 1,
        "xp": 0,
        "dias": {},
        "resultados": {},
        "dominio": {},
        "conceitos": {},
        "fila_revisao": [],
        "ultimo_uso_modelo": {},
        "conquistas_vistas": [],
        "basico_concluido": False,
    }


def carregar() -> dict:
    with _trava:
        if not os.path.exists(ARQ_PROGRESSO):
            return _novo_progresso()
        with open(ARQ_PROGRESSO, encoding="utf-8") as f:
            dados = json.load(f)
        base = _novo_progresso()
        base.update(dados)
        return base


def salvar(p: dict) -> None:
    with _trava:
        os.makedirs(PASTA_DADOS, exist_ok=True)
        tmp = ARQ_PROGRESSO + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(p, f, ensure_ascii=False, indent=1)
        os.replace(tmp, ARQ_PROGRESSO)


def importar(dados: dict) -> dict:
    """Valida e substitui o progresso salvo por um JSON exportado anteriormente."""
    if not isinstance(dados, dict):
        raise ValueError("Arquivo de progresso inválido: esperado objeto JSON.")
    for campo in ("dias", "resultados", "dominio", "conceitos", "ultimo_uso_modelo"):
        if campo in dados and not isinstance(dados[campo], dict):
            raise ValueError(f"Arquivo inválido: campo '{campo}' deve ser um objeto.")
    for campo in ("fila_revisao", "conquistas_vistas"):
        if campo in dados and not isinstance(dados[campo], list):
            raise ValueError(f"Arquivo inválido: campo '{campo}' deve ser uma lista.")
    base = _novo_progresso()
    base.update(dados)
    if not isinstance(base["estagio_atual"], int) or not 1 <= base["estagio_atual"] <= TOTAL_ESTAGIOS:
        raise ValueError("Arquivo inválido: 'estagio_atual' fora do intervalo permitido.")
    if not isinstance(base["estagio_max"], int) or not 1 <= base["estagio_max"] <= TOTAL_ESTAGIOS:
        raise ValueError("Arquivo inválido: 'estagio_max' fora do intervalo permitido.")
    if not isinstance(base["xp"], int) or base["xp"] < 0:
        raise ValueError("Arquivo inválido: 'xp' deve ser um inteiro não negativo.")
    with _trava:
        salvar(base)
    return estado()


# ---------------------------------------------------------------------------
# Geração do plano diário
# ---------------------------------------------------------------------------

def _escolher_modelo(r, estagio_n, usados_hoje: Counter, ultimo_uso: dict):
    modelos = modelos_do_estagio(estagio_n)
    if not modelos:
        return None
    r.shuffle(modelos)
    modelos.sort(key=lambda m: (usados_hoje[m.id], ultimo_uso.get(m.id, "")))
    return modelos[0]


def gerar_plano(p: dict, data: str, conjunto: int) -> list[dict]:
    r = random.Random(f"plano:{data}:{conjunto}:{p['criado_em']}")
    atual = p["estagio_atual"]
    usados = Counter()
    ultimo = p["ultimo_uso_modelo"]
    itens = []

    def add(modelo, origem):
        usados[modelo.id] += 1
        itens.append({"modelo": modelo.id, "semente": r.randrange(10**9), "origem": origem,
                      "estagio": modelo.estagio, "dificuldade": modelo.dificuldade})

    revisoes = []
    if conjunto == 0:
        vencidas = [f for f in p["fila_revisao"] if f["vencimento"] <= data and f["modelo"] in REGISTRO]
        for f in vencidas[:3]:
            revisoes.append(REGISTRO[f["modelo"]])

    anteriores = list(range(1, atual))
    n_atual = QUESTOES_POR_DIA - len(revisoes) if not anteriores else 11
    n_aquec = QUESTOES_POR_DIA - len(revisoes) - n_atual

    pesos = [1 / (atual - k) ** 0.8 for k in anteriores]
    aquec = []
    for _ in range(n_aquec):
        k = r.choices(anteriores, weights=pesos)[0]
        m = _escolher_modelo(r, k, usados, ultimo)
        if m:
            usados[m.id] += 1
            aquec.append(m)
    for m in aquec:
        usados[m.id] -= 1
    for m in sorted(aquec, key=lambda m: (m.dificuldade, m.estagio)):
        add(m, "aquecimento")
    for m in revisoes:
        add(m, "revisao")
    novos = []
    for _ in range(n_atual):
        m = _escolher_modelo(r, atual, usados, ultimo)
        if m:
            usados[m.id] += 1
            novos.append(m)
    for m in novos:
        usados[m.id] -= 1
    novos.sort(key=lambda m: m.dificuldade)
    for i, m in enumerate(novos):
        origem = "desafio" if i >= len(novos) - 2 and m.dificuldade >= 4 else "novo"
        add(m, origem)

    for i, it in enumerate(itens):
        it["id"] = f"{data}_{conjunto}_{i + 1:02d}"
        it["n"] = i + 1
        ultimo[it["modelo"]] = data
    return itens


def garantir_dia(p: dict, data: str) -> dict:
    dia = p["dias"].get(data)
    if dia is None:
        dia = {"conjuntos": [gerar_plano(p, data, 0)], "estagio": p["estagio_atual"]}
        p["dias"][data] = dia
        salvar(p)
    return dia


def treino_extra(data: str) -> dict:
    with _trava:
        p = carregar()
        dia = garantir_dia(p, data)
        dia["conjuntos"].append(gerar_plano(p, data, len(dia["conjuntos"])))
        salvar(p)
        return {"conjunto": len(dia["conjuntos"]) - 1}


def _achar_item(p: dict, inst_id: str) -> dict:
    data, conj, _ = inst_id.split("_")
    for it in p["dias"][data]["conjuntos"][int(conj)]:
        if it["id"] == inst_id:
            return it
    raise KeyError(inst_id)


# ---------------------------------------------------------------------------
# Questões
# ---------------------------------------------------------------------------

def _gerar(it: dict) -> dict:
    return REGISTRO[it["modelo"]].gerar(it["semente"])


def _esperados(it: dict, q: dict) -> list[str]:
    chave = (it["modelo"], it["semente"])
    if chave not in _cache_esperado:
        _cache_esperado[chave] = [executar_referencia(q["solucao"], t["entrada"], t["chamada"])
                                  for t in q["testes"]]
    return _cache_esperado[chave]


def _conceitos_info(ids):
    return [{"id": c, "nome": CONCEITOS[c]["nome"], "resumo": CONCEITOS[c]["resumo"]}
            for c in ids if c in CONCEITOS]


def _resultado(p, inst_id):
    return p["resultados"].get(inst_id) or {"status": "pendente", "tentativas": 0, "dicas": 0}


def resumo_item(p, it) -> dict:
    m = REGISTRO.get(it["modelo"])
    res = _resultado(p, it["id"])
    q = _gerar(it) if m else {"titulo": "(modelo removido)"}
    return {
        "id": it["id"], "n": it["n"], "titulo": q["titulo"], "tipo": m.tipo if m else "codigo",
        "tipo_nome": TIPOS.get(m.tipo, "") if m else "", "estagio": it["estagio"],
        "dificuldade": it["dificuldade"], "origem": it["origem"],
        "conceitos": _conceitos_info(m.conceitos if m else []),
        "status": res["status"], "tentativas": res["tentativas"],
    }


def questao(inst_id: str) -> dict:
    with _trava:
        p = carregar()
        it = _achar_item(p, inst_id)
        m = REGISTRO[it["modelo"]]
        q = _gerar(it)
        res = _resultado(p, inst_id)
        esperados = _esperados(it, q)
        pub = resumo_item(p, it)
        pub.update({
            "enunciado": q["enunciado"],
            "codigo_inicial": q["codigo_inicial"],
            "codigo_salvo": res.get("codigo"),
            "dicas_total": len(q["dicas"]),
            "dicas_reveladas": q["dicas"][: res.get("dicas", 0)],
            "n_testes": len(q["testes"]),
            "estagio_nome": estagio(it["estagio"])["nome"],
            "xp_ganho": res.get("xp", 0),
        })
        if m.tipo == "prever":
            pub["trecho"] = q["solucao"]
            pub["entrada_prever"] = q["testes"][0]["entrada"]
            pub["exemplos"] = []
        else:
            vis = max(1, min(q["testes_visiveis"], len(q["testes"])))
            pub["exemplos"] = [{"entrada": t["entrada"], "chamada": t["chamada"], "saida": s}
                               for t, s in list(zip(q["testes"], esperados))[:vis]]
        if res["status"] in ("resolvido", "solucao"):
            pub["solucao"] = q["solucao"]
            pub["explicacao"] = q["explicacao"]
            if m.tipo == "prever":
                pub["saida_correta"] = esperados[0]
        return pub


def revelar_dica(inst_id: str) -> dict:
    with _trava:
        p = carregar()
        it = _achar_item(p, inst_id)
        q = _gerar(it)
        res = p["resultados"].setdefault(inst_id, _resultado(p, inst_id))
        if res.get("dicas", 0) < len(q["dicas"]):
            res["dicas"] = res.get("dicas", 0) + 1
        salvar(p)
        return {"dicas_reveladas": q["dicas"][: res["dicas"]]}


def revelar_solucao(inst_id: str) -> dict:
    with _trava:
        p = carregar()
        it = _achar_item(p, inst_id)
        q = _gerar(it)
        res = p["resultados"].setdefault(inst_id, _resultado(p, inst_id))
        if res["status"] == "pendente":
            res["status"] = "solucao"
            res["quando"] = _agora()
            _agendar_revisao(p, it["modelo"], hoje(), reiniciar=True)
        salvar(p)
        out = {"solucao": q["solucao"], "explicacao": q["explicacao"]}
        if REGISTRO[it["modelo"]].tipo == "prever":
            out["saida_correta"] = _esperados(it, q)[0]
        return out


def salvar_rascunho(inst_id: str, codigo: str) -> None:
    with _trava:
        p = carregar()
        _achar_item(p, inst_id)
        res = p["resultados"].setdefault(inst_id, _resultado(p, inst_id))
        res["codigo"] = codigo
        salvar(p)


def _agendar_revisao(p, modelo, data, reiniciar=False):
    fila = p["fila_revisao"]
    for f in fila:
        if f["modelo"] == modelo:
            if reiniciar:
                f["nivel"] = 0
                f["vencimento"] = _somar_dias(data, INTERVALOS_REVISAO[0])
            return
    fila.append({"modelo": modelo, "nivel": 0, "vencimento": _somar_dias(data, INTERVALOS_REVISAO[0]),
                 "desde": data})


def _avancar_revisao(p, modelo, data):
    for f in list(p["fila_revisao"]):
        if f["modelo"] == modelo:
            f["nivel"] += 1
            if f["nivel"] >= len(INTERVALOS_REVISAO):
                p["fila_revisao"].remove(f)
            else:
                f["vencimento"] = _somar_dias(data, INTERVALOS_REVISAO[f["nivel"]])


def verificar(inst_id: str, codigo: str = "", resposta: str | None = None) -> dict:
    with _trava:
        p = carregar()
        it = _achar_item(p, inst_id)
    m = REGISTRO[it["modelo"]]
    q = _gerar(it)
    esperados = _esperados(it, q)

    resultados = []
    if m.tipo == "prever":
        cmp = executor.comparar(resposta or "", esperados[0])
        resultados.append({"n": 1, "entrada": q["testes"][0]["entrada"], "chamada": "",
                           "obtido": resposta or "", "status": cmp,
                           "esperado": esperados[0] if cmp != "diferente" else None})
    else:
        for i, (t, esp) in enumerate(zip(q["testes"], esperados)):
            r = executor.executar(codigo, t["entrada"], t["chamada"], eco=False)
            cmp = "erro" if r["erro"] else executor.comparar(r["saida"], esp)
            resultados.append({"n": i + 1, "entrada": t["entrada"], "chamada": t["chamada"],
                               "obtido": r["saida"], "esperado": esp, "status": cmp, "erro": r["erro"]})
            if r["erro"] and r["erro"]["tipo"] in ("SyntaxError", "IndentationError", "Tempo"):
                break  # não adianta rodar os outros testes
    passou = len(resultados) == len(q["testes"]) and all(x["status"] in ("exato", "quase") for x in resultados)

    with _trava:
        p = carregar()
        res = p["resultados"].setdefault(inst_id, _resultado(p, inst_id))
        if m.tipo != "prever":
            res["codigo"] = codigo
        else:
            res["codigo"] = resposta
        res["tentativas"] = res.get("tentativas", 0) + 1
        dia_hoje = hoje()
        xp = 0
        desbloqueou = None
        concluiu_basico = False
        era_pendente = res["status"] == "pendente"
        for c in m.conceitos:
            st = p["conceitos"].setdefault(c, {"acertos": 0, "erros": 0})
            if passou and era_pendente:
                st["acertos"] += 1
            elif not passou and res["tentativas"] == 1:
                st["erros"] += 1
        if passou and era_pendente:
            dicas = res.get("dicas", 0)
            xp = 10 * m.dificuldade - 3 * dicas
            if res["tentativas"] == 1 and dicas == 0:
                xp += 5
            xp = max(2, xp)
            res.update(status="resolvido", xp=xp, quando=_agora(), dia=dia_hoje)
            p["xp"] += xp
            dom = p["dominio"].setdefault(str(m.estagio), {"acertos": 0})
            dom["acertos"] += 1
            if res["tentativas"] >= 3:
                _agendar_revisao(p, m.id, dia_hoje)
            elif it["origem"] == "revisao":
                _avancar_revisao(p, m.id, dia_hoje)
            atual = p["estagio_atual"]
            if (atual == p["estagio_max"] and p["dominio"].get(str(atual), {}).get("acertos", 0) >= META_ESTAGIO):
                if atual < TOTAL_ESTAGIOS:
                    p["estagio_max"] = atual + 1
                    desbloqueou = atual + 1
                elif not p["basico_concluido"]:
                    p["basico_concluido"] = True
                    concluiu_basico = True
        elif passou and res["status"] == "solucao":
            res["refeito"] = True
        salvar(p)

    return {
        "passou": passou,
        "resultados": resultados,
        "xp": xp,
        "tentativas": res["tentativas"],
        "desbloqueou": desbloqueou,
        "concluiu_basico": concluiu_basico,
        "solucao": q["solucao"] if passou else None,
        "explicacao": q["explicacao"] if passou else None,
        "saida_correta": esperados[0] if passou and m.tipo == "prever" else None,
    }


def mudar_estagio(n: int) -> dict:
    with _trava:
        p = carregar()
        if 1 <= n <= p["estagio_max"]:
            p["estagio_atual"] = n
            salvar(p)
        return {"estagio_atual": p["estagio_atual"]}


def regenerar_hoje() -> dict:
    """Recria o plano de hoje (só se nenhuma questão foi tocada) — útil após trocar de estágio."""
    with _trava:
        p = carregar()
        d = hoje()
        dia = p["dias"].get(d)
        if dia:
            ids = [it["id"] for conj in dia["conjuntos"] for it in conj]
            if any(i in p["resultados"] for i in ids):
                return {"ok": False, "motivo": "Você já começou o plano de hoje. Use o Treino extra."}
            del p["dias"][d]
        garantir_dia(p, d)
        return {"ok": True}


# ---------------------------------------------------------------------------
# Painel
# ---------------------------------------------------------------------------

def _resolvidos_por_dia(p):
    cont = Counter()
    for r in p["resultados"].values():
        if r.get("status") == "resolvido" and r.get("dia"):
            cont[r["dia"]] += 1
    return cont


def _sequencia(cont):
    d = date.today()
    if not cont.get(d.isoformat()):
        d -= timedelta(days=1)
    n = 0
    while cont.get(d.isoformat()):
        n += 1
        d -= timedelta(days=1)
    melhor = atual = 0
    if cont:
        dias = sorted(date.fromisoformat(x) for x in cont)
        ant = None
        for x in dias:
            atual = atual + 1 if ant and (x - ant).days == 1 else 1
            melhor = max(melhor, atual)
            ant = x
    return n, melhor


def nivel_xp(xp):
    nivel, falta, custo = 1, xp, 100
    while falta >= custo:
        falta -= custo
        nivel += 1
        custo = int(custo * 1.15)
    return {"nivel": nivel, "no_nivel": falta, "para_proximo": custo}


def _conquistas(p, cont, seq_melhor):
    res = [r for r in p["resultados"].values() if r.get("status") == "resolvido"]
    total = len(res)
    por_tipo = Counter()
    sem_dica = 0
    for inst, r in p["resultados"].items():
        if r.get("status") != "resolvido":
            continue
        try:
            it = _achar_item(p, inst)
            por_tipo[REGISTRO[it["modelo"]].tipo] += 1
        except (KeyError, ValueError):
            pass
        if r.get("dicas", 0) == 0 and r.get("tentativas") == 1:
            sem_dica += 1
    dia_completo = any(
        all(p["resultados"].get(it["id"], {}).get("status") == "resolvido" for it in dia["conjuntos"][0])
        for dia in p["dias"].values())
    lista = [
        ("primeiro", "👣", "Primeiro passo", "Resolveu sua primeira questão", total >= 1),
        ("dez", "🔟", "Aquecendo", "10 questões resolvidas", total >= 10),
        ("cem", "💯", "Centenário", "100 questões resolvidas", total >= 100),
        ("quinhentos", "🚀", "Imparável", "500 questões resolvidas", total >= 500),
        ("dia20", "🌟", "Dia perfeito", "Resolveu as 20 questões de um dia", dia_completo),
        ("seq3", "🔥", "Embalado", "3 dias seguidos praticando", seq_melhor >= 3),
        ("seq7", "📅", "Uma semana!", "7 dias seguidos praticando", seq_melhor >= 7),
        ("seq30", "🏅", "Hábito formado", "30 dias seguidos praticando", seq_melhor >= 30),
        ("bugs", "🐞", "Caçador de bugs", "Corrigiu 15 códigos com bug", por_tipo["corrigir"] >= 15),
        ("mente", "🧠", "Mente de interpretador", "Previu 15 saídas corretamente", por_tipo["prever"] >= 15),
        ("lacunas", "🧩", "Quebra-cabeças", "Completou 15 códigos com lacunas", por_tipo["completar"] >= 15),
        ("limpo", "🎯", "De primeira", "25 questões sem dica e na 1ª tentativa", sem_dica >= 25),
        ("maratona", "🏃", "Maratonista", "Resolveu 40 questões num só dia", max(cont.values(), default=0) >= 40),
    ]
    for e in ESTAGIOS:
        lista.append((f"est{e['n']}", e["icone"], f"Estágio {e['n']} dominado", e["nome"],
                      p["dominio"].get(str(e["n"]), {}).get("acertos", 0) >= META_ESTAGIO))
    return [{"id": i, "icone": ic, "nome": n, "desc": d, "ok": ok} for i, ic, n, d, ok in lista]


def estado(data: str | None = None) -> dict:
    with _trava:
        p = carregar()
        d_hoje = hoje()
        garantir_dia(p, d_hoje)
        data = data if data in p["dias"] else d_hoje
        dia = p["dias"][data]
        cont = _resolvidos_por_dia(p)
        seq, melhor = _sequencia(cont)
        conquistas = _conquistas(p, cont, melhor)
        novas = [c for c in conquistas if c["ok"] and c["id"] not in p["conquistas_vistas"]]
        if novas:
            p["conquistas_vistas"].extend(c["id"] for c in novas)
            salvar(p)
        conjuntos = [[resumo_item(p, it) for it in conj] for conj in dia["conjuntos"]]
        estagios = []
        for e in ESTAGIOS:
            ac = p["dominio"].get(str(e["n"]), {}).get("acertos", 0)
            estagios.append({**e, "acertos": ac, "meta": META_ESTAGIO,
                             "conceitos_info": _conceitos_info(e["conceitos"]),
                             "liberado": e["n"] <= p["estagio_max"], "modelos": len(modelos_do_estagio(e["n"]))})
        conc = []
        for cid, st in p["conceitos"].items():
            if cid in CONCEITOS:
                tot = st["acertos"] + st["erros"]
                conc.append({"id": cid, "nome": CONCEITOS[cid]["nome"], "acertos": st["acertos"],
                             "erros": st["erros"], "taxa": round(st["acertos"] / tot * 100) if tot else 0})
        return {
            "hoje": d_hoje,
            "data": data,
            "conjuntos": conjuntos,
            "estagio_atual": p["estagio_atual"],
            "estagio_max": p["estagio_max"],
            "estagio_do_dia": dia["estagio"],
            "estagios": estagios,
            "xp": p["xp"],
            "nivel": nivel_xp(p["xp"]),
            "sequencia": seq,
            "melhor_sequencia": melhor,
            "calendario": dict(cont),
            "dias_com_plano": sorted(p["dias"].keys()),
            "conceitos": sorted(conc, key=lambda c: c["taxa"]),
            "conquistas": conquistas,
            "novas_conquistas": novas,
            "fila_revisao": len(p["fila_revisao"]),
            "total_resolvidos": sum(cont.values()),
            "basico_concluido": p["basico_concluido"],
            "meta_estagio": META_ESTAGIO,
        }
