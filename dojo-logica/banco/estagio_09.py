"""Estágio 9 - Repetição com for e range() (sem listas e sem def)."""

from .base import exercicio


@exercicio(estagio=9, dificuldade=1, tipo="codigo", conceitos=["for_range", "input"])
def repetir_mensagem_n_vezes(r):
    frase = r.choice(["Praticar todos os dias!", "Foco na lógica!", "Python é incrível!"])
    casos = [r.randint(2, 5), r.randint(3, 6), 1]
    n0 = casos[0]
    ex0 = "\n".join(f"{i} - {frase}" for i in range(1, n0 + 1))
    return dict(
        titulo="Repetindo N vezes com numeração",
        enunciado=(
            f"Leia um inteiro `n` e use `for` com `range()` para imprimir a frase `\"{frase}\"` `n` vezes, "
            "numerada de `1` até `n`:\n\n"
            f"Exemplo para `n = {n0}`:\n```\n{ex0}\n```"
        ),
        solucao=(
            'n = int(input("Quantas vezes? "))\n'
            "for i in range(1, n + 1):\n"
            f'    print(f"{{i}} - {frase}")\n'
        ),
        testes=[{"entrada": str(x)} for x in casos],
        testes_visiveis=1,
        dicas=[
            "Lembre que `range(1, n)` para no `n - 1`! Para ir até `n` inclusive, use `range(1, n + 1)`.",
            "Combine `i` e a frase usando f-string.",
        ],
        explicacao=(
            "Em `range(inicio, fim)`, o valor `fim` é exclusivo (fica de fora), por isso passamos `n + 1` como limite superior."
        ),
    )


@exercicio(estagio=9, dificuldade=1, tipo="completar", conceitos=["for_range", "acumulador"])
def completar_soma_intervalo_for(r):
    casos = [
        (r.randint(2, 5), r.randint(7, 12)),
        (1, r.randint(5, 10)),
        (4, 4),
    ]
    a0, b0 = casos[0]
    return dict(
        titulo="Soma de A até B",
        enunciado=(
            "Complete as lacunas `___` para ler dois inteiros `a` e `b` (`a <= b`) e somar todos os números de `a` até `b` (inclusive):\n\n"
            f"Exemplo (`{a0}` e `{b0}`):\n```\nSoma: {sum(range(a0, b0 + 1))}\n```"
        ),
        codigo_inicial=(
            'a = int(input("Início: "))\n'
            'b = int(input("Fim: "))\n'
            "soma = 0\n"
            "for n in ___(a, b + ___):\n"
            "    soma += ___\n"
            'print("Soma:", soma)\n'
        ),
        solucao=(
            'a = int(input("Início: "))\n'
            'b = int(input("Fim: "))\n'
            "soma = 0\n"
            "for n in range(a, b + 1):\n"
            "    soma += n\n"
            'print("Soma:", soma)\n'
        ),
        testes=[{"entrada": f"{a}\n{b}"} for a, b in casos],
        testes_visiveis=1,
        dicas=[
            "Use `range(a, b + 1)` para que `b` também entre na soma.",
            "A cada volta do laço, acumule a variável do laço `n` dentro de `soma`.",
        ],
        explicacao=(
            "O `for` visita automaticamente cada número do intervalo sem precisar de variável contadora manual nem incremento."
        ),
    )


@exercicio(estagio=9, dificuldade=2, tipo="prever", conceitos=["for_range", "teste_de_mesa"])
def prever_range_com_passo(r):
    ini = r.randint(2, 5)
    fim = ini + r.randint(8, 12)
    passo = r.randint(2, 3)
    return dict(
        titulo="Pulando de passo em passo",
        enunciado=(
            "Observe o terceiro argumento de `range(inicio, fim, passo)` e escreva exatamente o que o código imprime:"
        ),
        solucao=(
            f"for k in range({ini}, {fim}, {passo}):\n"
            '    print(k, end=" ")\n'
            "print()\n"
            "for j in range(3, 0, -1):\n"
            "    print(j)\n"
        ),
        dicas=[
            f"O primeiro `for` começa em `{ini}`, soma `{passo}` a cada passo e para estritamente **antes** de `{fim}`.",
            "O segundo `for` usa passo `-1`: ele conta para trás (`3, 2, 1`), parando antes do `0`.",
        ],
        explicacao=(
            "O `print()` vazio quebra a linha após os números impressos com `end=\" \"`, e o segundo laço ilustra "
            "a contagem regressiva com passo negativo em `range(3, 0, -1)`."
        ),
    )


