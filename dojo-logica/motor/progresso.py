"""Plano diário, progresso do aluno, XP, revisão espaçada, Museu de Bugs, Caderno Feynman e Simulado de Entrevista."""

from __future__ import annotations

import ast
import json
import os
import random
import threading
import time
from collections import Counter
from datetime import date, datetime, timedelta

from banco import REGISTRO, TIPOS, executar_referencia, modelos_do_estagio
from . import analisador, executor
from .conceitos import CONCEITOS
from .estagios import ESTAGIOS, TOTAL_BASICO, TOTAL_ESTAGIOS, TRILHAS, estagio

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_DADOS = os.path.join(RAIZ, "dados")
ARQ_PROGRESSO = os.path.join(PASTA_DADOS, "progresso.json")

QUESTOES_POR_DIA = 20
META_ESTAGIO = 20
INTERVALOS_REVISAO = [1, 3, 7, 14, 30]  # estilo Anki SM-2 simplificado para retenção de longo prazo

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
    agora = _agora()
    return {
        "versao": 2,
        "criado_em": agora,
        "atualizado_em": agora,
        "estagio_atual": 1,
        "estagio_max": 1,
        "modo_livre": False,
        "xp": 0,
        "dias": {},
        "resultados": {},
        "dominio": {},
        "conceitos": {},
        "fila_revisao": [],
        "ultimo_uso_modelo": {},
        "conquistas_vistas": [],
        "basico_concluido": False,
        "padroes": {},
        "bugs": [],
        "simulados": [],
        "simulado_ativo": None,
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
        p["atualizado_em"] = _agora()
        os.makedirs(PASTA_DADOS, exist_ok=True)
        tmp = ARQ_PROGRESSO + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(p, f, ensure_ascii=False, indent=1)
        os.replace(tmp, ARQ_PROGRESSO)


def importar(dados: dict) -> dict:
    """Valida e substitui o progresso salvo por um JSON exportado ou vindo da nuvem."""
    if not isinstance(dados, dict):
        raise ValueError("Arquivo de progresso inválido: esperado objeto JSON.")
    for campo in ("dias", "resultados", "dominio", "conceitos", "ultimo_uso_modelo", "padroes"):
        if campo in dados and not isinstance(dados[campo], dict):
            raise ValueError(f"Arquivo inválido: campo '{campo}' deve ser um objeto.")
    for campo in ("fila_revisao", "conquistas_vistas", "bugs", "simulados"):
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
# Validação segura de argumentos para o tipo "quebrar"
# ---------------------------------------------------------------------------

def _eh_literal_seguro(no: ast.AST) -> bool:
    if isinstance(no, ast.Constant):
        return True
    if isinstance(no, ast.UnaryOp) and isinstance(no.op, (ast.UAdd, ast.USub)):
        return isinstance(no.operand, ast.Constant) and isinstance(no.operand.value, (int, float))
    if isinstance(no, (ast.List, ast.Tuple, ast.Set)):
        return all(_eh_literal_seguro(el) for el in no.elts)
    if isinstance(no, ast.Dict):
        return all(
            (k is not None and _eh_literal_seguro(k) and _eh_literal_seguro(v))
            for k, v in zip(no.keys, no.values)
        )
    return False


def _validar_args_literais(texto: str) -> bool:
    if not texto.strip():
        return False
    try:
        arvore = ast.parse(f"_f({texto})", mode="eval")
    except SyntaxError:
        return False
    if not isinstance(arvore.body, ast.Call):
        return False
    if arvore.body.keywords:
        return all(_eh_literal_seguro(kw.value) for kw in arvore.body.keywords) and all(
            _eh_literal_seguro(a) for a in arvore.body.args
        )
    return all(_eh_literal_seguro(a) for a in arvore.body.args)


# ---------------------------------------------------------------------------
# Geração do plano diário e treinos extras
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
        for f in vencidas[:4]:
            revisoes.append(REGISTRO[f["modelo"]])

    anteriores = list(range(1, atual))
    n_atual = QUESTOES_POR_DIA - len(revisoes) if not anteriores else 11
    n_aquec = max(0, QUESTOES_POR_DIA - len(revisoes) - n_atual)

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


def treino_bugs() -> dict:
    """Gera um treino cirúrgico de 10 questões focado nos bugs e conceitos mais frágeis do aluno."""
    with _trava:
        p = carregar()
        data = hoje()
        dia = garantir_dia(p, data)
        conjunto_idx = len(dia["conjuntos"])
        r = random.Random(f"bugs:{data}:{conjunto_idx}:{len(p['bugs'])}")

        # Modelos com mais bugs recentes + conceitos com menor taxa de acerto
        modelos_bug = Counter(b["modelo_id"] for b in p["bugs"] if b.get("modelo_id") in REGISTRO)
        conceitos_fracos = sorted(
            [
                (cid, st["acertos"] / max(1, st["acertos"] + st["erros"]))
                for cid, st in p["conceitos"].items()
                if st["erros"] > 0
            ],
            key=lambda x: x[1],
        )
        cids_alvo = [c for c, _ in conceitos_fracos[:4]]

        candidatos = []
        for mid, _ in modelos_bug.most_common(6):
            candidatos.append(REGISTRO[mid])

        pool = [m for m in REGISTRO.values() if m.estagio <= p["estagio_max"]]
        r.shuffle(pool)
        for m in pool:
            if len(candidatos) >= 10:
                break
            if any(c in cids_alvo for c in m.conceitos) and m not in candidatos:
                candidatos.append(m)

        # Completa com questões de depuração/quebrar/corrigir se ainda faltarem
        for m in pool:
            if len(candidatos) >= 10:
                break
            if m.tipo in ("corrigir", "quebrar", "prever") and m not in candidatos:
                candidatos.append(m)
        for m in pool:
            if len(candidatos) >= 10:
                break
            if m not in candidatos:
                candidatos.append(m)

        candidatos = candidatos[:10]
        candidatos.sort(key=lambda m: (m.dificuldade, m.estagio))
        itens = []
        for i, m in enumerate(candidatos):
            itens.append({
                "id": f"{data}_{conjunto_idx}_{i + 1:02d}",
                "n": i + 1,
                "modelo": m.id,
                "semente": r.randrange(10**9),
                "origem": "revisao",
                "estagio": m.estagio,
                "dificuldade": m.dificuldade,
            })

        dia["conjuntos"].append(itens)
        salvar(p)
        return {"conjunto": conjunto_idx, "total": len(itens), "conceitos_foco": cids_alvo}


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
        if REGISTRO[it["modelo"]].tipo == "quebrar":
            _cache_esperado[chave] = []
        else:
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
            "padrao": p["padroes"].get(inst_id),
            "tem_benchmark": bool(q.get("benchmark")),
        })
        if m.tipo == "prever":
            pub["trecho"] = q["solucao"]
            pub["entrada_prever"] = q["testes"][0]["entrada"]
            pub["exemplos"] = []
        elif m.tipo == "quebrar":
            pub["trecho"] = q["codigo_inicial"]
            pub["modo_quebrar"] = q.get("modo_quebrar", "input")
            pub["funcao_quebrar"] = q.get("funcao_quebrar", "")
            pub["placeholder_quebrar"] = q.get("placeholder_quebrar", "")
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
            elif m.tipo == "quebrar":
                pub["entrada_quebrar_exemplo"] = q["testes"][0]["entrada"]
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
        tipo = REGISTRO[it["modelo"]].tipo
        if tipo == "prever":
            out["saida_correta"] = _esperados(it, q)[0]
        elif tipo == "quebrar":
            out["entrada_quebrar_exemplo"] = q["testes"][0]["entrada"]
        return out


