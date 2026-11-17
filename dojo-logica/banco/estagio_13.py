"""Estágio 13 - Desafios de lógica integrando todo o nível básico."""

from .base import exercicio


@exercicio(estagio=13, dificuldade=2, tipo="codigo", conceitos=["for_range", "elif", "teste_de_mesa"])
def fizzbuzz_customizado(r):
    d1 = r.choice([2, 3, 4])
    d2 = r.choice([5, 7])
    p1 = r.choice(["Fizz", "Plim", "Zap"])
    p2 = r.choice(["Buzz", "Plom", "Bam"])
    casos = [r.randint(12, 18), r.randint(20, 25), d1 * d2]
    n0 = casos[0]
    ex_linhas = []
    for i in range(1, min(n0, 10) + 1):
        if i % d1 == 0 and i % d2 == 0:
            ex_linhas.append(p1 + p2)
        elif i % d1 == 0:
            ex_linhas.append(p1)
        elif i % d2 == 0:
            ex_linhas.append(p2)
        else:
            ex_linhas.append(str(i))
    return dict(
        titulo=f"Desafio {p1}{p2}",
        enunciado=(
            f"Leia um inteiro positivo `n` e imprima os números de `1` até `n` (um por linha), seguindo estas regras:\n"
            f"- Se for múltiplo de **{d1} e {d2}**, imprima `{p1 + p2}`\n"
            f"- Se for múltiplo apenas de **{d1}**, imprima `{p1}`\n"
            f"- Se for múltiplo apenas de **{d2}**, imprima `{p2}`\n"
            "- Caso contrário, imprima o próprio número.\n\n"
            f"Primeiras linhas para `n = {n0}`:\n```\n" + "\n".join(ex_linhas[:6]) + "\n...\n```"
        ),
        solucao=(
            'n = int(input("N: "))\n'
            "for i in range(1, n + 1):\n"
            f"    if i % {d1} == 0 and i % {d2} == 0:\n"
            f'        print("{p1 + p2}")\n'
            f"    elif i % {d1} == 0:\n"
            f'        print("{p1}")\n'
            f"    elif i % {d2} == 0:\n"
            f'        print("{p2}")\n'
            "    else:\n"
            "        print(i)\n"
        ),
        testes=[{"entrada": str(x)} for x in casos],
        testes_visiveis=1,
        dicas=[
            "A ordem do `if/elif` é crucial: teste primeiro se é múltiplo dos **dois** (`and`)!",
            "Se testar `d1` antes, um múltiplo de ambos nunca chegaria no bloco combinado.",
        ],
        explicacao=(
            "Colocar a condição mais restritiva (`d1 and d2`) no topo da cadeia `if/elif/else` evita que "
            "a primeira condição capture múltiplos comuns antes da hora."
        ),
    )


@exercicio(estagio=13, dificuldade=2, tipo="prever", conceitos=["listas", "funcoes", "return", "teste_de_mesa"])
def prever_lista_mutada_em_funcao(r):
    a = r.randint(2, 6)
    b = r.randint(7, 12)
    c = r.randint(13, 18)
    return dict(
        titulo="Passagem de lista para função",
        enunciado=(
            "Atenção: listas são **mutáveis**! Alterar a lista recebida altera o mesmo objeto fora da função.\n\n"
            "Faça o teste de mesa e escreva exatamente a saída:"
        ),
        solucao=(
            "def processar(itens, k):\n"
            "    for i in range(len(itens)):\n"
            "        if itens[i] % 2 == 0:\n"
            "            itens[i] += k\n"
            "    return sum(itens)\n"
            "\n"
            f"dados = [{a}, {b}, {c}]\n"
            "total = processar(dados, 1)\n"
            "print(dados)\n"
            "print(total)\n"
        ),
        dicas=[
            "Todo item **par** de `dados` recebe `+ 1` no próprio lugar.",
            "No final, `dados` está modificado e `total` vale a soma dos novos elementos.",
        ],
        explicacao=(
            f"Como `itens` aponta para a mesma lista `dados`, os pares somam 1 e `dados` sai modificado para "
            f"`{[x + 1 if x % 2 == 0 else x for x in (a, b, c)]}`, cuja soma é `{sum(x + 1 if x % 2 == 0 else x for x in (a, b, c))}`."
        ),
    )


