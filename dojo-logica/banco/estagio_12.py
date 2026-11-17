"""Estágio 12 - Funções (def, parâmetros, return, valor padrão e escopo)."""

from .base import exercicio


@exercicio(estagio=12, dificuldade=1, tipo="funcao", conceitos=["funcoes", "return"])
def funcao_dobro_e_soma(r):
    fator = r.choice([2, 3, 4, 5])
    nome_f = {2: "dobro", 3: "triplo", 4: "quadruplo", 5: "quintuplo"}[fator]
    vals = [r.randint(2, 10), r.randint(11, 25), 0, -r.randint(1, 9)]
    return dict(
        titulo=f"Função {nome_f}(n)",
        enunciado=(
            f"Escreva uma função chamada `{nome_f}(n)` que receba um número `n` e **retorne** (`return`) `n * {fator}`.\n\n"
            f"**Atenção:** a função deve usar `return` (não `print`).\n"
            f"Exemplo: `{nome_f}({vals[0]})` deve retornar `{vals[0] * fator}`."
        ),
        solucao=(
            f"def {nome_f}(n):\n"
            f"    return n * {fator}\n"
        ),
        testes=[{"entrada": "", "chamada": f"print({nome_f}({v}))"} for v in vals],
        testes_visiveis=2,
        dicas=[
            f"Comece com `def {nome_f}(n):` e dentro dela retorne o cálculo com `return`.",
            "Não coloque `input()` nem `print()` dentro da função — os testes vão chamar sua função diretamente.",
        ],
        explicacao=(
            f"A função `{nome_f}` recebe `n` como parâmetro e devolve `n * {fator}` usando `return`, "
            "permitindo que quem a chamou use ou imprima o resultado."
        ),
    )


@exercicio(estagio=12, dificuldade=1, tipo="completar", conceitos=["funcoes", "return", "comparacao"])
def completar_eh_par(r):
    vals = [r.randrange(2, 30, 2), r.randrange(3, 31, 2), 0, -r.randint(1, 10)]
    return dict(
        titulo="Função booleana eh_par(n)",
        enunciado=(
            "Complete as lacunas `___` para que a função `eh_par(n)` retorne `True` se `n` for par, ou `False` caso contrário.\n\n"
            f"Exemplo: `eh_par({vals[0]})` -> `True`"
        ),
        codigo_inicial=(
            "___ eh_par(n):\n"
            "    ___ n % 2 == 0\n"
        ),
        solucao=(
            "def eh_par(n):\n"
            "    return n % 2 == 0\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(eh_par({v}))"} for v in vals],
        testes_visiveis=2,
        dicas=[
            "Use `def` para definir a função e `return` para devolver o resultado booleano.",
            "A expressão `n % 2 == 0` já vale `True` ou `False`, não precisa de `if/else`!",
        ],
        explicacao=(
            "Retornar diretamente uma expressão booleana (`return n % 2 == 0`) é mais curto e limpo do que escrever `if ...: return True else: return False`."
        ),
    )


@exercicio(estagio=12, dificuldade=2, tipo="corrigir", conceitos=["funcoes", "return", "depuracao"])
def corrigir_print_em_vez_de_return(r):
    a = r.randint(3, 9)
    b = r.randint(4, 10)
    vals = [(a, b), (r.randint(2, 8), r.randint(2, 8)), (10, 5), (0, 7)]
    return dict(
        titulo="A função que devolve None!",
        enunciado=(
            "O programa define `area_retangulo(largura, altura)` e depois usa o valor retornado em outra conta (`area * 2`).\n"
            "Mas está dando `TypeError` porque a função está usando `print()` no lugar de `return`!\n\n"
            f"Para `({a}, {b})`, `print(area_retangulo({a}, {b}) * 2)` deveria mostrar `{a * b * 2}`. Corrija a função."
        ),
        codigo_inicial=(
            "def area_retangulo(largura, altura):\n"
            "    area = largura * altura\n"
            "    print(area)\n"
        ),
        solucao=(
            "def area_retangulo(largura, altura):\n"
            "    area = largura * altura\n"
            "    return area\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(area_retangulo({x}, {y}) * 2)"} for x, y in vals],
        testes_visiveis=1,
        dicas=[
            "Uma função sem `return` devolve automaticamente `None` (`None * 2` gera `TypeError`).",
            "Troque `print(area)` por `return area`.",
        ],
        explicacao=(
            "`print()` apenas escreve na tela e devolve `None`. Quando queremos usar o resultado em contas ou guardá-lo em variáveis, "
            "precisamos usar `return`."
        ),
    )


