"""
Rastreador passo a passo (teste de mesa automático).

Uso: python rastreador.py config.json
config: {"codigo": str, "entrada": str}
Imprime no stdout um JSON: {"passos": [...], "erro": {...}|null, "limite": bool}
Cada passo: {"linha": n, "evento": "line"|"return", "escopo": "principal"|"nome_funcao",
             "vars": {nome: [repr, tipo]}, "pilha": [...], "saida": "texto acumulado",
             "retorno": [repr, tipo] (só em return)}
"""

import builtins
import io
import json
import sys
import time
import types

ARQ = "seu_codigo.py"
MAX_PASSOS = 600
MAX_REPR = 90


class Limite(Exception):
    pass


class _TempoLimite(Exception):
    pass


def resumo(v):
    if isinstance(v, types.FunctionType):
        return [f"função {v.__name__}()", "function"]
    try:
        r = repr(v)
    except Exception:  # noqa: BLE001
        r = "<?>"
    if len(r) > MAX_REPR:
        r = r[: MAX_REPR - 3] + "..."
    return [r, type(v).__name__]


def snapshot(d):
    out = {}
    for k, v in d.items():
        if k.startswith("__") or isinstance(v, types.ModuleType):
            continue
        if isinstance(v, (types.BuiltinFunctionType, type)):
            continue
        out[k] = resumo(v)
    return out


def rastrear_codigo(codigo: str, entrada: str = "", limite_segundos: float | None = None) -> dict:
    """Executa o código passo a passo e retorna ``{"passos", "erro", "limite"}``."""
    linhas_entrada = iter(entrada.split("\n")) if entrada else iter(())
    saida = io.StringIO()
    passos = []
    inicio = time.perf_counter()

    def _input(prompt=""):
        try:
            valor = next(linhas_entrada)
        except StopIteration:
            raise EOFError("SEM_ENTRADA") from None
        saida.write(f"{prompt}{valor}\n")
        return valor

    def pilha_de(frame):
        nomes = []
        f = frame
        while f is not None:
            if f.f_code.co_filename == ARQ:
                nomes.append("principal" if f.f_code.co_name == "<module>" else f.f_code.co_name)
            f = f.f_back
        return list(reversed(nomes))

    def registrar(frame, evento, arg=None):
        if len(passos) >= MAX_PASSOS:
            raise Limite()
        if limite_segundos is not None and (time.perf_counter() - inicio) > limite_segundos:
            raise _TempoLimite()
        escopo = "principal" if frame.f_code.co_name == "<module>" else frame.f_code.co_name
        p = {
            "linha": frame.f_lineno,
            "evento": evento,
            "escopo": escopo,
            "vars": snapshot(frame.f_locals),
            "globais": snapshot(frame.f_globals) if escopo != "principal" else None,
            "pilha": pilha_de(frame),
            "saida": saida.getvalue(),
        }
        if evento == "return":
            p["retorno"] = resumo(arg)
        passos.append(p)

    def rastro(frame, evento, arg):
        if frame.f_code.co_filename != ARQ:
            return None
        if evento in ("line", "return"):
            registrar(frame, evento, arg)
        return rastro

    b = dict(builtins.__dict__)
    b["input"] = _input
    g = {"__name__": "__main__", "__builtins__": b}
    erro = None
    limite = False
    try:
        cod = compile(codigo, ARQ, "exec")
    except SyntaxError as e:
        return {
            "passos": [],
            "limite": False,
            "erro": {
                "tipo": "SyntaxError",
                "mensagem": e.msg,
                "linha": e.lineno,
                "texto": (e.text or "").rstrip(),
            },
        }

    orig_stdout = sys.stdout
    orig_trace = sys.gettrace()
    sys.stdout = saida
    sys.settrace(rastro)
    try:
        exec(cod, g)
    except Limite:
        limite = True
    except _TempoLimite:
        erro = {
            "tipo": "Tempo",
            "mensagem": f"O programa passou de {limite_segundos:g} segundos.",
            "linha": None,
            "texto": "",
        }
        limite = True
    except SystemExit:
        pass
    except BaseException as e:  # noqa: BLE001
        tb = e.__traceback__
        linha = None
        while tb is not None:
            if tb.tb_frame.f_code.co_filename == ARQ:
                linha = tb.tb_lineno
            tb = tb.tb_next
        erro = {"tipo": type(e).__name__, "mensagem": str(e), "linha": linha, "texto": ""}
    finally:
        sys.settrace(orig_trace)
        sys.stdout = orig_stdout

    if passos:
        final = dict(passos[-1])
        final["evento"] = "fim"
        final["saida"] = saida.getvalue()
        passos.append(final)
    return {"passos": passos, "erro": erro, "limite": limite}


def main():
    with open(sys.argv[1], encoding="utf-8") as f:
        cfg = json.load(f)
    dados = rastrear_codigo(cfg["codigo"], cfg.get("entrada", ""))
    sys.stdout.write(json.dumps(dados, ensure_ascii=False))


if __name__ == "__main__":
    main()