@exercicio(estagio=9, dificuldade=2, tipo="codigo", conceitos=["for_range", "acumulador"])
def calcular_fatorial_for(r):
    casos = [r.randint(4, 7), r.randint(2, 6), 0, 1]
    n0 = casos[0]
    fat = 1
    for i in range(1, n0 + 1):
        fat *= i
    return dict(
        titulo="Fatorial com for",
        enunciado=(
            "O fatorial de `n` (`n!`) é o produto `1 * 2 * ... * n` (por definição, `0! = 1`).\n\n"
            "Leia um inteiro `n >= 0` e calcule `n!` usando `for` e um acumulador multiplicativo:\n"
            f"Exemplo para `n = {n0}`:\n```\n{n0}! = {fat}\n```"
        ),
        solucao=(
            'n = int(input("N: "))\n'
            "fat = 1\n"
            "for i in range(1, n + 1):\n"
            "    fat *= i\n"
            'print(f"{n}! = {fat}")\n'
        ),
        testes=[{"entrada": str(x)} for x in casos],
        testes_visiveis=1,
        dicas=[
            "Um acumulador de **multiplicação** deve começar valendo `1` (nunca `0`!).",
            "Se `n == 0`, `range(1, 1)` fica vazio e `fat` permanece `1`, acertando `0! = 1` automaticamente.",
        ],
        explicacao=(
            "Iniciar `fat = 1` trata tanto o caso base `0!` quanto o elemento neutro da multiplicação para os laços seguintes."
        ),
    )


@exercicio(estagio=9, dificuldade=2, tipo="corrigir", conceitos=["for_range", "acumulador", "depuracao"])
def corrigir_range_off_by_one(r):
    mult = r.choice([3, 5, 7])
    casos = [mult * r.randint(3, 5), mult * r.randint(2, 4), mult]
    n0 = casos[0]
    s0 = sum(x for x in range(1, n0 + 1) if x % mult == 0)
    return dict(
        titulo=f"Soma dos múltiplos de {mult} esquecendo o último!",
        enunciado=(
            f"O programa deveria ler `n` e somar todos os múltiplos de `{mult}` de `1` até `n` **inclusive**.\n"
            f"Para `n = {n0}`, a saída correta é:\n```\nSoma: {s0}\n```\n"
            "Mas está deixando o último valor de fora quando `n` é múltiplo! Corrija o bug."
        ),
        codigo_inicial=(
            'n = int(input("N: "))\n'
            "soma = 0\n"
            "for i in range(1, n):\n"
            f"    if i % {mult} == 0:\n"
            "        soma += i\n"
            'print("Soma:", soma)\n'
        ),
        solucao=(
            'n = int(input("N: "))\n'
            "soma = 0\n"
            "for i in range(1, n + 1):\n"
            f"    if i % {mult} == 0:\n"
            "        soma += i\n"
            'print("Soma:", soma)\n'
        ),
        testes=[{"entrada": str(x)} for x in casos],
        testes_visiveis=1,
        dicas=[
            "Em `range(1, n)`, qual é o maior número gerado?",
            "Troque `n` por `n + 1` dentro do `range`.",
        ],
        explicacao=(
            "O erro *off-by-one* em `range(1, n)` fazia o laço parar em `n - 1`. Usando `range(1, n + 1)`, o próprio `n` passa a ser testado."
        ),
    )


