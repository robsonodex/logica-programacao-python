"""Estágio 5 - Comparação e lógica (==, !=, <, >, <=, >=, and, or, not)."""

from .base import exercicio

NOMES = ["Ana", "Bruno", "Carla", "Diego", "Elisa", "Fábio", "Gabi", "Heitor", "Iara", "João"]


@exercicio(estagio=5, dificuldade=1, tipo="codigo", conceitos=["comparacao", "input", "conversao"])
def pode_pela_idade(r):
    acao, limite = r.choice([
        ("tirar a carteira de motorista", 18),
        ("votar", 16),
        ("ver um filme de classificação 14 anos", 14),
        ("andar sozinho na montanha-russa", 12),
        ("ter a meia-entrada de idoso", 60),
    ])
    idades = [limite, limite - 1, r.randint(limite + 1, limite + 30), r.randint(1, limite - 2)]
    exemplo = idades[0]
    return dict(
        titulo="Já tem idade?",
        enunciado=(
            f"Para **{acao}** é preciso ter **{limite} anos ou mais**.\n\n"
            "Escreva um programa que lê a idade de uma pessoa (um número inteiro) e mostra `True` se ela "
            "pode ou `False` se não pode. **Não use if** — a própria comparação já responde a pergunta!\n\n"
            f"Exemplo: se a idade digitada for {exemplo}, a saída deve ser:\n"
            f"```\nPode {acao}? {exemplo >= limite}\n```"
        ),
        solucao=(
            'idade = int(input("Idade: "))\n'
            f"pode = idade >= {limite}\n"
            f'print("Pode {acao}?", pode)\n'
        ),
        testes=[{"entrada": str(i)} for i in idades],
        testes_visiveis=2,
        dicas=[
            "Uma comparação como `idade >= 18` vale `True` ou `False` — e esse valor pode ser guardado numa variável ou impresso.",
            f"\"{limite} anos ou mais\" inclui o próprio {limite}: use `>=`, e não `>`.",
            f"Estrutura: `pode = idade >= {limite}` e depois `print(\"Pode {acao}?\", pode)`.",
        ],
        explicacao=(
            f"A expressão `idade >= {limite}` é uma pergunta que o Python responde com `True` ou `False`. "
            "Guardamos a resposta numa variável e a imprimimos ao lado do texto. "
            f"O erro mais comum é usar `>`: aí quem tem exatamente {limite} anos ficaria de fora."
        ),
    )


@exercicio(estagio=5, dificuldade=1, tipo="prever", conceitos=["comparacao", "teste_de_mesa"])
def prever_comparacoes_basicas(r):
    a = r.randint(1, 20)
    b = r.choice([a, r.randint(1, 20), r.randint(1, 20)])
    return dict(
        titulo="Verdadeiro ou falso?",
        enunciado=(
            "Sem executar, escreva exatamente o que o programa abaixo vai mostrar. "
            "Lembre que cada `print` de uma comparação mostra `True` ou `False`."
        ),
        solucao=(
            f"a = {a}\n"
            f"b = {b}\n"
            "print(a > b)\n"
            "print(a == b)\n"
            "print(a != b)\n"
            "print(a <= b)\n"
        ),
        dicas=[
            "Troque mentalmente `a` e `b` pelos seus valores e responda cada pergunta com sim (True) ou não (False).",
            "`==` pergunta \"é igual?\", `!=` pergunta \"é diferente?\" e `<=` pergunta \"é menor **ou igual**?\".",
        ],
        explicacao=(
            f"Com a = {a} e b = {b}: `{a} > {b}` é {a > b}, `{a} == {b}` é {a == b}, "
            f"`{a} != {b}` é {a != b} e `{a} <= {b}` é {a <= b}. "
            "Repare que `==` e `!=` sempre dão respostas opostas, e que `<=` é verdadeiro também quando os valores são iguais."
        ),
    )


