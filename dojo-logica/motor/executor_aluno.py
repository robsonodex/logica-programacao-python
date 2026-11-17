"""
Processo-filho que executa o código do aluno.

Uso: python executor_aluno.py config.json   (a entrada do programa vem pelo stdin)
config: {"codigo": str, "chamada": str, "eco": bool}

- eco=True  (botão Executar): mostra a mensagem do input() e o valor digitado, como num terminal.
- eco=False (botão Verificar): input() não imprime nada, para comparar só os prints.
Erros são enviados ao stderr numa linha  @@ERRO@@{json}.
"""

import builtins
import io
import json
import sys
import time
import traceback

ARQ = "seu_codigo.py"


class _TempoEsgotado(BaseException):
    pass


def _extrair_erro(exc: BaseException) -> dict:
    info = {"tipo": type(exc).__name__, "mensagem": str(exc), "linha": None, "texto": ""}
    if isinstance(exc, SyntaxError) and exc.filename == ARQ:
        info["linha"] = exc.lineno
        info["texto"] = (exc.text or "").rstrip()
        info["mensagem"] = exc.msg
    else:
        quadros = traceback.extract_tb(exc.__traceback__)
        do_aluno = [q for q in quadros if q.filename == ARQ]
        if do_aluno:
            info["linha"] = do_aluno[-1].lineno
            info["texto"] = (do_aluno[-1].line or "").strip()
        elif any(q.filename == "teste_automatico.py" for q in quadros):
            info["no_teste"] = True
    return info


def executar_isolado(
    codigo: str,
    entrada_stream,
    chamada: str = "",
    eco: bool = False,
    limite_segundos: float | None = None,
    saida_stream=None,
) -> dict | None:
    """Executa código do aluno com input/namespace isolados.

    Quando ``saida_stream`` é fornecido (modo subprocesso), escreve nele e retorna
    ``dict`` de erro apenas se houver falha. Caso contrário, captura stdout e
    retorna ``{"saida": str, "erro": dict | None, "tempo": float}``.
    """
    capturar = saida_stream is None
    buf_out = io.StringIO() if capturar else saida_stream

    def _input(prompt=""):
        linha = entrada_stream.readline()
        if linha == "":
            raise EOFError("SEM_ENTRADA")
        linha = linha.rstrip("\r\n")
        if eco:
            buf_out.write(f"{prompt}{linha}\n")
        return linha

    b = dict(builtins.__dict__)
    b["input"] = _input
    g = {"__name__": "__main__", "__builtins__": b}

    inicio = time.perf_counter()
    passos = 0

    def _vigiar(frame, evento, arg):
        nonlocal passos
        if evento == "line" and limite_segundos is not None:
            passos += 1
            if passos % 200 == 0 and (time.perf_counter() - inicio) > limite_segundos:
                raise _TempoEsgotado()
        return _vigiar

    orig_stdout = sys.stdout
    orig_trace = sys.gettrace()
    erro = None
    try:
        if capturar:
            sys.stdout = buf_out
        if limite_segundos is not None:
            sys.settrace(_vigiar)
        exec(compile(codigo, ARQ, "exec"), g)
        if chamada:
            exec(compile(chamada, "teste_automatico.py", "exec"), g)
    except SystemExit:
        pass
    except _TempoEsgotado:
        erro = {
            "tipo": "Tempo",
            "mensagem": f"O programa passou de {limite_segundos:g} segundos.",
            "linha": None,
            "texto": "",
        }
    except BaseException as e:  # noqa: BLE001
        if capturar:
            buf_out.flush()
        else:
            sys.stdout.flush()
        erro = _extrair_erro(e)
    finally:
        sys.settrace(orig_trace)
        if capturar:
            sys.stdout = orig_stdout

    tempo = round(time.perf_counter() - inicio, 3)
    if capturar:
        return {"saida": buf_out.getvalue(), "erro": erro, "tempo": tempo}
    return erro


def main():
    with open(sys.argv[1], encoding="utf-8") as f:
        cfg = json.load(f)
    erro = executar_isolado(
        cfg["codigo"],
        sys.stdin,
        chamada=cfg.get("chamada", ""),
        eco=cfg.get("eco", False),
        saida_stream=sys.stdout,
    )
    if erro is not None:
        sys.stderr.write("@@ERRO@@" + json.dumps(erro, ensure_ascii=False) + "\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
