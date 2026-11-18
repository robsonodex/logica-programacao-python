"""Estágio 17 - Padrões Clássicos de Entrevista (Dois Ponteiros, Janela Deslizante, Pilha, Busca Binária, Recursão)."""

from .base import exercicio


@exercicio(estagio=17, dificuldade=2, tipo="funcao", conceitos=["dois_ponteiros", "strings", "funcoes"])
def palindromo_dois_ponteiros(r):
    pal_sim = r.choice(["arara", "Anotaram a data da maratona", "Socorram me subi no onibus em Marrocos", "ovo"])
    pal_nao = r.choice(["python", "logica de programacao", "entrevista"])
    casos = [pal_sim, pal_nao, "a", "", "A man, a plan, a canal: Panama"]
    return dict(
        titulo="Palíndromo ignorando pontuação (Dois Ponteiros)",
        enunciado=(
            "Escreva `eh_palindromo(texto)` retornando `True` se `texto` for um palíndromo considerando "
            "**apenas letras e números** (`isalnum()`) e ignorando maiúsculas/minúsculas.\n\n"
            f"Exemplo: `eh_palindromo({pal_sim!r})` -> `True`"
        ),
        solucao=(
            "def eh_palindromo(texto):\n"
            "    esq, dir_ = 0, len(texto) - 1\n"
            "    while esq < dir_:\n"
            "        while esq < dir_ and not texto[esq].isalnum():\n"
            "            esq += 1\n"
            "        while esq < dir_ and not texto[dir_].isalnum():\n"
            "            dir_ -= 1\n"
            "        if texto[esq].lower() != texto[dir_].lower():\n"
            "            return False\n"
            "        esq += 1\n"
            "        dir_ -= 1\n"
            "    return True\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(eh_palindromo({c!r}))"} for c in casos],
        testes_visiveis=2,
        dicas=[
            "Use dois índices: `esq = 0` e `dir_ = len(texto) - 1`, avançando enquanto `esq < dir_`.",
            "Pule caracteres onde `not ch.isalnum()` e compare `texto[esq].lower()` com `texto[dir_].lower()`.",
        ],
        explicacao=(
            "O padrão Dois Ponteiros resolve em `O(n)` de tempo e `O(1)` de memória extra, sem precisar criar cópia invertida da string."
        ),
    )


@exercicio(estagio=17, dificuldade=3, tipo="funcao", conceitos=["janela_deslizante", "listas", "funcoes"])
def maior_soma_janela(r):
    nums = [r.randint(-5, 15) for _ in range(7)]
    k = r.choice([2, 3])
    casos = [(nums, k), ([2, 1, 5, 1, 3, 2], 3), ([-3, -1, -4, -2], 2), ([10], 2)]
    esp0 = max(sum(nums[i:i + k]) for i in range(len(nums) - k + 1))
    return dict(
        titulo="Janela Deslizante: maior soma de k elementos",
        enunciado=(
            "Escreva `maior_soma_k(nums, k)` que retorna a **maior soma possível** de `k` elementos "
            "**consecutivos** em `nums`.\n\n"
            "- Se `k <= 0` ou `len(nums) < k`, retorne `None`.\n"
            f"- Exemplo: `maior_soma_k({nums!r}, {k})` -> `{esp0}`"
        ),
        solucao=(
            "def maior_soma_k(nums, k):\n"
            "    if k <= 0 or len(nums) < k:\n"
            "        return None\n"
            "    soma = sum(nums[:k])\n"
            "    melhor = soma\n"
            "    for i in range(k, len(nums)):\n"
            "        soma += nums[i] - nums[i - k]\n"
            "        if soma > melhor:\n"
            "            melhor = soma\n"
            "    return melhor\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(maior_soma_k({n!r}, {kv}))"} for n, kv in casos],
        testes_visiveis=2,
        dicas=[
            "Calcule a primeira janela `soma = sum(nums[:k])` e inicialize `melhor = soma` (não `0`, pois pode haver negativos!).",
            "Para cada índice `i` de `k` até o fim, faça `soma += nums[i] - nums[i - k]`.",
        ],
        explicacao=(
            "Deslizar a janela somando quem entra e subtraindo quem sai resolve em `O(n)` independente do tamanho de `k`."
        ),
    )