@exercicio(estagio=13, dificuldade=3, tipo="funcao", conceitos=["funcoes", "return", "while"])
def mdc_euclides(r):
    casos = [
        (r.randint(4, 9) * 6, r.randint(3, 8) * 6),
        (48, 18),
        (17, 5),
        (100, 25),
    ]
    import math
    a0, b0 = casos[0]
    return dict(
        titulo="Máximo Divisor Comum (Algoritmo de Euclides)",
        enunciado=(
            "O algoritmo de Euclides calcula o **MDC(a, b)** repetindo enquanto `b != 0`:\n"
            "- O novo `a` recebe o antigo `b`\n"
            "- O novo `b` recebe `a % b`\n"
            "Quando `b` chega a `0`, o MDC é `a`!\n\n"
            "Escreva a função `mdc(a, b)` usando `while` e `return`.\n"
            f"Exemplo: `mdc({a0}, {b0})` -> `{math.gcd(a0, b0)}`"
        ),
        solucao=(
            "def mdc(a, b):\n"
            "    while b != 0:\n"
            "        resto = a % b\n"
            "        a = b\n"
            "        b = resto\n"
            "    return a\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(mdc({a}, {b}))"} for a, b in casos],
        testes_visiveis=2,
        dicas=[
            "Guarde `resto = a % b` antes de sobrescrever `a = b`, depois faça `b = resto`.",
            "Quando `b == 0`, o `while` encerra e você dá `return a`.",
        ],
        explicacao=(
            "O algoritmo de Euclides reduz o problema rapidamente dividindo e usando o resto até sobrar resto zero, "
            "sem precisar testar todos os divisores possíveis."
        ),
    )


@exercicio(estagio=13, dificuldade=3, tipo="codigo", conceitos=["for_range", "while", "if_else"])
def primos_no_intervalo(r):
    a1 = r.randint(2, 10)
    b1 = a1 + r.randint(12, 22)
    casos = [(a1, b1), (10, 30), (1, 10), (14, 16)]
    def eh_p(n):
        return n >= 2 and all(n % d != 0 for d in range(2, int(n ** 0.5) + 1))
    ex0 = " ".join(str(x) for x in range(a1, b1 + 1) if eh_p(x))
    return dict(
        titulo="Caçador de primos no intervalo",
        enunciado=(
            "Leia dois inteiros `inicio` e `fim` (`inicio <= fim`, um por linha).\n\n"
            "Encontre e imprima todos os números **primos** entre `inicio` e `fim` (inclusive) na mesma linha separados por espaço "
            "(se não houver nenhum, imprima `Nenhum`).\n\n"
            f"Exemplo (`{a1}` a `{b1}`):\n```\n{ex0}\n```"
        ),
        solucao=(
            'inicio = int(input("Início: "))\n'
            'fim = int(input("Fim: "))\n'
            "primos = []\n"
            "for n in range(inicio, fim + 1):\n"
            "    if n < 2:\n"
            "        continue\n"
            "    eh_primo = True\n"
            "    for d in range(2, n):\n"
            "        if n % d == 0:\n"
            "            eh_primo = False\n"
            "            break\n"
            "    if eh_primo:\n"
            "        primos.append(str(n))\n"
            "if len(primos) == 0:\n"
            '    print("Nenhum")\n'
            "else:\n"
            '    print(" ".join(primos))\n'
        ),
        testes=[{"entrada": f"{a}\n{b}"} for a, b in casos],
        testes_visiveis=1,
        dicas=[
            "Use um `for n in range(inicio, fim + 1):` por fora, e outro `for` (ou função `eh_primo(n)`) para testar cada `n`.",
            "Guarde os primos numa lista e use `\" \".join(...)` ou imprima `Nenhum` se a lista ficar vazia.",
        ],
        explicacao=(
            "Combinamos laços aninhados, flag booleana `eh_primo` com `break` e uma lista para coletar os resultados antes de formatar a saída."
        ),
    )


