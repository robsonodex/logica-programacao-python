"""Estágio 18 - Complexidade (Big-O), Benchmark Empírico e Otimização de Algoritmos."""

from .base import exercicio


@exercicio(estagio=18, dificuldade=2, tipo="funcao", conceitos=["complexidade", "sets", "funcoes"])
def otimizar_intersecao_grande(r):
    a1 = r.sample(range(1, 30), 6)
    b1 = r.sample(range(1, 30), 6)
    casos = [(a1, b1), ([1, 2, 3, 4], [3, 4, 5, 6]), ([], [1, 2]), ([1, 1, 2], [2, 2, 3])]
    return dict(
        titulo="Desafio Big-O: contar comuns em O(n)",
        enunciado=(
            "Escreva `contar_comuns(a, b)` que retorna quantos valores **distintos** aparecem tanto em `a` quanto em `b`.\n\n"
            "**Meta de entrevista:** resolva em **`O(n + m)`** (o Raio-X vai medir quantos passos seu código dá em listas de tamanho 20, 80 e 200!)."
        ),
        solucao=(
            "def contar_comuns(a, b):\n"
            "    return len(set(a) & set(b))\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(contar_comuns({x!r}, {y!r}))"} for x, y in casos],
        benchmark={
            "esperado": "O(n)",
            "chamadas": [
                (20, "contar_comuns(list(range(20)), list(range(10, 30)))"),
                (80, "contar_comuns(list(range(80)), list(range(40, 120)))"),
                (200, "contar_comuns(list(range(200)), list(range(100, 300)))"),
            ],
        },
        testes_visiveis=2,
        dicas=[
            "Fazer `if x in b` dentro de `for x in a` vira `O(n²)` quando `b` é uma lista.",
            "Converta para `set` antes de comparar: `len(set(a) & set(b))`.",
        ],
        explicacao=(
            "Usar conjuntos transforma uma busca quadrática em tempo linear `O(n + m)`, aprovado pelo medidor de Big-O."
        ),
    )


@exercicio(estagio=18, dificuldade=3, tipo="funcao", conceitos=["complexidade", "dicionarios", "funcoes"])
def numero_que_falta_linear(r):
    n = r.randint(5, 12)
    faltando = r.randint(0, n)
    arr = [i for i in range(n + 1) if i != faltando]
    r.shuffle(arr)
    casos = [arr, [0, 1, 3], [1, 2, 3], [0]]
    return dict(
        titulo="Número faltante em O(n) e O(1) de memória",
        enunciado=(
            "A lista `nums` contém `n` números distintos tirados de `0, 1, 2, ..., n` — ou seja, falta exatamente **1** número.\n\n"
            "Escreva `numero_faltante(nums)` que retorna o número ausente em **`O(n)`**.\n"
            f"Exemplo: `numero_faltante({arr!r})` -> `{faltando}`"
        ),
        solucao=(
            "def numero_faltante(nums):\n"
            "    n = len(nums)\n"
            "    soma_esperada = n * (n + 1) // 2\n"
            "    return soma_esperada - sum(nums)\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(numero_faltante({c!r}))"} for c in casos],
        benchmark={
            "esperado": "O(n)",
            "chamadas": [
                (20, "numero_faltante(list(range(20)))"),
                (80, "numero_faltante(list(range(80)))"),
                (200, "numero_faltante(list(range(200)))"),
            ],
        },
        testes_visiveis=2,
        dicas=[
            "A soma de `0` até `n` tem fórmula fechada: `n * (n + 1) // 2`.",
            "Subtraia `sum(nums)` da soma esperada — sem ordenar e sem laço aninhado!",
        ],
        explicacao=(
            "Comparar a soma teórica da progressão aritmética com `sum(nums)` acha o faltante em `O(n)` de tempo e `O(1)` de espaço extra."
        ),
    )


@exercicio(estagio=18, dificuldade=3, tipo="funcao", conceitos=["complexidade", "listas", "funcoes"])
def somas_de_intervalo_prefixo(r):
    nums = [r.randint(1, 10) for _ in range(6)]
    consultas = [(0, 2), (1, 4), (2, 5)]
    casos = [(nums, consultas), ([5, 10, 15], [(0, 0), (0, 2)]), ([1, 2, 3, 4], [(1, 2)])]
    return dict(
        titulo="Soma de Prefixos (Prefix Sum) para múltiplas consultas",
        enunciado=(
            "Escreva `somar_intervalos(nums, consultas)` onde `consultas` é uma lista de tuplas `(inicio, fim)` (inclusive). "
            "Retorne uma lista com a soma `nums[inicio] + ... + nums[fim]` para cada consulta.\n\n"
            "**Meta Big-O:** construa um vetor de **somas acumuladas (prefix sum)** para responder cada consulta em **`O(1)`**!"
        ),
        solucao=(
            "def somar_intervalos(nums, consultas):\n"
            "    pref = [0]\n"
            "    for x in nums:\n"
            "        pref.append(pref[-1] + x)\n"
            "    return [pref[fim + 1] - pref[ini] for ini, fim in consultas]\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(somar_intervalos({n!r}, {q!r}))"} for n, q in casos],
        benchmark={
            "esperado": "O(n)",
            "chamadas": [
                (20, "somar_intervalos(list(range(20)), [(0, 19)] * 20)"),
                (80, "somar_intervalos(list(range(80)), [(0, 79)] * 80)"),
                (200, "somar_intervalos(list(range(200)), [(0, 199)] * 200)"),
            ],
        },
        testes_visiveis=1,
        dicas=[
            "Crie `pref = [0]` onde `pref[k]` guarda a soma dos primeiros `k` elementos.",
            "A soma de `ini` até `fim` (inclusive) é simplesmente `pref[fim + 1] - pref[ini]`!",
        ],
        explicacao=(
            "Sem prefix sum, `M` consultas sobre `N` itens custam `O(N * M)`. Com prefix sum, cai para `O(N + M)`."
        ),
    )


