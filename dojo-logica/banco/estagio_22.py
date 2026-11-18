"""Estágio 22 - Auditoria de Código Gerado por IA ('Onde a IA Errou?')."""

from .base import exercicio


@exercicio(estagio=22, dificuldade=2, tipo="corrigir", conceitos=["auditoria_ia", "funcoes", "depuracao"])
def ia_bug_argumento_mutavel(r):
    item1 = r.choice(["login", "checkout", "webhook"])
    item2 = r.choice(["email", "pdf", "relatorio"])
    casos = [
        f"print(registrar_log({item1!r}), registrar_log({item2!r}))",
        "print(registrar_log('a', ['init']), registrar_log('b'))",
        "print(registrar_log('x'))",
    ]
    return dict(
        titulo="Auditoria de IA #1: vazamento entre usuários (lista=[])",
        enunciado=(
            "Uma IA gerou a função `registrar_log(evento, historico=[])` para adicionar `evento` à lista `historico` "
            "(criando uma lista nova quando `historico` não for passado) e retorná-la.\n\n"
            "**Problema em produção:** dados de uma chamada estão vazando para a chamada seguinte! Encontre e corrija o bug."
        ),
        codigo_inicial=(
            "def registrar_log(evento, historico=[]):\n"
            "    historico.append(evento)\n"
            "    return historico\n"
        ),
        solucao=(
            "def registrar_log(evento, historico=None):\n"
            "    if historico is None:\n"
            "        historico = []\n"
            "    historico.append(evento)\n"
            "    return historico\n"
        ),
        testes=[{"entrada": "", "chamada": c} for c in casos],
        testes_visiveis=1,
        dicas=[
            "Em Python, valores padrão de parâmetros são avaliados **uma única vez** quando `def` é definido.",
            "Troque `historico=[]` por `historico=None` e crie `historico = []` dentro da função quando `historico is None`.",
        ],
        explicacao=(
            "Um dos bugs mais graves gerados por IA em APIs Python: usar lista/dict mutável como argumento padrão compartilha o mesmo objeto entre requisições!"
        ),
    )


@exercicio(estagio=22, dificuldade=3, tipo="corrigir", conceitos=["auditoria_ia", "listas", "depuracao"])
def ia_bug_mutar_lista_no_for(r):
    lim = r.choice([10, 15, 20, 25])
    casos = [
        ([lim - 1, lim - 2, lim + 5, lim - 3, lim + 1], lim),
        ([2, 4, 6, 8], 10),
        ([15, 25], 10),
        ([], 10),
    ]
    return dict(
        titulo="Auditoria de IA #2: remover itens durante o for",
        enunciado=(
            "A IA escreveu `remover_menores(nums, limite)` para retornar uma lista contendo **apenas** os números "
            "maiores ou iguais a `limite`.\n\n"
            "Em produção, alguns números menores que `limite` escapam do filtro quando aparecem seguidos! Corrija a função sem mutar a lista durante a iteração."
        ),
        codigo_inicial=(
            "def remover_menores(nums, limite):\n"
            "    for x in nums:\n"
            "        if x < limite:\n"
            "            nums.remove(x)\n"
            "    return nums\n"
        ),
        solucao=(
            "def remover_menores(nums, limite):\n"
            "    return [x for x in nums if x >= limite]\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(remover_menores({n!r}, {lm}))"} for n, lm in casos],
        testes_visiveis=2,
        dicas=[
            "Quando você faz `nums.remove(x)` dentro de `for x in nums:`, os índices deslocam para a esquerda e o próximo item é pulado!",
            "Em vez de remover durante o laço, construa uma nova lista: `[x for x in nums if x >= limite]`.",
        ],
        explicacao=(
            "Mutar uma coleção enquanto itera sobre ela causa bugs silenciosos que passam despercebidos em testes com elementos espaçados."
        ),
    )


@exercicio(estagio=22, dificuldade=3, tipo="corrigir", conceitos=["auditoria_ia", "dicionarios", "depuracao"])
def ia_bug_or_com_zero(r):
    padrao = r.choice([10, 15, 20])
    casos = [
        ({"desconto": 0}, padrao),
        ({"desconto": 5}, padrao),
        ({}, padrao),
        ({"desconto": None}, padrao),
    ]
    return dict(
        titulo="Auditoria de IA #3: o perigo do `valor or padrao` quando valor é 0",
        enunciado=(
            "A IA escreveu `obter_desconto(cfg, padrao)` para usar `cfg['desconto']` quando definido e usar `padrao` "
            "somente quando a chave faltar ou for `None`.\n\n"
            "**Problema em produção:** quando um cupom define `desconto = 0` (sem desconto), o sistema aplica o desconto padrão por engano! Corrija."
        ),
        codigo_inicial=(
            "def obter_desconto(cfg, padrao):\n"
            "    return cfg.get('desconto') or padrao\n"
        ),
        solucao=(
            "def obter_desconto(cfg, padrao):\n"
            "    val = cfg.get('desconto')\n"
            "    return padrao if val is None else val\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(obter_desconto({c!r}, {p}))"} for c, p in casos],
        testes_visiveis=2,
        dicas=[
            "Em Python, `0`, `0.0`, `False` e `\"\"` são *falsy*, então `0 or padrao` devolve `padrao`!",
            "Compare explicitamente com `if val is None:` em vez de usar `or`.",
        ],
        explicacao=(
            "Usar `x or padrao` com valores numéricos ou booleanos é um erro recorrente de LLMs que causa prejuízo real em regras financeiras."
        ),
    )


