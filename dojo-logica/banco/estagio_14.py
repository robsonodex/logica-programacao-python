"""Estágio 14 - Dicionários e Sets (Hash Maps, frequência, agrupamento e O(1))."""

from .base import exercicio


@exercicio(estagio=14, dificuldade=1, tipo="funcao", conceitos=["dicionarios", "funcoes", "return"])
def contar_frequencia(r):
    palavras_pool = ["python", "logica", "dados", "ia", "fluxo", "codigo", "api", "agente"]
    amostra1 = [r.choice(palavras_pool[:5]) for _ in range(r.randint(5, 8))]
    amostra2 = [r.choice(palavras_pool[3:]) for _ in range(r.randint(4, 7))]
    casos = [amostra1, amostra2, [], [palavras_pool[0]] * 3]
    esp0 = {}
    for w in amostra1:
        esp0[w] = esp0.get(w, 0) + 1
    return dict(
        titulo="Contador de frequência com dicionário",
        enunciado=(
            "Escreva a função `contar_palavras(lista)` que recebe uma lista de strings e retorna um "
            "**dicionário** mapeando cada palavra à quantidade de vezes que ela aparece.\n\n"
            f"Exemplo: `contar_palavras({amostra1!r})` -> `{esp0!r}`"
        ),
        solucao=(
            "def contar_palavras(lista):\n"
            "    cont = {}\n"
            "    for item in lista:\n"
            "        cont[item] = cont.get(item, 0) + 1\n"
            "    return cont\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(sorted(contar_palavras({c!r}).items()))"} for c in casos],
        testes_visiveis=2,
        dicas=[
            "Comece com um dicionário vazio `cont = {}`.",
            "Para cada item da lista, atualize com `cont[item] = cont.get(item, 0) + 1`.",
        ],
        explicacao=(
            "O método `.get(chave, 0)` evita `KeyError` na primeira ocorrência de cada palavra, "
            "permitindo contar todas as frequências em uma única passada `O(n)`."
        ),
    )


@exercicio(estagio=14, dificuldade=2, tipo="funcao", conceitos=["sets", "funcoes", "return"])
def elementos_em_comum(r):
    a1 = [r.randint(1, 12) for _ in range(6)]
    b1 = [r.randint(1, 12) for _ in range(6)]
    casos = [(a1, b1), ([1, 2, 2, 3], [2, 3, 4]), ([1, 2], [3, 4]), ([], [1, 2])]
    com0 = sorted(set(a1) & set(b1))
    return dict(
        titulo="Interseção ordenada com Set",
        enunciado=(
            "Escreva a função `em_comum(a, b)` que recebe duas listas de inteiros e retorna uma **lista ordenada** "
            "sem repetições contendo apenas os elementos presentes nas duas listas.\n\n"
            f"Exemplo: `em_comum({a1!r}, {b1!r})` -> `{com0!r}`"
        ),
        solucao=(
            "def em_comum(a, b):\n"
            "    return sorted(set(a) & set(b))\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(em_comum({a!r}, {b!r}))"} for a, b in casos],
        testes_visiveis=2,
        dicas=[
            "Converta as duas listas em `set` para eliminar duplicatas e ganhar busca `O(1)`.",
            "A interseção de conjuntos em Python é `set(a) & set(b)`, depois ordene com `sorted(...)`.",
        ],
        explicacao=(
            "Usar `set(a) & set(b)` calcula a interseção em tempo linear `O(n + m)`, evitando o custo `O(n * m)` "
            "de checar `if x in b` dentro de um `for`."
        ),
    )


@exercicio(estagio=14, dificuldade=2, tipo="completar", conceitos=["dicionarios", "funcoes", "return"])
def completar_agrupar_por_inicial(r):
    nomes1 = r.sample(["Ana", "Alice", "Bruno", "Bia", "Carla", "Caio", "Diego"], 5)
    nomes2 = r.sample(["Eva", "Edu", "Fabi", "Gabi", "Gil"], 4)
    casos = [nomes1, nomes2, []]
    return dict(
        titulo="Agrupar nomes pela letra inicial",
        enunciado=(
            "Complete as lacunas `___` para agrupar uma lista de nomes num dicionário onde a chave é a "
            "primeira letra em maiúscula e o valor é a lista de nomes que começam com ela.\n\n"
            f"Exemplo de entrada: `{nomes1!r}`"
        ),
        codigo_inicial=(
            "def agrupar_inicial(nomes):\n"
            "    grupos = ___\n"
            "    for nome in nomes:\n"
            "        if not nome:\n"
            "            continue\n"
            "        letra = nome[___].upper()\n"
            "        grupos.___(letra, []).append(nome)\n"
            "    return grupos\n"
        ),
        solucao=(
            "def agrupar_inicial(nomes):\n"
            "    grupos = {}\n"
            "    for nome in nomes:\n"
            "        if not nome:\n"
            "            continue\n"
            "        letra = nome[0].upper()\n"
            "        grupos.setdefault(letra, []).append(nome)\n"
            "    return grupos\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(sorted(agrupar_inicial({c!r}).items()))"} for c in casos],
        testes_visiveis=1,
        dicas=[
            "Um dicionário vazio se cria com `{}` e o primeiro caractere está no índice `0`.",
            "O método `.setdefault(chave, [])` cria a lista se a chave não existir e devolve a lista para dar `.append()`.",
        ],
        explicacao=(
            "`setdefault(letra, [])` evita escrever `if letra not in grupos: grupos[letra] = []` antes de cada `append`, "
            "padrão muito usado para agrupar registros."
        ),
    )