@exercicio(estagio=18, dificuldade=4, tipo="funcao", conceitos=["complexidade", "sets", "funcoes"])
def remover_duplicatas_preservando_ordem(r):
    base = [r.randint(1, 6) for _ in range(9)]
    casos = [base, ["a", "b", "a", "c", "b"], [], [7, 7, 7]]
    return dict(
        titulo="Deduplicar mantendo a ordem em O(n)",
        enunciado=(
            "Escreva `unicos_em_ordem(itens)` que remove duplicatas **preservando a ordem da primeira aparição** "
            "em tempo **`O(n)`** (não use `if x not in res:` com lista!).\n\n"
            f"Exemplo: `unicos_em_ordem({base!r})`"
        ),
        solucao=(
            "def unicos_em_ordem(itens):\n"
            "    vistos = set()\n"
            "    res = []\n"
            "    for x in itens:\n"
            "        if x not in vistos:\n"
            "            vistos.add(x)\n"
            "            res.append(x)\n"
            "    return res\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(unicos_em_ordem({c!r}))"} for c in casos],
        benchmark={
            "esperado": "O(n)",
            "chamadas": [
                (20, "unicos_em_ordem(list(range(20)) * 2)"),
                (80, "unicos_em_ordem(list(range(80)) * 2)"),
                (200, "unicos_em_ordem(list(range(200)) * 2)"),
            ],
        },
        testes_visiveis=1,
        dicas=[
            "Fazer `if x not in res:` onde `res` é lista vira `O(n²)`!",
            "Mantenha um conjunto auxiliar `vistos = set()` para checar pertinência em `O(1)` (ou use `list(dict.fromkeys(itens))`).",
        ],
        explicacao=(
            "Combinar `set` (busca `O(1)`) + `list` (ordem preservada) mantém a ordem original com complexidade linear."
        ),
    )


@exercicio(estagio=18, dificuldade=4, tipo="funcao", conceitos=["complexidade", "sets", "funcoes"])
def maior_sequencia_consecutiva(r):
    ini = r.randint(10, 40)
    seq = [ini, ini + 1, ini + 2, ini + 3, 1, 99, 2]
    r.shuffle(seq)
    casos = [seq, [100, 4, 200, 1, 3, 2], [], [5, 5, 5]]
    return dict(
        titulo="Entrevista Avançada: maior sequência consecutiva em O(n)",
        enunciado=(
            "Escreva `maior_consecutiva(nums)` que retorna o comprimento da maior sequência de inteiros "
            "consecutivos presentes em `nums` (em qualquer ordem na lista).\n\n"
            "- Exemplo: `[100, 4, 200, 1, 3, 2]` -> `4` (sequência `1, 2, 3, 4`).\n"
            "- Meta: **`O(n)`** usando `set` (sem ordenar!)."
        ),
        solucao=(
            "def maior_consecutiva(nums):\n"
            "    conj = set(nums)\n"
            "    melhor = 0\n"
            "    for x in conj:\n"
            "        if x - 1 not in conj:\n"
            "            atual = x\n"
            "            tam = 1\n"
            "            while atual + 1 in conj:\n"
            "                atual += 1\n"
            "                tam += 1\n"
            "            if tam > melhor:\n"
            "                melhor = tam\n"
            "    return melhor\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(maior_consecutiva({c!r}))"} for c in casos],
        benchmark={
            "esperado": "O(n)",
            "chamadas": [
                (20, "maior_consecutiva(list(range(0, 40, 2)) + list(range(5)))"),
                (80, "maior_consecutiva(list(range(0, 160, 2)) + list(range(10)))"),
                (200, "maior_consecutiva(list(range(0, 400, 2)) + list(range(20)))"),
            ],
        },
        testes_visiveis=2,
        dicas=[
            "Coloque tudo em `conj = set(nums)`.",
            "Só comece a contar para frente quando `x - 1 not in conj` (ou seja, `x` é o INÍCIO de uma sequência) — assim cada número é visitado no máximo 2 vezes!",
        ],
        explicacao=(
            "Ignorar elementos que têm antecessor `x - 1` no conjunto garante que o `while` interno só rode a partir do começo de cada bloco, mantendo `O(n)` total."
        ),
    )