@exercicio(estagio=9, dificuldade=3, tipo="codigo", conceitos=["for_range", "acumulador", "contador"])
def ler_n_notas_e_media(r):
    def seq():
        k = r.randint(3, 5)
        return [k] + [round(r.uniform(5.0, 9.5), 1) for _ in range(k)]
    casos = [seq(), seq(), [2, 8.0, 6.0]]
    c0 = casos[0]
    m0 = sum(c0[1:]) / c0[0]
    return dict(
        titulo="Lendo exatamente N notas",
        enunciado=(
            "Primeiro, o programa lê um inteiro `n` indicando **quantas notas** serão digitadas.\n"
            "Em seguida, lê exatamente `n` notas (`float`, uma por linha) usando `for`.\n\n"
            "Mostre a média das notas com 2 casas decimais:\n"
            f"Exemplo (para `n={c0[0]}` e notas `{' '.join(map(str, c0[1:]))}`):\n```\nMédia: {m0:.2f}\n```"
        ),
        solucao=(
            'n = int(input("Quantidade de notas: "))\n'
            "soma = 0.0\n"
            "for _ in range(n):\n"
            '    nota = float(input("Nota: "))\n'
            "    soma += nota\n"
            "media = soma / n\n"
            'print(f"Média: {media:.2f}")\n'
        ),
        testes=[{"entrada": "\n".join(map(str, c))} for c in casos],
        testes_visiveis=1,
        dicas=[
            "Leia `n` antes do laço e faça `for _ in range(n):` para repetir `n` vezes.",
            "Em cada repetição, leia uma `nota` com `float(input())` e some em `soma`.",
        ],
        explicacao=(
            "Quando já sabemos de início quantas entradas virão (`n`), `for _ in range(n):` lê exatamente a quantidade certa "
            "sem precisar de sentinela nem contador manual."
        ),
    )


@exercicio(estagio=9, dificuldade=3, tipo="codigo", conceitos=["for_range", "if_else", "input"])
def maior_entre_n_leituras(r):
    def seq():
        k = r.randint(4, 6)
        return [k] + [r.randint(-20, 60) for _ in range(k)]
    casos = [seq(), seq(), [3, -15, -3, -9]]
    c0 = casos[0]
    return dict(
        titulo="Campeão entre N competidores",
        enunciado=(
            "Leia um inteiro `n` (`n >= 1`) e, em seguida, leia `n` pontuações inteiras (que podem ser negativas!).\n\n"
            "Sem usar listas, descubra e mostre a **maior** pontuação:\n"
            f"Exemplo (`n={c0[0]}`, valores `{' '.join(map(str, c0[1:]))}`):\n```\nMaior: {max(c0[1:])}\n```"
        ),
        solucao=(
            'n = int(input("Quantidade: "))\n'
            "maior = int(input())\n"
            "for _ in range(n - 1):\n"
            "    valor = int(input())\n"
            "    if valor > maior:\n"
            "        maior = valor\n"
            'print("Maior:", maior)\n'
        ),
        testes=[{"entrada": "\n".join(map(str, c))} for c in casos],
        testes_visiveis=1,
        dicas=[
            "Como os números podem ser negativos, nunca comece `maior = 0`!",
            "Leia o primeiro valor antes do laço para ser o `maior` inicial e repita `range(n - 1)` para ler os demais.",
        ],
        explicacao=(
            "Lendo a 1ª pontuação antes do `for` e rodando `n - 1` vezes, o algoritmo funciona mesmo quando todos os valores são negativos."
        ),
    )


@exercicio(estagio=9, dificuldade=3, tipo="prever", conceitos=["for_range", "acumulador", "teste_de_mesa"])
def prever_for_sobre_texto(r):
    palavra = r.choice(["logica", "codigo", "python", "treino"])
    alvo = r.choice([c for c in set(palavra)])
    return dict(
        titulo="Percorrendo letras com for",
        enunciado=(
            "O `for` também percorre cada caractere de uma string, um por volta!\n\n"
            "Faça o teste de mesa e escreva exatamente o que o trecho imprime:"
        ),
        solucao=(
            f'texto = "{palavra}"\n'
            "cont = 0\n"
            "for letra in texto:\n"
            f'    if letra == "{alvo}":\n'
            "        cont += 1\n"
            "print(len(texto), cont)\n"
        ),
        dicas=[
            "`for letra in texto:` visita uma letra por vez da esquerda para a direita.",
            f"Conte quantas vezes `'{alvo}'` aparece em `\"{palavra}\"`, e lembre que `len(texto)` é o total de letras.",
        ],
        explicacao=(
            f"A palavra `\"{palavra}\"` tem {len(palavra)} letras e contém a letra `'{alvo}'` {palavra.count(alvo)} vez(es)."
        ),
    )