@exercicio(estagio=13, dificuldade=3, tipo="funcao", conceitos=["funcoes", "return", "while"])
def decimal_para_binario(r):
    casos = [r.randint(10, 35), r.randint(40, 100), 0, 1, 8]
    n0 = casos[0]
    return dict(
        titulo="Conversor decimal -> binário manual",
        enunciado=(
            "Sem usar `bin()`, escreva uma função `para_binario(n)` que receba um inteiro `n >= 0` e **retorne uma string** "
            "com a representação binária dele.\n\n"
            "Dica do método das divisões sucessivas por 2:\n"
            "- Se `n == 0`, retorne `\"0\"`\n"
            "- Enquanto `n > 0`, pegue o resto `n % 2`, adicione à **esquerda** da string (`str(n % 2) + bin_str`) e faça `n //= 2`.\n\n"
            f"Exemplo: `para_binario({n0})` -> `\"{bin(n0)[2:]}\"`"
        ),
        solucao=(
            "def para_binario(n):\n"
            "    if n == 0:\n"
            '        return "0"\n'
            '    resultado = ""\n'
            "    while n > 0:\n"
            "        resultado = str(n % 2) + resultado\n"
            "        n //= 2\n"
            "    return resultado\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(para_binario({v}))"} for v in casos],
        testes_visiveis=2,
        dicas=[
            "Trate `if n == 0: return \"0\"` logo no início.",
            "Concatenar `str(n % 2) + resultado` (resto à esquerda) já monta os dígitos na ordem certa sem precisar inverter depois!",
        ],
        explicacao=(
            "Os restos das divisões sucessivas por 2 saem do dígito menos significativo para o mais significativo; "
            "por isso colocamos cada novo resto à esquerda do texto acumulado."
        ),
    )


@exercicio(estagio=13, dificuldade=3, tipo="corrigir", conceitos=["funcoes", "listas", "depuracao"])
def corrigir_segundo_maior_com_empate(r):
    a, b, c = sorted(r.sample(range(10, 50), 3))
    l1 = [c, c, b, a]
    l2 = [a, b, c]
    l3 = [-5, -5, -10, -2]
    l4 = [10, 20, 20]
    return dict(
        titulo="Empate no maior enganou o segundo maior!",
        enunciado=(
            "A função `segundo_maior(lista)` deveria retornar o segundo maior valor **distinto** (ex.: em `[10, 10, 8, 5]`, o segundo maior é `8`).\n"
            "Mas o código falha quando o maior número aparece repetido ou quando há valores menores no começo! Corrija."
        ),
        codigo_inicial=(
            "def segundo_maior(lista):\n"
            "    ordenada = sorted(lista)\n"
            "    return ordenada[-2]\n"
        ),
        solucao=(
            "def segundo_maior(lista):\n"
            "    maior = max(lista)\n"
            "    candidatos = []\n"
            "    for x in lista:\n"
            "        if x < maior:\n"
            "            candidatos.append(x)\n"
            "    return max(candidatos)\n"
        ),
        testes=[
            {"entrada": "", "chamada": f"print(segundo_maior({l1}))"},
            {"entrada": "", "chamada": f"print(segundo_maior({l2}))"},
            {"entrada": "", "chamada": f"print(segundo_maior({l3}))"},
            {"entrada": "", "chamada": f"print(segundo_maior({l4}))"},
        ],
        testes_visiveis=2,
        dicas=[
            "Se `lista = [20, 20, 10]`, `sorted(lista)[-2]` devolve `20`, o próprio maior!",
            "Encontre primeiro o `maior = max(lista)`, filtre para fora os iguais a `maior`, e pegue o `max()` do que sobrar.",
        ],
        explicacao=(
            "Ordenar e pegar `[-2]` falha quando o maior valor aparece duplicado. Filtrar os elementos estritamente menores "
            "que `max(lista)` garante que encontramos o maior valor distinto abaixo do máximo."
        ),
    )