@exercicio(estagio=14, dificuldade=3, tipo="funcao", conceitos=["dicionarios", "complexidade", "funcoes", "return"])
def two_sum_indices(r):
    base = r.sample(range(1, 25), 5)
    i1, i2 = sorted(r.sample(range(5), 2))
    alvo1 = base[i1] + base[i2]
    casos = [
        (base, alvo1),
        ([3, 3], 6),
        ([1, 4, 7, 10], 11),
        ([2, 5, 9], 99),
    ]
    return dict(
        titulo="Clássico de Entrevista: Two Sum",
        enunciado=(
            "Escreva a função `two_sum(nums, alvo)` que recebe uma lista de inteiros e um `alvo`, e retorna "
            "uma lista `[i, j]` (`i < j`) com os **índices** de dois números cuja soma seja igual a `alvo`.\n\n"
            "- Se não existir nenhum par, retorne `[]`.\n"
            "- Tente resolver em `O(n)` usando um dicionário para lembrar os números já vistos.\n\n"
            f"Exemplo: `two_sum({base!r}, {alvo1})` -> `[{i1}, {i2}]` (ou outro par válido)"
        ),
        solucao=(
            "def two_sum(nums, alvo):\n"
            "    vistos = {}\n"
            "    for i, x in enumerate(nums):\n"
            "        falta = alvo - x\n"
            "        if falta in vistos:\n"
            "            return [vistos[falta], i]\n"
            "        vistos[x] = i\n"
            "    return []\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(two_sum({n!r}, {a}))"} for n, a in casos],
        testes_visiveis=2,
        dicas=[
            "Para cada número `x` no índice `i`, calcule `falta = alvo - x`.",
            "Se `falta` já está no dicionário `vistos`, devolva `[vistos[falta], i]`; caso contrário, guarde `vistos[x] = i`.",
        ],
        explicacao=(
            "O dicionário `vistos` guarda `valor -> índice`. Consultar `falta in vistos` custa `O(1)`, "
            "resolvendo o clássico Two Sum em uma única passada `O(n)`."
        ),
    )


@exercicio(estagio=14, dificuldade=3, tipo="funcao", conceitos=["dicionarios", "strings", "funcoes", "return"])
def eh_anagrama(r):
    pares_sim = [("amor", "roma"), ("pedra", "padre"), ("listen", "silent"), ("gato", "toga")]
    pares_nao = [("casa", "caso"), ("aab", "abb"), ("python", "typhoon"), ("a", "aa")]
    p1 = r.choice(pares_sim)
    p2 = r.choice(pares_nao)
    casos = [p1, p2, ("Roma", "amor"), ("", "")]
    return dict(
        titulo="Verificador de anagramas",
        enunciado=(
            "Escreva a função `sao_anagramas(a, b)` que retorna `True` se `a` e `b` forem anagramas "
            "(mesmas letras com as mesmas quantidades, ignorando maiúsculas/minúsculas e espaços), "
            "ou `False` caso contrário.\n\n"
            f"Exemplo: `sao_anagramas({p1[0]!r}, {p1[1]!r})` -> `True`"
        ),
        solucao=(
            "def sao_anagramas(a, b):\n"
            "    a = a.replace(' ', '').lower()\n"
            "    b = b.replace(' ', '').lower()\n"
            "    if len(a) != len(b):\n"
            "        return False\n"
            "    cont = {}\n"
            "    for ch in a:\n"
            "        cont[ch] = cont.get(ch, 0) + 1\n"
            "    for ch in b:\n"
            "        if cont.get(ch, 0) == 0:\n"
            "            return False\n"
            "        cont[ch] -= 1\n"
            "    return True\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(sao_anagramas({x!r}, {y!r}))"} for x, y in casos],
        testes_visiveis=2,
        dicas=[
            "Normalize primeiro removendo espaços e aplicando `.lower()`.",
            "Se os tamanhos forem diferentes, já retorne `False`; depois compare a frequência de cada caractere com um dicionário.",
        ],
        explicacao=(
            "Contar letras com dicionário resolve anagramas em tempo `O(n)` sem precisar ordenar as strings (`O(n log n)`)."
        ),
    )