@exercicio(estagio=5, dificuldade=2, tipo="completar", conceitos=["comparacao", "aritmeticos"])
def senha_par_fila(r):
    brinquedo = r.choice(["roda-gigante", "carrossel", "trem fantasma", "barco viking"])
    par = r.randrange(2, 200, 2)
    impar = r.randrange(1, 200, 2)
    testes = [par, impar, 0, r.randrange(201, 999, 2) + 1, r.randrange(201, 999, 2)]
    return dict(
        titulo="Fila A ou fila B?",
        enunciado=(
            f"Na fila do **{brinquedo}**, quem tem senha **par** vai para a fila A. "
            "Complete as lacunas `___` para que o programa leia a senha (inteiro) e mostre `True` se a pessoa "
            "vai para a fila A, ou `False` caso contrário.\n\n"
            f"Exemplo para a senha {par}:\n```\nFila A: True\n```"
        ),
        codigo_inicial=(
            'senha = int(input("Senha: "))\n'
            "eh_par = senha ___ 2 == ___\n"
            'print("Fila A:", eh_par)\n'
        ),
        solucao=(
            'senha = int(input("Senha: "))\n'
            "eh_par = senha % 2 == 0\n"
            'print("Fila A:", eh_par)\n'
        ),
        testes=[{"entrada": str(t)} for t in testes],
        dicas=[
            "Um número é par quando a divisão por 2 não deixa resto.",
            "O operador `%` dá o resto da divisão. Qual deve ser o resto para o número ser par?",
            "A expressão fica `senha % 2 == 0`.",
        ],
        explicacao=(
            "`senha % 2` calcula o resto da divisão por 2: dá 0 para pares e 1 para ímpares. "
            "Comparando esse resto com `== 0` obtemos diretamente `True` ou `False`. "
            "O zero também é par, pois 0 dividido por 2 não deixa resto."
        ),
    )


@exercicio(estagio=5, dificuldade=2, tipo="prever", conceitos=["logicos", "teste_de_mesa"])
def prever_tabela_verdade(r):
    v1, v2 = r.choice([
        ("tem_ingresso", "tem_documento"),
        ("choveu", "tem_guarda_chuva"),
        ("estudou", "dormiu_bem"),
        ("tem_saldo", "cartao_valido"),
        ("fez_aquecimento", "bebeu_agua"),
    ])
    a = r.choice([True, False])
    b = r.choice([True, False])
    return dict(
        titulo="Tabela-verdade na prática",
        enunciado=(
            "Faça o teste de mesa e escreva exatamente o que será mostrado.\n\n"
            "Lembre: `and` só é `True` se **os dois** forem `True`; `or` é `True` se **pelo menos um** for `True`; "
            "`not` inverte o valor."
        ),
        solucao=(
            f"{v1} = {a}\n"
            f"{v2} = {b}\n"
            f"print({v1} and {v2})\n"
            f"print({v1} or {v2})\n"
            f"print(not {v1})\n"
            f"print(not {v1} or {v2})\n"
        ),
        dicas=[
            "Resolva uma linha de cada vez, trocando cada variável pelo seu valor.",
            f"Na última linha, o `not` é feito **antes** do `or`: primeiro calcule `not {v1}`.",
        ],
        explicacao=(
            f"Com {v1} = {a} e {v2} = {b}: `and` dá {a and b}, `or` dá {a or b} e `not {v1}` dá {not a}. "
            f"Na última linha, o Python calcula primeiro `not {v1}` ({not a}) e depois faz o `or` com {b}, "
            f"resultando em {(not a) or b}. O `not` tem prioridade maior que `and` e `or`."
        ),
    )


@exercicio(estagio=5, dificuldade=3, tipo="codigo", conceitos=["comparacao", "logicos", "input", "conversao"])
def temperatura_ideal(r):
    lugar, mn, mx = r.choice([
        ("aquário de peixes tropicais", 24, 28),
        ("piscina aquecida", 26, 30),
        ("adega de vinhos", 10, 14),
        ("estufa de orquídeas", 18, 26),
        ("geladeira de vacinas", 2, 8),
    ])
    meio = r.randint(mn + 1, mx - 1)
    testes = [meio, mn, mx, mn - r.randint(1, 5), mx + r.randint(1, 5), f"{mx}.5"]
    return dict(
        titulo="Está na faixa certa?",
        enunciado=(
            f"Um sensor mede a temperatura de uma **{lugar}**. Ela é ideal quando está **entre {mn} e {mx} graus, "
            "incluindo os extremos**.\n\n"
            "Escreva um programa que lê a temperatura (número real, `float`) e mostra `True` se ela é ideal "
            "ou `False` se não é. Não use if.\n\n"
            f"Exemplo para a temperatura {meio}:\n```\nTemperatura ideal: True\n```"
        ),
        solucao=(
            'temperatura = float(input("Temperatura: "))\n'
            f"ideal = temperatura >= {mn} and temperatura <= {mx}\n"
            'print("Temperatura ideal:", ideal)\n'
        ),
        testes=[{"entrada": str(t)} for t in testes],
        testes_visiveis=2,
        dicas=[
            "\"Estar entre dois valores\" são duas condições ao mesmo tempo: não pode estar abaixo do mínimo **e** não pode passar do máximo.",
            "Use `and` para juntar as duas comparações. Como os extremos contam, use `>=` e `<=`.",
            f"Estrutura: `ideal = temperatura >= {mn} and temperatura <= {mx}`.",
        ],
        explicacao=(
            f"A temperatura é ideal só se as duas condições forem verdadeiras: `temperatura >= {mn}` **e** "
            f"`temperatura <= {mx}`, por isso usamos `and`. Se usássemos `or`, qualquer valor passaria em pelo menos "
            f"uma das condições. Em Python também dá para escrever `{mn} <= temperatura <= {mx}`, que significa o mesmo."
        ),
    )