@exercicio(estagio=17, dificuldade=3, tipo="funcao", conceitos=["pilha_fila", "dicionarios", "funcoes"])
def parenteses_balanceados(r):
    validos = ["()", "()[]{}", "{[()]}", "(([]){})"]
    invalidos = ["(]", "([)]", "(((", "}", "{[}"]
    casos = [r.choice(validos), r.choice(invalidos), "", "({[]})"]
    return dict(
        titulo="Clássico de Pilha: parênteses balanceados",
        enunciado=(
            "Escreva `balanceado(s)` que recebe uma string contendo apenas `()[]{}` e retorna `True` se "
            "todos os pares abrirem e fecharem na ordem correta, ou `False` caso contrário.\n\n"
            "Exemplo: `balanceado('{[()]}')` -> `True`, `balanceado('([)]')` -> `False`"
        ),
        solucao=(
            "def balanceado(s):\n"
            "    pares = {')': '(', ']': '[', '}': '{'}\n"
            "    pilha = []\n"
            "    for ch in s:\n"
            "        if ch in '([{':\n"
            "            pilha.append(ch)\n"
            "        elif ch in pares:\n"
            "            if not pilha or pilha.pop() != pares[ch]:\n"
            "                return False\n"
            "    return len(pilha) == 0\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(balanceado({c!r}))"} for c in casos],
        testes_visiveis=2,
        dicas=[
            "Use uma lista `pilha = []`: empilhe quando abrir (`(`, `[`, `{`).",
            "Ao fechar, cheque se a pilha não está vazia e se `pilha.pop()` corresponde ao fechamento. No fim, a pilha deve ficar vazia!",
        ],
        explicacao=(
            "O último símbolo aberto precisa ser o primeiro fechado (LIFO). Checar `len(pilha) == 0` no final captura aberturas sem fechamento."
        ),
    )


@exercicio(estagio=17, dificuldade=3, tipo="funcao", conceitos=["busca_binaria", "listas", "funcoes"])
def busca_binaria_indice(r):
    nums = sorted(r.sample(range(1, 60), 9))
    alvo_ok = r.choice(nums)
    alvo_nao = nums[-1] + 5
    casos = [(nums, alvo_ok), (nums, alvo_nao), ([nums[0]], nums[0]), ([], 5)]
    return dict(
        titulo="Busca Binária O(log n)",
        enunciado=(
            "Escreva `busca_binaria(nums, alvo)` que recebe uma lista **ordenada** de inteiros e retorna "
            "o **índice** de `alvo`, ou `-1` se não existir.\n\n"
            f"Exemplo: `busca_binaria({nums!r}, {alvo_ok})` -> `{nums.index(alvo_ok)}`"
        ),
        solucao=(
            "def busca_binaria(nums, alvo):\n"
            "    esq, dir_ = 0, len(nums) - 1\n"
            "    while esq <= dir_:\n"
            "        meio = (esq + dir_) // 2\n"
            "        if nums[meio] == alvo:\n"
            "            return meio\n"
            "        elif nums[meio] < alvo:\n"
            "            esq = meio + 1\n"
            "        else:\n"
            "            dir_ = meio - 1\n"
            "    return -1\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(busca_binaria({n!r}, {a}))"} for n, a in casos],
        testes_visiveis=2,
        dicas=[
            "Mantenha `esq = 0`, `dir_ = len(nums) - 1` e repita `while esq <= dir_:`.",
            "Atualize sempre com `esq = meio + 1` ou `dir_ = meio - 1` para nunca entrar em loop infinito.",
        ],
        explicacao=(
            "A cada iteração a busca binária corta o intervalo pela metade, encontrando o elemento em no máximo `log2(n)` passos."
        ),
    )


