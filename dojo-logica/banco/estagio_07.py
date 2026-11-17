"""Estágio 7 - Vários caminhos: if/elif/else, faixas de valores e condições compostas."""

from .base import exercicio

NOMES = ["Ana", "Bruno", "Carla", "Diego", "Elisa", "Fábio", "Gabi", "Heitor", "Iara", "João"]


def _linhas(*valores):
    return "\n".join(str(v) for v in valores)


# ---------------------------------------------------------------------------
# codigo
# ---------------------------------------------------------------------------

@exercicio(estagio=7, dificuldade=1, tipo="codigo", conceitos=["elif", "input"])
def categoria_por_idade(r):
    esporte = r.choice(["natação", "judô", "xadrez", "atletismo", "vôlei", "skate"])
    testes = [
        {"entrada": str(r.randint(5, 9))},
        {"entrada": str(r.choice([10, 13]))},
        {"entrada": str(r.choice([14, 17]))},
        {"entrada": "18"},
        {"entrada": str(r.randint(19, 60))},
    ]
    r.shuffle(testes)
    exemplo = int(testes[0]["entrada"])
    if exemplo < 10:
        cat = "Mirim"
    elif exemplo < 14:
        cat = "Infantil"
    elif exemplo < 18:
        cat = "Juvenil"
    else:
        cat = "Adulto"
    return dict(
        titulo=f"Categorias do campeonato de {esporte}",
        enunciado=(
            f"No campeonato de {esporte}, cada atleta joga numa categoria de acordo com a idade:\n"
            "- menos de 10 anos: **Mirim**\n"
            "- de 10 a 13 anos: **Infantil**\n"
            "- de 14 a 17 anos: **Juvenil**\n"
            "- 18 anos ou mais: **Adulto**\n\n"
            "O programa lê a idade (um número inteiro) e mostra a categoria. "
            f"Por exemplo, se a idade digitada for {exemplo}, a saída deve ser:\n"
            f"```\nCategoria: {cat}\n```"
        ),
        solucao=(
            'idade = int(input("Idade: "))\n'
            "if idade < 10:\n"
            '    print("Categoria: Mirim")\n'
            "elif idade < 14:\n"
            '    print("Categoria: Infantil")\n'
            "elif idade < 18:\n"
            '    print("Categoria: Juvenil")\n'
            "else:\n"
            '    print("Categoria: Adulto")\n'
        ),
        testes=testes,
        testes_visiveis=2,
        dicas=[
            "Com `if`/`elif`/`else` o Python testa as condições de cima para baixo e executa **só o primeiro** bloco verdadeiro.",
            "Comece pela menor faixa: `if idade < 10:`. Se não for, a próxima pergunta só precisa ser `elif idade < 14:`.",
            "Estrutura: `if idade < 10:` ... `elif idade < 14:` ... `elif idade < 18:` ... `else:` ...",
        ],
        explicacao=(
            "Como o `elif` só é testado quando todas as condições acima foram falsas, ao chegar em "
            "`elif idade < 14` já sabemos que a idade é pelo menos 10. Por isso não precisamos escrever "
            "`idade >= 10 and idade < 14`: a ordem das condições faz parte do raciocínio. O `else` pega "
            "todo o resto (18 ou mais)."
        ),
    )


@exercicio(estagio=7, dificuldade=2, tipo="codigo", conceitos=["elif", "comparacao"])
def pix_com_regras(r):
    limite = r.choice([500, 800, 1000, 1500])
    saldo_alto = r.randint(limite + 200, limite + 3000)
    saldo_baixo = r.randint(50, limite - 100)
    testes = [
        {"entrada": _linhas(f"{saldo_baixo}.00", r.choice(["0", "-20"]))},
        {"entrada": _linhas(f"{saldo_baixo}.00", f"{saldo_baixo + r.randint(1, 80)}.50")},
        {"entrada": _linhas(f"{saldo_alto}.00", f"{limite + r.randint(1, 150)}.00")},
        {"entrada": _linhas(f"{saldo_alto}.00", f"{r.randint(10, limite - 1)}.{r.randint(10, 99)}")},
        {"entrada": _linhas(f"{saldo_alto}.00", f"{limite}.00")},
    ]
    return dict(
        titulo="Enviando um Pix à noite",
        enunciado=(
            "Um banco aplica estas regras para um Pix feito à noite. O programa lê o **saldo** e o "
            "**valor do Pix** (dois números reais, um por linha) e mostra **uma** mensagem, "
            "verificando as regras **nesta ordem**:\n"
            "1. valor menor ou igual a zero: `Valor inválido`\n"
            "2. valor maior que o saldo: `Saldo insuficiente`\n"
            f"3. valor maior que o limite noturno de R$ {limite}: `Acima do limite noturno`\n"
            "4. caso contrário: o Pix é enviado.\n\n"
            "Exemplo com saldo `2000.00` e valor `150.25`:\n"
            "```\nPix de R$ 150.25 enviado! Saldo restante: R$ 1849.75\n```"
        ),
        solucao=(
            'saldo = float(input("Saldo: "))\n'
            'valor = float(input("Valor do Pix: "))\n'
            "if valor <= 0:\n"
            '    print("Valor inválido")\n'
            "elif valor > saldo:\n"
            '    print("Saldo insuficiente")\n'
            f"elif valor > {limite}:\n"
            '    print("Acima do limite noturno")\n'
            "else:\n"
            '    print(f"Pix de R$ {valor:.2f} enviado! Saldo restante: R$ {saldo - valor:.2f}")\n'
        ),
        testes=testes,
        testes_visiveis=2,
        dicas=[
            "Cada regra vira uma condição; use `if` para a primeira e `elif` para as seguintes.",
            "Siga exatamente a ordem pedida: o primeiro teste verdadeiro decide a mensagem.",
            f"Estrutura: `if valor <= 0:` ... `elif valor > saldo:` ... `elif valor > {limite}:` ... `else:` ...",
        ],
        explicacao=(
            "A cadeia `if/elif/else` garante que só uma mensagem seja mostrada. A ordem importa: se um valor "
            "negativo chegasse no `else`, o banco 'enviaria' um Pix negativo. Repare que o limite usa `>` "
            f"e não `>=`: um Pix de exatamente R$ {limite} ainda é permitido."
        ),
    )