@exercicio(estagio=12, dificuldade=2, tipo="prever", conceitos=["funcoes", "return", "teste_de_mesa"])
def prever_escopo_local_funcao(r):
    x_fora = r.randint(10, 30)
    soma = r.randint(3, 9)
    return dict(
        titulo="Variável de dentro não muda a de fora!",
        enunciado=(
            "Variáveis criadas ou alteradas dentro de uma função são **locais**.\n\n"
            "Faça o teste de mesa e escreva exatamente a saída do código:"
        ),
        solucao=(
            "def alterar(x):\n"
            f"    x = x + {soma}\n"
            "    print(x)\n"
            "    return x\n"
            "\n"
            f"x = {x_fora}\n"
            "y = alterar(x)\n"
            "print(x)\n"
            "print(y)\n"
        ),
        dicas=[
            "Quando `alterar(x)` roda, um `x` local nasce dentro da função; somar nele **não altera** o `x` de fora.",
            "Já `y` recebe o valor devolvido pelo `return x`.",
        ],
        explicacao=(
            f"Dentro da função o `x` local vira `{x_fora + soma}` e é impresso e retornado para `y`. "
            f"Mas o `x` global continua valendo `{x_fora}`."
        ),
    )


@exercicio(estagio=12, dificuldade=2, tipo="funcao", conceitos=["funcoes", "return", "elif"])
def funcao_maior_de_tres(r):
    casos = [
        (r.randint(10, 30), r.randint(31, 60), r.randint(1, 9)),
        (r.randint(40, 80), r.randint(10, 39), r.randint(5, 20)),
        (r.randint(1, 10), r.randint(11, 20), r.randint(50, 90)),
        (-5, -2, -10),
        (7, 7, 3),
    ]
    a0, b0, c0 = casos[0]
    return dict(
        titulo="Função maior_de_tres(a, b, c)",
        enunciado=(
            "Escreva uma função `maior_de_tres(a, b, c)` que receba três números e **retorne** o maior deles "
            "(sem usar a função pronta `max()`).\n\n"
            f"Exemplo: `maior_de_tres({a0}, {b0}, {c0})` retorna `{max(a0, b0, c0)}`."
        ),
        solucao=(
            "def maior_de_tres(a, b, c):\n"
            "    maior = a\n"
            "    if b > maior:\n"
            "        maior = b\n"
            "    if c > maior:\n"
            "        maior = c\n"
            "    return maior\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(maior_de_tres({a}, {b}, {c}))"} for a, b, c in casos],
        testes_visiveis=1,
        dicas=[
            "Comece supondo `maior = a`.",
            "Teste `if b > maior:` e depois `if c > maior:` (dois `if` separados, não `elif`!), e dê `return maior`.",
        ],
        explicacao=(
            "Assumir `maior = a` e atualizar com dois `if`s independentes funciona inclusive para números negativos e empates."
        ),
    )


@exercicio(estagio=12, dificuldade=3, tipo="funcao", conceitos=["funcoes", "return", "for_range"])
def funcao_fatorial_e_combinacao(r):
    casos = [0, 1, r.randint(3, 5), r.randint(6, 7)]
    return dict(
        titulo="Função fatorial(n)",
        enunciado=(
            "Escreva uma função `fatorial(n)` que receba um inteiro `n >= 0` e retorne `n!`.\n\n"
            f"Exemplo: `fatorial({casos[2]})` retorna `{1 if casos[2] <= 1 else __import__('math').factorial(casos[2])}`."
        ),
        solucao=(
            "def fatorial(n):\n"
            "    res = 1\n"
            "    for i in range(1, n + 1):\n"
            "        res *= i\n"
            "    return res\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(fatorial({v}))"} for v in casos],
        testes_visiveis=2,
        dicas=[
            "Inicie `res = 1` e multiplique por `i` para `i` em `range(1, n + 1)`.",
            "No final, use `return res`.",
        ],
        explicacao=(
            "Encapsular o cálculo em `fatorial(n)` permite reutilizá-lo em fórmulas maiores sem duplicar o laço."
        ),
    )