@exercicio(estagio=13, dificuldade=3, tipo="completar", conceitos=["for_range", "if_else", "acumulador"])
def completar_numero_perfeito(r):
    casos = [6, 28, r.choice([12, 18, 24, 30]), 1]
    n0 = r.choice([6, 28])
    return dict(
        titulo="Verificador de número perfeito",
        enunciado=(
            "Um número inteiro positivo é **perfeito** quando é igual à soma de seus divisores próprios (menores que ele). "
            "Ex.: `6 = 1 + 2 + 3`.\n\n"
            "Complete as lacunas `___` para ler `n` e imprimir `Perfeito` ou `Não perfeito`:"
        ),
        codigo_inicial=(
            'n = int(input("N: "))\n'
            "soma_div = ___\n"
            "for d in range(1, ___):\n"
            "    if n % d == ___:\n"
            "        soma_div += d\n"
            "if n > 0 and soma_div ___ n:\n"
            '    print("Perfeito")\n'
            "else:\n"
            '    print("Não perfeito")\n'
        ),
        solucao=(
            'n = int(input("N: "))\n'
            "soma_div = 0\n"
            "for d in range(1, n):\n"
            "    if n % d == 0:\n"
            "        soma_div += d\n"
            "if n > 0 and soma_div == n:\n"
            '    print("Perfeito")\n'
            "else:\n"
            '    print("Não perfeito")\n'
        ),
        testes=[{"entrada": str(x)} for x in casos],
        testes_visiveis=2,
        dicas=[
            "Como divisores próprios são estritamente menores que `n`, use `range(1, n)`.",
            "No fim, compare `soma_div == n`.",
        ],
        explicacao=(
            "Usar `range(1, n)` exclui automaticamente o próprio `n` da soma dos divisores; então comparamos se a soma iguala `n`."
        ),
    )


@exercicio(estagio=13, dificuldade=4, tipo="funcao", conceitos=["funcoes", "strings", "for_range"])
def comprimir_rle_caracteres(r):
    casos = [
        "".join(r.choice("ABC") * r.randint(2, 4) for _ in range(3)),
        "aaabbc",
        "xxxx",
        "abc",
    ]
    def rle(s):
        out = ""
        cont = 1
        for i in range(1, len(s)):
            if s[i] == s[i - 1]:
                cont += 1
            else:
                out += s[i - 1] + str(cont)
                cont = 1
        return out + s[-1] + str(cont)
    s0 = casos[0]
    return dict(
        titulo="Compressão de texto (RLE)",
        enunciado=(
            "Escreva uma função `comprimir(texto)` que receba uma string não vazia e comprima repetições consecutivas "
            "no formato `<letra><quantidade>`.\n\n"
            f"Exemplo: `comprimir(\"{s0}\")` -> `\"{rle(s0)}\"` e `comprimir(\"abc\")` -> `\"a1b1c1\"`."
        ),
        solucao=(
            "def comprimir(texto):\n"
            '    resultado = ""\n'
            "    cont = 1\n"
            "    for i in range(1, len(texto)):\n"
            "        if texto[i] == texto[i - 1]:\n"
            "            cont += 1\n"
            "        else:\n"
            "            resultado += texto[i - 1] + str(cont)\n"
            "            cont = 1\n"
            "    resultado += texto[-1] + str(cont)\n"
            "    return resultado\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(comprimir({s!r}))"} for s in casos],
        testes_visiveis=2,
        dicas=[
            "Percorra os índices a partir de `1`, comparando `texto[i]` com a letra anterior `texto[i - 1]`.",
            "Quando mudar de letra, grave `texto[i - 1] + str(cont)` e zere `cont = 1`. Não esqueça de gravar o **último grupo** após sair do `for`!",
        ],
        explicacao=(
            "O último bloco consecutivo nunca encontra uma 'próxima letra diferente' dentro do `for`, por isso precisamos "
            "adicionar `texto[-1] + str(cont)` logo depois que o laço termina."
        ),
    )


@exercicio(estagio=13, dificuldade=4, tipo="funcao", conceitos=["funcoes", "strings", "listas"])
def verificar_anagramas(r):
    verdadeiros = [
        ("amor", "Roma"), ("iracema", "America"), ("python", "typhon"),
        ("casa", "saca"), ("pedra", "padre"), ("rota", "ator"), ("lago", "algo"),
    ]
    falsos = [("teste", "teto"), ("ab", "abc"), ("casa", "casas"), ("bola", "bota")]
    pares = r.sample(verdadeiros, 3) + r.sample(falsos, 2)
    r.shuffle(pares)
    return dict(
        titulo="Detector de anagramas",
        enunciado=(
            "Duas palavras são **anagramas** se possuem exatamente as mesmas letras com as mesmas quantidades (ignorando maiúsculas/minúsculas). "
            "Ex.: `\"amor\"` e `\"Roma\"`.\n\n"
            "Escreva a função `sao_anagramas(p1, p2)` retornando `True` ou `False`."
        ),
        solucao=(
            "def sao_anagramas(p1, p2):\n"
            "    a = sorted(p1.lower())\n"
            "    b = sorted(p2.lower())\n"
            "    return a == b\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(sao_anagramas({x!r}, {y!r}))"} for x, y in pares],
        testes_visiveis=2,
        dicas=[
            "Coloque ambas as palavras em minúsculas com `.lower()`.",
            "Se você ordenar as letras das duas palavras com `sorted()`, anagramas viram listas idênticas!",
        ],
        explicacao=(
            "Ordenar os caracteres (`sorted(palavra.lower())`) transforma a verificação de frequências de todas as letras "
            "em uma simples comparação de igualdade `a == b`."
        ),
    )