@exercicio(estagio=17, dificuldade=4, tipo="funcao", conceitos=["recursao", "listas", "funcoes"])
def achatar_lista_aninhada(r):
    a, b, c, d = r.sample(range(1, 20), 4)
    aninhada = [a, [b, [c]], d]
    casos = [aninhada, [[1, 2], [], [3, [4, [5]]]], [], [10]]
    return dict(
        titulo="Recursão: achatar lista aninhada (flatten)",
        enunciado=(
            "Escreva `achatar(itens)` que recebe uma lista que pode conter inteiros e outras listas aninhadas "
            "em qualquer profundidade e retorna uma única lista plana com todos os inteiros na ordem.\n\n"
            f"Exemplo: `achatar({aninhada!r})` -> `[{a}, {b}, {c}, {d}]`"
        ),
        solucao=(
            "def achatar(itens):\n"
            "    res = []\n"
            "    for x in itens:\n"
            "        if isinstance(x, list):\n"
            "            res.extend(achatar(x))\n"
            "        else:\n"
            "            res.append(x)\n"
            "    return res\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(achatar({c!r}))"} for c in casos],
        testes_visiveis=2,
        dicas=[
            "Percorra cada elemento `x`: se `isinstance(x, list)`, chame `achatar(x)` recursivamente e estenda `res`.",
            "Caso base: quando `x` não é lista, basta fazer `res.append(x)`.",
        ],
        explicacao=(
            "Recursão resolve naturalmente estruturas de profundidade desconhecida (listas aninhadas, árvores, JSONs complexos)."
        ),
    )


@exercicio(estagio=17, dificuldade=4, tipo="funcao", conceitos=["janela_deslizante", "sets", "strings"])
def maior_substring_sem_repetir(r):
    amostras = ["abcabcbb", "bbbbb", "pwwkew", "abcdef", "abba"]
    s1 = r.choice(amostras)
    casos = [s1, "pwwkew", "abba", "", "a"]
    return dict(
        titulo="Janela Variável: maior substring sem repetir caracteres",
        enunciado=(
            "Escreva `maior_sem_repetir(s)` que retorna o **comprimento** da maior substring contígua de `s` "
            "que não contém nenhum caractere repetido.\n\n"
            "Exemplo: `maior_sem_repetir('pwwkew')` -> `3` (`'wke'`)"
        ),
        solucao=(
            "def maior_sem_repetir(s):\n"
            "    vistos = set()\n"
            "    esq = 0\n"
            "    melhor = 0\n"
            "    for dir_, ch in enumerate(s):\n"
            "        while ch in vistos:\n"
            "            vistos.remove(s[esq])\n"
            "            esq += 1\n"
            "        vistos.add(ch)\n"
            "        if dir_ - esq + 1 > melhor:\n"
            "            melhor = dir_ - esq + 1\n"
            "    return melhor\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(maior_sem_repetir({c!r}))"} for c in casos],
        testes_visiveis=2,
        dicas=[
            "Mantenha um `set` com os caracteres dentro da janela atual `[esq..dir_]`.",
            "Enquanto `s[dir_]` já estiver no `set`, remova `s[esq]` e avance `esq += 1`.",
        ],
        explicacao=(
            "Cada ponteiro (`esq` e `dir_`) percorre a string no máximo uma vez, garantindo complexidade `O(n)` neste clássico de entrevistas."
        ),
    )