@exercicio(estagio=22, dificuldade=4, tipo="quebrar", conceitos=["auditoria_ia", "depuracao"])
def ia_quebrar_fronteira_desconto(r):
    lim = r.choice([100, 200, 500])
    return dict(
        titulo="Auditoria de IA #4: ache o caso que quebra a regra de frete grátis",
        enunciado=(
            f"Regra de negócio: compras **a partir de R$ {lim}** (`>= {lim}`) têm frete grátis (`0.0`); abaixo disso pagam `25.0`.\n\n"
            "A IA gerou a função `calcular_frete(valor)` abaixo. **Encontre o valor numérico** que prova que o código da IA viola a regra!"
        ),
        modo_quebrar="args",
        funcao_quebrar="calcular_frete",
        placeholder_quebrar=f"Ex.: {lim}",
        codigo_inicial=(
            "def calcular_frete(valor):\n"
            f"    if valor > {lim}:\n"
            "        return 0.0\n"
            "    return 25.0\n"
        ),
        solucao=(
            "def calcular_frete(valor):\n"
            f"    if valor >= {lim}:\n"
            "        return 0.0\n"
            "    return 25.0\n"
        ),
        testes=[{"entrada": str(lim)}],
        testes_visiveis=0,
        dicas=[
            "Compare o texto da regra ('a partir de', ou seja, `>=`) com o operador no `if` gerado pela IA (`>`).",
            "Qual é o único valor exato na fronteira onde `>` e `>=` discordam?",
        ],
        explicacao=(
            f"Na fronteira exata `valor = {lim}`, a IA usou `>` em vez de `>=`, cobrando frete indevido. Sempre teste o valor exato da fronteira!"
        ),
    )


@exercicio(estagio=22, dificuldade=4, tipo="corrigir", conceitos=["auditoria_ia", "dicionarios", "depuracao"])
def ia_bug_copia_rasa_matriz(r):
    val = r.randint(1, 9)
    casos = [
        f"g = criar_grade(2, 2); g[0][0] = {val}; print(g)",
        "g = criar_grade(3, 2); g[1][1] = 7; print(g)",
    ]
    return dict(
        titulo="Auditoria de IA #5: linhas clonadas por referência (`[[0]*c]*l`)",
        enunciado=(
            "A IA escreveu `criar_grade(linhas, colunas)` usando `[[0] * colunas] * linhas` para criar uma matriz de zeros.\n\n"
            "**Problema:** ao alterar `g[0][0] = 5`, TODAS as linhas mudam juntas na coluna 0! Corrija a função para criar linhas independentes."
        ),
        codigo_inicial=(
            "def criar_grade(linhas, colunas):\n"
            "    return [[0] * colunas] * linhas\n"
        ),
        solucao=(
            "def criar_grade(linhas, colunas):\n"
            "    return [[0] * colunas for _ in range(linhas)]\n"
        ),
        testes=[{"entrada": "", "chamada": c} for c in casos],
        testes_visiveis=1,
        dicas=[
            "`[[0] * colunas] * linhas` repete a **mesma referência de lista** várias vezes.",
            "Use uma list comprehension `[[0] * colunas for _ in range(linhas)]` para criar uma lista nova por linha.",
        ],
        explicacao=(
            "Multiplicar uma lista de objetos mutáveis clona ponteiros, não objetos. A comprehension instancia uma linha independente a cada iteração."
        ),
    )


@exercicio(estagio=22, dificuldade=5, tipo="quebrar", conceitos=["auditoria_ia", "depuracao", "strings"])
def ia_quebrar_normalizador_slug(r):
    ex = r.choice(["'  Curso   Python  '", "'Guia  de  IA'", "'  Automacao '"])
    return dict(
        titulo="Auditoria de IA #6: quebre o gerador de slug de URL",
        enunciado=(
            "Uma IA gerou `gerar_slug(titulo)` para transformar títulos em slugs limpos de URL: minúsculo, "
            "espaços trocados por `-`, **sem** múltiplos hifens seguidos (`--`) e **sem** hífen no começo ou no fim.\n\n"
            "**Seu desafio:** forneça uma string (entre aspas) que faça o código da IA gerar um slug fora do padrão!"
        ),
        modo_quebrar="args",
        funcao_quebrar="gerar_slug",
        placeholder_quebrar="Ex.: '  Curso   Python  '",
        codigo_inicial=(
            "def gerar_slug(titulo):\n"
            "    return titulo.lower().replace(' ', '-')\n"
        ),
        solucao=(
            "def gerar_slug(titulo):\n"
            "    return '-'.join(titulo.lower().split())\n"
        ),
        testes=[{"entrada": ex}],
        testes_visiveis=0,
        dicas=[
            "Veja o que `.replace(' ', '-')` faz quando há espaços no início, no fim ou dois espaços seguidos.",
            "Compare com `'-'.join(titulo.lower().split())`!",
        ],
        explicacao=(
            "`.replace(' ', '-')` transforma espaços extras em `'--'` ou hifens nas pontas (`'-curso---python-'`). "
            "`'-'.join(titulo.lower().split())` resolve todos esses edge cases numa linha."
        ),
    )