def salvar_rascunho(inst_id: str, codigo: str) -> None:
    with _trava:
        p = carregar()
        _achar_item(p, inst_id)
        res = p["resultados"].setdefault(inst_id, _resultado(p, inst_id))
        res["codigo"] = codigo
        salvar(p)


def salvar_padrao(questao_id: str, contrato: str = "", edge_cases: str = "", plano: str = "", feynman: str = "") -> dict:
    """Salva o raciocínio de 'Pensar Antes de Codar' e a frase Feynman no Caderno de Padrões Mentais."""
    with _trava:
        p = carregar()
        it = _achar_item(p, questao_id)
        q = _gerar(it)
        reg = {
            "questao_id": questao_id,
            "modelo_id": it["modelo"],
            "titulo": q["titulo"],
            "estagio": it["estagio"],
            "contrato": (contrato or "").strip(),
            "edge_cases": (edge_cases or "").strip(),
            "plano": (plano or "").strip(),
            "feynman": (feynman or "").strip(),
            "atualizado_em": _agora(),
        }
        p["padroes"][questao_id] = reg
        salvar(p)
        return {"ok": True, "padrao": reg}


def excluir_padrao(questao_id: str) -> dict:
    with _trava:
        p = carregar()
        removido = p["padroes"].pop(questao_id, None) is not None
        if removido:
            salvar(p)
        return {"ok": True, "removido": removido}


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