@exercicio(estagio=12, dificuldade=3, tipo="funcao", conceitos=["funcoes", "return", "fstring"])
def funcao_valor_padrao_desconto(r):
    taxa_padrao = r.choice([10, 15, 20])
    p0 = r.randint(80, 200)
    t_custom = r.choice([25, 30, 5])
    return dict(
        titulo=f"Parâmetro com valor padrão (taxa={taxa_padrao})",
        enunciado=(
            f"Escreva uma função `preco_com_desconto(preco, desconto={taxa_padrao})` onde o segundo parâmetro tem valor padrão `{taxa_padrao}` (%).\n\n"
            "A função deve retornar o preço final **arredondado para 2 casas** (`round(..., 2)`).\n"
            f"Exemplo:\n"
            f"- `preco_com_desconto({p0})` -> usa `{taxa_padrao}%` -> `{round(p0 * (1 - taxa_padrao / 100), 2)}`\n"
            f"- `preco_com_desconto({p0}, {t_custom})` -> usa `{t_custom}%` -> `{round(p0 * (1 - t_custom / 100), 2)}`"
        ),
        solucao=(
            f"def preco_com_desconto(preco, desconto={taxa_padrao}):\n"
            "    final = preco * (1 - desconto / 100)\n"
            "    return round(final, 2)\n"
        ),
        testes=[
            {"entrada": "", "chamada": f"print(f'{{preco_com_desconto({p0}):.2f}}')"},
            {"entrada": "", "chamada": f"print(f'{{preco_com_desconto({p0}, {t_custom}):.2f}}')"},
            {"entrada": "", "chamada": "print(f'{preco_com_desconto(100):.2f}')"},
            {"entrada": "", "chamada": "print(f'{preco_com_desconto(100, 50):.2f}')"},
        ],
        testes_visiveis=2,
        dicas=[
            f"Na assinatura, escreva `def preco_com_desconto(preco, desconto={taxa_padrao}):`.",
            "Se quem chama não passar o 2º argumento, `desconto` assume o valor padrão automaticamente.",
        ],
        explicacao=(
            "Parâmetros com valor padrão tornam argumentos opcionais, mantendo a função prática para o caso comum e flexível quando precisar personalizar."
        ),
    )


@exercicio(estagio=12, dificuldade=3, tipo="corrigir", conceitos=["funcoes", "return", "listas", "depuracao"])
def corrigir_return_precoce_laco(r):
    alvo = r.randint(10, 30)
    l1 = [r.randint(1, 9), alvo, r.randint(31, 40)]
    l2 = [alvo, 5, 6]
    l3 = [1, 2, 3]
    l4 = [4, 8, alvo]
    return dict(
        titulo="Return prematuro dentro do laço!",
        enunciado=(
            "A função `contem(lista, alvo)` deveria retornar `True` se `alvo` estiver em qualquer posição da lista, "
            "ou `False` se não estiver.\n\n"
            "Mas ela só acerta quando `alvo` é o **primeiro** item da lista! Descubra o bug clássico e corrija."
        ),
        codigo_inicial=(
            "def contem(lista, alvo):\n"
            "    for item in lista:\n"
            "        if item == alvo:\n"
            "            return True\n"
            "        else:\n"
            "            return False\n"
        ),
        solucao=(
            "def contem(lista, alvo):\n"
            "    for item in lista:\n"
            "        if item == alvo:\n"
            "            return True\n"
            "    return False\n"
        ),
        testes=[
            {"entrada": "", "chamada": f"print(contem({l1}, {alvo}))"},
            {"entrada": "", "chamada": f"print(contem({l2}, {alvo}))"},
            {"entrada": "", "chamada": f"print(contem({l3}, {alvo}))"},
            {"entrada": "", "chamada": f"print(contem({l4}, {alvo}))"},
        ],
        testes_visiveis=2,
        dicas=[
            "Assim que o Python encontra um `return`, a função **termina na hora**!",
            "Se o 1º item não for `alvo`, o `else: return False` encerra a função sem olhar o resto da lista. Tire o `return False` de dentro do `for`!",
        ],
        explicacao=(
            "Para ter certeza de que um elemento **não** existe, precisamos terminar o laço inteiro. Por isso `return True` "
            "pode ficar dentro do `if`, mas `return False` só pode acontecer **depois** do `for`."
        ),
    )


