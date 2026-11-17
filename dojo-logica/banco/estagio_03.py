"""Estágio 3 - Entrada de dados (input) e conversão na leitura."""

from .base import exercicio

NOMES = ["Ana", "Bruno", "Carla", "Diego", "Elisa", "Fábio", "Gabi", "Heitor", "Iara", "João"]
CIDADES = ["Recife", "Curitiba", "Manaus", "Salvador", "Fortaleza", "Belém", "Vitória"]


@exercicio(estagio=3, dificuldade=1, tipo="codigo", conceitos=["input", "fstring"])
def saudacao_usuario(r):
    nomes = r.sample(NOMES, 3)
    cidades = r.sample(CIDADES, 3)
    testes = [{"entrada": f"{n}\n{c}"} for n, c in zip(nomes, cidades)]
    return dict(
        titulo="Apresentação interativa",
        enunciado=(
            "Escreva um programa que leia **o nome** de uma pessoa e depois **a cidade** onde ela mora (um por linha).\n\n"
            "Em seguida, mostre a saudação exata abaixo:\n"
            f"```\nOlá, {nomes[0]}! Bem-vindo(a) de {cidades[0]}.\n```"
        ),
        solucao=(
            'nome = input("Nome: ")\n'
            'cidade = input("Cidade: ")\n'
            'print(f"Olá, {nome}! Bem-vindo(a) de {cidade}.")\n'
        ),
        testes=testes,
        testes_visiveis=1,
        dicas=[
            "Use `input()` duas vezes, na mesma ordem pedida no enunciado: primeiro nome, depois cidade.",
            "Como ambos são textos, não precisa converter com `int()` ou `float()`.",
        ],
        explicacao=(
            "Cada chamada a `input()` lê uma linha da entrada do usuário como `str`. Depois, a f-string monta "
            "a frase colocando o ponto final colado ao nome da cidade."
        ),
    )


@exercicio(estagio=3, dificuldade=1, tipo="completar", conceitos=["input", "conversao"])
def completar_dobro_numero(r):
    nums = [r.randint(2, 15), r.randint(20, 50), 0, -r.randint(3, 12)]
    return dict(
        titulo="Lendo um inteiro e dobrando",
        enunciado=(
            "Complete as lacunas `___` para ler um número inteiro digitado pelo usuário e mostrar o dobro dele.\n\n"
            f"Exemplo para entrada `{nums[0]}`:\n```\nDobro: {nums[0] * 2}\n```"
        ),
        codigo_inicial=(
            'numero = ___(input("Número: "))\n'
            "dobro = numero * ___\n"
            'print("Dobro:", dobro)\n'
        ),
        solucao=(
            'numero = int(input("Número: "))\n'
            "dobro = numero * 2\n"
            'print("Dobro:", dobro)\n'
        ),
        testes=[{"entrada": str(x)} for x in nums],
        testes_visiveis=1,
        dicas=[
            "`input()` sempre devolve texto (`str`). Converta logo na leitura usando `int(...)`.",
            "Sem o `int()`, multiplicar texto por `2` repetiria o texto (ex.: `\"5\" * 2` viraria `\"55\"`)!",
        ],
        explicacao=(
            "`int(input(...))` converte o texto digitado em inteiro antes de guardar na variável. "
            "Assim `numero * 2` faz uma multiplicação numérica."
        ),
    )