@exercicio(estagio=7, dificuldade=3, tipo="codigo", conceitos=["elif", "aritmeticos", "fstring"])
def classificar_imc(r):
    def caso():
        altura = r.randint(150, 195) / 100
        alvo = r.choice([r.randint(15, 17), r.randint(20, 23), r.randint(26, 28), r.randint(32, 38)])
        peso = round(alvo * altura ** 2, 1)
        return {"entrada": _linhas(peso, f"{altura:.2f}")}

    faixas = [r.randint(15, 17), r.randint(20, 23), r.randint(26, 28), r.randint(32, 38)]
    testes = []
    for alvo in faixas:
        altura = r.randint(150, 195) / 100
        testes.append({"entrada": _linhas(round(alvo * altura ** 2, 1), f"{altura:.2f}")})
    testes.append(caso())
    r.shuffle(testes)
    return dict(
        titulo="Calculadora de IMC da academia",
        enunciado=(
            "A academia quer uma calculadora de IMC. O programa lê o **peso** (kg) e a **altura** (m), "
            "dois números reais, um por linha, calcula `imc = peso / altura²` e mostra o IMC com **1 casa "
            "decimal** e a classificação:\n"
            "- menor que 18.5: `Abaixo do peso`\n"
            "- de 18.5 até menos de 25: `Peso normal`\n"
            "- de 25 até menos de 30: `Sobrepeso`\n"
            "- 30 ou mais: `Obesidade`\n\n"
            "Exemplo com peso `70` e altura `1.75`:\n"
            "```\nIMC: 22.9\nPeso normal\n```"
        ),
        solucao=(
            'peso = float(input("Peso (kg): "))\n'
            'altura = float(input("Altura (m): "))\n'
            "imc = peso / altura ** 2\n"
            'print(f"IMC: {imc:.1f}")\n'
            "if imc < 18.5:\n"
            '    print("Abaixo do peso")\n'
            "elif imc < 25:\n"
            '    print("Peso normal")\n'
            "elif imc < 30:\n"
            '    print("Sobrepeso")\n'
            "else:\n"
            '    print("Obesidade")\n'
        ),
        testes=testes,
        testes_visiveis=2,
        dicas=[
            "Primeiro calcule o IMC numa variável; `altura ** 2` eleva a altura ao quadrado.",
            "Para mostrar 1 casa decimal use `f\"IMC: {imc:.1f}\"`. Depois classifique com `if/elif/else`.",
            "Estrutura: `if imc < 18.5:` ... `elif imc < 25:` ... `elif imc < 30:` ... `else:` ...",
        ],
        explicacao=(
            "Guardar o resultado em `imc` evita repetir a conta em cada condição. Como as faixas estão em "
            "ordem crescente, cada `elif` só precisa do limite superior: se o programa chegou em "
            "`elif imc < 25`, é porque o IMC já não é menor que 18.5. Cuidado com a precedência: "
            "`peso / altura ** 2` faz a potência antes da divisão, que é o que queremos."
        ),
    )


@exercicio(estagio=7, dificuldade=3, tipo="codigo", conceitos=["elif", "logicos", "comparacao"])
def maior_de_tres(r):
    jogo = r.choice(["boliche", "dardos", "minigolfe", "fliperama", "quiz"])
    def trio():
        return [r.randint(0, 300) for _ in range(3)]
    t1 = trio()
    t2 = trio()
    x = r.randint(50, 200)
    t3 = r.choice([[x, x, x], [x, x, x - 10], [x - 10, x, x], [x, x - 10, x]])
    t4 = sorted(trio())  # maior no fim
    t5 = sorted(trio(), reverse=True)  # maior no começo
    testes = [{"entrada": _linhas(*t)} for t in (t1, t2, t3, t4, t5)]
    a, b, c = t1
    maior = a if a >= b and a >= c else (b if b >= c else c)
    return dict(
        titulo=f"Recorde da rodada de {jogo}",
        enunciado=(
            f"Três amigos jogaram uma rodada de {jogo}. O programa lê as três pontuações (números inteiros, "
            "uma por linha) e mostra a maior delas.\n\n"
            "**Não use** a função `max()`: resolva com `if/elif/else` e operadores lógicos.\n\n"
            f"Exemplo com as pontuações `{a}`, `{b}` e `{c}`:\n"
            f"```\nMaior pontuação: {maior}\n```"
        ),
        solucao=(
            'a = int(input("Pontuação 1: "))\n'
            'b = int(input("Pontuação 2: "))\n'
            'c = int(input("Pontuação 3: "))\n'
            "if a >= b and a >= c:\n"
            "    maior = a\n"
            "elif b >= c:\n"
            "    maior = b\n"
            "else:\n"
            "    maior = c\n"
            'print("Maior pontuação:", maior)\n'
        ),
        testes=testes,
        testes_visiveis=2,
        dicas=[
            "`a` é a maior quando é maior ou igual a `b` **e** maior ou igual a `c`.",
            "Se `a` não é a maior, a disputa fica só entre `b` e `c`: basta uma comparação no `elif`.",
            "Estrutura: `if a >= b and a >= c:` ... `elif b >= c:` ... `else:` ... e guarde o resultado em `maior`.",
        ],
        explicacao=(
            "A primeira condição verifica se `a` vence os outros dois ao mesmo tempo (por isso o `and`). "
            "Se não vence, a maior está entre `b` e `c`, e uma única comparação resolve. Usar `>=` em vez "
            "de `>` é importante nos empates: com `>`, três pontuações iguais cairiam em casos inesperados."
        ),
    )