@exercicio(estagio=18, dificuldade=3, tipo="corrigir", conceitos=["complexidade", "dicionarios", "depuracao"])
def corrigir_pares_soma_repetida(r):
    metade = r.randint(4, 15)
    alvo = metade * 2
    casos = [([metade, 1, alvo - 1], alvo), ([metade, metade, 2], alvo), ([metade, 1, 2], alvo), ([metade], alvo)]
    return dict(
        titulo="Bug ao contar pares que somam alvo",
        enunciado=(
            "A função `existe_par(nums, alvo)` deve retornar `True` se existirem **dois elementos em posições distintas** "
            "cuja soma seja `alvo`.\n\n"
            "O código abaixo usa `set`, mas tem um bug clássico quando `alvo / 2` aparece só uma vez na lista. Corrija-o!"
        ),
        codigo_inicial=(
            "def existe_par(nums, alvo):\n"
            "    conj = set(nums)\n"
            "    for x in nums:\n"
            "        if (alvo - x) in conj:\n"
            "            return True\n"
            "    return False\n"
        ),
        solucao=(
            "def existe_par(nums, alvo):\n"
            "    vistos = set()\n"
            "    for x in nums:\n"
            "        if (alvo - x) in vistos:\n"
            "            return True\n"
            "        vistos.add(x)\n"
            "    return False\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(existe_par({n!r}, {a}))"} for n, a in casos],
        testes_visiveis=2,
        dicas=[
            "Se `nums = [6]` e `alvo = 12`, `alvo - 6 == 6` está em `set(nums)` — mas é o MESMO elemento!",
            "Construa `vistos = set()` aos poucos: verifique `(alvo - x) in vistos` ANTES de fazer `vistos.add(x)`.",
        ],
        explicacao=(
            "Adicionar `x` em `vistos` somente após testar `alvo - x` impede que um número forme par consigo mesmo."
        ),
    )


@exercicio(estagio=18, dificuldade=4, tipo="prever", conceitos=["complexidade", "teste_de_mesa"])
def prever_operacoes_laco(r):
    n = r.choice([4, 5, 6])
    return dict(
        titulo="Teste de mesa: quantas comparações faz O(n²)?",
        enunciado="Conte quantas vezes `passos` será incrementado e escreva a saída exata:",
        solucao=(
            f"n = {n}\n"
            "passos = 0\n"
            "for i in range(n):\n"
            "    for j in range(i + 1, n):\n"
            "        passos += 1\n"
            "print(passos)\n"
        ),
        dicas=[
            "Para cada `i`, `j` percorre apenas os índices maiores que `i` (pares únicos sem repetir).",
            "A quantidade total de pares em `n` itens é `n * (n - 1) // 2`.",
        ],
        explicacao=(
            f"O laço triangular executa `n * (n - 1) // 2 = {n * (n - 1) // 2}` vezes — ainda assim quadrático `O(n²)` quando `n` cresce."
        ),
    )


@exercicio(estagio=18, dificuldade=5, tipo="quebrar", conceitos=["complexidade", "depuracao"])
def quebrar_subarray_maximo_kadane(r):
    a = -r.randint(2, 6)
    b = -r.randint(7, 15)
    return dict(
        titulo="Quebre o código: maior soma contígua (Kadane)",
        enunciado=(
            "A função `maior_subarray(nums)` deveria retornar a maior soma de uma sublista **não vazia** contígua "
            "de `nums` (Algoritmo de Kadane em `O(n)`).\n\n"
            "**Seu desafio:** forneça uma lista não vazia que faça o código abaixo retornar o valor errado!"
        ),
        modo_quebrar="args",
        funcao_quebrar="maior_subarray",
        placeholder_quebrar="Ex.: [-3, -1, -5]",
        codigo_inicial=(
            "def maior_subarray(nums):\n"
            "    atual = 0\n"
            "    melhor = 0\n"
            "    for x in nums:\n"
            "        atual = max(0, atual + x)\n"
            "        melhor = max(melhor, atual)\n"
            "    return melhor\n"
        ),
        solucao=(
            "def maior_subarray(nums):\n"
            "    atual = melhor = nums[0]\n"
            "    for x in nums[1:]:\n"
            "        atual = max(x, atual + x)\n"
            "        melhor = max(melhor, atual)\n"
            "    return melhor\n"
        ),
        testes=[{"entrada": f"[{a}, {b}]"}],
        testes_visiveis=0,
        dicas=[
            "Repare em `melhor = 0` e `max(0, ...)` — isso assume que escolher 0 elementos (sublista vazia) seria permitido.",
            "O que acontece se a lista só tiver números negativos?",
        ],
        explicacao=(
            f"Com `[{a}, {b}]`, a maior sublista não vazia tem soma `{max(a, b)}`, mas o código bugado retorna `0`. "
            "Inicializar `atual = melhor = nums[0]` resolve para qualquer lista não vazia."
        ),
    )