@exercicio(estagio=5, dificuldade=3, tipo="corrigir", conceitos=["comparacao", "conversao", "depuracao"])
def cofre_sem_conversao(r):
    senha = r.randint(1000, 9999)
    errada = r.choice([senha + 1, senha - 1, r.randint(1000, 9999)])
    if errada == senha:
        errada = senha + 2
    testes = [senha, errada, int(str(senha)[::-1]) + 10000]
    return dict(
        titulo="O cofre que nunca abre",
        enunciado=(
            f"O cofre digital deveria abrir quando a pessoa digita a senha **{senha}**. "
            "O programa lê a tentativa e mostra `True` se ela está certa ou `False` se está errada:\n"
            f"```\nCofre aberto: True\n```\n"
            "Mas mesmo digitando a senha certa ele sempre mostra `False`. Encontre e corrija o bug."
        ),
        codigo_inicial=(
            f"senha_correta = {senha}\n"
            'tentativa = input("Digite a senha: ")\n'
            'print("Cofre aberto:", tentativa == senha_correta)\n'
        ),
        solucao=(
            f"senha_correta = {senha}\n"
            'tentativa = int(input("Digite a senha: "))\n'
            'print("Cofre aberto:", tentativa == senha_correta)\n'
        ),
        testes=[{"entrada": str(t)} for t in testes],
        dicas=[
            "Qual é o tipo do valor que o `input()` devolve? E qual é o tipo de `senha_correta`?",
            f"Para o Python, o texto `\"{senha}\"` e o número `{senha}` são coisas diferentes, então `==` dá `False`.",
            "Converta a tentativa com `int(...)` antes de comparar.",
        ],
        explicacao=(
            "O `input()` sempre devolve um texto (str). Comparar um texto com um número usando `==` nunca dá `True`, "
            "porque são tipos diferentes — e o Python nem avisa com erro. Convertendo a entrada com `int()`, "
            "comparamos número com número e o cofre abre quando deve."
        ),
    )


@exercicio(estagio=5, dificuldade=3, tipo="completar", conceitos=["comparacao", "logicos", "aritmeticos"])
def aprovacao_media_frequencia(r):
    m = r.choice([5, 6, 7])
    f = r.choice([70, 75, 80])
    testes = [
        (m - 1, m + 1, f),
        (r.randint(m + 1, 10), 10, f - r.randint(1, 10)),
        (m - 2, m - 1, 100),
        (m, r.randint(m, 10), r.randint(f + 1, 100)),
        (r.randint(0, m - 1), r.randint(0, m - 1), r.randint(0, f - 1)),
    ]
    return dict(
        titulo="Passou de ano?",
        enunciado=(
            f"Na escola, o aluno é aprovado se a **média das duas notas for pelo menos {m}** **e** a "
            f"**frequência for pelo menos {f}%**.\n\n"
            "O programa lê a nota 1, a nota 2 (números reais) e a frequência (inteiro), nessa ordem. "
            "Complete as lacunas `___`.\n\n"
            f"Exemplo para as notas {m - 1} e {m + 1} e frequência {f}:\n"
            f"```\nMédia: {m:.1f}\nAprovado: True\n```"
        ),
        codigo_inicial=(
            'nota1 = float(input("Nota 1: "))\n'
            'nota2 = float(input("Nota 2: "))\n'
            'frequencia = int(input("Frequência (%): "))\n'
            "media = ___\n"
            f"aprovado = media >= {m} ___ frequencia >= {f}\n"
            'print(f"Média: {media:.1f}")\n'
            'print("Aprovado:", aprovado)\n'
        ),
        solucao=(
            'nota1 = float(input("Nota 1: "))\n'
            'nota2 = float(input("Nota 2: "))\n'
            'frequencia = int(input("Frequência (%): "))\n'
            "media = (nota1 + nota2) / 2\n"
            f"aprovado = media >= {m} and frequencia >= {f}\n"
            'print(f"Média: {media:.1f}")\n'
            'print("Aprovado:", aprovado)\n'
        ),
        testes=[{"entrada": f"{a}\n{b}\n{c}"} for a, b, c in testes],
        testes_visiveis=2,
        dicas=[
            "A média de duas notas é a soma dividida por 2 — cuidado com a ordem das contas!",
            "Sem parênteses, `nota1 + nota2 / 2` divide só a nota2. Use `(nota1 + nota2) / 2`.",
            "As duas exigências precisam ser cumpridas ao mesmo tempo: qual operador lógico exige isso?",
        ],
        explicacao=(
            "Os parênteses garantem que a soma seja feita antes da divisão. Depois, como o aluno precisa cumprir "
            f"**as duas** regras (média ≥ {m} e frequência ≥ {f}%), juntamos as comparações com `and`: basta uma "
            "delas ser `False` para o resultado ser `False`."
        ),
    )