@exercicio(estagio=13, dificuldade=4, tipo="codigo", conceitos=["listas", "for_range", "contador"])
def maior_sequencia_positiva(r):
    def gerar_seq():
        vals = [r.choice([-2, -1, 1, 2, 3, 4]) for _ in range(r.randint(6, 9))]
        return [len(vals)] + vals
    casos = [gerar_seq(), [6, 2, 5, -1, 3, 4, 8], [4, -1, -2, -3, -4]]
    c0 = casos[0]
    best = cur = 0
    for x in c0[1:]:
        if x > 0:
            cur += 1
            if cur > best:
                best = cur
        else:
            cur = 0
    return dict(
        titulo="Maior sequência de dias no lucro",
        enunciado=(
            "Leia `n` e depois `n` valores inteiros representando o lucro diário de uma loja.\n\n"
            "Descubra o tamanho da **maior sequência consecutiva** de dias com lucro **estritamente positivo (`> 0`)**:\n"
            f"Exemplo (`n={c0[0]}`, dias `{' '.join(map(str, c0[1:]))}`):\n```\nMaior sequência: {best}\n```"
        ),
        solucao=(
            'n = int(input("Dias: "))\n'
            "atual = 0\n"
            "melhor = 0\n"
            "for _ in range(n):\n"
            "    lucro = int(input())\n"
            "    if lucro > 0:\n"
            "        atual += 1\n"
            "        if atual > melhor:\n"
            "            melhor = atual\n"
            "    else:\n"
            "        atual = 0\n"
            'print("Maior sequência:", melhor)\n'
        ),
        testes=[{"entrada": "\n".join(map(str, c))} for c in casos],
        testes_visiveis=1,
        dicas=[
            "Mantenha dois contadores: `atual` (tamanho da sequência presente) e `melhor` (recorde até agora).",
            "Quando o lucro for `<= 0`, zere `atual = 0`; quando for `> 0`, some `1` e atualize `melhor` se `atual > melhor`.",
        ],
        explicacao=(
            "Esse algoritmo acompanha a sequência contínua em uma única passada sem precisar guardar todos os trechos na memória."
        ),
    )


@exercicio(estagio=13, dificuldade=4, tipo="codigo", conceitos=["while", "elif", "contador"])
def simulacao_jogo_adivinhacao(r):
    secreto = r.randint(20, 60)
    casos = [
        f"{secreto}\n{secreto - 10}\n{secreto + 5}\n{secreto}",
        f"{secreto}\n{secreto}",
        f"50\n10\n80\n40\n55\n50",
    ]
    return dict(
        titulo="Simulador de adivinhação",
        enunciado=(
            "Leia primeiro o `numero_secreto` (`int`). Em seguida, leia palpites (`int`, um por linha) em um `while` até acertar:\n"
            "- Se o palpite for menor: imprima `Maior`\n"
            "- Se o palpite for maior: imprima `Menor`\n"
            "- Quando acertar: imprima `Acertou em X tentativas!` (trocando `X` pela contagem) e encerre.\n\n"
            f"Exemplo (secreto `{secreto}`, palpites `{secreto - 10}`, `{secreto + 5}`, `{secreto}`):\n"
            "```\nMaior\nMenor\nAcertou em 3 tentativas!\n```"
        ),
        solucao=(
            "secreto = int(input())\n"
            "tentativas = 0\n"
            "while True:\n"
            "    palpite = int(input())\n"
            "    tentativas += 1\n"
            "    if palpite < secreto:\n"
            '        print("Maior")\n'
            "    elif palpite > secreto:\n"
            '        print("Menor")\n'
            "    else:\n"
            '        print(f"Acertou em {tentativas} tentativas!")\n'
            "        break\n"
        ),
        testes=[{"entrada": c} for c in casos],
        testes_visiveis=1,
        dicas=[
            "Incremente `tentativas += 1` logo após ler cada palpite.",
            "Se `palpite == secreto`, imprima a mensagem e use `break` para sair do laço.",
        ],
        explicacao=(
            "Usar `while True:` com `break` quando acerta evita ter que duplicar o `input()` antes e dentro do laço."
        ),
    )