@exercicio(estagio=7, dificuldade=4, tipo="codigo", conceitos=["elif", "logicos", "if_else"])
def tipo_de_triangulo(r):
    lado = r.randint(3, 20)
    eq = [lado, lado, lado]
    base = r.randint(3, 15)
    perna = r.randint(base // 2 + 1, 20)
    if perna == base:
        perna += 1
    iso = r.choice([[perna, perna, base], [base, perna, perna], [perna, base, perna]])
    a = r.randint(3, 10)
    b = a + r.randint(1, 5)
    c = b + r.randint(1, a - 1)
    esc = [a, b, c]
    r.shuffle(esc)
    x = r.randint(2, 8)
    y = r.randint(2, 8)
    inv = r.choice([[x, y, x + y], [x + y + r.randint(1, 5), x, y]])
    r.shuffle(inv)
    testes = [{"entrada": _linhas(*t)} for t in (esc, eq, iso, inv)]
    r.shuffle(testes)
    return dict(
        titulo="Que triângulo é esse?",
        enunciado=(
            "O programa lê três lados (números inteiros, um por linha) e mostra:\n"
            "- `Não forma triângulo` se algum lado for **maior ou igual** à soma dos outros dois;\n"
            "- senão, `Equilátero` (três lados iguais), `Isósceles` (exatamente dois iguais) "
            "ou `Escaleno` (todos diferentes).\n\n"
            "Exemplos:\n"
            "```\nlados 5, 5, 5  ->  Equilátero\nlados 4, 4, 6  ->  Isósceles\n"
            "lados 3, 4, 5  ->  Escaleno\nlados 1, 2, 3  ->  Não forma triângulo\n```\n"
            "A saída é só a palavra (ex.: `Escaleno`)."
        ),
        solucao=(
            'a = int(input("Lado a: "))\n'
            'b = int(input("Lado b: "))\n'
            'c = int(input("Lado c: "))\n'
            "if a < b + c and b < a + c and c < a + b:\n"
            "    if a == b and b == c:\n"
            '        print("Equilátero")\n'
            "    elif a == b or b == c or a == c:\n"
            '        print("Isósceles")\n'
            "    else:\n"
            '        print("Escaleno")\n'
            "else:\n"
            '    print("Não forma triângulo")\n'
        ),
        testes=testes,
        testes_visiveis=2,
        dicas=[
            "Primeiro descubra se os lados formam um triângulo; só depois faz sentido classificar.",
            "Um triângulo existe quando **cada** lado é menor que a soma dos outros dois (use `and`). Dentro desse `if`, coloque outro `if/elif/else`.",
            "Ordem dentro do if: teste primeiro `a == b and b == c` (equilátero); depois `a == b or b == c or a == c` (isósceles); senão é escaleno.",
        ],
        explicacao=(
            "O `if` externo garante que só classificamos lados válidos — esse é o papel do if aninhado. "
            "Dentro dele, a ordem importa: um triângulo equilátero também tem 'dois lados iguais', então se "
            "testássemos isósceles primeiro, ele nunca seria reconhecido como equilátero. Um erro comum é "
            "esquecer o caso de igualdade (1, 2, 3): os lados ficam 'deitados' e não formam triângulo."
        ),
    )


@exercicio(estagio=7, dificuldade=4, tipo="codigo", conceitos=["elif", "if_else", "input", "fstring"])
def calculadora_com_operador(r):
    def n():
        return r.randint(1, 60)
    testes = [
        {"entrada": _linhas(n(), "+", n())},
        {"entrada": _linhas(n(), "-", n())},
        {"entrada": _linhas(n(), "*", n())},
        {"entrada": _linhas(n(), "/", r.randint(1, 9))},
        {"entrada": _linhas(n(), "/", 0)},
        {"entrada": _linhas(n(), r.choice(["%", "x", "^", ":"]), n())},
    ]
    r.shuffle(testes)
    return dict(
        titulo="Calculadora de bolso",
        enunciado=(
            "Faça uma calculadora. O programa lê, um por linha: o primeiro número (real), o **operador** "
            "como texto (`+`, `-`, `*` ou `/`) e o segundo número (real).\n\n"
            "Mostre `Resultado: ` seguido da conta com **2 casas decimais**. Casos especiais:\n"
            "- divisão por zero: `Erro: divisão por zero`\n"
            "- operador diferente dos quatro: `Operador inválido`\n\n"
            "Exemplos:\n"
            "```\n7, *, 3   ->  Resultado: 21.00\n10, /, 4  ->  Resultado: 2.50\n"
            "5, /, 0   ->  Erro: divisão por zero\n5, ?, 2   ->  Operador inválido\n```"
        ),
        solucao=(
            'a = float(input("Primeiro número: "))\n'
            'operador = input("Operador: ")\n'
            'b = float(input("Segundo número: "))\n'
            'if operador == "+":\n'
            '    print(f"Resultado: {a + b:.2f}")\n'
            'elif operador == "-":\n'
            '    print(f"Resultado: {a - b:.2f}")\n'
            'elif operador == "*":\n'
            '    print(f"Resultado: {a * b:.2f}")\n'
            'elif operador == "/":\n'
            "    if b == 0:\n"
            '        print("Erro: divisão por zero")\n'
            "    else:\n"
            '        print(f"Resultado: {a / b:.2f}")\n'
            "else:\n"
            '    print("Operador inválido")\n'
        ),
        testes=testes,
        testes_visiveis=2,
        dicas=[
            "O operador é lido como texto, então compare com strings: `operador == \"+\"`.",
            "Faça uma cadeia `if/elif` com um ramo para cada operador e um `else` final para operadores inválidos.",
            "No ramo da divisão, coloque um `if b == 0:` aninhado antes de dividir.",
        ],
        explicacao=(
            "Cada `elif` compara o texto digitado com um operador; o `else` final captura qualquer coisa "
            "diferente. A verificação de divisão por zero fica **dentro** do ramo `/`, porque só faz sentido "
            "se a operação for divisão — isso é um if aninhado. Sem ela, o programa quebraria com "
            "`ZeroDivisionError`."
        ),
    )


@exercicio(estagio=7, dificuldade=5, tipo="codigo", conceitos=["elif", "aritmeticos", "fstring"])
def imposto_progressivo(r):
    l1 = r.choice([2000, 2500, 3000])
    l2 = l1 + r.choice([1500, 2000, 2500])
    p1 = r.choice([10, 15])
    p2 = p1 + r.choice([10, 12])
    testes = [
        {"entrada": str(r.randint(800, l1 - 1))},
        {"entrada": str(l1)},
        {"entrada": str(r.randint(l1 + 1, l2 - 1))},
        {"entrada": str(l2)},
        {"entrada": str(r.randint(l2 + 1, l2 + 6000))},
    ]
    r.shuffle(testes)
    ex = l2 + 1000
    imp_ex = (l2 - l1) * p1 / 100 + 1000 * p2 / 100
    return dict(
        titulo="Imposto por faixas",
        enunciado=(
            "Em um país fictício, o imposto é **progressivo**: cada pedaço do salário paga a taxa da sua faixa.\n"
            f"- até R$ {l1}: isento;\n"
            f"- a parte entre R$ {l1} e R$ {l2}: paga {p1}%;\n"
            f"- a parte acima de R$ {l2}: paga {p2}%.\n\n"
            "O programa lê o salário (número real) e mostra o imposto com 2 casas decimais.\n\n"
            f"Exemplo: salário `{ex}` paga {p1}% sobre {l2 - l1} e {p2}% sobre 1000:\n"
            f"```\nImposto: R$ {imp_ex:.2f}\n```"
        ),
        solucao=(
            'salario = float(input("Salário: "))\n'
            f"if salario <= {l1}:\n"
            "    imposto = 0\n"
            f"elif salario <= {l2}:\n"
            f"    imposto = (salario - {l1}) * {p1} / 100\n"
            "else:\n"
            f"    imposto = ({l2} - {l1}) * {p1} / 100 + (salario - {l2}) * {p2} / 100\n"
            'print(f"Imposto: R$ {imposto:.2f}")\n'
        ),
        testes=testes,
        testes_visiveis=2,
        dicas=[
            "Separe em três casos com `if/elif/else`, um por faixa, e calcule o imposto numa variável.",
            f"Na faixa do meio, só a parte que passa de {l1} é tributada: `salario - {l1}`.",
            f"Na última faixa, some o imposto completo da faixa do meio (`({l2} - {l1}) * {p1} / 100`) "
            f"com {p2}% do que passa de {l2}.",
        ],
        explicacao=(
            "No imposto progressivo, quem ganha mais não paga a taxa maior sobre **tudo**, só sobre o pedaço "
            "acima do limite. Por isso, na faixa mais alta, somamos o valor fixo da faixa do meio inteira com a "
            "taxa maior aplicada apenas ao excedente. Usar `<=` nos limites garante que um salário exatamente "
            f"igual a {l1} fique isento."
        ),
    )


# ---------------------------------------------------------------------------
# prever
# ---------------------------------------------------------------------------

@exercicio(estagio=7, dificuldade=2, tipo="prever", conceitos=["elif", "teste_de_mesa"])
def prever_primeiro_verdadeiro(r):
    temp = r.randint(5, 38)
    return dict(
        titulo="Só um caminho é escolhido",
        enunciado=(
            "Faça o teste de mesa e escreva exatamente o que o programa mostra. "
            "Lembre: numa cadeia `if/elif/else`, só **um** bloco é executado."
        ),
        solucao=(
            f"temperatura = {temp}\n"
            "if temperatura >= 10:\n"
            '    print("Leve um casaco leve")\n'
            "elif temperatura >= 20:\n"
            '    print("Camiseta resolve")\n'
            "elif temperatura >= 30:\n"
            '    print("Calor! Beba água")\n'
            "else:\n"
            '    print("Frio! Leve um agasalho")\n'
            'print("Bom passeio")\n'
        ),
        dicas=[
            "O Python testa as condições de cima para baixo e para no **primeiro** verdadeiro.",
            f"Pergunte: {temp} >= 10? Se sim, os `elif` de baixo nem são olhados.",
        ],
        explicacao=(
            f"Com temperatura {temp}, a primeira condição verdadeira decide tudo. Repare que esse código tem um "
            "problema de lógica: qualquer valor 10 ou maior cai no primeiro bloco, então os ramos de 20 e 30 "
            "nunca executam. A última linha, fora do if, sempre roda."
        ),
    )


@exercicio(estagio=7, dificuldade=3, tipo="prever", conceitos=["elif", "logicos", "teste_de_mesa"])
def prever_entrada_no_show(r):
    idade = r.choice([r.randint(12, 17), r.randint(18, 40)])
    ingresso = r.choice([True, False])
    acompanhado = r.choice([True, False])
    return dict(
        titulo="Pode entrar no show?",
        enunciado="Faça o teste de mesa e escreva exatamente o que o programa abaixo mostra.",
        solucao=(
            f"idade = {idade}\n"
            f"tem_ingresso = {ingresso}\n"
            f"acompanhado = {acompanhado}\n"
            "if idade >= 18 or acompanhado:\n"
            "    if tem_ingresso:\n"
            '        print("Pode entrar")\n'
            "    else:\n"
            '        print("Compre o ingresso")\n'
            "elif tem_ingresso:\n"
            '    print("Precisa de um acompanhante")\n'
            "else:\n"
            '    print("Não pode entrar")\n'
            "if not tem_ingresso and idade < 18:\n"
            '    print("Fale com o responsável")\n'
        ),
        dicas=[
            "Calcule primeiro `idade >= 18 or acompanhado`: basta uma das partes ser True.",
            "Se o if externo for verdadeiro, só o if de dentro decide; o `elif` e o `else` externos são pulados. O último `if` é independente e sempre é testado.",
        ],
        explicacao=(
            f"`idade >= 18` é {idade >= 18} e `acompanhado` é {acompanhado}, então a condição externa vale "
            f"{idade >= 18 or acompanhado}. A partir daí, `tem_ingresso` ({ingresso}) escolhe a mensagem. O último "
            "`if` está fora da cadeia, por isso é avaliado de qualquer jeito: `not tem_ingresso and idade < 18` "
            f"vale {(not ingresso) and idade < 18}."
        ),
    )


@exercicio(estagio=7, dificuldade=4, tipo="prever", conceitos=["elif", "if_else", "teste_de_mesa"])
def prever_ifs_separados(r):
    v = r.randint(6, 20)
    lim = r.choice([4, 5, 6])
    return dict(
        titulo="if separado ou elif?",
        enunciado=(
            "Os dois trechos parecem iguais, mas um usa `if` separados e o outro usa `elif`. "
            "Faça o teste de mesa com atenção e escreva exatamente o que é mostrado."
        ),
        solucao=(
            f"x = {v}\n"
            "if x > 10:\n"
            "    x = x - 4\n"
            f"if x > {lim}:\n"
            "    x = x * 2\n"
            "print(x)\n"
            f"y = {v}\n"
            "if y > 10:\n"
            "    y = y - 4\n"
            f"elif y > {lim}:\n"
            "    y = y * 2\n"
            "print(y)\n"
        ),
        dicas=[
            "Dois `if` seguidos são independentes: o segundo é testado sempre, já com o valor atualizado.",
            "Com `elif`, se o primeiro bloco executar, o segundo é pulado.",
        ],
        explicacao=(
            f"No primeiro trecho, x começa com {v}; o segundo `if` é testado com o valor que x tiver **depois** "
            "do primeiro bloco, então os dois podem executar. No segundo trecho, o `elif` só é olhado se "
            "`y > 10` for falso, então no máximo uma das contas acontece. Trocar `if` por `elif` (ou o "
            "contrário) muda o resultado!"
        ),
    )


# ---------------------------------------------------------------------------
# corrigir
# ---------------------------------------------------------------------------

@exercicio(estagio=7, dificuldade=2, tipo="corrigir", conceitos=["elif", "comparacao", "depuracao"])
def corrigir_conta_de_luz(r):
    f1 = r.choice([100, 120, 150])
    f2 = f1 + r.choice([100, 150])
    t1, t2, t3 = r.choice([(0.50, 0.70, 0.90), (0.60, 0.80, 1.10), (0.55, 0.75, 0.95)])
    testes = [
        {"entrada": str(r.randint(30, f1 - 1))},
        {"entrada": str(f1)},
        {"entrada": str(r.randint(f1 + 1, f2 - 1))},
        {"entrada": str(f2)},
        {"entrada": str(r.randint(f2 + 1, f2 + 300))},
    ]

    def cod(op):
        return (
            'consumo = int(input("Consumo (kWh): "))\n'
            f"if consumo {op} {f1}:\n"
            f"    tarifa = {t1:.2f}\n"
            f"elif consumo {op} {f2}:\n"
            f"    tarifa = {t2:.2f}\n"
            "else:\n"
            f"    tarifa = {t3:.2f}\n"
            'print(f"Total: R$ {consumo * tarifa:.2f}")\n'
        )

    return dict(
        titulo="A conta de luz que cobra errado",
        enunciado=(
            "A companhia de energia cobra o kWh conforme a faixa de consumo:\n"
            f"- **até {f1} kWh (inclusive)**: R$ {t1:.2f} por kWh\n"
            f"- **até {f2} kWh (inclusive)**: R$ {t2:.2f} por kWh\n"
            f"- acima de {f2} kWh: R$ {t3:.2f} por kWh\n\n"
            "O programa lê o consumo (inteiro) e mostra o total, mas alguns clientes estão reclamando que "
            f"pagaram caro demais. Exemplo: consumo de {f1} kWh deveria mostrar:\n"
            f"```\nTotal: R$ {f1 * t1:.2f}\n```\nEncontre e corrija o bug."
        ),
        codigo_inicial=cod("<"),
        solucao=cod("<="),
        testes=testes,
        testes_visiveis=1,
        dicas=[
            f"Teste mentalmente com consumo exatamente igual a {f1}. Em qual faixa ele cai?",
            "'Até X inclusive' significa que X também entra na faixa. Qual operador inclui o próprio valor?",
        ],
        explicacao=(
            f"Com `<`, um consumo de exatamente {f1} kWh dava False na primeira condição e ia para a faixa "
            "mais cara. Erros de **fronteira** como esse são muito comuns: sempre teste o valor exato do "
            "limite. Trocar `<` por `<=` inclui o limite na faixa certa."
        ),
    )


@exercicio(estagio=7, dificuldade=3, tipo="corrigir", conceitos=["elif", "comparacao", "depuracao"])
def corrigir_ordem_das_notas(r):
    aprov = r.choice([6, 7])
    rec = r.choice([4, 5])
    exc = r.choice([9, 9.5])
    testes = [
        {"entrada": str(r.choice([10, exc]))},
        {"entrada": str(aprov)},
        {"entrada": f"{r.randint(aprov, 8)}.{r.randint(1, 4)}"},
        {"entrada": str(rec)},
        {"entrada": f"{r.randint(0, rec - 1)}.{r.randint(0, 9)}"},
    ]
    r.shuffle(testes)

    def cod(ordem):
        partes = {
            "exc": (f"nota >= {exc}", "Excelente"),
            "aprov": (f"nota >= {aprov}", "Aprovado"),
            "rec": (f"nota >= {rec}", "Recuperação"),
        }
        linhas = 'nota = float(input("Nota: "))\n'
        for i, chave in enumerate(ordem):
            cond, msg = partes[chave]
            linhas += ("if " if i == 0 else "elif ") + cond + ":\n"
            linhas += f'    print("{msg}")\n'
        linhas += 'else:\n    print("Reprovado")\n'
        return linhas

    return dict(
        titulo="Ninguém é aprovado!",
        enunciado=(
            "O boletim deveria classificar a nota (número real) assim:\n"
            f"- {exc} ou mais: `Excelente`\n"
            f"- de {aprov} até menos de {exc}: `Aprovado`\n"
            f"- de {rec} até menos de {aprov}: `Recuperação`\n"
            f"- menos de {rec}: `Reprovado`\n\n"
            "Mas todos os alunos com nota boa estão aparecendo em recuperação. "
            "O programa roda sem erro — o problema é de lógica. Corrija-o."
        ),
        codigo_inicial=cod(["rec", "aprov", "exc"]),
        solucao=cod(["exc", "aprov", "rec"]),
        testes=testes,
        testes_visiveis=1,
        dicas=[
            "Faça o teste de mesa com nota 10: qual é a primeira condição verdadeira?",
            "Na cadeia `if/elif`, só o primeiro bloco verdadeiro roda. Condições mais 'largas' engolem as mais 'estreitas' que vêm depois.",
            f"Reordene: comece pela condição mais exigente (`nota >= {exc}`) e vá descendo.",
        ],
        explicacao=(
            f"Uma nota 10 também é `>= {rec}`, então a primeira condição já era verdadeira e o programa "
            "mostrava 'Recuperação' sem nem olhar as outras. Quando as faixas usam `>=`, a ordem certa é da "
            "maior para a menor: assim cada `elif` só é testado para as notas que não couberam acima."
        ),
    )


@exercicio(estagio=7, dificuldade=3, tipo="corrigir", conceitos=["elif", "logicos", "depuracao"])
def corrigir_frete_gratis(r):
    minimo = r.choice([99, 120, 150, 200])
    dist = r.choice([10, 15, 20, 30])
    frete = r.choice([12.90, 15.50, 19.90])
    loja = r.choice(["livraria", "pet shop", "loja de games", "farmácia", "hortifrúti"])
    testes = [
        {"entrada": _linhas(f"{minimo + r.randint(0, 80)}.00", r.randint(1, dist))},
        {"entrada": _linhas(f"{minimo + r.randint(1, 80)}.90", r.randint(dist + 1, dist + 40))},
        {"entrada": _linhas(f"{r.randint(20, minimo - 1)}.50", r.randint(1, dist))},
        {"entrada": _linhas(f"{r.randint(20, minimo - 1)}.00", r.randint(dist + 1, dist + 40))},
    ]
    r.shuffle(testes)

    def cod(op):
        return (
            'valor = float(input("Valor da compra: "))\n'
            'distancia = int(input("Distância (km): "))\n'
            f"if valor >= {minimo} {op} distancia <= {dist}:\n"
            '    print("Frete grátis!")\n'
            "else:\n"
            f'    print("Frete: R$ {frete:.2f}")\n'
        )

    return dict(
        titulo=f"Frete grátis da {loja}",
        enunciado=(
            f"A {loja} dá frete grátis **somente** quando as duas regras valem ao mesmo tempo: compra de "
            f"pelo menos R$ {minimo} **e** entrega a até {dist} km. Nos outros casos, o frete custa "
            f"R$ {frete:.2f}.\n\n"
            "O programa lê o valor da compra (real) e a distância (inteiro), mas a loja está dando frete grátis "
            "para gente demais. Corrija o bug.\n\n"
            "Saídas possíveis:\n"
            f"```\nFrete grátis!\nFrete: R$ {frete:.2f}\n```"
        ),
        codigo_inicial=cod("or"),
        solucao=cod("and"),
        testes=testes,
        testes_visiveis=1,
        dicas=[
            f"Teste com uma compra de R$ {minimo + 50} entregue a {dist + 20} km. Deveria ter frete grátis?",
            "`or` dá True se **pelo menos uma** parte for verdadeira; `and` exige que **as duas** sejam.",
        ],
        explicacao=(
            "Com `or`, bastava cumprir uma das regras para ganhar o frete. A frase 'as duas regras ao mesmo "
            "tempo' é a dica de que precisamos de `and`. Para conferir uma condição composta, teste as quatro "
            "combinações: as duas verdadeiras, só a primeira, só a segunda e nenhuma."
        ),
    )


# ---------------------------------------------------------------------------
# completar
# ---------------------------------------------------------------------------

@exercicio(estagio=7, dificuldade=3, tipo="completar", conceitos=["elif", "logicos", "aritmeticos"])
def completar_ano_bissexto(r):
    comuns = r.choice([1900, 1800, 2100, 2200])
    secular = r.choice([2000, 1600, 2400])
    quatro = r.choice([1996, 2004, 2012, 2020, 2024, 1988])
    nao = r.choice([2023, 2019, 2001, 1999, 2025, 2026])
    testes = [{"entrada": str(a)} for a in (quatro, nao, comuns, secular)]
    r.shuffle(testes)
    return dict(
        titulo="O ano é bissexto?",
        enunciado=(
            "Um ano é bissexto quando é divisível por 4 **e não** é divisível por 100 — **ou** quando é "
            "divisível por 400. Por isso 2024 e 2000 são bissextos, mas "
            f"{comuns} não é.\n\n"
            "Complete as lacunas `___`. Exemplos de saída:\n"
            f"```\n{quatro} é bissexto\n{comuns} não é bissexto\n```"
        ),
        codigo_inicial=(
            'ano = int(input("Ano: "))\n'
            "if (ano % ___ == 0 and ano % ___ != 0) ___ ano % ___ == 0:\n"
            '    print(ano, "é bissexto")\n'
            "else:\n"
            '    print(ano, "não é bissexto")\n'
        ),
        solucao=(
            'ano = int(input("Ano: "))\n'
            "if (ano % 4 == 0 and ano % 100 != 0) or ano % 400 == 0:\n"
            '    print(ano, "é bissexto")\n'
            "else:\n"
            '    print(ano, "não é bissexto")\n'
        ),
        testes=testes,
        testes_visiveis=2,
        dicas=[
            "`ano % 4 == 0` significa 'o resto da divisão por 4 é zero', ou seja, é divisível por 4.",
            "A frase tem duas partes ligadas por **ou**: (por 4 e não por 100) **ou** (por 400).",
            "Os números das lacunas são 4, 100 e 400, e o operador entre as duas partes é `or`.",
        ],
        explicacao=(
            "O parêntese agrupa a primeira regra (divisível por 4 e não por 100), e o `or` permite a exceção "
            f"dos anos divisíveis por 400. Assim {comuns} é barrado pela regra do 100, mas {secular} é salvo "
            "pela regra do 400. Teste sempre os quatro tipos de ano: comum, múltiplo de 4, múltiplo de 100 "
            "e múltiplo de 400."
        ),
    )


@exercicio(estagio=7, dificuldade=3, tipo="completar", conceitos=["elif", "aritmeticos"])
def completar_multa_velocidade(r):
    limite = r.choice([40, 50, 60, 80, 100])
    testes = [
        {"entrada": str(r.randint(limite - 20, limite))},
        {"entrada": str(limite + limite // 5)},
        {"entrada": str(limite + r.randint(1, limite // 5))},
        {"entrada": str(limite + limite // 2)},
        {"entrada": str(limite + r.randint(limite // 5 + 1, limite // 2))},
        {"entrada": str(limite + r.randint(limite // 2 + 1, limite))},
    ]
    r.shuffle(testes)
    return dict(
        titulo="Radar da avenida",
        enunciado=(
            f"Um radar numa via com limite de {limite} km/h lê a velocidade medida (inteiro) e calcula "
            "o excesso em porcentagem. A classificação é:\n"
            "- até o limite: `Dentro do limite`\n"
            "- até 20% acima: `Infração média`\n"
            "- mais de 20% e até 50% acima: `Infração grave`\n"
            "- mais de 50% acima: `Infração gravíssima`\n\n"
            "Complete as lacunas `___`."
        ),
        codigo_inicial=(
            f"limite = {limite}\n"
            'velocidade = int(input("Velocidade medida: "))\n'
            "excesso = (velocidade - limite) * 100 / limite\n"
            "if velocidade <= limite:\n"
            '    print("Dentro do limite")\n'
            "elif excesso <= ___:\n"
            '    print("Infração média")\n'
            "___ excesso <= ___:\n"
            '    print("Infração grave")\n'
            "___\n"
            '    print("Infração gravíssima")\n'
        ),
        solucao=(
            f"limite = {limite}\n"
            'velocidade = int(input("Velocidade medida: "))\n'
            "excesso = (velocidade - limite) * 100 / limite\n"
            "if velocidade <= limite:\n"
            '    print("Dentro do limite")\n'
            "elif excesso <= 20:\n"
            '    print("Infração média")\n'
            "elif excesso <= 50:\n"
            '    print("Infração grave")\n'
            "else:\n"
            '    print("Infração gravíssima")\n'
        ),
        testes=testes,
        testes_visiveis=2,
        dicas=[
            "`excesso` já está em porcentagem: 20% acima vira o número 20.",
            "Como o `elif` só roda se as condições de cima falharam, não é preciso escrever `excesso > 20` na faixa grave.",
            "As lacunas são: `20`, `elif`, `50` e `else:`.",
        ],
        explicacao=(
            f"O cálculo `(velocidade - limite) * 100 / limite` transforma o excesso em porcentagem; por exemplo, "
            f"{limite + limite // 5} km/h dá exatamente 20%. As faixas vão da menor para a maior com `<=`, então "
            "cada `elif` herda a informação de que as condições anteriores falharam. O `else` cobre tudo acima "
            "de 50%."
        ),
    )


@exercicio(estagio=7, dificuldade=4, tipo="completar", conceitos=["elif", "logicos"])
def completar_jokenpo(r):
    n1, n2 = r.sample(NOMES, 2)
    jogadas = ["pedra", "papel", "tesoura"]
    testes = [{"entrada": _linhas(j, j)} for j in [r.choice(jogadas)]]
    pares = [("pedra", "tesoura"), ("tesoura", "papel"), ("papel", "pedra"),
             ("tesoura", "pedra"), ("papel", "tesoura"), ("pedra", "papel")]
    escolhidos = r.sample(pares[:3], 2) + r.sample(pares[3:], 2)
    testes += [{"entrada": _linhas(a, b)} for a, b in escolhidos]
    r.shuffle(testes)
    return dict(
        titulo=f"Jokenpô: {n1} contra {n2}",
        enunciado=(
            f"{n1} e {n2} vão jogar pedra, papel e tesoura. O programa lê a jogada de {n1} e depois a de "
            f"{n2} (textos em minúsculas, um por linha). Regras: pedra quebra tesoura, tesoura corta papel e "
            "papel embrulha pedra.\n\n"
            "Complete as lacunas `___`. Saídas possíveis:\n"
            f"```\nEmpate!\n{n1} venceu!\n{n2} venceu!\n```"
        ),
        codigo_inicial=(
            f'jogada1 = input("{n1}: ")\n'
            f'jogada2 = input("{n2}: ")\n'
            "if jogada1 == ___:\n"
            '    print("Empate!")\n'
            'elif (jogada1 == "pedra" and jogada2 == "tesoura") or \\\n'
            '        (jogada1 == "tesoura" and jogada2 == ___) or \\\n'
            '        (jogada1 == ___ and jogada2 == ___):\n'
            f'    print("{n1} venceu!")\n'
            "___\n"
            f'    print("{n2} venceu!")\n'
        ),
        solucao=(
            f'jogada1 = input("{n1}: ")\n'
            f'jogada2 = input("{n2}: ")\n'
            "if jogada1 == jogada2:\n"
            '    print("Empate!")\n'
            'elif (jogada1 == "pedra" and jogada2 == "tesoura") or \\\n'
            '        (jogada1 == "tesoura" and jogada2 == "papel") or \\\n'
            '        (jogada1 == "papel" and jogada2 == "pedra"):\n'
            f'    print("{n1} venceu!")\n'
            "else:\n"
            f'    print("{n2} venceu!")\n'
        ),
        testes=testes,
        testes_visiveis=2,
        dicas=[
            "Empate acontece quando as duas jogadas são iguais — compare uma variável com a outra.",
            f"O `elif` lista as três maneiras de {n1} ganhar, cada uma entre parênteses com `and`, ligadas por `or`. A barra `\\` no fim da linha só continua a condição na linha de baixo.",
            f"Se não foi empate e {n1} não ganhou, só sobra uma possibilidade: use `else:`.",
        ],
        explicacao=(
            "Cada vitória é uma combinação de duas condições que precisam valer juntas (`and`), e basta uma das "
            "três combinações acontecer (`or`). Testar o empate primeiro simplifica o resto: depois dele, se "
            f"{n1} não venceu, com certeza {n2} venceu, e o `else` resolve sem listar mais três casos."
        ),
    )
