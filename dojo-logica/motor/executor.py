"""Executa código do aluno em processo separado, compara saídas e traduz erros."""

from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import tempfile
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
FILHO = os.path.join(AQUI, "executor_aluno.py")
RASTREADOR = os.path.join(AQUI, "rastreador.py")
LIMITE_SEGUNDOS = 5
LIMITE_SAIDA = 20000

_ENV = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")


def _rodar_filho(script: str, cfg: dict, stdin_txt: str = "", limite: float = LIMITE_SEGUNDOS):
    fd, caminho = tempfile.mkstemp(suffix=".json", prefix="dojo_")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False)
        flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        inicio = time.perf_counter()
        try:
            p = subprocess.run(
                [sys.executable, "-X", "utf8", script, caminho],
                input=stdin_txt.encode("utf-8"),
                capture_output=True,
                timeout=limite,
                env=_ENV,
                creationflags=flags,
            )
        except subprocess.TimeoutExpired as e:
            out = (e.stdout or b"").decode("utf-8", "replace")
            return {"saida": out[:LIMITE_SAIDA], "erro": {
                "tipo": "Tempo", "mensagem": f"O programa passou de {limite:g} segundos.",
                "linha": None, "texto": ""}, "tempo": limite}
        tempo = time.perf_counter() - inicio
        out = p.stdout.decode("utf-8", "replace")
        err = p.stderr.decode("utf-8", "replace")
        erro = None
        for linha in err.splitlines():
            if linha.startswith("@@ERRO@@"):
                erro = json.loads(linha[8:])
        if erro is None and p.returncode not in (0, None) and script == FILHO:
            erro = {"tipo": "Erro", "mensagem": err.strip()[-500:], "linha": None, "texto": ""}
        if len(out) > LIMITE_SAIDA:
            out = out[:LIMITE_SAIDA] + "\n... (saída cortada: muito texto!)"
        return {"saida": out, "erro": erro, "tempo": round(tempo, 3), "stderr": err}
    finally:
        try:
            os.remove(caminho)
        except OSError:
            pass


def _executar_em_processo(codigo: str, stdin_txt: str, chamada: str, eco: bool) -> dict:
    from .executor_aluno import executar_isolado

    r = executar_isolado(
        codigo,
        io.StringIO(stdin_txt),
        chamada=chamada,
        eco=eco,
        limite_segundos=LIMITE_SEGUNDOS,
    )
    if len(r["saida"]) > LIMITE_SAIDA:
        r["saida"] = r["saida"][:LIMITE_SAIDA] + "\n... (saída cortada: muito texto!)"
    return r


def _rastrear_em_processo(codigo: str, entrada: str) -> dict:
    from .rastreador import rastrear_codigo

    return rastrear_codigo(codigo, entrada, limite_segundos=8.0)


def executar(codigo: str, entrada: str = "", chamada: str = "", eco: bool = False) -> dict:
    stdin_txt = entrada + ("\n" if entrada and not entrada.endswith("\n") else "")
    if sys.platform == "emscripten":
        r = _executar_em_processo(codigo, stdin_txt, chamada, eco)
    else:
        r = _rodar_filho(FILHO, {"codigo": codigo, "chamada": chamada, "eco": eco}, stdin_txt)
        r.pop("stderr", None)
    if r["erro"]:
        r["erro"]["explicacao"] = traduzir_erro(r["erro"])
    return r


def rastrear(codigo: str, entrada: str = "") -> dict:
    if sys.platform == "emscripten":
        dados = _rastrear_em_processo(codigo, entrada)
    else:
        r = _rodar_filho(RASTREADOR, {"codigo": codigo, "entrada": entrada}, "", limite=10)
        if r.get("erro") and r["erro"]["tipo"] == "Tempo":
            return {"passos": [], "erro": {**r["erro"], "explicacao": traduzir_erro(r["erro"])}, "limite": True}
        try:
            dados = json.loads(r["saida"])
        except (json.JSONDecodeError, TypeError):
            return {"passos": [], "erro": {"tipo": "Erro", "mensagem": r.get("stderr", "")[-500:],
                                           "linha": None, "texto": "", "explicacao": ""}, "limite": False}
    if dados.get("erro"):
        dados["erro"]["explicacao"] = traduzir_erro(dados["erro"])
    return dados