@exercicio(estagio=9, dificuldade=3, tipo="corrigir", conceitos=["for_range", "acumulador", "depuracao"])
def corrigir_acumulador_zerado_dentro(r):
    casos = [r.randint(4, 7), r.randint(3, 6), 1]
    n0 = casos[0]
    s0 = sum(i * i for i in range(1, n0 + 1))
    return dict(
        titulo="A soma que sempre recomeça do zero!",
        enunciado=(
            f"O programa deveria somar os quadrados de `1` até `n` (`1² + 2² + ... + n²`).\n"
            f"Para `n = {n0}`, deveria dar:\n```\nSoma dos quadrados: {s0}\n```\n"
            "Mas está imprimindo só o quadrado de `n`! Encontre o erro e corrija."
        ),
        codigo_inicial=(
            'n = int(input("N: "))\n'
            "for i in range(1, n + 1):\n"
            "    soma = 0\n"
            "    soma += i ** 2\n"
            'print("Soma dos quadrados:", soma)\n'
        ),
        solucao=(
            'n = int(input("N: "))\n'
            "soma = 0\n"
            "for i in range(1, n + 1):\n"
            "    soma += i ** 2\n"
            'print("Soma dos quadrados:", soma)\n'
        ),
        testes=[{"entrada": str(x)} for x in casos],
        testes_visiveis=1,
        dicas=[
            "Olhe onde `soma = 0` está colocado: ele é executado **em toda volta** do `for`!",
            "Mova `soma = 0` para **antes** da linha do `for`.",
        ],
        explicacao=(
            "Zerar um acumulador dentro do laço apaga tudo o que foi somado nas voltas anteriores. "
            "Inicializações de acumuladores e contadores ficam sempre fora e antes do laço."
        ),
    )


@exercicio(estagio=9, dificuldade=3, tipo="completar", conceitos=["for_range", "contador"])
def completar_contar_aprovados(r):
    media_corte = r.choice([5.5, 6.0, 6.5, 7.0])
    def seq():
        k = r.randint(4, 6)
        return [k] + [round(r.uniform(3.5, 9.5), 1) for _ in range(k)]
    casos = [seq(), seq(), [3, media_corte, round(media_corte - 1.5, 1), 8.5]]
    c0 = casos[0]
    ap0 = sum(1 for x in c0[1:] if x >= media_corte)
    return dict(
        titulo="Contando alunos aprovados",
        enunciado=(
            f"Leia `n` e depois `n` notas (`float`). Complete as lacunas `___` para contar quantos alunos tiraram "
            f"nota maior ou igual a **{media_corte:.1f}**:\n\n"
            f"Exemplo (`n={c0[0]}`, notas `{' '.join(map(str, c0[1:]))}`):\n```\nAprovados: {ap0}\n```"
        ),
        codigo_inicial=(
            'n = int(input("Alunos: "))\n'
            "aprovados = ___\n"
            "for i in range(___):\n"
            '    nota = float(input("Nota: "))\n'
            f"    if nota >= {media_corte}:\n"
            "        aprovados += ___\n"
            'print("Aprovados:", aprovados)\n'
        ),
        solucao=(
            'n = int(input("Alunos: "))\n'
            "aprovados = 0\n"
            "for i in range(n):\n"
            '    nota = float(input("Nota: "))\n'
            f"    if nota >= {media_corte}:\n"
            "        aprovados += 1\n"
            'print("Aprovados:", aprovados)\n'
        ),
        testes=[{"entrada": "\n".join(map(str, c))} for c in casos],
        testes_visiveis=1,
        dicas=[
            "Inicie o contador `aprovados` com `0` antes do laço e faça o `for` repetir `n` vezes com `range(n)`.",
            "Dentro do `if`, some `1` em `aprovados` toda vez que a nota atingir a média.",
        ],
        explicacao=(
            "Um contador iniciado em `0` antes do `for` recebe `+= 1` somente quando o `if` interno é satisfeito."
        ),
    )