@exercicio(estagio=3, dificuldade=2, tipo="corrigir", conceitos=["input", "conversao", "depuracao"])
def corrigir_input_sem_int(r):
    pares = [(r.randint(3, 12), r.randint(4, 15)), (r.randint(10, 40), r.randint(20, 50)), (0, r.randint(5, 9))]
    a0, b0 = pares[0]
    return dict(
        titulo="Por que 3 + 4 deu 34?!",
        enunciado=(
            "O programa lê dois números inteiros e deveria somá-los, mas quando recebe `3` e `4`, imprime `34`!\n\n"
            "Descubra a causa e corrija para que para entrada `3` e `4` (ou no exemplo abaixo) mostre a soma matemática:\n"
            f"Entrada:\n```\n{a0}\n{b0}\n```\nSaída esperada:\n```\nSoma: {a0 + b0}\n```"
        ),
        codigo_inicial=(
            'a = input("Primeiro: ")\n'
            'b = input("Segundo: ")\n'
            "soma = a + b\n"
            'print("Soma:", soma)\n'
        ),
        solucao=(
            'a = int(input("Primeiro: "))\n'
            'b = int(input("Segundo: "))\n'
            "soma = a + b\n"
            'print("Soma:", soma)\n'
        ),
        testes=[{"entrada": f"{x}\n{y}"} for x, y in pares],
        testes_visiveis=1,
        dicas=[
            "Qual é o tipo que `input()` devolve por padrão?",
            "Como `a` e `b` são strings, `a + b` está colando os dois textos! Converta ambos com `int()`.",
        ],
        explicacao=(
            "Esse é o erro mais clássico com `input()`: como ele devolve `str`, o operador `+` concatena os textos "
            "em vez de somar os números. Envolver com `int()` resolve."
        ),
    )


@exercicio(estagio=3, dificuldade=2, tipo="codigo", conceitos=["input", "conversao", "fstring"])
def idade_em_ano_futuro(r):
    alvo = r.randint(2030, 2050)
    ex_nome = r.choice(NOMES)
    testes = [
        {"entrada": f"{ex_nome}\n{r.randint(1990, 2008)}"},
        {"entrada": f"{r.choice(NOMES)}\n{r.randint(1975, 1989)}"},
        {"entrada": f"{r.choice(NOMES)}\n{r.randint(2009, 2018)}"},
    ]
    nasc0 = int(testes[0]["entrada"].split("\n")[1])
    return dict(
        titulo=f"Quantos anos você terá em {alvo}?",
        enunciado=(
            f"Leia o **nome** (texto) e o **ano de nascimento** (inteiro) de uma pessoa, um por linha.\n\n"
            f"Mostre quantos anos ela completará em **{alvo}** no formato exato:\n"
            f"```\nEm {alvo}, {ex_nome} terá {alvo - nasc0} anos.\n```"
        ),
        solucao=(
            'nome = input("Nome: ")\n'
            'nascimento = int(input("Ano de nascimento: "))\n'
            f"idade = {alvo} - nascimento\n"
            f'print(f"Em {alvo}, {{nome}} terá {{idade}} anos.")\n'
        ),
        testes=testes,
        testes_visiveis=1,
        dicas=[
            "Leia `nome = input(...)` e `nascimento = int(input(...))`.",
            f"Subtraia `nascimento` de `{alvo}` e exiba com f-string.",
        ],
        explicacao=(
            "Lemos `nome` como texto e `nascimento` convertido para `int`, pois precisamos subtrair do ano alvo."
        ),
    )


@exercicio(estagio=3, dificuldade=2, tipo="prever", conceitos=["input", "conversao", "teste_de_mesa"])
def prever_leitura_ordem(r):
    a = r.randint(4, 12)
    b = r.randint(2, 7)
    nome = r.choice(["Lia", "Caio", "Téo", "Nina"])
    return dict(
        titulo="Rastreando um programa com input()",
        enunciado=(
            f"Suponha que o usuário digite na entrada, nesta ordem:\n```\n{nome}\n{a}\n{b}\n```\n"
            "Escreva exatamente o que o programa vai imprimir na saída (lembre que mensagens dentro do `input(\"...\")` "
            "não fazem parte do `print`)."
        ),
        solucao=(
            "nome = input()\n"
            "x = int(input())\n"
            "y = int(input())\n"
            "z = x * y\n"
            'print(f"{nome}: {z}")\n'
        ),
        testes=[{"entrada": f"{nome}\n{a}\n{b}"}],
        dicas=[
            "Cada `input()` consome uma linha da entrada, na ordem em que aparece no código.",
            f"A 1ª linha vai para `nome`, a 2ª para `x` ({a}) e a 3ª para `y` ({b}).",
        ],
        explicacao=(
            f"O primeiro `input()` lê `\"{nome}\"`; o segundo converte `\"{a}\"` para `{a}`; o terceiro converte `\"{b}\"` para `{b}`. "
            f"`z` recebe `{a} * {b} = {a * b}`, imprimindo `{nome}: {a * b}`."
        ),
    )