def _avaliar_quebrar(q: dict, entrada_aluno: str) -> tuple[bool, list[dict]]:
    txt = (entrada_aluno or "").strip()
    if not txt:
        return False, [{
            "n": 1, "entrada": "", "chamada": "", "obtido": "", "esperado": "",
            "status": "erro",
            "erro": {
                "tipo": "EntradaVazia",
                "mensagem": "Digite uma entrada para tentar quebrar o código.",
                "linha": None, "texto": "",
                "explicacao": "Pense em um caso de borda (vazio, negativo, repetido, None ou fronteira).",
            },
        }]

    modo = q.get("modo_quebrar", "input")
    if modo == "args":
        if not _validar_args_literais(txt):
            return False, [{
                "n": 1, "entrada": txt, "chamada": "", "obtido": "", "esperado": "",
                "status": "erro",
                "erro": {
                    "tipo": "EntradaInvalida",
                    "mensagem": "Use apenas valores literais Python válidos.",
                    "linha": None, "texto": txt,
                    "explicacao": "Escreva valores como números, textos entre aspas (`'abc'`), listas (`[-1, -2]`), dicionários (`{'a': None}`), `True`, `False` ou `None`.",
                },
            }]
        chamada = f"print(repr({q['funcao_quebrar']}({txt})))"
        ent = ""
    else:
        chamada = ""
        ent = txt

    r_ref = executor.executar(q["solucao"], ent, chamada, eco=False)
    if r_ref["erro"]:
        return False, [{
            "n": 1, "entrada": txt, "chamada": chamada,
            "obtido": "", "esperado": "", "status": "erro",
            "erro": {
                "tipo": "ContratoViolado",
                "mensagem": f"Sua entrada não atende às regras do enunciado ({r_ref['erro']['tipo']}: {r_ref['erro']['mensagem']}).",
                "linha": None, "texto": txt,
                "explicacao": "A entrada precisa ser válida segundo o enunciado, fazendo apenas o código bugado falhar.",
            },
        }]

    r_bug = executor.executar(q["codigo_inicial"], ent, chamada, eco=False)
    if r_bug["erro"]:
        quebrou = True
        obtido_txt = f"Erro no código bugado -> {r_bug['erro']['tipo']}: {r_bug['erro']['mensagem']}"
    else:
        quebrou = executor.comparar(r_bug["saida"], r_ref["saida"]) == "diferente"
        obtido_txt = r_bug["saida"]

    return quebrou, [{
        "n": 1,
        "entrada": txt,
        "chamada": chamada,
        "obtido": obtido_txt,
        "esperado": r_ref["saida"],
        "status": "exato" if quebrou else "diferente",
        "erro": None,
        "quebrar_modo": True,
    }]


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
        passou = cmp in ("exato", "quase")
    elif m.tipo == "quebrar":
        passou, resultados = _avaliar_quebrar(q, resposta or "")
    else:
        for i, (t, esp) in enumerate(zip(q["testes"], esperados)):
            r = executor.executar(codigo, t["entrada"], t["chamada"], eco=False)
            cmp = "erro" if r["erro"] else executor.comparar(r["saida"], esp)
            resultados.append({"n": i + 1, "entrada": t["entrada"], "chamada": t["chamada"],
                               "obtido": r["saida"], "esperado": esp, "status": cmp, "erro": r["erro"]})
            if r["erro"] and r["erro"]["tipo"] in ("SyntaxError", "IndentationError", "Tempo"):
                break
        passou = len(resultados) == len(q["testes"]) and all(x["status"] in ("exato", "quase") for x in resultados)

    # Raio-X automático (AST + Eficiência/Big-O) quando o código do aluno passa
    raio_x = None
    if passou and m.tipo in ("codigo", "funcao", "corrigir", "completar"):
        raio_x = {
            "qualidade": analisador.analisar_codigo(codigo, m.tipo),
            "eficiencia": analisador.medir_complexidade(codigo, q.get("benchmark"), q["testes"]),
        }

    bug_registrado = None
    if not passou and m.tipo in ("codigo", "funcao", "corrigir", "completar"):
        bug_info = analisador.classificar_bug(resultados, codigo, m.tipo)
        bug_registrado = {
            **bug_info,
            "modelo_id": m.id,
            "estagio": m.estagio,
            "criado_em": _agora(),
        }

    with _trava:
        p = carregar()
        res = p["resultados"].setdefault(inst_id, _resultado(p, inst_id))
        res["codigo"] = codigo if m.tipo not in ("prever", "quebrar") else resposta
        res["tentativas"] = res.get("tentativas", 0) + 1
        dia_hoje = hoje()
        xp = 0
        desbloqueou = None
        concluiu_basico = False
        era_pendente = res["status"] == "pendente"

        if bug_registrado:
            p["bugs"].append(bug_registrado)
            if len(p["bugs"]) > 500:
                p["bugs"] = p["bugs"][-500:]

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
            if inst_id in p["padroes"] and p["padroes"][inst_id].get("plano"):
                xp += 4  # bônus por aplicar "Pensar Antes de Codar"
            xp = max(2, xp)
            res.update(status="resolvido", xp=xp, quando=_agora(), dia=dia_hoje)
            if raio_x:
                res["nota_qualidade"] = raio_x["qualidade"]["nota"]
            p["xp"] += xp
            dom = p["dominio"].setdefault(str(m.estagio), {"acertos": 0})
            dom["acertos"] += 1
            # Revisão espaçada inteligente: qualquer dificuldade (errou antes ou pediu dica) volta para consolidar
            if res["tentativas"] >= 2 or dicas > 0:
                _agendar_revisao(p, m.id, dia_hoje)
            elif it["origem"] == "revisao":
                _avancar_revisao(p, m.id, dia_hoje)
            atual = p["estagio_atual"]
            if atual == p["estagio_max"] and p["dominio"].get(str(atual), {}).get("acertos", 0) >= META_ESTAGIO:
                if atual < TOTAL_ESTAGIOS:
                    p["estagio_max"] = atual + 1
                    desbloqueou = atual + 1
                if atual == TOTAL_BASICO and not p["basico_concluido"]:
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
        "entrada_quebrar_exemplo": q["testes"][0]["entrada"] if passou and m.tipo == "quebrar" else None,
        "raio_x": raio_x,
        "bug": bug_registrado,
    }