@exercicio(estagio=5, dificuldade=3, tipo="prever", conceitos=["comparacao", "logicos", "precedencia", "teste_de_mesa"])
def prever_precedencia_logica(r):
    a, b, c = r.sample(range(1, 21), 3)
    return dict(
        titulo="Quem o Python resolve primeiro?",
        enunciado=(
            "Escreva exatamente o que o programa vai mostrar.\n\n"
            "Ordem de prioridade: primeiro as **comparações** (`<`, `>`...), depois o `not`, depois o `and` "
            "e, por último, o `or`."
        ),
        solucao=(
            f"a = {a}\n"
            f"b = {b}\n"
            f"c = {c}\n"
            "print(a > b and b > c)\n"
            "print(a > b or b > c)\n"
            "print(not a > b)\n"
            "print(a < b or b < c and c < a)\n"
        ),
        dicas=[
            "Calcule primeiro cada comparação isolada (`a > b`, `b > c`...) e anote True/False embaixo de cada uma.",
            "Na última linha o `and` é feito antes do `or`: é como se fosse `a < b or (b < c and c < a)`.",
        ],
        explicacao=(
            f"Com a={a}, b={b}, c={c}: `a > b` é {a > b}, `b > c` é {b > c}. Assim, a linha 1 dá {a > b and b > c} "
            f"e a linha 2 dá {a > b or b > c}. O `not a > b` primeiro compara e depois inverte: {not a > b}. "
            f"Na última, o Python resolve `b < c and c < a` ({b < c and c < a}) antes do `or` com `a < b` ({a < b}), "
            f"resultando em {a < b or b < c and c < a}."
        ),
    )


@exercicio(estagio=5, dificuldade=3, tipo="codigo", conceitos=["comparacao", "logicos", "input"])
def login_usuario_senha(r):
    usuario = r.choice(["ana", "bruno", "carla", "diego", "elisa", "fabio", "gabi", "heitor"])
    senha = r.choice(["gato", "sol", "lua", "pipoca", "trem", "pizza"]) + str(r.randint(10, 99))
    outro = r.choice(["admin", "visitante", "teste", "root"])
    testes = [
        (usuario, senha),
        (usuario, senha + "0"),
        (outro, senha),
        (usuario.capitalize(), senha),
        (outro, "123456"),
    ]
    return dict(
        titulo="Tela de login",
        enunciado=(
            f"Um sistema só libera o acesso para o usuário `{usuario}` com a senha `{senha}`.\n\n"
            "Escreva um programa que lê o usuário e a senha (dois textos, um por linha) e mostra `True` se os "
            "**dois** estiverem corretos ou `False` caso contrário. Atenção: letras maiúsculas e minúsculas fazem diferença.\n\n"
            f"Exemplo (usuário `{usuario}`, senha `{senha}`):\n```\nAcesso liberado: True\n```"
        ),
        solucao=(
            'usuario = input("Usuário: ")\n'
            'senha = input("Senha: ")\n'
            f'liberado = usuario == "{usuario}" and senha == "{senha}"\n'
            'print("Acesso liberado:", liberado)\n'
        ),
        testes=[{"entrada": f"{u}\n{s}"} for u, s in testes],
        testes_visiveis=2,
        dicas=[
            "Textos também podem ser comparados com `==`: `\"ana\" == \"ana\"` é True.",
            "São duas condições que precisam ser verdadeiras juntas — use `and`.",
            f"Estrutura: `liberado = usuario == \"{usuario}\" and senha == \"{senha}\"`.",
        ],
        explicacao=(
            "Comparar textos com `==` verifica se eles são exatamente iguais, letra por letra — por isso "
            f"`\"{usuario.capitalize()}\"` é diferente de `\"{usuario}\"`. Como usuário **e** senha precisam estar certos, "
            "juntamos as duas comparações com `and`."
        ),
    )