@exercicio(estagio=12, dificuldade=3, tipo="prever", conceitos=["funcoes", "return", "teste_de_mesa"])
def prever_funcao_chamando_funcao(r):
    a = r.randint(2, 5)
    b = r.randint(3, 6)
    return dict(
        titulo="Uma função chamando outra",
        enunciado=(
            "Acompanhe a ordem em que as funções são chamadas e o que cada `return` devolve.\n\n"
            "Escreva exatamente a saída produzida:"
        ),
        solucao=(
            "def quadrado(n):\n"
            "    return n * n\n"
            "\n"
            "def soma_quadrados(x, y):\n"
            "    return quadrado(x) + quadrado(y)\n"
            "\n"
            f"res = soma_quadrados({a}, {b})\n"
            "print(res)\n"
        ),
        dicas=[
            f"`soma_quadrados({a}, {b})` primeiro chama `quadrado({a})` e depois `quadrado({b})`.",
            "Some os dois valores retornados por `quadrado` para descobrir o retorno de `soma_quadrados`.",
        ],
        explicacao=(
            f"`quadrado({a})` retorna `{a * a}` e `quadrado({b})` retorna `{b * b}`; `soma_quadrados` soma ambos devolvendo `{a * a + b * b}`."
        ),
    )


@exercicio(estagio=12, dificuldade=3, tipo="completar", conceitos=["funcoes", "return", "listas"])
def completar_filtrar_maiores_funcao(r):
    corte = r.randint(10, 20)
    l1 = [corte - 3, corte, corte + 5, corte + 1, corte - 10]
    l2 = [corte - 5, corte - 1]
    l3 = [corte + 2, corte + 8]
    l4 = []
    return dict(
        titulo="Função que devolve uma nova lista",
        enunciado=(
            "Complete as lacunas `___` da função `filtrar_maiores(lista, limite)` para que ela retorne uma **nova lista** "
            "contendo apenas os números **estritamente maiores** que `limite`.\n\n"
            f"Exemplo: `filtrar_maiores({l1}, {corte})` -> `{[x for x in l1 if x > corte]}`"
        ),
        codigo_inicial=(
            "def filtrar_maiores(lista, limite):\n"
            "    nova = ___\n"
            "    for x in lista:\n"
            "        if x ___ limite:\n"
            "            nova.append(___)\n"
            "    ___ nova\n"
        ),
        solucao=(
            "def filtrar_maiores(lista, limite):\n"
            "    nova = []\n"
            "    for x in lista:\n"
            "        if x > limite:\n"
            "            nova.append(x)\n"
            "    return nova\n"
        ),
        testes=[
            {"entrada": "", "chamada": f"print(filtrar_maiores({l1}, {corte}))"},
            {"entrada": "", "chamada": f"print(filtrar_maiores({l2}, {corte}))"},
            {"entrada": "", "chamada": f"print(filtrar_maiores({l3}, {corte}))"},
            {"entrada": "", "chamada": f"print(filtrar_maiores({l4}, {corte}))"},
        ],
        testes_visiveis=1,
        dicas=[
            "Comece criando uma lista vazia `nova = []` e, ao final do `for`, dê `return nova`.",
            "\"Estritamente maiores\" usa `>`.",
        ],
        explicacao=(
            "Criar uma nova lista acumuladora dentro da função evita modificar a lista original de quem chamou a função."
        ),
    )