@exercicio(estagio=9, dificuldade=4, tipo="codigo", conceitos=["for_range", "input"])
def escadinha_asteriscos(r):
    simb = r.choice(["*", "#", "+"])
    casos = [r.randint(3, 6), r.randint(2, 5), 1]
    n0 = casos[0]
    ex0 = "\n".join(simb * i for i in range(1, n0 + 1))
    return dict(
        titulo="Escada de símbolos",
        enunciado=(
            f"Leia um inteiro `n` e desenhe uma escada de `n` degraus usando o caractere `\"{simb}\"`:\n\n"
            f"Exemplo para `n = {n0}`:\n```\n{ex0}\n```"
        ),
        solucao=(
            'n = int(input("Altura: "))\n'
            "for i in range(1, n + 1):\n"
            f'    print("{simb}" * i)\n'
        ),
        testes=[{"entrada": str(x)} for x in casos],
        testes_visiveis=1,
        dicas=[
            "Em Python, `\"*\" * i` repete o símbolo `i` vezes.",
            "Faça `i` ir de `1` até `n` com `range(1, n + 1)`.",
        ],
        explicacao=(
            "Combinar `range(1, n + 1)` com repetição de string (`simbolo * i`) desenha padrões em triângulo com apenas duas linhas."
        ),
    )


@exercicio(estagio=9, dificuldade=4, tipo="codigo", conceitos=["for_range", "if_else", "contador"])
def verificar_numero_primo_for(r):
    casos = [
        r.choice([7, 11, 13, 17, 19]),
        r.choice([4, 9, 12, 15, 21]),
        2,
        1,
    ]
    n0 = casos[0]
    return dict(
        titulo="Detector de número primo",
        enunciado=(
            "Um número inteiro maior que `1` é **primo** quando tem exatamente **2 divisores** (`1` e ele mesmo).\n\n"
            "Leia um inteiro positivo `n`, conte quantos divisores ele possui de `1` até `n` usando `for`, "
            "e imprima `Primo` ou `Não primo`.\n\n"
            f"Exemplo para `{n0}`:\n```\nPrimo\n```"
        ),
        solucao=(
            'n = int(input("Número: "))\n'
            "divisores = 0\n"
            "for d in range(1, n + 1):\n"
            "    if n % d == 0:\n"
            "        divisores += 1\n"
            "if divisores == 2:\n"
            '    print("Primo")\n'
            "else:\n"
            '    print("Não primo")\n'
        ),
        testes=[{"entrada": str(x)} for x in casos],
        testes_visiveis=2,
        dicas=[
            "Teste cada `d` de `1` até `n`: se `n % d == 0`, `d` é um divisor — some 1 ao contador.",
            "No fim, só é primo se `divisores == 2` (isso já descarta o número `1`, que só tem 1 divisor!).",
        ],
        explicacao=(
            "Contar os divisores de `1` a `n` resolve até o caso especial `1` (que tem 1 divisor e não é primo) "
            "e `2` (que tem 2 divisores e é primo)."
        ),
    )


@exercicio(estagio=9, dificuldade=4, tipo="prever", conceitos=["for_range", "teste_de_mesa"])
def prever_for_aninhado(r):
    lin = r.randint(2, 3)
    col = r.randint(2, 4)
    return dict(
        titulo="Laço dentro de laço (for aninhado)",
        enunciado=(
            "Quando há um `for` dentro de outro, para **cada passo** do laço externo, o laço interno roda **inteiro**.\n\n"
            "Faça o teste de mesa e escreva exatamente a saída:"
        ),
        solucao=(
            f"for i in range(1, {lin + 1}):\n"
            f"    for j in range(1, {col + 1}):\n"
            '        print(f"({i},{j})", end=" ")\n'
            "    print()\n"
        ),
        dicas=[
            f"Quando `i = 1`, `j` percorre de `1` até `{col}` na mesma linha.",
            "O `print()` sem nada pertence ao laço externo (`i`), então ele pula uma linha ao terminar cada linha da grade.",
        ],
        explicacao=(
            f"O laço externo controla as `{lin}` linhas e o interno gera as `{col}` colunas de pares `(i,j)` em cada linha."
        ),
    )