@exercicio(estagio=5, dificuldade=3, tipo="corrigir", conceitos=["logicos", "comparacao", "depuracao"])
def frete_gratis_and_or(r):
    loja = r.choice(["livraria", "loja de games", "farmácia", "pet shop", "loja de roupas"])
    lim = r.choice([79, 99, 120, 150, 199])
    testes = [
        (lim + r.randint(1, 80), "s"),
        (lim, "n"),
        (lim - r.randint(1, 40), "s"),
        (lim - r.randint(1, 40), "n"),
        (lim + r.randint(1, 80), "n"),
    ]
    return dict(
        titulo="Frete grátis para quem?",
        enunciado=(
            f"Numa **{loja}** online, o frete é grátis se a compra for de **pelo menos R$ {lim}** **ou** se o "
            "cliente for VIP. O programa lê o valor da compra (número real) e se o cliente é VIP (`s` ou `n`), "
            "e mostra `True` ou `False`:\n"
            "```\nFrete grátis: True\n```\n"
            "Mas clientes que deveriam ganhar frete grátis estão pagando. Encontre e corrija o bug."
        ),
        codigo_inicial=(
            'valor = float(input("Valor da compra: "))\n'
            'vip = input("Cliente VIP (s/n)? ")\n'
            f'frete_gratis = valor >= {lim} and vip == "s"\n'
            'print("Frete grátis:", frete_gratis)\n'
        ),
        solucao=(
            'valor = float(input("Valor da compra: "))\n'
            'vip = input("Cliente VIP (s/n)? ")\n'
            f'frete_gratis = valor >= {lim} or vip == "s"\n'
            'print("Frete grátis:", frete_gratis)\n'
        ),
        testes=[{"entrada": f"{v}\n{s}"} for v, s in testes],
        dicas=[
            f"Teste mentalmente um cliente que **não** é VIP mas comprou R$ {lim + 50}. O que o código mostra?",
            "Releia a regra: basta **uma** das duas condições ser verdadeira.",
            "`and` exige as duas; `or` aceita qualquer uma.",
        ],
        explicacao=(
            "O código usava `and`, que só dá `True` quando as duas condições são verdadeiras: só o VIP que gastou "
            f"muito ganhava frete. A regra diz \"pelo menos R$ {lim} **ou** VIP\", então o operador certo é `or`, "
            "que dá `True` quando qualquer uma delas é verdadeira."
        ),
    )


@exercicio(estagio=5, dificuldade=3, tipo="codigo", conceitos=["comparacao", "logicos", "aritmeticos"])
def forma_triangulo(r):
    k = r.randint(1, 4)
    a, b = r.randint(2, 9), r.randint(2, 9)
    testes = [
        (3 * k, 4 * k, 5 * k),
        (a, b, a + b),
        (r.randint(1, 3), r.randint(1, 3), r.randint(10, 20)),
        (a, a, a),
        (r.randint(15, 25), r.randint(2, 5), r.randint(2, 5)),
        (a + b - 1, a, b),
    ]
    ex = testes[0]
    return dict(
        titulo="Dá para montar o triângulo?",
        enunciado=(
            "Você tem três palitos de tamanhos diferentes. Eles só formam um triângulo se **cada lado for menor "
            "que a soma dos outros dois**.\n\n"
            "Escreva um programa que lê os três tamanhos (inteiros, um por linha) e mostra `True` se formam um "
            "triângulo ou `False` se não formam. Não use if.\n\n"
            f"Exemplo para {ex[0]}, {ex[1]} e {ex[2]}:\n```\nForma triângulo: True\n```"
        ),
        solucao=(
            'a = int(input("Lado 1: "))\n'
            'b = int(input("Lado 2: "))\n'
            'c = int(input("Lado 3: "))\n'
            "forma = a < b + c and b < a + c and c < a + b\n"
            'print("Forma triângulo:", forma)\n'
        ),
        testes=[{"entrada": f"{x}\n{y}\n{z}"} for x, y, z in testes],
        testes_visiveis=2,
        dicas=[
            "São três verificações: uma para cada lado.",
            "Escreva `a < b + c`, `b < a + c` e `c < a + b`. Como todas precisam valer, junte com `and`.",
            "Cuidado com o caso em que um lado é **igual** à soma dos outros: os palitos ficam deitados numa linha reta e não formam triângulo.",
        ],
        explicacao=(
            "Se algum lado for maior ou igual à soma dos outros dois, as pontas não se encontram. Por isso testamos os "
            "três lados e exigimos que **todas** as condições sejam verdadeiras com `and`. "
            "Usamos `<` (e não `<=`) porque, quando um lado é igual à soma dos outros, o 'triângulo' vira uma linha reta."
        ),
    )