@exercicio(estagio=13, dificuldade=4, tipo="corrigir", conceitos=["while", "listas", "depuracao"])
def corrigir_simulacao_estoque(r):
    ini = r.randint(15, 25)
    casos = [
        f"{ini}\n-5\n-12\n+10\n0",
        "10\n-4\n-8\n0",
        "20\n-5\n-5\n-5\n0",
    ]
    return dict(
        titulo="Estoque permitindo saldo negativo!",
        enunciado=(
            "O programa lê o estoque inicial (`int`) e depois movimentações (`int` positivas ou negativas) até digitar `0`.\n"
            "Se uma retirada deixaria o estoque **abaixo de 0**, ela deve ser **recusada** imprimindo `Estoque insuficiente` (sem alterar o saldo)! "
            "No fim (`0`), imprime `Estoque final: X`.\n\n"
            "Mas o código atual está descontando mesmo quando falta estoque! Corrija."
        ),
        codigo_inicial=(
            "estoque = int(input())\n"
            "mov = int(input())\n"
            "while mov != 0:\n"
            "    estoque += mov\n"
            "    if estoque < 0:\n"
            '        print("Estoque insuficiente")\n'
            "    mov = int(input())\n"
            'print("Estoque final:", estoque)\n'
        ),
        solucao=(
            "estoque = int(input())\n"
            "mov = int(input())\n"
            "while mov != 0:\n"
            "    if estoque + mov < 0:\n"
            '        print("Estoque insuficiente")\n'
            "    else:\n"
            "        estoque += mov\n"
            "    mov = int(input())\n"
            'print("Estoque final:", estoque)\n'
        ),
        testes=[{"entrada": c} for c in casos],
        testes_visiveis=1,
        dicas=[
            "Não podemos alterar `estoque` antes de checar se a operação é válida!",
            "Teste `if estoque + mov < 0:` antes — só altere `estoque` no `else:`.",
        ],
        explicacao=(
            "Testar o resultado projetado (`estoque + mov < 0`) antes de aplicar a alteração preserva o estado consistente do sistema."
        ),
    )


@exercicio(estagio=13, dificuldade=5, tipo="funcao", conceitos=["funcoes", "listas", "for_range", "return"])
def soma_diagonais_matriz(r):
    def mat(k):
        return [[r.randint(1, 9) for _ in range(k)] for _ in range(k)]
    m1 = mat(3)
    m2 = mat(2)
    m3 = [[5]]
    m4 = mat(4)
    p1 = sum(m1[i][i] for i in range(3))
    s1 = sum(m1[i][2 - i] for i in range(3))
    return dict(
        titulo="Diagonais de uma matriz quadrada",
        enunciado=(
            "Representamos uma matriz `N x N` como uma lista de listas (ex.: `[[1, 2], [3, 4]]`).\n\n"
            "Escreva a função `soma_diagonais(matriz)` que retorne uma lista `[diag_principal, diag_secundaria]`:\n"
            "- Diagonal principal: elementos onde linha == coluna (`matriz[i][i]`)\n"
            "- Diagonal secundária: elementos `matriz[i][n - 1 - i]`\n\n"
            f"Exemplo para `{m1}` -> `[{p1}, {s1}]`"
        ),
        solucao=(
            "def soma_diagonais(matriz):\n"
            "    n = len(matriz)\n"
            "    principal = 0\n"
            "    secundaria = 0\n"
            "    for i in range(n):\n"
            "        principal += matriz[i][i]\n"
            "        secundaria += matriz[i][n - 1 - i]\n"
            "    return [principal, secundaria]\n"
        ),
        testes=[
            {"entrada": "", "chamada": f"print(soma_diagonais({m1}))"},
            {"entrada": "", "chamada": f"print(soma_diagonais({m2}))"},
            {"entrada": "", "chamada": f"print(soma_diagonais({m3}))"},
            {"entrada": "", "chamada": f"print(soma_diagonais({m4}))"},
        ],
        testes_visiveis=1,
        dicas=[
            "Com `n = len(matriz)`, um único `for i in range(n):` percorre as duas diagonais ao mesmo tempo!",
            "Na diagonal secundária, enquanto a linha `i` sobe (`0, 1, ...`), a coluna desce (`n - 1 - i`).",
        ],
        explicacao=(
            "Cada elemento de uma lista de listas é acessado com dois colchetes `matriz[linha][coluna]`, e a relação entre "
            "linha e coluna nas diagonais resolve tudo em tempo linear sem precisar de dois `for`."
        ),
    )