def mudar_estagio(n: int) -> dict:
    with _trava:
        p = carregar()
        if 1 <= n <= p["estagio_max"]:
            p["estagio_atual"] = n
            salvar(p)
        return {"estagio_atual": p["estagio_atual"]}


def desbloquear(estagio_alvo: int | None = None, modo_livre: bool | None = None) -> dict:
    """Permite liberar trilhas avançadas (Entrevista 14-18, IA 19-22 ou todos os 22 estágios)."""
    with _trava:
        p = carregar()
        if modo_livre:
            p["modo_livre"] = True
            p["estagio_max"] = TOTAL_ESTAGIOS
        elif estagio_alvo is not None:
            alvo = max(1, min(int(estagio_alvo), TOTAL_ESTAGIOS))
            p["estagio_max"] = max(p["estagio_max"], alvo)
        salvar(p)
        return {"estagio_max": p["estagio_max"], "modo_livre": p["modo_livre"]}


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
# Simulador de Entrevista Técnica
# ---------------------------------------------------------------------------

def _estagios_da_trilha(trilha: str) -> list[int]:
    if trilha == "basico":
        return list(range(1, 14))
    if trilha == "entrevista":
        return list(range(14, 19))
    if trilha == "ia_automacao":
        return list(range(19, 23))
    return list(range(10, TOTAL_ESTAGIOS + 1))