@exercicio(estagio=14, dificuldade=3, tipo="prever", conceitos=["dicionarios", "sets", "teste_de_mesa"])
def prever_dict_get_e_set(r):
    a = r.randint(1, 5)
    b = a + r.randint(1, 4)
    return dict(
        titulo="Teste de mesa: dicionário e conjunto",
        enunciado=(
            "Acompanhe cuidadosamente o dicionário e o conjunto e escreva exatamente a saída do código:"
        ),
        solucao=(
            f"itens = [{a}, {b}, {a}, {b}, {a}]\n"
            "cont = {}\n"
            "for x in itens:\n"
            "    cont[x] = cont.get(x, 0) + 1\n"
            f"print(cont.get({a}, 0), cont.get(99, -1))\n"
            "print(len(set(itens)))\n"
        ),
        dicas=[
            f"O valor `{a}` aparece 3 vezes e `{b}` aparece 2 vezes.",
            "`cont.get(99, -1)` retorna `-1` porque a chave `99` não existe, e `set(itens)` mantém só os distintos.",
        ],
        explicacao=(
            f"`cont[{a}]` vale 3, `cont.get(99, -1)` devolve o padrão `-1` sem erro, e `set(itens)` tem 2 valores distintos."
        ),
    )


@exercicio(estagio=14, dificuldade=4, tipo="corrigir", conceitos=["dicionarios", "depuracao", "funcoes"])
def corrigir_primeiro_caractere_unico(r):
    palavras = r.sample(["abacaxi", "arara", "banana", "python", "aabb", "codigo"], 4)
    casos = palavras + ["aabbcc", "x"]
    return dict(
        titulo="Bug no primeiro caractere que não repete",
        enunciado=(
            "A função `primeiro_unico(texto)` deveria retornar o **primeiro caractere** que aparece apenas 1 vez "
            "em `texto` (ou `\"\"` se todos repetirem).\n\n"
            "O código abaixo tem um bug lógico: ele testa `cont[ch] == 1` durante a própria contagem ou usa chave errada. Corrija-o!"
        ),
        codigo_inicial=(
            "def primeiro_unico(texto):\n"
            "    cont = {}\n"
            "    for ch in texto:\n"
            "        cont[ch] = cont.get(ch, 0) + 1\n"
            "        if cont[ch] == 1:\n"
            "            return ch\n"
            "    return ''\n"
        ),
        solucao=(
            "def primeiro_unico(texto):\n"
            "    cont = {}\n"
            "    for ch in texto:\n"
            "        cont[ch] = cont.get(ch, 0) + 1\n"
            "    for ch in texto:\n"
            "        if cont[ch] == 1:\n"
            "            return ch\n"
            "    return ''\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(repr(primeiro_unico({p!r})))"} for p in casos],
        testes_visiveis=2,
        dicas=[
            "Na primeira aparição de QUALQUER letra, `cont[ch]` vale `1` — mesmo que ela vá repetir depois!",
            "Faça dois laços separados: primeiro conte todas as letras, depois percorra `texto` novamente buscando a primeira com `cont[ch] == 1`.",
        ],
        explicacao=(
            "Só dá para saber se um caractere é único depois de contar a string inteira. Separar em duas passadas mantém `O(n)` e garante a resposta certa."
        ),
    )


@exercicio(estagio=14, dificuldade=4, tipo="quebrar", conceitos=["dicionarios", "sets", "depuracao"])
def quebrar_duplicata_falsa(r):
    alvo = r.randint(2, 9)
    return dict(
        titulo="Quebre o código: detector de duplicatas",
        enunciado=(
            "Um candidato escreveu `tem_duplicata(nums)` para retornar `True` se houver qualquer número repetido "
            "na lista `nums`, ou `False` se todos forem distintos.\n\n"
            "**Seu desafio (Caçador de Edge Cases):** encontre uma lista de inteiros que faça o código abaixo "
            "retornar a resposta **errada** (por exemplo: `[1, 2, 1]`)."
        ),
        modo_quebrar="args",
        funcao_quebrar="tem_duplicata",
        placeholder_quebrar="Ex.: [1, 2, 1]",
        codigo_inicial=(
            "def tem_duplicata(nums):\n"
            "    for i in range(len(nums) - 1):\n"
            "        if nums[i] == nums[i + 1]:\n"
            "            return True\n"
            "    return False\n"
        ),
        solucao=(
            "def tem_duplicata(nums):\n"
            "    return len(nums) != len(set(nums))\n"
        ),
        testes=[{"entrada": f"[{alvo}, {alvo + 1}, {alvo}]"}],
        testes_visiveis=0,
        dicas=[
            "Repare no que o código bugado compara: apenas `nums[i]` com o vizinho imediato `nums[i + 1]`!",
            "O que acontece se o número repetido não estiver lado a lado?",
        ],
        explicacao=(
            "O código bugado só detecta duplicatas **adjacentes**. Qualquer lista com elementos repetidos separados "
            f"(como `[{alvo}, {alvo + 1}, {alvo}]`) quebra a função; usar `set` resolve em `O(n)`."
        ),
    )
