"""Estágio 4 - Operadores aritméticos (+, -, *, /, //, %, **) e precedência."""

from .base import exercicio


@exercicio(estagio=4, dificuldade=1, tipo="codigo", conceitos=["aritmeticos", "input", "conversao"])
def divisao_inteira_e_resto(r):
    casos = [
        (r.randint(25, 95), r.randint(4, 12)),
        (r.randint(10, 50), r.randint(3, 9)),
        (r.randint(12, 40), 4),
    ]
    a0, b0 = casos[0]
    return dict(
        titulo="Dividindo balas entre amigos",
        enunciado=(
            "Leia dois inteiros (um por linha): o total de **balas** e a quantidade de **amigos**.\n\n"
            "Calcule quantas balas inteiras **cada amigo** recebe igualmente e quantas **sobram** no pacote.\n"
            f"Exemplo para `{a0}` balas e `{b0}` amigos:\n"
            f"```\nCada amigo: {a0 // b0}\nSobram: {a0 % b0}\n```"
        ),
        solucao=(
            'balas = int(input("Balas: "))\n'
            'amigos = int(input("Amigos: "))\n'
            "por_pessoa = balas // amigos\n"
            "sobra = balas % amigos\n"
            'print("Cada amigo:", por_pessoa)\n'
            'print("Sobram:", sobra)\n'
        ),
        testes=[{"entrada": f"{a}\n{b}"} for a, b in casos],
        testes_visiveis=1,
        dicas=[
            "Use `//` (divisão inteira) para descobrir quantas balas inteiras cabem para cada pessoa.",
            "Use `%` (módulo / resto) para descobrir quantas sobram sem poder dividir igualmente.",
        ],
        explicacao=(
            "A divisão comum `/` daria um número decimal como `4.75` balas, mas não queremos partir balas ao meio. "
            "`//` dá o quociente inteiro e `%` dá o resto da divisão."
        ),
    )


@exercicio(estagio=4, dificuldade=1, tipo="prever", conceitos=["aritmeticos", "precedencia", "teste_de_mesa"])
def prever_precedencia_basica(r):
    a = r.randint(2, 6)
    b = r.randint(3, 7)
    c = r.randint(2, 4)
    return dict(
        titulo="Quem faz a conta primeiro?",
        enunciado=(
            "Lembre-se da ordem de precedência (`**` -> `* / // %` -> `+ -`) e parênteses.\n\n"
            "Sem executar, escreva exatamente a saída do código abaixo:"
        ),
        solucao=(
            f"a = {a}\n"
            f"b = {b}\n"
            f"c = {c}\n"
            "print(a + b * c)\n"
            "print((a + b) * c)\n"
            "print(c ** 2 + a)\n"
        ),
        dicas=[
            "Na primeira linha, a multiplicação `b * c` acontece antes da soma `+ a`.",
            "Na terceira linha, a potência `c ** 2` é calculada antes da soma.",
        ],
        explicacao=(
            f"`a + b * c` faz `{a} + ({b} * {c}) = {a + b * c}`. Com parênteses `(a + b) * c`, soma antes dando `{(a + b) * c}`. "
            f"Por fim `c ** 2 + a` faz `{c ** 2} + {a} = {c ** 2 + a}`."
        ),
    )