@exercicio(estagio=3, dificuldade=3, tipo="codigo", conceitos=["input", "conversao", "fstring"])
def compra_no_mercado(r):
    casos = [
        (r.choice(["Maçã", "Banana", "Queijo", "Café"]), round(r.uniform(3.5, 18.9), 2), r.randint(2, 6)),
        (r.choice(["Arroz", "Suco", "Pão"]), round(r.uniform(5.0, 25.5), 2), r.randint(1, 4)),
        ("Azeite", round(r.uniform(22.0, 39.9), 2), r.randint(2, 5)),
    ]
    prod0, p0, q0 = casos[0]
    return dict(
        titulo="Caixa do mercado",
        enunciado=(
            "Faça um programa que leia, um por linha:\n"
            "1. O nome do produto (`str`)\n"
            "2. O preço unitário (`float`)\n"
            "3. A quantidade comprada (`int`)\n\n"
            "Mostre o resumo com o total formatado em duas casas decimais:\n"
            f"```\n{q0}x {prod0} -> R$ {p0 * q0:.2f}\n```"
        ),
        solucao=(
            'produto = input("Produto: ")\n'
            'preco = float(input("Preço: "))\n'
            'qtd = int(input("Quantidade: "))\n'
            "total = preco * qtd\n"
            'print(f"{qtd}x {produto} -> R$ {total:.2f}")\n'
        ),
        testes=[{"entrada": f"{pr}\n{p:.2f}\n{q}"} for pr, p, q in casos],
        testes_visiveis=1,
        dicas=[
            "Atenção ao tipo de cada leitura: texto (`input`), decimal (`float(input())`) e inteiro (`int(input())`).",
            "Use `f\"{qtd}x {produto} -> R$ {total:.2f}\"` no `print`.",
        ],
        explicacao=(
            "Cada dado usa a conversão apropriada: preço tem centavos (`float`), quantidade é inteira (`int`), "
            "e o nome fica em `str`. Multiplicando os dois números e usando `:.2f`, obtemos o valor exato."
        ),
    )


@exercicio(estagio=3, dificuldade=3, tipo="corrigir", conceitos=["input", "conversao", "depuracao"])
def corrigir_float_com_int(r):
    casos = [
        (round(r.uniform(1.5, 9.5), 1), round(r.uniform(2.5, 9.5), 1)),
        (round(r.uniform(3.2, 8.7), 1), round(r.uniform(4.1, 7.9), 1)),
        (10.0, 5.5),
    ]
    n1, n2 = casos[0]
    return dict(
        titulo="Notas quebradas quebram o programa!",
        enunciado=(
            "Este programa lê duas notas que podem ter casas decimais (ex.: `7.5` e `8.0`) e deveria imprimir a soma "
            "com 2 casas decimais:\n"
            f"Entrada:\n```\n{n1}\n{n2}\n```\nSaída esperada:\n```\nSoma das notas: {n1 + n2:.2f}\n```\n"
            "Mas está dando `ValueError`! Corrija o tipo da conversão."
        ),
        codigo_inicial=(
            'nota1 = int(input("Nota 1: "))\n'
            'nota2 = int(input("Nota 2: "))\n'
            "soma = nota1 + nota2\n"
            'print(f"Soma das notas: {soma:.2f}")\n'
        ),
        solucao=(
            'nota1 = float(input("Nota 1: "))\n'
            'nota2 = float(input("Nota 2: "))\n'
            "soma = nota1 + nota2\n"
            'print(f"Soma das notas: {soma:.2f}")\n'
        ),
        testes=[{"entrada": f"{a}\n{b}"} for a, b in casos],
        testes_visiveis=1,
        dicas=[
            "Quando o usuário digita `7.5`, `int(\"7.5\")` falha com `ValueError` porque existe um ponto decimal.",
            "Troque `int(` por `float(` nas duas leituras.",
        ],
        explicacao=(
            "Para valores que podem conter casas decimais (preços, notas, alturas, pesos), devemos converter a leitura "
            "do `input()` com `float()`, nunca com `int()`."
        ),
    )