def _bissexto(ano):
    return (ano % 4 == 0 and ano % 100 != 0) or ano % 400 == 0


@exercicio(estagio=5, dificuldade=4, tipo="codigo", conceitos=["comparacao", "logicos", "aritmeticos"])
def ano_bissexto(r):
    div400 = r.choice([1600, 2000, 2400])
    div100 = r.choice([1700, 1800, 1900, 2100, 2200, 2300])
    div4 = r.choice([y for y in range(1904, 2100, 4) if y % 100 != 0])
    comum = r.choice([y for y in range(1901, 2100) if y % 4 != 0])
    testes = [div4, comum, div100, div400]
    r.shuffle(testes)
    ex = testes[0]
    return dict(
        titulo="Fevereiro tem 29 dias?",
        enunciado=(
            "Um ano é **bissexto** se:\n"
            "- for divisível por 4 **e não** for divisível por 100; **ou**\n"
            "- for divisível por 400.\n\n"
            "Escreva um programa que lê um ano (inteiro) e mostra `True` se ele é bissexto ou `False` se não é. "
            "Não use if.\n\n"
            f"Exemplo para o ano {ex}:\n```\nBissexto: {_bissexto(ex)}\n```"
        ),
        solucao=(
            'ano = int(input("Ano: "))\n'
            "bissexto = (ano % 4 == 0 and ano % 100 != 0) or ano % 400 == 0\n"
            'print("Bissexto:", bissexto)\n'
        ),
        testes=[{"entrada": str(t)} for t in testes],
        testes_visiveis=2,
        dicas=[
            "\"Divisível por 4\" em Python é `ano % 4 == 0`; \"não divisível por 100\" é `ano % 100 != 0`.",
            "A primeira regra junta duas condições com `and`; as duas regras se juntam com `or`.",
            "Estrutura: `(divisível por 4 and não divisível por 100) or divisível por 400`.",
        ],
        explicacao=(
            "Cada regra vira uma comparação com `%`. A primeira regra exige duas coisas ao mesmo tempo (`and`), "
            "e o ano é bissexto se cumprir a primeira regra **ou** a segunda (`or`). Os parênteses deixam a "
            "intenção clara. Por isso 1900 não é bissexto (divisível por 100, mas não por 400) e 2000 é."
        ),
    )


@exercicio(estagio=5, dificuldade=4, tipo="corrigir", conceitos=["logicos", "precedencia", "depuracao"])
def brinde_parenteses(r):
    loja = r.choice(["sorveteria", "livraria", "loja de brinquedos", "cafeteria", "papelaria"])
    n = r.randint(3, 6)
    testes = [
        (n, "s", "n"),
        (n + r.randint(1, 4), "n", "s"),
        (n - r.randint(1, n - 1), "n", "s"),
        (n - 1, "s", "n"),
        (n + r.randint(1, 4), "n", "n"),
    ]
    return dict(
        titulo="O brinde generoso demais",
        enunciado=(
            f"Numa **{loja}**, o cliente ganha um brinde se comprar **pelo menos {n} itens** **e** "
            "(for aniversariante **ou** tiver cupom).\n\n"
            "O programa lê a quantidade de itens (inteiro), se é aniversariante (`s`/`n`) e se tem cupom (`s`/`n`), "
            "e mostra:\n```\nGanha brinde: True\n```\n"
            f"Mas clientes com cupom que compraram menos de {n} itens também estão ganhando o brinde. Corrija o bug."
        ),
        codigo_inicial=(
            'itens = int(input("Quantidade de itens: "))\n'
            'aniversariante = input("Aniversariante (s/n)? ")\n'
            'cupom = input("Tem cupom (s/n)? ")\n'
            f'brinde = itens >= {n} and aniversariante == "s" or cupom == "s"\n'
            'print("Ganha brinde:", brinde)\n'
        ),
        solucao=(
            'itens = int(input("Quantidade de itens: "))\n'
            'aniversariante = input("Aniversariante (s/n)? ")\n'
            'cupom = input("Tem cupom (s/n)? ")\n'
            f'brinde = itens >= {n} and (aniversariante == "s" or cupom == "s")\n'
            'print("Ganha brinde:", brinde)\n'
        ),
        testes=[{"entrada": f"{i}\n{a}\n{c}"} for i, a, c in testes],
        testes_visiveis=2,
        dicas=[
            "Teste mentalmente: 1 item, não aniversariante, com cupom. O que deveria dar? O que o código dá?",
            "O `and` é calculado **antes** do `or`. Então o código está fazendo `(itens e aniversário) or cupom`.",
            "Use parênteses para agrupar o `or`: `itens >= ... and (... or ...)`.",
        ],
        explicacao=(
            "Como o `and` tem prioridade sobre o `or`, o código original era lido como "
            f"`(itens >= {n} and aniversariante == \"s\") or cupom == \"s\"` — ou seja, ter cupom bastava. "
            "Os parênteses forçam o `or` a ser resolvido primeiro, e o resultado dele é que precisa andar junto "
            "com a quantidade mínima de itens."
        ),
    )