@exercicio(estagio=17, dificuldade=4, tipo="quebrar", conceitos=["busca_binaria", "depuracao"])
def quebrar_busca_binaria_um_elemento(r):
    v = r.randint(5, 50)
    return dict(
        titulo="Quebre o código: busca binária com bug de fronteira",
        enunciado=(
            "Um candidato escreveu `buscar(nums, alvo)` para retornar o índice de `alvo` numa lista ordenada "
            "(ou `-1` se não encontrar).\n\n"
            "**Seu desafio:** forneça `nums, alvo` (ex.: `[10], 10`) onde `nums` é uma lista ordenada e o código "
            "abaixo retorna o resultado **errado**!"
        ),
        modo_quebrar="args",
        funcao_quebrar="buscar",
        placeholder_quebrar="Ex.: [7], 7",
        codigo_inicial=(
            "def buscar(nums, alvo):\n"
            "    esq, dir_ = 0, len(nums) - 1\n"
            "    while esq < dir_:\n"
            "        meio = (esq + dir_) // 2\n"
            "        if nums[meio] == alvo:\n"
            "            return meio\n"
            "        elif nums[meio] < alvo:\n"
            "            esq = meio + 1\n"
            "        else:\n"
            "            dir_ = meio - 1\n"
            "    return -1\n"
        ),
        solucao=(
            "def buscar(nums, alvo):\n"
            "    esq, dir_ = 0, len(nums) - 1\n"
            "    while esq <= dir_:\n"
            "        meio = (esq + dir_) // 2\n"
            "        if nums[meio] == alvo:\n"
            "            return meio\n"
            "        elif nums[meio] < alvo:\n"
            "            esq = meio + 1\n"
            "        else:\n"
            "            dir_ = meio - 1\n"
            "    return -1\n"
        ),
        testes=[{"entrada": f"[{v}], {v}"}],
        testes_visiveis=0,
        dicas=[
            "Veja a condição do laço: `while esq < dir_:`.",
            "Quando sobra apenas 1 elemento no intervalo (`esq == dir_`), o laço nem entra!",
        ],
        explicacao=(
            f"Com `while esq < dir_:`, quando `nums = [{v}]` e `alvo = {v}` (ou quando o alvo está no último elemento restante), "
            "`esq == dir_` sai do laço e retorna `-1` erroneamente. O correto é `while esq <= dir_:`."
        ),
    )


@exercicio(estagio=17, dificuldade=5, tipo="funcao", conceitos=["dois_ponteiros", "listas", "funcoes"])
def mesclar_listas_ordenadas(r):
    a = sorted(r.sample(range(1, 30), 4))
    b = sorted(r.sample(range(1, 30), 4))
    casos = [(a, b), ([1, 3, 5], [2, 4, 6]), ([], [1, 2]), ([5, 10], [])]
    return dict(
        titulo="Mesclar duas listas ordenadas em O(n + m)",
        enunciado=(
            "Escreva `mesclar(a, b)` que recebe duas listas já ordenadas e retorna uma nova lista ordenada "
            "com todos os elementos de ambas **sem usar `sorted()`** (use Dois Ponteiros).\n\n"
            f"Exemplo: `mesclar({a!r}, {b!r})` -> `{sorted(a + b)!r}`"
        ),
        solucao=(
            "def mesclar(a, b):\n"
            "    i = j = 0\n"
            "    res = []\n"
            "    while i < len(a) and j < len(b):\n"
            "        if a[i] <= b[j]:\n"
            "            res.append(a[i])\n"
            "            i += 1\n"
            "        else:\n"
            "            res.append(b[j])\n"
            "            j += 1\n"
            "    res.extend(a[i:])\n"
            "    res.extend(b[j:])\n"
            "    return res\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(mesclar({x!r}, {y!r}))"} for x, y in casos],
        testes_visiveis=2,
        dicas=[
            "Mantenha `i = 0` em `a` e `j = 0` em `b`, sempre copiando o menor entre `a[i]` e `b[j]`.",
            "Quando uma das listas acabar, adicione o restante da outra com `res.extend(a[i:])` e `res.extend(b[j:])`.",
        ],
        explicacao=(
            "Essa é a etapa de combinação do Merge Sort: percorre cada lista apenas uma vez em `O(n + m)`."
        ),
    )