def iniciar_simulado(trilha: str = "entrevista", duracao_min: int = 30) -> dict:
    """Cria um simulado cronometrado de 3 problemas sem dicas e com casos de borda ocultos."""
    with _trava:
        p = carregar()
        estagios_ok = set(_estagios_da_trilha(trilha))
        pool = [
            m for m in REGISTRO.values()
            if m.estagio in estagios_ok and m.tipo in ("funcao", "codigo", "corrigir", "quebrar")
        ]
        if len(pool) < 3:
            pool = [m for m in REGISTRO.values() if m.tipo in ("funcao", "codigo", "corrigir", "quebrar")]

        semente_base = int(time.time() * 1000) % 10**9
        r = random.Random(semente_base)
        r.shuffle(pool)

        faceis = [m for m in pool if m.dificuldade <= 2]
        medios = [m for m in pool if m.dificuldade == 3]
        dificeis = [m for m in pool if m.dificuldade >= 4]

        escolhidos = []
        for grupo in (faceis, medios, dificeis):
            for m in grupo:
                if m not in escolhidos:
                    escolhidos.append(m)
                    break
        for m in pool:
            if len(escolhidos) >= 3:
                break
            if m not in escolhidos:
                escolhidos.append(m)

        sim_id = f"sim_{int(time.time())}"
        itens = []
        questoes_pub = []
        for idx, m in enumerate(escolhidos[:3], start=1):
            sem = r.randrange(10**9)
            q = m.gerar(sem)
            itens.append({"n": idx, "modelo": m.id, "semente": sem, "estagio": m.estagio, "tipo": m.tipo})

            pub = {
                "n": idx,
                "modelo": m.id,
                "titulo": q["titulo"],
                "tipo": m.tipo,
                "tipo_nome": TIPOS.get(m.tipo, ""),
                "estagio": m.estagio,
                "dificuldade": m.dificuldade,
                "enunciado": q["enunciado"],
                "codigo_inicial": q["codigo_inicial"],
                "modo_quebrar": q.get("modo_quebrar", "input"),
                "funcao_quebrar": q.get("funcao_quebrar", ""),
                "placeholder_quebrar": q.get("placeholder_quebrar", ""),
                "n_testes": len(q["testes"]),
                "exemplos": [],
            }
            if m.tipo == "quebrar":
                pub["trecho"] = q["codigo_inicial"]
            else:
                t0 = q["testes"][0]
                esp0 = executar_referencia(q["solucao"], t0["entrada"], t0["chamada"])
                pub["exemplos"] = [{"entrada": t0["entrada"], "chamada": t0["chamada"], "saida": esp0}]
            questoes_pub.append(pub)

        ativo = {
            "id": sim_id,
            "trilha": trilha,
            "duracao_min": max(10, min(90, int(duracao_min))),
            "iniciado_em": _agora(),
            "itens": itens,
        }
        p["simulado_ativo"] = ativo
        salvar(p)
        return {**ativo, "questoes": questoes_pub}


