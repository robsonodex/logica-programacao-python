"""
Valida todos os modelos do banco de exercícios.

Uso:
    python ferramentas/validar_banco.py            # valida tudo
    python ferramentas/validar_banco.py 3 4        # só os estágios 3 e 4
    python ferramentas/validar_banco.py --mostrar estagio_03.soma   # imprime uma questão gerada

Para cada modelo, gera a questão com várias sementes e verifica:
- campos obrigatórios e tipos
- o gabarito roda sem erro em todos os testes e produz saída
- "corrigir": o código inicial realmente falha em pelo menos um teste
- "completar": o código inicial contém ___
- variedade: sementes diferentes geram questões diferentes
"""

import os
import sys
import threading

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from banco import REGISTRO, executar_referencia  # noqa: E402
from motor.conceitos import CONCEITOS  # noqa: E402

SEMENTES = range(25)


def rodar_com_limite(codigo, entrada, chamada, limite=2.0):
    res = {}

    def alvo():
        try:
            res["saida"] = executar_referencia(codigo, entrada, chamada)
        except BaseException as e:  # noqa: BLE001
            res["erro"] = f"{type(e).__name__}: {e}"

    t = threading.Thread(target=alvo, daemon=True)
    t.start()
    t.join(limite)
    if t.is_alive():
        return None, "TEMPO ESGOTADO (loop infinito?)"
    return res.get("saida"), res.get("erro")


def validar_modelo(m):
    problemas = []
    avisos = []
    enunciados = set()
    if not 1 <= m.dificuldade <= 5:
        problemas.append("dificuldade fora de 1..5")
    for c in m.conceitos:
        if c not in CONCEITOS:
            problemas.append(f"conceito sem lição em motor/conceitos.py: {c}")
    for s in SEMENTES:
        try:
            q = m.gerar(s)
        except Exception as e:  # noqa: BLE001
            problemas.append(f"semente {s}: erro ao gerar: {type(e).__name__}: {e}")
            break
        for campo, tipo in (("titulo", str), ("enunciado", str), ("solucao", str),
                            ("dicas", list), ("explicacao", str)):
            if not isinstance(q.get(campo), tipo) or not q.get(campo):
                problemas.append(f"campo '{campo}' ausente/vazio ou de tipo errado")
        if problemas:
            break
        if not 2 <= len(q["dicas"]) <= 4:
            problemas.append("use de 2 a 4 dicas")
        enunciados.add(q["enunciado"] + q["solucao"] + q["codigo_inicial"] + repr(q["testes"]))
        if m.tipo in ("corrigir", "completar", "quebrar") and not q["codigo_inicial"].strip():
            problemas.append("tipo exige codigo_inicial")
        if m.tipo == "completar" and "___" not in q["codigo_inicial"]:
            problemas.append("codigo_inicial de 'completar' precisa ter ___")
        if m.tipo == "quebrar":
            t0 = q["testes"][0]
            chamada_q = f"print(repr({q['funcao_quebrar']}({t0['entrada']})))" if q.get("modo_quebrar") == "args" else t0["chamada"]
            ent_q = "" if q.get("modo_quebrar") == "args" else t0["entrada"]
            s_ref, e_ref = rodar_com_limite(q["solucao"], ent_q, chamada_q)
            if e_ref:
                problemas.append(f"semente {s}: gabarito de 'quebrar' falhou na entrada de exemplo -> {e_ref}")
            else:
                s_bug, e_bug = rodar_com_limite(q["codigo_inicial"], ent_q, chamada_q)
                if not e_bug and s_bug is not None and s_bug.strip() == (s_ref or "").strip():
                    problemas.append(f"semente {s}: entrada de exemplo não quebrou o código bugado")
            if problemas:
                break
            continue
        if m.tipo in ("codigo", "funcao", "corrigir", "completar"):
            usa_input = "input(" in q["solucao"]
            if (usa_input or m.tipo == "funcao") and len(q["testes"]) < 3:
                problemas.append(f"semente {s}: use pelo menos 3 testes")
        saidas = []
        for i, t in enumerate(q["testes"]):
            saida, erro = rodar_com_limite(q["solucao"], t["entrada"], t["chamada"])
            if erro:
                problemas.append(f"semente {s}, teste {i}: gabarito falhou -> {erro}")
                continue
            if not saida.strip():
                problemas.append(f"semente {s}, teste {i}: gabarito não imprimiu nada")
            saidas.append(saida)
        if m.tipo == "corrigir" and saidas:
            falhou = False
            for t, esperado in zip(q["testes"], saidas):
                saida, erro = rodar_com_limite(q["codigo_inicial"], t["entrada"], t["chamada"])
                if erro or saida is None or saida.split() != esperado.split():
                    falhou = True
                    break
            if not falhou:
                problemas.append(f"semente {s}: o código com bug passa em todos os testes (bug não detectado)")
        if m.tipo == "prever" and "input(" in q["solucao"] and not q["testes"][0]["entrada"]:
            problemas.append("prever com input() precisa de entrada no teste")
        if problemas:
            break
    if len(enunciados) < 3:
        avisos.append(f"pouca variedade: só {len(enunciados)} versões distintas em {len(SEMENTES)} sementes")
    return problemas, avisos


def mostrar(mid, semente=0):
    m = REGISTRO[mid]
    q = m.gerar(semente)
    print(f"== {mid} (estágio {m.estagio}, dif {m.dificuldade}, {m.tipo}, {m.conceitos})")
    for k in ("titulo", "enunciado", "codigo_inicial", "solucao", "explicacao"):
        print(f"--- {k}:\n{q[k]}")
    print("--- dicas:", *q["dicas"], sep="\n  * ")
    for t in q["testes"]:
        print(f"--- teste entrada={t['entrada']!r} chamada={t['chamada']!r}")
        print(executar_referencia(q["solucao"], t["entrada"], t["chamada"]))


def main():
    args = sys.argv[1:]
    if args and args[0] == "--mostrar":
        mostrar(args[1], int(args[2]) if len(args) > 2 else 0)
        return
    filtro = {int(a) for a in args}
    total_erros = 0
    por_estagio = {}
    for mid, m in sorted(REGISTRO.items(), key=lambda kv: (kv[1].estagio, kv[0])):
        if filtro and m.estagio not in filtro:
            continue
        por_estagio.setdefault(m.estagio, []).append(m)
        problemas, avisos = validar_modelo(m)
        if problemas or avisos:
            print(f"[{'ERRO' if problemas else 'aviso'}] {mid}")
            for p in problemas[:5]:
                print("    x", p)
            for a in avisos:
                print("    !", a)
        total_erros += bool(problemas)
    print()
    for e, ms in sorted(por_estagio.items()):
        tipos = {}
        for m in ms:
            tipos[m.tipo] = tipos.get(m.tipo, 0) + 1
        difs = sorted(m.dificuldade for m in ms)
        print(f"Estágio {e:2}: {len(ms):3} modelos | tipos {tipos} | dificuldades {difs}")
    print(f"\n{'OK' if not total_erros else f'{total_erros} modelo(s) com erro'}")
    sys.exit(1 if total_erros else 0)


if __name__ == "__main__":
    main()