@exercicio(estagio=4, dificuldade=2, tipo="corrigir", conceitos=["precedencia", "aritmeticos", "depuracao"])
def corrigir_media_sem_parenteses(r):
    casos = [
        (round(r.uniform(5.0, 9.0), 1), round(r.uniform(5.0, 9.0), 1), round(r.uniform(5.0, 9.0), 1)),
        (6.0, 8.0, 10.0),
        (10.0, 4.0, 4.0),
    ]
    n1, n2, n3 = casos[0]
    m0 = (n1 + n2 + n3) / 3
    return dict(
        titulo="O clássico bug da média errada",
        enunciado=(
            "O programa lê três notas (`float`) e deveria mostrar a média aritmética com 2 casas decimais.\n"
            f"Para `{n1}`, `{n2}` e `{n3}`, a saída deve ser:\n```\nMédia: {m0:.2f}\n```\n"
            "Mas está calculando errado! Corrija o problema."
        ),
        codigo_inicial=(
            'n1 = float(input("N1: "))\n'
            'n2 = float(input("N2: "))\n'
            'n3 = float(input("N3: "))\n'
            "media = n1 + n2 + n3 / 3\n"
            'print(f"Média: {media:.2f}")\n'
        ),
        solucao=(
            'n1 = float(input("N1: "))\n'
            'n2 = float(input("N2: "))\n'
            'n3 = float(input("N3: "))\n'
            "media = (n1 + n2 + n3) / 3\n"
            'print(f"Média: {media:.2f}")\n'
        ),
        testes=[{"entrada": f"{a}\n{b}\n{c}"} for a, b, c in casos],
        testes_visiveis=1,
        dicas=[
            "Qual operação o Python executa primeiro em `n1 + n2 + n3 / 3`?",
            "Coloque parênteses em volta da soma das três notas antes de dividir por 3.",
        ],
        explicacao=(
            "Sem parênteses, a divisão `/` tem prioridade maior que `+`, então o Python dividia apenas `n3` por 3. "
            "Os parênteses `(n1 + n2 + n3)` garantem que a soma aconteça antes da divisão."
        ),
    )


@exercicio(estagio=4, dificuldade=2, tipo="completar", conceitos=["aritmeticos", "fstring"])
def completar_desconto_porcentagem(r):
    casos = [
        (round(r.uniform(80.0, 250.0), 2), r.choice([10, 15, 20, 25])),
        (round(r.uniform(40.0, 150.0), 2), r.choice([5, 12, 30])),
        (200.00, 15),
    ]
    p0, d0 = casos[0]
    desc0 = p0 * d0 / 100
    final0 = p0 - desc0
    return dict(
        titulo="Desconto na etiqueta",
        enunciado=(
            "Complete as lacunas `___` para ler o preço original (`float`) e o percentual de desconto (`int`), "
            "calcular o valor do desconto e o preço final:\n\n"
            f"Exemplo (`{p0:.2f}` e `{d0}%`):\n```\nDesconto: R$ {desc0:.2f}\nFinal: R$ {final0:.2f}\n```"
        ),
        codigo_inicial=(
            'preco = float(input("Preço: "))\n'
            'perc = int(input("Desconto (%): "))\n'
            "desconto = preco * ___ / 100\n"
            "final = preco - ___\n"
            'print(f"Desconto: R$ {desconto:.2f}")\n'
            'print(f"Final: R$ {final:.2f}")\n'
        ),
        solucao=(
            'preco = float(input("Preço: "))\n'
            'perc = int(input("Desconto (%): "))\n'
            "desconto = preco * perc / 100\n"
            "final = preco - desconto\n"
            'print(f"Desconto: R$ {desconto:.2f}")\n'
            'print(f"Final: R$ {final:.2f}")\n'
        ),
        testes=[{"entrada": f"{p:.2f}\n{d}"} for p, d in casos],
        testes_visiveis=1,
        dicas=[
            "`X%` de um preço é `preco * perc / 100`.",
            "Depois de calcular `desconto`, subtraia-o do `preco` original.",
        ],
        explicacao=(
            "Multiplicamos o preço pelo percentual e dividimos por 100 para achar quanto será abatido; "
            "em seguida subtraímos esse valor de `preco`."
        ),
    )