def avaliar_simulado(simulado_id: str, respostas: list[dict], duracao_usada_seg: int = 0) -> dict:
    """Avalia o simulado inteiro contra todos os casos ocultos + AST + Big-O e gera o boletim de 4 notas."""
    with _trava:
        p = carregar()
        ativo = p.get("simulado_ativo")
        if not ativo or ativo.get("id") != simulado_id:
            raise ValueError("Simulado não encontrado ou já encerrado.")

    mapa_resp = {int(r["n"]): r for r in (respostas or [])}
    detalhes = []
    tot_testes = 0
    ok_testes = 0
    tot_bordas = 0
    ok_bordas = 0
    notas_qualidade = []
    notas_eficiencia = []

    for it in ativo["itens"]:
        m = REGISTRO[it["modelo"]]
        q = m.gerar(it["semente"])
        resp_item = mapa_resp.get(it["n"], {})
        codigo = resp_item.get("codigo", "")
        raciocinio = (resp_item.get("raciocinio", "") or "").strip()

        if m.tipo == "quebrar":
            passou, res_list = _avaliar_quebrar(q, codigo)
            tot_testes += 1
            tot_bordas += 1
            if passou:
                ok_testes += 1
                ok_bordas += 1
            raio = None
            notas_eficiencia.append(100 if passou else 30)
            notas_qualidade.append(100 if passou else 40)
        else:
            esperados = [executar_referencia(q["solucao"], t["entrada"], t["chamada"]) for t in q["testes"]]
            res_list = []
            for i, (t, esp) in enumerate(zip(q["testes"], esperados)):
                r = executor.executar(codigo, t["entrada"], t["chamada"], eco=False)
                cmp = "erro" if r["erro"] else executor.comparar(r["saida"], esp)
                ok_i = cmp in ("exato", "quase")
                tot_testes += 1
                if ok_i:
                    ok_testes += 1
                if i > 0 or len(q["testes"]) == 1:
                    tot_bordas += 1
                    if ok_i:
                        ok_bordas += 1
                res_list.append({
                    "n": i + 1, "entrada": t["entrada"], "chamada": t["chamada"],
                    "obtido": r["saida"], "esperado": esp, "status": cmp, "erro": r["erro"],
                })
                if r["erro"] and r["erro"]["tipo"] in ("SyntaxError", "IndentationError", "Tempo"):
                    restantes = len(q["testes"]) - (i + 1)
                    tot_testes += restantes
                    tot_bordas += restantes
                    break
            passou = len(res_list) == len(q["testes"]) and all(x["status"] in ("exato", "quase") for x in res_list)
            qual = analisador.analisar_codigo(codigo, m.tipo)
            efic = analisador.medir_complexidade(codigo, q.get("benchmark"), q["testes"]) if passou else {"otimo": False}
            raio = {"qualidade": qual, "eficiencia": efic}
            notas_qualidade.append(qual["nota"] if codigo.strip() else 0)
            if passou:
                notas_eficiencia.append(100 if efic.get("otimo", True) else 65)
            else:
                notas_eficiencia.append(35 if any(x["status"] in ("exato", "quase") for x in res_list) else 0)

        detalhes.append({
            "n": it["n"],
            "titulo": q["titulo"],
            "tipo": m.tipo,
            "estagio": m.estagio,
            "passou": passou,
            "raciocinio_preenchido": len(raciocinio) >= 15,
            "resultados": res_list,
            "raio_x": raio,
            "solucao": q["solucao"],
            "explicacao": q["explicacao"],
            "entrada_quebrar_exemplo": q["testes"][0]["entrada"] if m.tipo == "quebrar" else None,
        })

    nota_correcao = round((ok_testes / max(1, tot_testes)) * 100)
    nota_edge = round((ok_bordas / max(1, tot_bordas)) * 100)
    nota_qualidade = round(sum(notas_qualidade) / max(1, len(notas_qualidade)))
    nota_eficiencia = round(sum(notas_eficiencia) / max(1, len(notas_eficiencia)))
    bonus_raciocinio = 3 if all(d["raciocinio_preenchido"] for d in detalhes) else 0
    nota_geral = min(
        100,
        round(0.40 * nota_correcao + 0.25 * nota_edge + 0.20 * nota_qualidade + 0.15 * nota_eficiencia) + bonus_raciocinio,
    )

    if nota_geral >= 85:
        veredito = "Aprovado com destaque — raciocínio e código em nível de entrevista técnica."
    elif nota_geral >= 70:
        veredito = "Aprovado — boa base; refine casos de borda e eficiência para passar de primeira."
    elif nota_geral >= 50:
        veredito = "Quase lá — pratique edge cases (Quebre o Código) e revisão espaçada."
    else:
        veredito = "Em construção — reforce os fundamentos da trilha no Treino do Dia e refaça."

    boletim = {
        "id": simulado_id,
        "trilha": ativo["trilha"],
        "duracao_seg": max(0, int(duracao_usada_seg)),
        "criado_em": _agora(),
        "nota_geral": nota_geral,
        "nota_correcao": nota_correcao,
        "nota_eficiencia": nota_eficiencia,
        "nota_qualidade": nota_qualidade,
        "nota_edge_cases": nota_edge,
        "veredito": veredito,
        "resolvidas": sum(1 for d in detalhes if d["passou"]),
        "total": len(detalhes),
        "detalhes": detalhes,
    }

    with _trava:
        p = carregar()
        p["simulado_ativo"] = None
        resumo_salvo = {k: v for k, v in boletim.items() if k != "detalhes"}
        p["simulados"].insert(0, resumo_salvo)
        p["simulados"] = p["simulados"][:50]
        p["xp"] += max(10, nota_geral // 2)
        salvar(p)

    return boletim


# ---------------------------------------------------------------------------
# Painel e estatísticas
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


def _resumo_museu_bugs(p: dict) -> list[dict]:
    cont = Counter(b.get("categoria", "logica_geral") for b in p.get("bugs", []))
    saida = []
    for cat, qtd in cont.most_common(6):
        meta = analisador.CATEGORIAS_BUG.get(cat, analisador.CATEGORIAS_BUG["logica_geral"])
        saida.append({
            "categoria": cat,
            "nome": meta["nome"],
            "cura": meta["cura"],
            "total": qtd,
        })
    return saida


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
        ("edge", "⚡", "Caçador de Edge Cases", "Quebrou 5 códigos com casos-limite", por_tipo["quebrar"] >= 5),
        ("feynman", "📘", "Método Feynman", "Registrou 10 padrões mentais no caderno", len(p.get("padroes", {})) >= 10),
        ("entrevista", "🎯", "Aprovado no Simulado", "Nota >= 70 em um Simulado de Entrevista",
         any(s.get("nota_geral", 0) >= 70 for s in p.get("simulados", []))),
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
                             "liberado": e["n"] <= p["estagio_max"] or p.get("modo_livre", False),
                             "modelos": len(modelos_do_estagio(e["n"]))})
        conc = []
        for cid, st in p["conceitos"].items():
            if cid in CONCEITOS:
                tot = st["acertos"] + st["erros"]
                conc.append({"id": cid, "nome": CONCEITOS[cid]["nome"], "acertos": st["acertos"],
                             "erros": st["erros"], "taxa": round(st["acertos"] / tot * 100) if tot else 0})
        padroes_lista = sorted(
            p.get("padroes", {}).values(),
            key=lambda x: x.get("atualizado_em", ""),
            reverse=True,
        )
        return {
            "hoje": d_hoje,
            "data": data,
            "conjuntos": conjuntos,
            "estagio_atual": p["estagio_atual"],
            "estagio_max": p["estagio_max"],
            "modo_livre": p.get("modo_livre", False),
            "estagio_do_dia": dia["estagio"],
            "trilhas": TRILHAS,
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
            "museu_bugs": _resumo_museu_bugs(p),
            "total_bugs": len(p.get("bugs", [])),
            "padroes": padroes_lista,
            "simulados": p.get("simulados", []),
        }