@exercicio(estagio=9, dificuldade=5, tipo="codigo", conceitos=["for_range", "acumulador"])
def fibonacci_n_termos(r):
    casos = [r.randint(5, 9), r.randint(3, 6), 1, 2]
    n0 = casos[0]
    seq = []
    a, b = 0, 1
    for _ in range(n0):
        seq.append(str(a))
        a, b = b, a + b
    return dict(
        titulo="Sequência de Fibonacci com for",
        enunciado=(
            "Na sequência de Fibonacci, os dois primeiros termos são `0` e `1`, e cada termo seguinte é a soma dos dois anteriores "
            "(`0, 1, 1, 2, 3, 5, 8...`).\n\n"
            "Leia um inteiro `n >= 1` e imprima os `n` primeiros termos na mesma linha separados por espaço:\n"
            f"Exemplo para `n = {n0}`:\n```\n{' '.join(seq)}\n```"
        ),
        solucao=(
            'n = int(input("Termos: "))\n'
            "a = 0\n"
            "b = 1\n"
            "for i in range(n):\n"
            '    print(a, end=" ")\n'
            "    proximo = a + b\n"
            "    a = b\n"
            "    b = proximo\n"
        ),
        testes=[{"entrada": str(x)} for x in casos],
        testes_visiveis=1,
        dicas=[
            "Comece com `a = 0` e `b = 1`. A cada volta do `for`, imprima `a`!",
            "Para avançar: calcule `proximo = a + b`, depois passe `b` para `a` e `proximo` para `b`.",
        ],
        explicacao=(
            "Guardar `proximo = a + b` antes de atualizar `a = b` evita perder a soma antes da troca, "
            "e imprimir `a` em toda volta já cobre perfeitamente `n = 1` e `n = 2`."
        ),
    )


@exercicio(estagio=9, dificuldade=5, tipo="corrigir", conceitos=["for_range", "if_else", "depuracao"])
def corrigir_for_aninhado_soma_linha(r):
    lin = r.randint(2, 4)
    col = r.randint(3, 5)
    ex_linhas = "\n".join(f"Linha {i}: {sum(i * j for j in range(1, col + 1))}" for i in range(1, lin + 1))
    return dict(
        titulo="O total da linha não reinicia!",
        enunciado=(
            f"O código deveria calcular e mostrar a soma de `i * j` separadamente para cada linha `i` (de `1` a `{lin}`) "
            f"e coluna `j` (de `1` a `{col}`):\n```\n{ex_linhas}\n```\n"
            "Mas está acumulando as linhas anteriores junto! Corrija a posição da inicialização."
        ),
        codigo_inicial=(
            "soma = 0\n"
            f"for i in range(1, {lin + 1}):\n"
            f"    for j in range(1, {col + 1}):\n"
            "        soma += i * j\n"
            '    print(f"Linha {i}: {soma}")\n'
        ),
        solucao=(
            f"for i in range(1, {lin + 1}):\n"
            "    soma = 0\n"
            f"    for j in range(1, {col + 1}):\n"
            "        soma += i * j\n"
            '    print(f"Linha {i}: {soma}")\n'
        ),
        dicas=[
            "Se queremos a soma **de cada linha**, `soma` deve voltar para `0` sempre que uma nova linha `i` começar!",
            "Coloque `soma = 0` dentro do `for i`, logo antes do `for j`.",
        ],
        explicacao=(
            "Em laços aninhados, um acumulador que pertence a cada grupo (cada linha `i`) precisa ser reiniciado "
            "no começo do laço externo, nunca antes dele."
        ),
    )