# ---------------------------------------------------------------------------
# Comparação de saídas
# ---------------------------------------------------------------------------

def normalizar(txt: str) -> list[str]:
    linhas = [l.rstrip() for l in txt.replace("\r\n", "\n").split("\n")]
    while linhas and not linhas[-1]:
        linhas.pop()
    while linhas and not linhas[0]:
        linhas.pop(0)
    return linhas


def comparar(obtido: str, esperado: str) -> str:
    """Retorna 'exato', 'quase' (difere só em espaços/maiúsculas) ou 'diferente'."""
    a, b = normalizar(obtido), normalizar(esperado)
    if a == b:
        return "exato"
    sa = [" ".join(l.split()).lower() for l in a if l.strip()]
    sb = [" ".join(l.split()).lower() for l in b if l.strip()]
    if sa == sb:
        return "quase"
    return "diferente"


# ---------------------------------------------------------------------------
# Erros em português
# ---------------------------------------------------------------------------

def traduzir_erro(erro: dict) -> str:
    tipo = erro.get("tipo", "")
    msg = erro.get("mensagem", "") or ""
    if tipo == "Tempo":
        return ("Seu programa demorou demais. O suspeito nº 1 é um **loop infinito**: confira se a condição "
                "do `while` em algum momento fica falsa (a variável de controle está mudando dentro do laço?).")
    if tipo == "EOFError" or "SEM_ENTRADA" in msg:
        return ("O programa chamou `input()` mais vezes do que há linhas de entrada. Confira quantos valores "
                "o enunciado diz que serão lidos — ou, no botão Executar, preencha a caixa **Entrada** "
                "(um valor por linha).")
    if tipo == "IndentationError" or tipo == "TabError":
        return ("Problema de **indentação** (os espaços no começo da linha). Em Python, o que está dentro de um "
                "`if`, `while`, `for` ou `def` precisa estar recuado (4 espaços) e alinhado. Linhas do mesmo "
                "bloco devem ter exatamente o mesmo recuo.")
    if tipo == "SyntaxError":
        dicas = ["O Python não conseguiu nem **entender** o código (erro de escrita/gramática)."]
        m = msg.lower()
        if "expected ':'" in m:
            dicas.append("Faltou os **dois-pontos `:`** no fim da linha do `if`/`elif`/`else`/`while`/`for`/`def`.")
        elif "unterminated string" in m or "eol while scanning" in m:
            dicas.append("Um texto foi aberto com aspas e **não foi fechado**.")
        elif "was never closed" in m or "unexpected eof" in m:
            dicas.append("Algum **parêntese, colchete ou aspas** foi aberto e não foi fechado.")
        elif "invalid syntax. maybe you meant '==' " in m or "maybe you meant '=='" in m:
            dicas.append("Para **comparar** use `==`. Um só `=` é para **guardar** valor em variável.")
        elif "invalid character" in m:
            dicas.append("Há um caractere estranho (talvez aspas “curvas” copiadas de outro lugar). Use aspas retas \" ou '.")
        elif "perhaps you forgot a comma" in m:
            dicas.append("Parece que faltou uma **vírgula** separando itens (por exemplo, dentro do `print`).")
        elif "cannot assign to" in m:
            dicas.append("O lado esquerdo do `=` precisa ser um **nome de variável**. Se queria comparar, use `==`.")
        elif "___" in (erro.get("texto") or ""):
            dicas.append("Ainda há uma lacuna `___` para completar.")
        dicas.append("Olhe a linha indicada **e a linha anterior** — às vezes o erro começa antes.")
        return " ".join(dicas)
    if tipo == "NameError":
        nome = msg.split("'")[1] if "'" in msg else "?"
        if nome == "___":
            return "Ainda existe uma lacuna `___` no código. Troque-a pelo código que falta."
        return (f"O Python não conhece nada chamado `{nome}`. Possíveis causas: a variável ainda não foi criada "
                "antes desta linha; erro de digitação (maiúsculas contam!); ou faltaram **aspas** se a intenção "
                "era escrever um texto.")
    if tipo == "TypeError":
        if "can only concatenate str" in msg or "unsupported operand" in msg and "str" in msg:
            return ("Você misturou **texto (str)** com **número** numa operação. Lembre: `input()` sempre devolve "
                    "texto — converta com `int()` ou `float()` para fazer contas, ou use `str()`/f-string para juntar "
                    "com texto.")
        if "not callable" in msg:
            return ("Algo que não é função foi usado com parênteses `()`. Você pode ter dado a uma variável o "
                    "mesmo nome de uma função (ex.: `print = 5` ou `sum = 0`).")
        if "missing" in msg and "argument" in msg:
            return "A função foi chamada com **menos argumentos** do que os parâmetros definidos no `def`."
        if "takes" in msg and "given" in msg:
            return "A função foi chamada com uma quantidade de argumentos diferente da definida no `def`."
        if "not supported between" in msg:
            return ("Você comparou (`<`, `>`) valores de tipos diferentes, como texto com número. Converta "
                    "o texto com `int()`/`float()` antes.")
        if "'str' object does not support item assignment" in msg:
            return "Strings são **imutáveis**: não dá para trocar uma letra com `texto[i] = ...`. Monte uma nova string."
        if "indices must be integers" in msg:
            return "O índice entre colchetes precisa ser um **inteiro**. Use `int()` ou `//` em vez de `/`."
        return "Operação com um tipo de dado inadequado. Confira os tipos das variáveis envolvidas (use `type()`)."
    if tipo == "ValueError":
        if "invalid literal for int()" in msg:
            return ("`int()` recebeu um texto que não é um número inteiro (ex.: `\"3.5\"`, `\"abc\"` ou vazio). Se o "
                    "valor pode ter casas decimais, use `float()`.")
        if "could not convert string to float" in msg:
            return "`float()` recebeu um texto que não representa um número. Em Python o decimal usa **ponto**: `3.5`."
        if "not in list" in msg:
            return "Você tentou remover/buscar na lista um valor que **não está** nela."
        return "Um valor com o tipo certo, mas conteúdo inválido, foi passado para uma função."
    if tipo == "ZeroDivisionError":
        return ("Divisão por **zero**! Nenhum número pode ser dividido por 0. Antes de dividir, verifique "
                "com `if` se o divisor é diferente de zero.")
    if tipo == "IndexError":
        return ("Índice fora do limite. Uma sequência com `n` itens tem índices de `0` até `n-1`. Confira se o "
                "laço não está indo um passo além (`range(len(lista))` já para no lugar certo).")
    if tipo == "KeyError":
        return "Você buscou uma chave que não existe no dicionário."
    if tipo == "AttributeError":
        return ("Esse tipo de dado não tem o método/atributo usado. Ex.: `append` é de listas, `upper` é de strings. "
                "Confira o tipo da variável e a grafia do método.")
    if tipo == "RecursionError":
        return "Uma função chamou a si mesma vezes demais (recursão sem fim)."
    if tipo == "UnboundLocalError":
        return ("Dentro da função você usou uma variável antes de dar valor a ela. Variáveis criadas dentro da "
                "função são **locais**; passe o valor como parâmetro.")
    return "Leia a mensagem do erro e a linha indicada. Use o Laboratório (rastreador) para ver o programa passo a passo."