@exercicio(estagio=4, dificuldade=2, tipo="codigo", conceitos=["aritmeticos", "input", "fstring"])
def calculo_imc(r):
    casos = [
        (round(r.uniform(55.0, 95.0), 1), round(r.uniform(1.58, 1.90), 2)),
        (round(r.uniform(48.0, 82.0), 1), round(r.uniform(1.52, 1.85), 2)),
        (70.0, 1.75),
    ]
    p0, a0 = casos[0]
    imc0 = p0 / (a0 ** 2)
    return dict(
        titulo="Calculadora de IMC",
        enunciado=(
            "O Índice de Massa Corporal é calculado por `IMC = peso / altura²`.\n\n"
            "Leia o `peso` em kg (`float`) e a `altura` em metros (`float`), calcule usando o operador de potência `**` "
            "e exiba com 2 casas decimais:\n"
            f"Exemplo (`{p0}`, `{a0:.2f}`):\n```\nIMC: {imc0:.2f}\n```"
        ),
        solucao=(
            'peso = float(input("Peso (kg): "))\n'
            'altura = float(input("Altura (m): "))\n'
            "imc = peso / (altura ** 2)\n"
            'print(f"IMC: {imc:.2f}")\n'
        ),
        testes=[{"entrada": f"{p}\n{a:.2f}"} for p, a in casos],
        testes_visiveis=1,
        dicas=[
            "Elevar ao quadrado em Python é `altura ** 2`.",
            "Use parênteses em `(altura ** 2)` para deixar a divisão clara e formate com `:.2f`.",
        ],
        explicacao=(
            "Embora `**` já tenha precedência maior que `/`, escrever `peso / (altura ** 2)` deixa a fórmula "
            "mais fácil de ler e evita enganos."
        ),
    )


@exercicio(estagio=4, dificuldade=3, tipo="codigo", conceitos=["aritmeticos", "input", "fstring"])
def converter_minutos_horas(r):
    casos = [r.randint(75, 290), r.randint(300, 600), 45, 120]
    m0 = casos[0]
    return dict(
        titulo="Minutos em horas e minutos",
        enunciado=(
            "Leia uma duração total em **minutos** (`int`) e converta para **horas** e **minutos restantes**.\n\n"
            f"Exemplo para `{m0}` minutos:\n"
            f"```\n{m0 // 60}h {m0 % 60}min\n```"
        ),
        solucao=(
            'total_min = int(input("Total de minutos: "))\n'
            "horas = total_min // 60\n"
            "minutos = total_min % 60\n"
            'print(f"{horas}h {minutos}min")\n'
        ),
        testes=[{"entrada": str(m)} for m in casos],
        testes_visiveis=1,
        dicas=[
            "Cada hora tem 60 minutos. Quantas vezes 60 cabe inteiro dentro de `total_min`?",
            "Use `// 60` para as horas e `% 60` para os minutos que sobrarem.",
        ],
        explicacao=(
            "A dupla `//` e `%` resolve conversões de unidades perfeitamente: `total_min // 60` encontra as horas completas "
            "e `total_min % 60` encontra o resto em minutos (sempre entre 0 e 59)."
        ),
    )


@exercicio(estagio=4, dificuldade=3, tipo="prever", conceitos=["aritmeticos", "precedencia", "teste_de_mesa"])
def prever_barra_dupla_e_modulo(r):
    x = r.randint(15, 29)
    y = r.randint(4, 7)
    return dict(
        titulo="Mistério do //, % e **",
        enunciado=(
            "Faça o teste de mesa das expressões abaixo e escreva exatamente a saída gerada:"
        ),
        solucao=(
            f"x = {x}\n"
            f"y = {y}\n"
            "a = x // y\n"
            "b = x % y\n"
            "c = a * y + b\n"
            "print(a, b, c)\n"
            "print(2 ** 3 * 2)\n"
        ),
        dicas=[
            "Multiplique o quociente inteiro `a` pelo divisor `y` e some o resto `b` — o que sempre retorna?",
            "Em `2 ** 3 * 2`, a potência `2 ** 3` roda antes da multiplicação.",
        ],
        explicacao=(
            f"`{x} // {y} = {x // y}` e `{x} % {y} = {x % y}`. Pela regra fundamental da divisão, `quociente * divisor + resto` "
            f"sempre recompõe o número original `{x}`. E `2 ** 3 * 2` faz `8 * 2 = 16`."
        ),
    )


