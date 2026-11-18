"""Estágio 15 - Tuplas, Comprehensions e Ordenação customizada (key=lambda)."""

from .base import exercicio


@exercicio(estagio=15, dificuldade=1, tipo="funcao", conceitos=["comprehensions", "funcoes", "return"])
def quadrados_dos_pares(r):
    l1 = [r.randint(-6, 12) for _ in range(6)]
    casos = [l1, [1, 2, 3, 4, 5, 6], [1, 3, 5], []]
    esp0 = [x * x for x in l1 if x % 2 == 0]
    return dict(
        titulo="Filtrar e transformar com list comprehension",
        enunciado=(
            "Escreva a função `quadrados_pares(nums)` que retorna uma nova lista com o **quadrado (`x ** 2`)** "
            "apenas dos números **pares** de `nums`, mantendo a ordem original.\n\n"
            f"Exemplo: `quadrados_pares({l1!r})` -> `{esp0!r}`"
        ),
        solucao=(
            "def quadrados_pares(nums):\n"
            "    return [x * x for x in nums if x % 2 == 0]\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(quadrados_pares({c!r}))"} for c in casos],
        testes_visiveis=2,
        dicas=[
            "Use uma list comprehension com filtro no final: `[expressao for x in nums if condicao]`.",
            "Um número é par quando `x % 2 == 0`.",
        ],
        explicacao=(
            "A list comprehension `[x * x for x in nums if x % 2 == 0]` filtra e transforma em uma única linha expressiva."
        ),
    )


@exercicio(estagio=15, dificuldade=2, tipo="funcao", conceitos=["tuplas", "funcoes", "return"])
def combinar_com_zip(r):
    nomes = r.sample(["Ana", "Bruno", "Carla", "Diego", "Elisa"], 3)
    notas = [round(r.uniform(5.0, 10.0), 1) for _ in range(3)]
    casos = [(nomes, notas), (["A", "B"], [10, 8]), ([], [])]
    esp0 = dict(zip(nomes, notas))
    return dict(
        titulo="Unir listas paralelas com zip",
        enunciado=(
            "Escreva a função `mapear_notas(nomes, notas)` que recebe duas listas de mesmo tamanho e retorna "
            "um dicionário associando cada nome à respectiva nota.\n\n"
            f"Exemplo: `mapear_notas({nomes!r}, {notas!r})` -> `{esp0!r}`"
        ),
        solucao=(
            "def mapear_notas(nomes, notas):\n"
            "    return {nome: nota for nome, nota in zip(nomes, notas)}\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(sorted(mapear_notas({a!r}, {b!r}).items()))"} for a, b in casos],
        testes_visiveis=1,
        dicas=[
            "`zip(nomes, notas)` gera pares `(nome, nota)` automaticamente.",
            "Você pode usar `dict(zip(nomes, notas))` ou uma dict comprehension.",
        ],
        explicacao=(
            "`zip()` emparelha sequências sem precisar controlar índices manualmente com `range(len(...))`."
        ),
    )


@exercicio(estagio=15, dificuldade=3, tipo="funcao", conceitos=["ordenacao", "tuplas", "funcoes", "return"])
def ranking_com_desempate(r):
    p1 = r.randint(50, 90)
    p2 = r.randint(50, 90)
    jogadores = [
        {"nome": "Carlos", "pontos": p1},
        {"nome": "Ana", "pontos": p1},
        {"nome": "Bruno", "pontos": p2},
    ]
    casos = [
        jogadores,
        [{"nome": "Zoe", "pontos": 10}, {"nome": "Bia", "pontos": 10}, {"nome": "Caio", "pontos": 20}],
        [],
    ]
    return dict(
        titulo="Ranking com critério de desempate",
        enunciado=(
            "Escreva a função `ranquear(jogadores)` que recebe uma lista de dicionários "
            "`{\"nome\": str, \"pontos\": int}` e retorna a lista dos **nomes** ordenados:\n"
            "1. Do **maior** para o menor número de `pontos`;\n"
            "2. Em caso de empate, por ordem **alfabética** crescente de `nome`.\n\n"
            "- Não modifique a lista recebida."
        ),
        solucao=(
            "def ranquear(jogadores):\n"
            "    ordenados = sorted(jogadores, key=lambda j: (-j['pontos'], j['nome']))\n"
            "    return [j['nome'] for j in ordenados]\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(ranquear({c!r}))"} for c in casos],
        testes_visiveis=1,
        dicas=[
            "Use `sorted(..., key=lambda j: ...)` para criar uma nova lista sem mutar a original.",
            "Retorne uma tupla `(-j['pontos'], j['nome'])`: o sinal negativo ordena pontos do maior para o menor e o nome desempata em A-Z.",
        ],
        explicacao=(
            "Em Python, tuplas são comparadas elemento a elemento. Usar `-j['pontos']` combinado com `j['nome']` "
            "resolve ordenação mista (decrescente + crescente) com elegância."
        ),
    )