@exercicio(estagio=13, dificuldade=5, tipo="codigo", conceitos=["listas", "for_range", "elif"])
def placar_campeonato_futebol(r):
    t1, t2 = r.sample(["Tigres", "Leões", "Águias", "Lobos", "Falcões"], 2)
    def jogo():
        return f"{r.randint(0, 4)} {r.randint(0, 4)}"
    c1 = f"{t1}\n{t2}\n3\n{jogo()}\n{jogo()}\n{jogo()}"
    c2 = f"Azul\nVerde\n4\n2 0\n1 1\n0 3\n2 2"
    c3 = f"A\nB\n2\n1 0\n2 1"
    return dict(
        titulo="Tabela de campeonato",
        enunciado=(
            "Dois times disputam `n` partidas. Leia:\n"
            "1. Nome do time A (`str`)\n"
            "2. Nome do time B (`str`)\n"
            "3. Número de partidas `n` (`int`)\n"
            "4. Nas `n` linhas seguintes: dois inteiros separados por espaço (`gols_A gols_B`).\n\n"
            "Vitória vale **3 pontos**, empate **1 ponto**, derrota **0 pontos**. "
            "Mostre os pontos de cada time e quem venceu (ou `Empate` se tiverem a mesma pontuação):"
            f"\n```\n{t1}: X pts\n{t2}: Y pts\nVencedor: ...\n```"
        ),
        solucao=(
            "time_a = input().strip()\n"
            "time_b = input().strip()\n"
            "n = int(input())\n"
            "pts_a = 0\n"
            "pts_b = 0\n"
            "for _ in range(n):\n"
            "    partes = input().split()\n"
            "    ga = int(partes[0])\n"
            "    gb = int(partes[1])\n"
            "    if ga > gb:\n"
            "        pts_a += 3\n"
            "    elif gb > ga:\n"
            "        pts_b += 3\n"
            "    else:\n"
            "        pts_a += 1\n"
            "        pts_b += 1\n"
            'print(f"{time_a}: {pts_a} pts")\n'
            'print(f"{time_b}: {pts_b} pts")\n'
            "if pts_a > pts_b:\n"
            '    print("Vencedor:", time_a)\n'
            "elif pts_b > pts_a:\n"
            '    print("Vencedor:", time_b)\n'
            "else:\n"
            '    print("Empate")\n'
        ),
        testes=[{"entrada": c} for c in (c1, c2, c3)],
        testes_visiveis=1,
        dicas=[
            "Para ler dois números na mesma linha, faça `partes = input().split()` e converta `int(partes[0])` e `int(partes[1])`.",
            "Compare `ga` e `gb` em cada partida e depois compare `pts_a` e `pts_b` no final.",
        ],
        explicacao=(
            "`input().split()` separa múltiplos valores digitados na mesma linha em uma lista de strings, "
            "permitindo ler placares no formato natural `2 1`."
        ),
    )