@exercicio(estagio=4, dificuldade=3, tipo="corrigir", conceitos=["aritmeticos", "precedencia", "depuracao"])
def corrigir_divisao_gorjeta_conta(r):
    casos = [
        (round(r.uniform(80.0, 200.0), 2), r.choice([10, 12, 15]), r.randint(2, 5)),
        (100.00, 10, 4),
        (150.00, 10, 3),
    ]
    v0, g0, p0 = casos[0]
    por_pessoa0 = (v0 * (1 + g0 / 100)) / p0
    return dict(
        titulo="Gorjeta dividida errado!",
        enunciado=(
            "Um grupo lê: valor da conta (`float`), percentual de gorjeta (`int`) e número de pessoas (`int`).\n"
            "O programa deveria somar a gorjeta ao total e só depois dividir igualmente pelas pessoas:\n"
            f"Entrada (`{v0:.2f}`, `{g0}`, `{p0}`):\n```\nCada pessoa paga: R$ {por_pessoa0:.2f}\n```\n"
            "Mas ele está dividindo só a gorjeta pelas pessoas! Encontre o bug de precedência e corrija."
        ),
        codigo_inicial=(
            'conta = float(input("Conta: "))\n'
            'gorjeta_pct = int(input("Gorjeta (%): "))\n'
            'pessoas = int(input("Pessoas: "))\n'
            "gorjeta = conta * gorjeta_pct / 100\n"
            "por_pessoa = conta + gorjeta / pessoas\n"
            'print(f"Cada pessoa paga: R$ {por_pessoa:.2f}")\n'
        ),
        solucao=(
            'conta = float(input("Conta: "))\n'
            'gorjeta_pct = int(input("Gorjeta (%): "))\n'
            'pessoas = int(input("Pessoas: "))\n'
            "gorjeta = conta * gorjeta_pct / 100\n"
            "por_pessoa = (conta + gorjeta) / pessoas\n"
            'print(f"Cada pessoa paga: R$ {por_pessoa:.2f}")\n'
        ),
        testes=[{"entrada": f"{v:.2f}\n{g}\n{p}"} for v, g, p in casos],
        testes_visiveis=1,
        dicas=[
            "Olhe a linha `por_pessoa = conta + gorjeta / pessoas`.",
            "Sem parênteses, apenas `gorjeta` está sendo dividida por `pessoas`!",
        ],
        explicacao=(
            "Por precedência, `/` executa antes de `+`. Colocando `(conta + gorjeta) / pessoas`, somamos "
            "a conta completa com a gorjeta antes de repartir entre os amigos."
        ),
    )


@exercicio(estagio=4, dificuldade=3, tipo="codigo", conceitos=["aritmeticos", "input"])
def separar_tres_digitos(r):
    casos = [r.randint(100, 999), r.randint(102, 895), 407, 920]
    n0 = casos[0]
    return dict(
        titulo="Desmontando um número de 3 dígitos",
        enunciado=(
            "Leia um número inteiro positivo de **3 dígitos** (entre `100` e `999`).\n\n"
            "Usando apenas operações matemáticas (`//` e `%`), extraia e mostre a **centena**, a **dezena** e a **unidade**:\n"
            f"Exemplo para `{n0}`:\n"
            f"```\nCentena: {n0 // 100}\nDezena: {(n0 // 10) % 10}\nUnidade: {n0 % 10}\n```"
        ),
        solucao=(
            'n = int(input("Número (100-999): "))\n'
            "centena = n // 100\n"
            "dezena = (n // 10) % 10\n"
            "unidade = n % 10\n"
            'print("Centena:", centena)\n'
            'print("Dezena:", dezena)\n'
            'print("Unidade:", unidade)\n'
        ),
        testes=[{"entrada": str(x)} for x in casos],
        testes_visiveis=1,
        dicas=[
            "Dividir por `100` com `//` pega a centena; pegar `% 10` pega o último dígito (unidade).",
            "Para achar a dezena, \"jogue fora\" a unidade com `n // 10` e pegue o último dígito com `% 10`.",
        ],
        explicacao=(
            "`n // 100` descarta os dois últimos dígitos, isolando a centena. `(n // 10) % 10` corta a unidade e pega "
            "o último algarismo que sobrou (a dezena). `n % 10` pega direto o último dígito."
        ),
    )