@exercicio(estagio=15, dificuldade=2, tipo="completar", conceitos=["comprehensions", "dicionarios", "funcoes"])
def completar_inverter_dicionario(r):
    d1 = {"a": r.randint(1, 5), "b": r.randint(6, 10), "c": r.randint(11, 15)}
    casos = [d1, {"x": 10, "y": 20}, {}]
    return dict(
        titulo="Inverter chaves e valores",
        enunciado=(
            "Complete as lacunas `___` para inverter um dicionário de valores únicos (`chave -> valor` vira `valor -> chave`).\n\n"
            f"Exemplo: `{d1!r}`"
        ),
        codigo_inicial=(
            "def inverter(d):\n"
            "    return {___: ___ for k, v in d.___()}\n"
        ),
        solucao=(
            "def inverter(d):\n"
            "    return {v: k for k, v in d.items()}\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(sorted(inverter({c!r}).items()))"} for c in casos],
        testes_visiveis=1,
        dicas=[
            "Para percorrer chaves e valores juntos, use `d.items()`.",
            "Na dict comprehension invertida, `v` vira a nova chave e `k` o novo valor: `{v: k ...}`.",
        ],
        explicacao=(
            "`d.items()` devolve tuplas `(k, v)` que são desempacotadas na comprehension para construir o mapa inverso."
        ),
    )


@exercicio(estagio=15, dificuldade=3, tipo="prever", conceitos=["ordenacao", "tuplas", "teste_de_mesa"])
def prever_sorted_vs_sort(r):
    nums = r.sample(range(1, 20), 4)
    return dict(
        titulo="Teste de mesa: sorted() vs .sort()",
        enunciado="Faça o teste de mesa e escreva exatamente a saída do programa abaixo:",
        solucao=(
            f"a = {nums!r}\n"
            "b = sorted(a)\n"
            "c = a.sort(reverse=True)\n"
            "print(b[0])\n"
            "print(a[0])\n"
            "print(c)\n"
        ),
        dicas=[
            "`sorted(a)` cria uma nova lista crescente (`b[0]` é o menor valor).",
            "`a.sort(reverse=True)` altera `a` no lugar (colocando o maior em `a[0]`) e retorna `None`!",
        ],
        explicacao=(
            "Pegadinha clássica de entrevista: `.sort()` muta a lista original e devolve `None`, enquanto `sorted()` devolve uma nova lista."
        ),
    )


@exercicio(estagio=15, dificuldade=3, tipo="corrigir", conceitos=["ordenacao", "depuracao", "funcoes"])
def corrigir_ordenar_palavras_tamanho(r):
    palavras = r.sample(["sol", "python", "ia", "dados", "codigo", "api", "bot"], 5)
    casos = [palavras, ["cc", "aa", "b", "ddd"], []]
    return dict(
        titulo="Bug ao ordenar por tamanho e ordem alfabética",
        enunciado=(
            "A função `ordenar_palavras(lista)` deve retornar uma nova lista ordenada primeiro pelo **comprimento** "
            "(menor para maior) e, em empate, em **ordem alfabética**.\n\n"
            "O código abaixo tem dois problemas: retorna `None` e ignora o desempate alfabético. Corrija-o!"
        ),
        codigo_inicial=(
            "def ordenar_palavras(lista):\n"
            "    return lista.sort(key=len)\n"
        ),
        solucao=(
            "def ordenar_palavras(lista):\n"
            "    return sorted(lista, key=lambda p: (len(p), p))\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(ordenar_palavras({c!r}))"} for c in casos],
        testes_visiveis=1,
        dicas=[
            "`lista.sort()` devolve `None`; troque por `sorted(lista, ...)`.",
            "Para desempatar alfabeticamente, use `key=lambda p: (len(p), p)`.",
        ],
        explicacao=(
            "`sorted()` devolve a nova lista ordenada e a tupla `(len(p), p)` garante desempate determinístico por ordem alfabética."
        ),
    )