@exercicio(estagio=3, dificuldade=3, tipo="completar", conceitos=["input", "conversao", "fstring"])
def completar_conversao_dolar(r):
    cot = round(r.uniform(4.80, 5.90), 2)
    casos = [
        (round(r.uniform(20.0, 150.0), 2), cot),
        (round(r.uniform(10.0, 80.0), 2), round(r.uniform(4.50, 5.50), 2)),
        (100.00, 5.00),
    ]
    reais0, cot0 = casos[0]
    return dict(
        titulo="Conversor de câmbio",
        enunciado=(
            "Complete as lacunas `___` para ler um valor em reais e a cotação do dólar (ambos `float`) e mostrar quantos "
            "dólares dá para comprar:\n\n"
            f"Exemplo para `{reais0:.2f}` reais e cotação `{cot0:.2f}`:\n"
            f"```\nUS$ {reais0 / cot0:.2f}\n```"
        ),
        codigo_inicial=(
            'reais = ___(input("Valor em R$: "))\n'
            'cotacao = float(___())\n'
            "dolares = reais / ___\n"
            'print(f"US$ {dolares:___}")\n'
        ),
        solucao=(
            'reais = float(input("Valor em R$: "))\n'
            'cotacao = float(input())\n'
            "dolares = reais / cotacao\n"
            'print(f"US$ {dolares:.2f}")\n'
        ),
        testes=[{"entrada": f"{reais:.2f}\n{c:.2f}"} for reais, c in casos],
        testes_visiveis=1,
        dicas=[
            "Valores monetários usam `float()` na leitura.",
            "Para saber quantos dólares valem `reais`, divida `reais` por `cotacao` e formate com `.2f`.",
        ],
        explicacao=(
            "Lemos ambos os decimais com `float(input())`, dividimos o valor em reais pela cotação e exibimos o resultado "
            "com `{dolares:.2f}`."
        ),
    )


@exercicio(estagio=3, dificuldade=3, tipo="codigo", conceitos=["input", "conversao", "fstring"])
def perimetro_retangulo(r):
    casos = [
        (round(r.uniform(3.0, 15.0), 1), round(r.uniform(2.0, 10.0), 1)),
        (round(r.uniform(5.0, 20.0), 1), round(r.uniform(1.5, 9.5), 1)),
        (10.0, 4.5),
    ]
    b0, h0 = casos[0]
    return dict(
        titulo="Medidas de um terreno",
        enunciado=(
            "Leia a **largura** e o **comprimento** de um terreno retangular (`float`, um por linha).\n\n"
            "Calcule e mostre a **área** (`largura * comprimento`) e o **perímetro** (`2 * (largura + comprimento)`), "
            "com 2 casas decimais:\n"
            f"Exemplo para `{b0}` e `{h0}`:\n"
            f"```\nÁrea: {b0 * h0:.2f}\nPerímetro: {2 * (b0 + h0):.2f}\n```"
        ),
        solucao=(
            'largura = float(input("Largura: "))\n'
            'comprimento = float(input("Comprimento: "))\n'
            "area = largura * comprimento\n"
            "perimetro = 2 * (largura + comprimento)\n"
            'print(f"Área: {area:.2f}")\n'
            'print(f"Perímetro: {perimetro:.2f}")\n'
        ),
        testes=[{"entrada": f"{b}\n{h}"} for b, h in casos],
        testes_visiveis=1,
        dicas=[
            "Use `float(input())` para ler largura e comprimento.",
            "No perímetro, não esqueça os parênteses: `2 * (largura + comprimento)`.",
        ],
        explicacao=(
            "Lemos as duas dimensões em `float`, calculamos área e perímetro (usando parênteses para somar os lados "
            "antes de multiplicar por 2) e imprimimos com `:.2f`."
        ),
    )