@exercicio(estagio=5, dificuldade=4, tipo="prever", conceitos=["comparacao", "strings", "teste_de_mesa"])
def prever_comparar_strings(r):
    f1, f2 = r.sample(["abacaxi", "banana", "caju", "damasco", "goiaba", "laranja", "manga", "uva"], 2)
    cap = r.choice(["Zebra", "Urso", "Tatu", "Pato"])
    low = r.choice(["abelha", "baleia", "coruja", "foca"])
    x = r.randint(10, 99)
    y = r.randint(2, 9)
    w = r.choice(["casa", "bola", "gato", "mesa", "sapo"])
    w2 = r.choice([w, w.capitalize()])
    return dict(
        titulo="Comparando textos",
        enunciado=(
            "Textos também podem ser comparados! O Python compara **letra por letra**, da esquerda para a direita, "
            "seguindo a ordem da tabela de caracteres: os dígitos vêm antes das letras maiúsculas, que vêm "
            "**antes** de todas as minúsculas.\n\n"
            "Escreva exatamente o que o programa vai mostrar."
        ),
        solucao=(
            f'print("{f1}" < "{f2}")\n'
            f'print("{cap}" < "{low}")\n'
            f'print("{x}" < "{y}")\n'
            f"print({x} < {y})\n"
            f'print("{w}" == "{w2}")\n'
        ),
        dicas=[
            "Entre palavras minúsculas, `<` funciona como a ordem do dicionário: a que vem antes é a \"menor\".",
            "Qualquer letra maiúscula é \"menor\" que qualquer minúscula. E com textos de números, compara-se o primeiro caractere: `\"5\"` vs `\"3\"`...",
            "Com aspas é texto (compara caractere por caractere); sem aspas é número (compara o valor).",
        ],
        explicacao=(
            f"`\"{f1}\" < \"{f2}\"` é {f1 < f2} pela ordem alfabética. `\"{cap}\" < \"{low}\"` é True porque maiúsculas vêm "
            f"antes das minúsculas. `\"{x}\" < \"{y}\"` compara textos: o primeiro caractere `{str(x)[0]}` contra `{y}`, "
            f"dando {str(x) < str(y)} — já como números, `{x} < {y}` é {x < y}. Por fim, `==` exige textos idênticos, "
            f"inclusive maiúsculas: {w == w2}."
        ),
    )