@exercicio(estagio=15, dificuldade=4, tipo="funcao", conceitos=["comprehensions", "dicionarios", "ordenacao"])
def top_k_frequentes(r):
    base = ["ia", "ia", "ia", "python", "python", "dados", "api", "api", "bot"]
    r.shuffle(base)
    k = r.choice([2, 3])
    casos = [(base, k), (["b", "a", "b", "a", "c"], 2), ([], 3)]
    return dict(
        titulo="Top K itens mais frequentes",
        enunciado=(
            "Escreva a função `top_k(itens, k)` que retorna uma lista com os `k` itens mais frequentes em `itens`, "
            "ordenados da maior frequência para a menor (desempate por ordem alfabética crescente).\n\n"
            "- Se `itens` tiver menos de `k` elementos distintos, retorne todos os existentes."
        ),
        solucao=(
            "def top_k(itens, k):\n"
            "    cont = {}\n"
            "    for x in itens:\n"
            "        cont[x] = cont.get(x, 0) + 1\n"
            "    ordenados = sorted(cont.items(), key=lambda par: (-par[1], par[0]))\n"
            "    return [chave for chave, _ in ordenados[:k]]\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(top_k({it!r}, {kv}))"} for it, kv in casos],
        testes_visiveis=1,
        dicas=[
            "Primeiro conte a frequência de cada item com um dicionário.",
            "Ordene `cont.items()` com `key=lambda par: (-par[1], par[0])` e pegue os `[:k]` primeiros.",
        ],
        explicacao=(
            "Combinar contagem com dicionário + `sorted` com tupla de desempate resolve um dos problemas mais cobrados em entrevistas."
        ),
    )


@exercicio(estagio=15, dificuldade=4, tipo="quebrar", conceitos=["ordenacao", "depuracao", "tuplas"])
def quebrar_segundo_maior(r):
    v = r.randint(5, 20)
    return dict(
        titulo="Quebre o código: segundo maior valor distinto",
        enunciado=(
            "A função `segundo_maior(nums)` deveria retornar o **segundo maior número distinto** da lista "
            "(para listas com pelo menos 2 valores distintos).\n\n"
            "**Seu desafio:** digite uma lista válida (com pelo menos 2 valores distintos) que faça o código abaixo "
            "retornar o valor errado!"
        ),
        modo_quebrar="args",
        funcao_quebrar="segundo_maior",
        placeholder_quebrar="Ex.: [5, 5, 2]",
        codigo_inicial=(
            "def segundo_maior(nums):\n"
            "    ordenada = sorted(nums)\n"
            "    return ordenada[-2]\n"
        ),
        solucao=(
            "def segundo_maior(nums):\n"
            "    unicos = sorted(set(nums))\n"
            "    return unicos[-2]\n"
        ),
        testes=[{"entrada": f"[{v}, {v}, {v - 3}]"}],
        testes_visiveis=0,
        dicas=[
            "O código ordena a lista e devolve `ordenada[-2]` sem remover números repetidos!",
            "O que acontece se o maior valor aparecer duas vezes na lista?",
        ],
        explicacao=(
            f"Quando o maior número se repete (ex.: `[{v}, {v}, {v - 3}]`), `ordenada[-2]` retorna o próprio maior (`{v}`) "
            f"em vez de `{v - 3}`. Usar `set(nums)` elimina a duplicata antes de ordenar."
        ),
    )
