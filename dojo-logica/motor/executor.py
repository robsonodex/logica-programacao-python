"""Executa código do aluno em processo separado, compara saídas e traduz erros."""

from __future__ import annotations

import io
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import unicodedata

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
# Comparação de saídas (Exato, Quase e Equivalência Lógica)
# ---------------------------------------------------------------------------

_PALAVRAS_NEUTRAS = {
    "o", "a", "os", "as", "de", "do", "da", "dos", "das", "e", "em", "no", "na",
    "nos", "nas", "um", "uma", "para", "ao", "com", "por", "que", "se", "seu",
    "sua", "foi", "eh", "esta", "sao", "numero", "valor", "resultado", "status",
    "situacao", "saida", "resposta", "total", "final",
}

_PARES_OPOSTOS = (
    ("par", "impar"),
    ("aprovado", "reprovado"),
    ("positivo", "negativo"),
    ("sim", "nao"),
    ("maior", "menor"),
    ("valido", "invalido"),
    ("verdadeiro", "falso"),
    ("true", "false"),
    ("ganhou", "perdeu"),
    ("ativo", "inativo"),
    ("dentro", "fora"),
    ("aceito", "recusado"),
)


def normalizar(txt: str) -> list[str]:
    linhas = [l.rstrip() for l in txt.replace("\r\n", "\n").split("\n")]
    while linhas and not linhas[-1]:
        linhas.pop()
    while linhas and not linhas[0]:
        linhas.pop(0)
    return linhas


def _sem_acentos(txt: str) -> str:
    nfkd = unicodedata.normalize("NFKD", txt)
    return "".join(ch for ch in nfkd if not unicodedata.combining(ch))


def _parece_estrutura_exata(linhas: list[str]) -> bool:
    """Identifica saídas técnicas (listas, dicts, tuplas, slugs, booleanos) que exigem contrato exato."""
    if not linhas:
        return True
    for l in linhas:
        s = l.strip()
        if not s:
            continue
        if s[0] in "[{('\"" or s in ("True", "False", "None"):
            return True
        if " " not in s and ("-" in s or "_" in s) and any(ch.isalpha() for ch in s):
            return True
    return False


def _tokens_texto(linha: str) -> list[str]:
    limpa = _sem_acentos(linha).lower()
    return re.findall(r"[a-z0-9]+", limpa)


def _extrair_numeros(linha: str) -> list[float]:
    brutos = re.findall(r"(?<![a-zA-Z0-9_])-?\d+(?:[.,]\d+)?(?![a-zA-Z0-9_])", linha)
    out = []
    for b in brutos:
        try:
            out.append(float(b.replace(",", ".")))
        except ValueError:
            pass
    return out


def _tem_contradicao(toks_a: set[str], toks_b: set[str]) -> bool:
    if ("nao" in toks_a) != ("nao" in toks_b):
        return True
    for w1, w2 in _PARES_OPOSTOS:
        if w1 in toks_b and w2 in toks_a and w2 not in toks_b:
            return True
        if w2 in toks_b and w1 in toks_a and w1 not in toks_b:
            return True
    return False


def _eh_equivalente_linha(la: str, lb: str) -> bool:
    nums_a = _extrair_numeros(la)
    nums_b = _extrair_numeros(lb)
    toks_a_list = _tokens_texto(la)
    toks_b_list = _tokens_texto(lb)
    toks_a = set(toks_a_list)
    toks_b = set(toks_b_list)

    if not toks_a_list or not toks_b_list:
        return False
    if _tem_contradicao(toks_a, toks_b):
        return False

    # 1. Saída numérica: mesmos valores calculados (ex.: "Media = 8.5" vs "Média final: 8.50")
    if nums_b:
        if len(nums_a) != len(nums_b):
            return False
        return all(abs(x - y) <= 1e-6 for x, y in zip(nums_a, nums_b))

    # Se o esperado não tem número, mas o aluno imprimiu números extras, não aprova por equivalência
    if nums_a:
        return False

    # 2. Classificação/decisão curta (ex.: "Par", "Aprovado", "Maior de idade")
    if len(toks_b_list) <= 4:
        relev_b = [t for t in toks_b_list if t not in _PALAVRAS_NEUTRAS] or toks_b_list
        return all(t in toks_a for t in relev_b) and len(toks_a_list) <= 10

    # 3. Frase textual com variáveis dinâmicas (ex.: "Bem vindo Iara ao curso de Logica")
    # Toda palavra com maiúscula no meio da frase (nomes/valores dinâmicos) deve estar presente
    palavras_orig = re.findall(r"[A-Za-zÀ-ÿ]+", lb)
    dinamicas = {
        _sem_acentos(w).lower()
        for idx, w in enumerate(palavras_orig)
        if idx > 0 and w[0].isupper()
    }
    if not dinamicas.issubset(toks_a):
        return False

    relev_b = [t for t in toks_b_list if t not in _PALAVRAS_NEUTRAS and len(t) > 1]
    if not relev_b:
        return False
    acertos = sum(1 for t in relev_b if t in toks_a)
    cobertura = acertos / len(relev_b)
    return cobertura >= 0.70 and len(toks_a_list) <= len(toks_b_list) * 2 + 3


def comparar(obtido: str, esperado: str, modo: str = "flexivel") -> str:
    """Compara saídas retornando 'exato', 'quase', 'equivalente' ou 'diferente'.

    - modo='rigoroso': exige correspondência exata linha a linha (Entrevista / Modo Rigoroso).
    - modo='padrao': aceita 'exato' e 'quase' por espaços/maiúsculas (funções e prever).
    - modo='flexivel': aceita 'exato', 'quase' (acentos/hífens/pontuação cosmética) e
      'equivalente' (mesmo resultado lógico/numérico com redação própria do aluno).
    """
    a, b = normalizar(obtido), normalizar(esperado)
    if a == b:
        return "exato"
    if modo == "rigoroso":
        return "diferente"

    sa = [" ".join(l.split()).lower() for l in a if l.strip()]
    sb = [" ".join(l.split()).lower() for l in b if l.strip()]
    if sa == sb:
        return "quase"

    if modo != "flexivel" or _parece_estrutura_exata(b):
        return "diferente"

    # Mesmo texto ignorando acentos, hífens e pontuação cosmética
    ca = [" ".join(_tokens_texto(l)) for l in a if l.strip()]
    cb = [" ".join(_tokens_texto(l)) for l in b if l.strip()]
    if ca and ca == cb:
        return "quase"

    # Equivalência lógica linha a linha (mesmos números/decisões/valores dinâmicos)
    a_ne = [l for l in a if l.strip()]
    b_ne = [l for l in b if l.strip()]
    if len(a_ne) == len(b_ne) and a_ne and all(_eh_equivalente_linha(la, lb) for la, lb in zip(a_ne, b_ne)):
        return "equivalente"

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