@exercicio(estagio=3, dificuldade=4, tipo="prever", conceitos=["input", "conversao", "teste_de_mesa"])
def prever_tres_leituras_trocadas(r):
    a = r.randint(10, 30)
    b = r.randint(2, 9)
    c = r.randint(1, 5)
    return dict(
        titulo="Ordem das entradas no teste de mesa",
        enunciado=(
            f"Um usuário digita as seguintes linhas de entrada:\n```\n{a}\n{b}\n{c}\n```\n"
            "Acompanhe passo a passo o código abaixo e escreva exatamente o que será impresso."
        ),
        solucao=(
            "x = input()\n"
            "y = int(input())\n"
            "z = int(input())\n"
            'print(x * z)\n'
            "print(y + z)\n"
        ),
        testes=[{"entrada": f"{a}\n{b}\n{c}"}],
        dicas=[
            "Repare que `x` foi lido **sem** `int()`! Ele continua sendo uma string.",
            "Multiplicar uma string `x` pelo inteiro `z` repete a string `z` vezes.",
        ],
        explicacao=(
            f"`x` guarda o texto `\"{a}\"`, então `x * {c}` repete o texto {c} vezes (`\"{str(a) * c}\"`). "
            f"Já `y` ({b}) e `z` ({c}) foram convertidos para `int`, então `y + z` soma numericamente dando `{b + c}`."
        ),
    )


@exercicio(estagio=3, dificuldade=4, tipo="codigo", conceitos=["input", "conversao", "fstring"])
def conversao_celsius_fahrenheit(r):
    temps = [0.0, float(r.randint(18, 38)), -5.0, float(r.randint(40, 100))]
    c0 = temps[0]
    f0 = c0 * 9 / 5 + 32
    return dict(
        titulo="Termômetro Celsius para Fahrenheit",
        enunciado=(
            "Leia uma temperatura em graus Celsius (`float`) e converta para Fahrenheit usando a fórmula:\n"
            "`F = C * 9 / 5 + 32`\n\n"
            f"Exemplo para `{c0}`:\n```\n{c0:.1f} C = {f0:.1f} F\n```"
        ),
        solucao=(
            'celsius = float(input("Celsius: "))\n'
            "fahrenheit = celsius * 9 / 5 + 32\n"
            'print(f"{celsius:.1f} C = {fahrenheit:.1f} F")\n'
        ),
        testes=[{"entrada": str(t)} for t in temps],
        testes_visiveis=1,
        dicas=[
            "Converta a entrada com `float(input())`, pois temperaturas podem ser decimais ou negativas.",
            "Formate ambos os valores com `:.1f` na f-string.",
        ],
        explicacao=(
            "Convertemos a leitura para `float`, aplicamos `celsius * 9 / 5 + 32` e mostramos ambos os números "
            "com uma casa decimal (`:.1f`)."
        ),
    )