@exercicio(estagio=13, dificuldade=5, tipo="funcao", conceitos=["funcoes", "strings", "return"])
def validar_digito_verificador_simples(r):
    def montar_doc(base):
        soma = sum(int(d) * (len(base) + 1 - i) for i, d in enumerate(base))
        dv = (soma * 10) % 11
        if dv == 10:
            dv = 0
        return base + str(dv)
    b1 = "".join(str(r.randint(1, 9)) for _ in range(5))
    v1 = montar_doc(b1)
    inv1 = b1 + str((int(v1[-1]) + 1) % 10)
    b2 = "".join(str(r.randint(0, 9)) for _ in range(5))
    v2 = montar_doc(b2)
    return dict(
        titulo="Validador de dígito verificador (estilo CPF)",
        enunciado=(
            "Documentos como o CPF usam um **dígito verificador (DV)** calculado com pesos decrescentes!\n\n"
            "Escreva a função `validar_codigo(codigo)` que recebe uma string numérica de **6 dígitos** (5 dígitos base + 1 DV):\n"
            "1. Multiplique os 5 primeiros dígitos pelos pesos `6, 5, 4, 3, 2` respectivamente e some tudo.\n"
            "2. Calcule `dv = (soma * 10) % 11`. Se `dv == 10`, ele vira `0`.\n"
            "3. Retorne `True` se `dv` for igual ao 6º dígito (`int(codigo[5])`), ou `False` caso contrário.\n\n"
            f"Exemplo: `validar_codigo(\"{v1}\")` -> `True`"
        ),
        solucao=(
            "def validar_codigo(codigo):\n"
            "    if len(codigo) != 6 or not codigo.isdigit():\n"
            "        return False\n"
            "    soma = 0\n"
            "    for i in range(5):\n"
            "        soma += int(codigo[i]) * (6 - i)\n"
            "    dv = (soma * 10) % 11\n"
            "    if dv == 10:\n"
            "        dv = 0\n"
            "    return dv == int(codigo[5])\n"
        ),
        testes=[
            {"entrada": "", "chamada": f"print(validar_codigo({v1!r}))"},
            {"entrada": "", "chamada": f"print(validar_codigo({inv1!r}))"},
            {"entrada": "", "chamada": f"print(validar_codigo({v2!r}))"},
            {"entrada": "", "chamada": "print(validar_codigo('123'))"},
        ],
        testes_visiveis=2,
        dicas=[
            "No `for i in range(5):`, quando `i` vale `0, 1, 2, 3, 4`, o peso `6 - i` vale `6, 5, 4, 3, 2`!",
            "Converta cada caractere `codigo[i]` com `int()` antes de multiplicar.",
        ],
        explicacao=(
            "Usar a relação matemática `6 - i` evita criar listas de pesos manualmente e mostra exatamente a lógica real "
            "por trás do módulo 11 usado em documentos brasileiros."
        ),
    )


@exercicio(estagio=13, dificuldade=5, tipo="codigo", conceitos=["while", "for_range", "if_else", "fstring"])
def caixa_eletronico_interativo_cedulas(r):
    cedulas_disp = [100, 50, 20, 10, 5, 2, 1]
    casos = [r.randint(138, 487), r.randint(43, 99), 200]
    v0 = casos[0]
    linhas = []
    rest = v0
    for c in cedulas_disp:
        q = rest // c
        rest %= c
        if q > 0:
            linhas.append(f"{q} nota(s) de R$ {c}")
    return dict(
        titulo="Caixa eletrônico inteligente (só notas usadas)",
        enunciado=(
            "Leia um valor inteiro de saque (`valor > 0`). Usando uma lista de cédulas `[100, 50, 20, 10, 5, 2, 1]` e um `for`, "
            "calcule o menor número de cédulas e imprima **apenas as cédulas com quantidade > 0**:\n\n"
            f"Exemplo para `{v0}`:\n```\n" + "\n".join(linhas) + "\n```"
        ),
        solucao=(
            'valor = int(input("Saque: "))\n'
            "cedulas = [100, 50, 20, 10, 5, 2, 1]\n"
            "for c in cedulas:\n"
            "    qtd = valor // c\n"
            "    valor %= c\n"
            "    if qtd > 0:\n"
            '        print(f"{qtd} nota(s) de R$ {c}")\n'
        ),
        testes=[{"entrada": str(x)} for x in casos],
        testes_visiveis=1,
        dicas=[
            "Guarde `[100, 50, 20, 10, 5, 2, 1]` numa lista e percorra com `for c in cedulas:`!",
            "Compare como isso é muito mais enxuto do que no estágio 4, quando ainda não conhecíamos listas nem laços!",
        ],
        explicacao=(
            "Fechamos o nível básico vendo a evolução do raciocínio: o mesmo problema de cédulas do estágio 4, "
            "que antes exigia repetir código para cada nota, agora se resolve com elegância em 6 linhas usando lista + laço."
        ),
    )