@exercicio(estagio=4, dificuldade=4, tipo="completar", conceitos=["aritmeticos", "precedencia"])
def completar_media_ponderada(r):
    p1, p2, p3 = r.choice([(2, 3, 5), (1, 2, 3), (2, 2, 6)])
    casos = [
        (round(r.uniform(5.0, 9.5), 1), round(r.uniform(5.0, 9.5), 1), round(r.uniform(5.0, 9.5), 1)),
        (8.0, 7.0, 9.0),
        (6.5, 8.5, 7.0),
    ]
    n1, n2, n3 = casos[0]
    mp0 = (n1 * p1 + n2 * p2 + n3 * p3) / (p1 + p2 + p3)
    return dict(
        titulo="Média ponderada das provas",
        enunciado=(
            f"Leia três notas (`float`) com pesos **{p1}**, **{p2}** e **{p3}**, respectivamente.\n\n"
            "Complete as lacunas `___` lembrando de dividir pela **soma dos pesos**!\n"
            f"Exemplo (`{n1}`, `{n2}`, `{n3}`):\n```\nMédia ponderada: {mp0:.2f}\n```"
        ),
        codigo_inicial=(
            'n1 = float(input("N1: "))\n'
            'n2 = float(input("N2: "))\n'
            'n3 = float(input("N3: "))\n'
            f"soma_notas = n1 * {p1} + n2 * {p2} + n3 * {p3}\n"
            f"soma_pesos = ___\n"
            "media = soma_notas / ___\n"
            'print(f"Média ponderada: {media:.2f}")\n'
        ),
        solucao=(
            'n1 = float(input("N1: "))\n'
            'n2 = float(input("N2: "))\n'
            'n3 = float(input("N3: "))\n'
            f"soma_notas = n1 * {p1} + n2 * {p2} + n3 * {p3}\n"
            f"soma_pesos = {p1} + {p2} + {p3}\n"
            "media = soma_notas / soma_pesos\n"
            'print(f"Média ponderada: {media:.2f}")\n'
        ),
        testes=[{"entrada": f"{a}\n{b}\n{c}"} for a, b, c in casos],
        testes_visiveis=1,
        dicas=[
            f"A soma dos pesos é `{p1} + {p2} + {p3}`.",
            "Na média ponderada, dividimos `soma_notas` por `soma_pesos` (não por 3!).",
        ],
        explicacao=(
            "Um erro muito comum é dividir média ponderada pela quantidade de provas (3) em vez da soma dos pesos. "
            "Guardar `soma_pesos` numa variável evita o erro e dispensa parênteses extras."
        ),
    )


@exercicio(estagio=4, dificuldade=4, tipo="codigo", conceitos=["aritmeticos", "input"])
def decompor_segundos_hms(r):
    casos = [r.randint(3665, 18500), r.randint(400, 3599), 7325, 59]
    s0 = casos[0]
    h0 = s0 // 3600
    m0 = (s0 % 3600) // 60
    seg0 = s0 % 60
    return dict(
        titulo="Cronômetro em HH:MM:SS",
        enunciado=(
            "Leia um tempo total em **segundos** (`int`).\n\n"
            "Converta e mostre no formato `HH:MM:SS` com dois dígitos em cada campo (`:02d`):\n"
            f"Exemplo para `{s0}` segundos:\n```\n{h0:02d}:{m0:02d}:{seg0:02d}\n```"
        ),
        solucao=(
            'total = int(input("Segundos: "))\n'
            "horas = total // 3600\n"
            "resto = total % 3600\n"
            "minutos = resto // 60\n"
            "segundos = resto % 60\n"
            'print(f"{horas:02d}:{minutos:02d}:{segundos:02d}")\n'
        ),
        testes=[{"entrada": str(s)} for s in casos],
        testes_visiveis=1,
        dicas=[
            "1 hora tem `60 * 60 = 3600` segundos. Use `total // 3600` para horas e `total % 3600` para o que sobrou.",
            "Do que sobrou (`resto`), tire os minutos com `// 60` e os segundos finais com `% 60`.",
        ],
        explicacao=(
            "Vamos quebrando da maior unidade para a menor usando sempre `//` (quantas unidades cabem) e `%` (o que sobra para a unidade menor)."
        ),
    )