@exercicio(estagio=3, dificuldade=4, tipo="corrigir", conceitos=["input", "conversao", "depuracao"])
def corrigir_ordem_leitura_e_calculo(r):
    casos = [
        (r.choice(NOMES), r.randint(150, 400), r.randint(2, 5)),
        (r.choice(NOMES), r.randint(80, 200), r.randint(2, 4)),
        ("Ana", 100, 4),
    ]
    n0, v0, d0 = casos[0]
    return dict(
        titulo="Conta dividida errada",
        enunciado=(
            "O programa lê: 1) nome do grupo (`str`), 2) valor da conta (`float`) e 3) número de amigos (`int`).\n"
            "Ele deveria mostrar quanto cada um paga com 2 casas decimais:\n"
            f"Entrada:\n```\n{n0}\n{v0}\n{d0}\n```\nSaída esperada:\n```\n{n0}: R$ {v0 / d0:.2f} por pessoa\n```\n"
            "Mas está cheio de problemas! Corrija o código."
        ),
        codigo_inicial=(
            'grupo = int(input("Grupo: "))\n'
            'valor = input("Valor: ")\n'
            'amigos = input("Amigos: ")\n'
            "cada = valor / amigos\n"
            'print(f"{grupo}: R$ {cada:.2f} por pessoa")\n'
        ),
        solucao=(
            'grupo = input("Grupo: ")\n'
            'valor = float(input("Valor: "))\n'
            'amigos = int(input("Amigos: "))\n'
            "cada = valor / amigos\n"
            'print(f"{grupo}: R$ {cada:.2f} por pessoa")\n'
        ),
        testes=[{"entrada": f"{g}\n{v}\n{a}"} for g, v, a in casos],
        testes_visiveis=1,
        dicas=[
            "`grupo` é um nome (texto)! Não use `int()` nele.",
            "Já `valor` precisa de `float()` e `amigos` precisa de `int()` para a divisão funcionar.",
        ],
        explicacao=(
            "As conversões estavam trocadas: o nome do grupo estava sendo convertido para `int` (quebrando com `ValueError`), "
            "enquanto os números ficaram como `str` (quebrando na divisão com `TypeError`)."
        ),
    )


@exercicio(estagio=3, dificuldade=4, tipo="completar", conceitos=["input", "conversao", "fstring"])
def completar_etiqueta_encomenda(r):
    casos = [
        (r.choice(NOMES), r.choice(CIDADES), round(r.uniform(1.2, 12.5), 2)),
        (r.choice(NOMES), r.choice(CIDADES), round(r.uniform(0.5, 5.0), 2)),
        ("Lucas", "Fortaleza", 3.4),
    ]
    n0, c0, p0 = casos[0]
    frete0 = p0 * 12
    return dict(
        titulo="Etiqueta de entrega",
        enunciado=(
            "O frete custa **R$ 12.00 por kg**. Complete as lacunas `___` para ler o destinatário, a cidade e o peso (em kg) "
            "e gerar a etiqueta:\n\n"
            f"Exemplo (`{n0}`, `{c0}`, `{p0}`):\n"
            f"```\nPara: {n0} ({c0}) | Peso: {p0:.2f} kg | Frete: R$ {frete0:.2f}\n```"
        ),
        codigo_inicial=(
            'dest = ___("Destinatário: ")\n'
            'cidade = input("Cidade: ")\n'
            'peso = ___(input("Peso (kg): "))\n'
            "frete = peso * 12\n"
            'print(f"Para: {dest} ({cidade}) | Peso: {peso:.2f} kg | Frete: R$ {___:.2f}")\n'
        ),
        solucao=(
            'dest = input("Destinatário: ")\n'
            'cidade = input("Cidade: ")\n'
            'peso = float(input("Peso (kg): "))\n'
            "frete = peso * 12\n"
            'print(f"Para: {dest} ({cidade}) | Peso: {peso:.2f} kg | Frete: R$ {frete:.2f}")\n'
        ),
        testes=[{"entrada": f"{n}\n{c}\n{p}"} for n, c, p in casos],
        testes_visiveis=1,
        dicas=[
            "O nome do destinatário é lido diretamente com `input(...)`.",
            "O peso pode ter casas decimais, então use `float(input(...))`.",
        ],
        explicacao=(
            "Combinamos leituras em texto (`dest`, `cidade`) com uma leitura numérica (`float` para `peso`) "
            "e formatamos tudo numa única f-string."
        ),
    )