@exercicio(estagio=12, dificuldade=4, tipo="funcao", conceitos=["funcoes", "return", "strings"])
def funcao_contar_vogais(r):
    palavras = [
        r.choice(["Python", "Programacao", "Algoritmo", "Abacaxi"]),
        "AEIOU",
        "rhythm",
        "Casa Amarela",
    ]
    p0 = palavras[0]
    v0 = sum(1 for c in p0.lower() if c in "aeiou")
    return dict(
        titulo="Função contar_vogais(texto)",
        enunciado=(
            "Escreva uma função `contar_vogais(texto)` que receba uma string e **retorne** a quantidade de vogais "
            "(`a, e, i, o, u`, maiúsculas ou minúsculas).\n\n"
            f"Exemplo: `contar_vogais(\"{p0}\")` -> `{v0}`"
        ),
        solucao=(
            "def contar_vogais(texto):\n"
            "    total = 0\n"
            "    for c in texto.lower():\n"
            '        if c in "aeiou":\n'
            "            total += 1\n"
            "    return total\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(contar_vogais({p!r}))"} for p in palavras],
        testes_visiveis=1,
        dicas=[
            "Percorra `texto.lower()` com `for` e incremente um contador se `c in \"aeiou\"`.",
            "Retorne o contador no final (`return total`).",
        ],
        explicacao=(
            "A lógica que já praticamos em scripts agora ganha um nome reutilizável que recebe qualquer texto como entrada."
        ),
    )


@exercicio(estagio=12, dificuldade=4, tipo="funcao", conceitos=["funcoes", "return", "for_range"])
def funcao_eh_primo_e_contagem(r):
    casos = [1, 2, 4, r.choice([11, 13, 17, 19]), r.choice([15, 21, 25]), 29]
    return dict(
        titulo="Função eh_primo(n)",
        enunciado=(
            "Escreva uma função `eh_primo(n)` que receba um inteiro `n` e retorne `True` se `n` for primo ou `False` caso contrário.\n\n"
            "Lembre: números menores que `2` (como `1`, `0` e negativos) **não** são primos."
        ),
        solucao=(
            "def eh_primo(n):\n"
            "    if n < 2:\n"
            "        return False\n"
            "    for d in range(2, n):\n"
            "        if n % d == 0:\n"
            "            return False\n"
            "    return True\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(eh_primo({v}))"} for v in casos],
        testes_visiveis=2,
        dicas=[
            "Se `n < 2`, retorne `False` logo no começo.",
            "Para `d` de `2` até `n - 1`: se encontrar qualquer divisor (`n % d == 0`), já pode dar `return False` na hora! Só retorne `True` depois do laço.",
        ],
        explicacao=(
            "Com `return` antecipado dentro do `for`, assim que encontramos um único divisor entre `2` e `n - 1`, "
            "provamos que não é primo e saímos imediatamente sem desperdiçar voltas."
        ),
    )


@exercicio(estagio=12, dificuldade=4, tipo="corrigir", conceitos=["funcoes", "return", "listas", "depuracao"])
def corrigir_parametro_ignorado_e_sem_chamada(r):
    l1 = [r.randint(2, 8), r.randint(9, 15), r.randint(1, 5)]
    l2 = [10, 20, 30, 40]
    l3 = [5]
    return dict(
        titulo="Função ignorando seu parâmetro!",
        enunciado=(
            "A função `media_lista(valores)` deveria calcular a média dos elementos da lista recebida no parâmetro `valores`.\n"
            "Mas o programador esqueceu de usar o parâmetro e criou uma lista fixa lá dentro (e ainda esqueceu de retornar `0` para lista vazia)! Corrija."
        ),
        codigo_inicial=(
            "def media_lista(valores):\n"
            "    valores = [1, 2, 3]\n"
            "    return sum(valores) / len(valores)\n"
        ),
        solucao=(
            "def media_lista(valores):\n"
            "    if len(valores) == 0:\n"
            "        return 0\n"
            "    return sum(valores) / len(valores)\n"
        ),
        testes=[
            {"entrada": "", "chamada": f"print(f'{{media_lista({l1}):.2f}}')"},
            {"entrada": "", "chamada": f"print(f'{{media_lista({l2}):.2f}}')"},
            {"entrada": "", "chamada": f"print(f'{{media_lista({l3}):.2f}}')"},
            {"entrada": "", "chamada": "print(f'{media_lista([]):.2f}')"},
        ],
        testes_visiveis=2,
        dicas=[
            "A linha `valores = [1, 2, 3]` está apagando a lista que foi passada pelo argumento!",
            "Remova essa atribuição fixa e trate `if len(valores) == 0: return 0` para evitar divisão por zero.",
        ],
        explicacao=(
            "Sobrescrever um parâmetro no início da função joga fora o argumento enviado por quem chamou. "
            "Tratar o caso de lista vazia antes de dividir evita `ZeroDivisionError`."
        ),
    )