@exercicio(estagio=4, dificuldade=4, tipo="prever", conceitos=["aritmeticos", "precedencia", "teste_de_mesa"])
def prever_operadores_compostos_e_sinal(r):
    a = r.randint(2, 5)
    b = r.randint(10, 19)
    return dict(
        titulo="Potência negativa e atribuição composta",
        enunciado=(
            "Atenção à precedência de `**` em relação ao sinal `-` e aos operadores `+=` e `//=`.\n\n"
            "Escreva exatamente a saída gerada pelo trecho:"
        ),
        solucao=(
            f"a = {a}\n"
            f"b = {b}\n"
            "b //= a\n"
            "b += 3\n"
            "print(b)\n"
            "print(-a ** 2)\n"
            "print((-a) ** 2)\n"
        ),
        dicas=[
            "`b //= a` é o mesmo que `b = b // a`.",
            "`-a ** 2` calcula `a ** 2` primeiro e só depois coloca o sinal `-`!",
        ],
        explicacao=(
            f"`b` faz `{b} // {a} = {b // a}` e soma 3, virando `{b // a + 3}`. "
            f"Em `-a ** 2`, a potência tem prioridade sobre o sinal unário `-`, gerando `-{a ** 2}`; já `(-a) ** 2` eleva o negativo ao quadrado, dando `{(-a) ** 2}`."
        ),
    )


@exercicio(estagio=4, dificuldade=4, tipo="corrigir", conceitos=["aritmeticos", "precedencia", "depuracao"])
def corrigir_porcentagem_e_precedencia(r):
    casos = [
        (round(r.uniform(1000.0, 4000.0), 2), r.choice([8, 12, 15])),
        (2500.00, 10),
        (1800.00, 5),
    ]
    s0, a0 = casos[0]
    novo0 = s0 * (1 + a0 / 100)
    return dict(
        titulo="Reajuste salarial explosivo!",
        enunciado=(
            "O programa lê um salário (`float`) e o percentual de aumento (`int`), por exemplo `2500.00` e `10` (10%).\n"
            f"Para `{s0:.2f}` com `{a0}%` de aumento, o novo salário deveria ser:\n```\nNovo salário: R$ {novo0:.2f}\n```\n"
            "Mas a fórmula atual multiplica o salário por um número gigante! Corrija a fórmula."
        ),
        codigo_inicial=(
            'salario = float(input("Salário: "))\n'
            'aumento = int(input("Aumento (%): "))\n'
            "novo = salario * (1 + aumento) / 100\n"
            'print(f"Novo salário: R$ {novo:.2f}")\n'
        ),
        solucao=(
            'salario = float(input("Salário: "))\n'
            'aumento = int(input("Aumento (%): "))\n'
            "novo = salario * (1 + aumento / 100)\n"
            'print(f"Novo salário: R$ {novo:.2f}")\n'
        ),
        testes=[{"entrada": f"{s:.2f}\n{a}"} for s, a in casos],
        testes_visiveis=1,
        dicas=[
            "Veja onde o `/ 100` foi parar: `(1 + aumento) / 100` divide o `1` por `100` também!",
            "O percentual deve ser dividido por 100 **antes** de somar com `1`: `1 + aumento / 100`.",
        ],
        explicacao=(
            "Um aumento de `10%` equivale a multiplicar por `1 + 0.10 = 1.10`. Com os parênteses errados em `(1 + aumento) / 100`, "
            "multiplicava por `0.11`, derrubando o salário para 11% do original!"
        ),
    )