@exercicio(estagio=3, dificuldade=5, tipo="codigo", conceitos=["input", "conversao", "fstring"])
def salario_por_horas_e_bonus(r):
    casos = [
        (r.randint(100, 180), round(r.uniform(20.0, 55.0), 2), round(r.uniform(100.0, 500.0), 2)),
        (r.randint(80, 160), round(r.uniform(15.0, 40.0), 2), 0.0),
        (160, 25.50, 300.00),
    ]
    h0, vh0, b0 = casos[0]
    tot0 = h0 * vh0 + b0
    return dict(
        titulo="Folha de pagamento simples",
        enunciado=(
            "Leia três valores (um por linha):\n"
            "1. Horas trabalhadas no mês (`int`)\n"
            "2. Valor pago por hora (`float`)\n"
            "3. Bônus fixo (`float`)\n\n"
            "Calcule o salário total (`horas * valor_hora + bonus`) e imprima:\n"
            f"Exemplo (`{h0}`, `{vh0:.2f}`, `{b0:.2f}`):\n"
            f"```\nSalário base: R$ {h0 * vh0:.2f}\nBônus: R$ {b0:.2f}\nTotal: R$ {tot0:.2f}\n```"
        ),
        solucao=(
            'horas = int(input("Horas: "))\n'
            'valor_hora = float(input("Valor/hora: "))\n'
            'bonus = float(input("Bônus: "))\n'
            "base = horas * valor_hora\n"
            "total = base + bonus\n"
            'print(f"Salário base: R$ {base:.2f}")\n'
            'print(f"Bônus: R$ {bonus:.2f}")\n'
            'print(f"Total: R$ {total:.2f}")\n'
        ),
        testes=[{"entrada": f"{h}\n{vh:.2f}\n{b:.2f}"} for h, vh, b in casos],
        testes_visiveis=1,
        dicas=[
            "Leia na ordem exata: `int` primeiro, depois dois `float`.",
            "Guarde `horas * valor_hora` em `base` para reutilizar tanto na exibição quanto na soma de `total`.",
        ],
        explicacao=(
            "Separar o cálculo em `base` e `total` evita calcular `horas * valor_hora` duas vezes e garante consistência "
            "nas três linhas impressas."
        ),
    )


@exercicio(estagio=3, dificuldade=5, tipo="codigo", conceitos=["input", "conversao", "fstring"])
def ficha_viagem_tres_entradas(r):
    casos = [
        (r.choice(CIDADES), r.randint(150, 600), round(r.uniform(55.0, 95.0), 1)),
        (r.choice(CIDADES), r.randint(200, 800), round(r.uniform(60.0, 100.0), 1)),
        ("Salvador", 300, 75.0),
    ]
    d0, km0, v0 = casos[0]
    t0 = km0 / v0
    return dict(
        titulo="Planejando a viagem",
        enunciado=(
            "Leia, um por linha:\n"
            "1. Cidade de destino (`str`)\n"
            "2. Distância em km (`int`)\n"
            "3. Velocidade média esperada em km/h (`float`)\n\n"
            "Calcule o tempo estimado (`distancia / velocidade`) e mostre com 2 casas decimais:\n"
            f"Exemplo (`{d0}`, `{km0}`, `{v0}`):\n"
            f"```\nDestino: {d0}\nDistância: {km0} km\nTempo estimado: {t0:.2f} horas\n```"
        ),
        solucao=(
            'destino = input("Destino: ")\n'
            'distancia = int(input("Distância (km): "))\n'
            'velocidade = float(input("Velocidade média (km/h): "))\n'
            "tempo = distancia / velocidade\n"
            'print(f"Destino: {destino}")\n'
            'print(f"Distância: {distancia} km")\n'
            'print(f"Tempo estimado: {tempo:.2f} horas")\n'
        ),
        testes=[{"entrada": f"{d}\n{km}\n{v}"} for d, km, v in casos],
        testes_visiveis=1,
        dicas=[
            "Atenção às três leituras em ordem: texto, inteiro e decimal.",
            "O tempo de viagem é dado por `distancia / velocidade`.",
        ],
        explicacao=(
            "Lemos os três dados com os tipos adequados e aplicamos a fórmula da velocidade média (`t = d / v`), "
            "formatando o tempo com `:.2f`."
        ),
    )