@exercicio(estagio=12, dificuldade=5, tipo="funcao", conceitos=["funcoes", "return", "listas"])
def funcao_estatisticas_duas_funcoes(r):
    l1 = [r.randint(5, 10), r.randint(4, 9), r.randint(6, 10), r.randint(3, 8)]
    l2 = [8.0, 9.0, 7.0]
    l3 = [4.0, 5.0, 6.0, 10.0]
    return dict(
        titulo="Compondo funções: média e acima da média",
        enunciado=(
            "Crie **duas** funções:\n"
            "1. `media(lista)`: retorna a média aritmética dos números da lista (`0` se vazia).\n"
            "2. `contar_acima_media(lista)`: usa `media(lista)` para descobrir a média e retorna **quantos** elementos da lista "
            "são **estritamente maiores** que essa média.\n\n"
            f"Exemplo: para `{l1}`, média = `{sum(l1)/len(l1):.2f}`, acima = `{sum(1 for x in l1 if x > sum(l1)/len(l1))}`."
        ),
        solucao=(
            "def media(lista):\n"
            "    if len(lista) == 0:\n"
            "        return 0\n"
            "    return sum(lista) / len(lista)\n"
            "\n"
            "def contar_acima_media(lista):\n"
            "    m = media(lista)\n"
            "    cont = 0\n"
            "    for x in lista:\n"
            "        if x > m:\n"
            "            cont += 1\n"
            "    return cont\n"
        ),
        testes=[
            {"entrada": "", "chamada": f"print(f'{{media({l1}):.2f}}', contar_acima_media({l1}))"},
            {"entrada": "", "chamada": f"print(f'{{media({l2}):.2f}}', contar_acima_media({l2}))"},
            {"entrada": "", "chamada": f"print(f'{{media({l3}):.2f}}', contar_acima_media({l3}))"},
            {"entrada": "", "chamada": "print(f'{media([]):.2f}', contar_acima_media([]))"},
        ],
        testes_visiveis=1,
        dicas=[
            "Dentro de `contar_acima_media(lista)`, chame `m = media(lista)` **uma vez** antes do `for`.",
            "Depois conte quantos itens têm `x > m`.",
        ],
        explicacao=(
            "Dividir responsabilidades entre funções pequenas (`media` e `contar_acima_media`) é a essência da modularização: "
            "uma função reaproveita o resultado retornado pela outra."
        ),
    )


@exercicio(estagio=12, dificuldade=5, tipo="codigo", conceitos=["funcoes", "return", "input"])
def programa_completo_com_funcoes(r):
    casos = [
        (r.randint(20, 40), r.randint(25, 45)),
        (10, 20),
        (5, 10),
    ]
    a0, b0 = casos[0]
    p0 = 2 * (a0 + b0)
    ar0 = a0 * b0
    return dict(
        titulo="Programa modularizado com funções",
        enunciado=(
            "Crie duas funções: `calcular_area(base, altura)` e `calcular_perimetro(base, altura)`, ambas usando `return`.\n\n"
            "Em seguida, no programa principal (fora das funções), leia `base` e `altura` inteiros com `input()`, "
            "chame suas duas funções e imprima:\n"
            f"Exemplo (`{a0}` e `{b0}`):\n```\nÁrea: {ar0}\nPerímetro: {p0}\n```"
        ),
        solucao=(
            "def calcular_area(base, altura):\n"
            "    return base * altura\n"
            "\n"
            "def calcular_perimetro(base, altura):\n"
            "    return 2 * (base + altura)\n"
            "\n"
            'b = int(input("Base: "))\n'
            'h = int(input("Altura: "))\n'
            'print("Área:", calcular_area(b, h))\n'
            'print("Perímetro:", calcular_perimetro(b, h))\n'
        ),
        testes=[{"entrada": f"{a}\n{b}"} for a, b in casos],
        testes_visiveis=1,
        dicas=[
            "Defina as duas funções primeiro (com `def` e `return`).",
            "Só depois, fora das funções (sem recuo), faça a leitura com `input()` e chame as funções no `print()`.",
        ],
        explicacao=(
            "Separar a lógica de cálculo em funções puras (que apenas recebem parâmetros e retornam valores) "
            "e deixar `input`/`print` no bloco principal é uma excelente prática de organização."
        ),
    )