@exercicio(estagio=5, dificuldade=4, tipo="completar", conceitos=["comparacao", "logicos", "aritmeticos"])
def saque_caixa_eletronico(r):
    saldo = r.randrange(200, 900, 10)
    limite = r.choice([300, 500, 600, 800, 1000])
    menor = min(saldo, limite)
    testes = [
        menor - r.randrange(10, 100, 10),
        menor - 5,
        saldo,
        limite,
        max(saldo, limite) + 50,
        0,
    ]
    ex = testes[0]
    return dict(
        titulo="Pode sacar?",
        enunciado=(
            f"Um caixa eletrônico só tem notas de 10 reais. A conta tem saldo de **R$ {saldo}** e o limite de saque "
            f"diário é **R$ {limite}**. Um saque só é permitido se o valor:\n"
            "- for maior que zero;\n"
            "- for múltiplo de 10;\n"
            "- não passar do saldo;\n"
            "- não passar do limite diário.\n\n"
            "O programa lê o valor do saque (inteiro). Complete as lacunas `___`.\n\n"
            f"Exemplo para o valor {ex}:\n```\nMúltiplo de 10: True\nPode sacar: True\n```"
        ),
        codigo_inicial=(
            f"saldo = {saldo}\n"
            'valor = int(input("Valor do saque: "))\n'
            "multiplo_de_10 = valor % 10 == ___\n"
            "tem_saldo = valor ___ saldo\n"
            f"dentro_do_limite = valor <= {limite}\n"
            "pode_sacar = valor > 0 and multiplo_de_10 and ___ and ___\n"
            'print("Múltiplo de 10:", multiplo_de_10)\n'
            'print("Pode sacar:", pode_sacar)\n'
        ),
        solucao=(
            f"saldo = {saldo}\n"
            'valor = int(input("Valor do saque: "))\n'
            "multiplo_de_10 = valor % 10 == 0\n"
            "tem_saldo = valor <= saldo\n"
            f"dentro_do_limite = valor <= {limite}\n"
            "pode_sacar = valor > 0 and multiplo_de_10 and tem_saldo and dentro_do_limite\n"
            'print("Múltiplo de 10:", multiplo_de_10)\n'
            'print("Pode sacar:", pode_sacar)\n'
        ),
        testes=[{"entrada": str(t)} for t in testes],
        testes_visiveis=2,
        dicas=[
            "Um número é múltiplo de 10 quando o resto da divisão por 10 é zero.",
            "\"Não passar do saldo\" quer dizer menor **ou igual** ao saldo.",
            "Guardar cada condição numa variável com nome claro deixa a expressão final fácil de ler: basta juntar todas com `and`.",
        ],
        explicacao=(
            "Cada regra virou uma variável booleana com nome explicativo. Como o saque só pode acontecer se **todas** "
            "as regras forem cumpridas, juntamos tudo com `and`. Usamos `<=` porque sacar exatamente o saldo "
            "(ou exatamente o limite) é permitido."
        ),
    )


@exercicio(estagio=5, dificuldade=5, tipo="codigo", conceitos=["comparacao", "logicos", "input", "conversao"])
def aniversario_primeiro(r):
    n1, n2 = r.sample(NOMES, 2)
    m = r.randint(2, 11)
    d = r.randint(2, 27)
    testes = [
        (d, m, d, m + 1),
        (r.randint(1, 28), m + 1, r.randint(1, 28), m),
        (d, m, d + 1, m),
        (d + 1, m, d, m),
        (d, m, d, m),
        (r.randint(20, 31), 1, r.randint(1, 5), 12),
    ]
    ex = testes[0]
    return dict(
        titulo="Quem faz aniversário primeiro?",
        enunciado=(
            f"**{n1}** e **{n2}** querem saber quem faz aniversário antes no ano.\n\n"
            f"Escreva um programa que lê, nesta ordem, o dia e o mês do aniversário de {n1} e depois o dia e o mês "
            f"do aniversário de {n2} (quatro inteiros, um por linha). Mostre `True` se o aniversário de {n1} vem "
            f"**antes** do de {n2} no calendário, ou `False` caso contrário (inclusive se for no mesmo dia). Não use if.\n\n"
            f"Exemplo para {n1} em {ex[0]}/{ex[1]} e {n2} em {ex[2]}/{ex[3]}:\n"
            f"```\n{n1} faz aniversário antes: True\n```"
        ),
        solucao=(
            'dia1 = int(input("Dia (1ª pessoa): "))\n'
            'mes1 = int(input("Mês (1ª pessoa): "))\n'
            'dia2 = int(input("Dia (2ª pessoa): "))\n'
            'mes2 = int(input("Mês (2ª pessoa): "))\n'
            "antes = mes1 < mes2 or (mes1 == mes2 and dia1 < dia2)\n"
            f'print("{n1} faz aniversário antes:", antes)\n'
        ),
        testes=[{"entrada": f"{a}\n{b}\n{c}\n{e}"} for a, b, c, e in testes],
        testes_visiveis=2,
        dicas=[
            "O mês é mais importante que o dia: 30/01 vem antes de 02/02, mesmo com 30 > 2.",
            "Há dois jeitos de vir antes: estar num mês menor, **ou** estar no mesmo mês com um dia menor.",
            "Estrutura: `mes1 < mes2 or (mes1 == mes2 and dia1 < dia2)`.",
        ],
        explicacao=(
            "Comparar datas é como comparar palavras no dicionário: primeiro olhamos o mês; só se os meses forem "
            "iguais é que o dia desempata. Por isso a condição tem duas partes ligadas por `or`, e a segunda parte "
            "exige mês igual **e** dia menor. Comparar só os dias (ou somar dia + mês) dá respostas erradas."
        ),
    )