@exercicio(estagio=4, dificuldade=5, tipo="codigo", conceitos=["aritmeticos", "input"])
def caixa_eletronico_cedulas(r):
    casos = [
        r.randint(137, 489),
        r.randint(60, 129),
        88,
        245,
    ]
    v0 = casos[0]
    n50 = v0 // 50
    r50 = v0 % 50
    n20 = r50 // 20
    r20 = r50 % 20
    n10 = r20 // 10
    n1 = r20 % 10
    return dict(
        titulo="Caixa eletrônico de cédulas",
        enunciado=(
            "Um caixa eletrônico possui apenas notas de **R$ 50**, **R$ 20**, **R$ 10** e **R$ 1**.\n\n"
            "Leia um valor inteiro de saque e calcule a quantidade de cada nota usando **o menor número possível de cédulas** "
            "(começando sempre da maior nota para a menor com `//` e `%`).\n\n"
            f"Exemplo para `R$ {v0}`:\n"
            f"```\n50: {n50}\n20: {n20}\n10: {n10}\n1: {n1}\n```"
        ),
        solucao=(
            'valor = int(input("Valor do saque: "))\n'
            "n50 = valor // 50\n"
            "resto = valor % 50\n"
            "n20 = resto // 20\n"
            "resto = resto % 20\n"
            "n10 = resto // 10\n"
            "n1 = resto % 10\n"
            'print("50:", n50)\n'
            'print("20:", n20)\n'
            'print("10:", n10)\n'
            'print("1:", n1)\n'
        ),
        testes=[{"entrada": str(x)} for x in casos],
        testes_visiveis=1,
        dicas=[
            "Comece tirando quantas notas de 50 cabem (`valor // 50`) e guarde o que falta sacar (`valor % 50`).",
            "Repita a mesma dupla `//` e `%` com o `resto` para 20 e depois para 10; o resto final são as notas de 1.",
        ],
        explicacao=(
            "Este algoritmo guloso usa sucessivamente divisão inteira e resto: a maior cédula reduz o valor o máximo possível, "
            "passando apenas a sobra para a cédula seguinte."
        ),
    )


@exercicio(estagio=4, dificuldade=5, tipo="codigo", conceitos=["aritmeticos", "precedencia", "fstring"])
def custo_viagem_combustivel(r):
    casos = [
        (r.randint(250, 520), round(r.uniform(10.5, 14.5), 1), round(r.uniform(5.20, 6.40), 2)),
        (r.randint(120, 300), round(r.uniform(9.0, 13.0), 1), round(r.uniform(5.00, 6.20), 2)),
        (360, 12.0, 5.50),
    ]
    d0, c0, p0 = casos[0]
    litros0 = (d0 * 2) / c0
    gasto0 = litros0 * p0
    return dict(
        titulo="Custo de ida e volta",
        enunciado=(
            "Leia três valores (um por linha):\n"
            "1. Distância **só de ida** entre duas cidades em km (`int`)\n"
            "2. Consumo do carro em km/litro (`float`)\n"
            "3. Preço do litro do combustível (`float`)\n\n"
            "Calcule quantos litros serão gastos na viagem **de ida e volta** e o custo total, com 2 casas decimais:\n"
            f"Exemplo (`{d0}`, `{c0}`, `{p0:.2f}`):\n"
            f"```\nLitros (ida e volta): {litros0:.2f}\nCusto total: R$ {gasto0:.2f}\n```"
        ),
        solucao=(
            'distancia_ida = int(input("Distância (km): "))\n'
            'consumo = float(input("Consumo (km/L): "))\n'
            'preco_litro = float(input("Preço/L: "))\n'
            "litros = (distancia_ida * 2) / consumo\n"
            "custo = litros * preco_litro\n"
            'print(f"Litros (ida e volta): {litros:.2f}")\n'
            'print(f"Custo total: R$ {custo:.2f}")\n'
        ),
        testes=[{"entrada": f"{d}\n{c}\n{p:.2f}"} for d, c, p in casos],
        testes_visiveis=1,
        dicas=[
            "Como é ida e volta, a distância total percorrida é `distancia_ida * 2`.",
            "Divida a distância total pelo consumo para achar os litros e multiplique pelo preço do litro.",
        ],
        explicacao=(
            "Multiplicamos a distância por 2 antes de dividir pelo consumo por litro. Em seguida, o número de litros "
            "vezes o preço por litro dá o orçamento exato da viagem."
        ),
    )
