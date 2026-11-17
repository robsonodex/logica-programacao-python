"""Estágio 2 - Tipos de dados (int, float, str, bool), conversões e f-strings."""

from .base import exercicio

PRODUTOS = ["Café", "Caderno", "Mochila", "Fone", "Caneta", "Garrafa", "Livro"]


@exercicio(estagio=2, dificuldade=1, tipo="codigo", conceitos=["tipos", "fstring"])
def ficha_com_fstring(r):
    nome = r.choice(["Ana", "Bruno", "Camila", "Daniel", "Eduarda", "Felipe"])
    idade = r.randint(16, 45)
    altura = round(r.uniform(1.55, 1.92), 2)
    return dict(
        titulo="Ficha formatada com f-string",
        enunciado=(
            f"Crie as variáveis `nome = \"{nome}\"`, `idade = {idade}` e `altura = {altura:.2f}`.\n\n"
            "Usando uma **f-string** (`f\"...\"`), imprima exatamente:\n"
            f"```\n{nome} tem {idade} anos e mede {altura:.2f}m.\n```"
        ),
        solucao=(
            f'nome = "{nome}"\n'
            f"idade = {idade}\n"
            f"altura = {altura:.2f}\n"
            'print(f"{nome} tem {idade} anos e mede {altura:.2f}m.")\n'
        ),
        dicas=[
            "Coloque a letra `f` antes das aspas no `print` e escreva os nomes das variáveis entre `{ }`.",
            "Para manter duas casas decimais mesmo se terminar em zero, use `{altura:.2f}`.",
        ],
        explicacao=(
            "A f-string substitui automaticamente `{nome}`, `{idade}` e `{altura:.2f}` pelos valores das variáveis, "
            "sem precisar usar `+` nem `str()`. O `:.2f` garante sempre duas casas decimais."
        ),
    )


@exercicio(estagio=2, dificuldade=1, tipo="prever", conceitos=["tipos", "teste_de_mesa"])
def prever_tipos_basicos(r):
    inteiro = r.randint(5, 50)
    decimal = round(r.uniform(1.2, 9.8), 1)
    texto = str(r.randint(10, 99))
    ativo = r.choice([True, False])
    return dict(
        titulo="Descubra o tipo de cada caixa",
        enunciado=(
            "A função `type()` mostra o tipo de um valor no formato `<class '...'>`.\n\n"
            "Sem executar, escreva exatamente o que o programa abaixo imprime."
        ),
        solucao=(
            f"a = {inteiro}\n"
            f"b = {decimal}\n"
            f'c = "{texto}"\n'
            f"d = {ativo}\n"
            "print(type(a))\n"
            "print(type(b))\n"
            "print(type(c))\n"
            "print(type(d))\n"
        ),
        dicas=[
            "Números sem ponto são `int`; com ponto são `float`; tudo entre aspas é `str`; `True`/`False` são `bool`.",
            "Lembre do formato exato que `type()` imprime: `<class 'int'>`, `<class 'float'>`, etc.",
        ],
        explicacao=(
            f"`{inteiro}` é `int`, `{decimal}` é `float`, `\"{texto}\"` está entre aspas então é `str` (mesmo contendo dígitos), "
            f"e `{ativo}` é `bool`."
        ),
    )


@exercicio(estagio=2, dificuldade=2, tipo="corrigir", conceitos=["tipos", "conversao", "depuracao"])
def corrigir_soma_texto_numero(r):
    a = r.randint(10, 40)
    b = r.randint(5, 30)
    return dict(
        titulo="Texto não se soma com número!",
        enunciado=(
            f"O programa deveria somar os valores `{a}` e `{b}` e mostrar:\n"
            f"```\nSoma: {a + b}\n```\n"
            "Mas um deles veio como texto e ocorreu um erro. Corrija convertendo para o tipo certo."
        ),
        codigo_inicial=(
            f'preco_texto = "{a}"\n'
            f"taxa = {b}\n"
            "total = preco_texto + taxa\n"
            'print("Soma:", total)\n'
        ),
        solucao=(
            f'preco_texto = "{a}"\n'
            f"taxa = {b}\n"
            "total = int(preco_texto) + taxa\n"
            'print("Soma:", total)\n'
        ),
        dicas=[
            "Veja o erro `TypeError`: você não pode somar `str` com `int`.",
            "Use `int(preco_texto)` para transformar o texto em número inteiro antes de somar.",
        ],
        explicacao=(
            "Como `preco_texto` está entre aspas, seu tipo é `str`. Somar `str` com `int` causa `TypeError`. "
            "Convertendo com `int(preco_texto)`, os dois lados viram inteiros e a soma funciona."
        ),
    )


@exercicio(estagio=2, dificuldade=2, tipo="completar", conceitos=["conversao", "fstring"])
def completar_etiqueta_preco(r):
    prod = r.choice(PRODUTOS)
    qtd = r.randint(2, 7)
    preco = round(r.uniform(3.15, 19.85), 2)
    return dict(
        titulo="Valor com duas casas decimais",
        enunciado=(
            f"Complete as lacunas `___` convertendo a string `preco_str` para decimal (`float`) e exibindo o total "
            f"com duas casas decimais:\n\n"
            f"Saída esperada:\n```\n{qtd}x {prod} = R$ {qtd * preco:.2f}\n```"
        ),
        codigo_inicial=(
            f'produto = "{prod}"\n'
            f"qtd = {qtd}\n"
            f'preco_str = "{preco:.2f}"\n'
            "preco = ___(preco_str)\n"
            "total = qtd * preco\n"
            'print(f"{qtd}x {produto} = R$ {total:___}")\n'
        ),
        solucao=(
            f'produto = "{prod}"\n'
            f"qtd = {qtd}\n"
            f'preco_str = "{preco:.2f}"\n'
            "preco = float(preco_str)\n"
            "total = qtd * preco\n"
            'print(f"{qtd}x {produto} = R$ {total:.2f}")\n'
        ),
        dicas=[
            "Como `preco_str` tem casas decimais, use `float(...)`, não `int(...)`.",
            "Dentro das chaves da f-string, o especificador para 2 casas decimais é `.2f`.",
        ],
        explicacao=(
            "Usamos `float(preco_str)` porque números com ponto decimal não podem ir direto para `int()`. "
            "Depois `{total:.2f}` garante a exibição no padrão monetário com duas casas."
        ),
    )


@exercicio(estagio=2, dificuldade=2, tipo="prever", conceitos=["tipos", "conversao", "teste_de_mesa"])
def prever_int_corta_decimal(r):
    a = r.randint(2, 9)
    b = r.randint(6, 9)
    c = r.randint(1, 4)
    val1 = float(f"{a}.{b}")
    val2 = float(f"{c}.9")
    return dict(
        titulo="int() arredonda ou corta?",
        enunciado=(
            "Observe com cuidado a diferença entre `int()` e `round()`. "
            "Sem executar, escreva exatamente a saída gerada pelo código."
        ),
        solucao=(
            f"x = {val1}\n"
            f"y = {val2}\n"
            "print(int(x))\n"
            "print(int(y))\n"
            "print(round(x))\n"
        ),
        dicas=[
            "`int()` aplicado a um `float` **trunca** (corta fora tudo depois do ponto).",
            "`round(x)` arredonda para o inteiro mais próximo.",
        ],
        explicacao=(
            f"`int({val1})` simplesmente descarta `.{b}`, resultando em `{int(val1)}`. "
            f"`int({val2})` descarta `.9`, resultando em `{int(val2)}`. Já `round({val1})` arredonda para `{round(val1)}`."
        ),
    )


@exercicio(estagio=2, dificuldade=2, tipo="codigo", conceitos=["tipos", "fstring"])
def linha_decorativa_repeticao(r):
    simbolo = r.choice(["=", "-", "*", "#"])
    largura = r.randint(12, 24)
    palavra = r.choice(["AVISO", "RELATÓRIO", "BOLETIM", "PLACAR"])
    return dict(
        titulo="Repetindo textos com *",
        enunciado=(
            f"Em Python, multiplicar uma string por um inteiro repete o texto! Por exemplo, `\"-\" * 3` gera `\"---\"`.\n\n"
            f"Crie `traco = \"{simbolo}\" * {largura}` e `titulo = \"{palavra}\"` e imprima:\n"
            f"```\n{simbolo * largura}\n{palavra}\n{simbolo * largura}\n```"
        ),
        solucao=(
            f'traco = "{simbolo}" * {largura}\n'
            f'titulo = "{palavra}"\n'
            "print(traco)\n"
            "print(titulo)\n"
            "print(traco)\n"
        ),
        dicas=[
            "Você pode multiplicar um caractere (`str`) por um número (`int`) usando `*`.",
            "Guarde a linha pronta em `traco` e imprima antes e depois de `titulo`.",
        ],
        explicacao=(
            "Quando multiplicamos uma `str` por um `int`, o Python repete aquela string tantas vezes quantas o número indicar. "
            "Se os dois fossem `str`, daria erro!"
        ),
    )


@exercicio(estagio=2, dificuldade=3, tipo="prever", conceitos=["conversao", "tipos", "teste_de_mesa"])
def prever_bool_valores(r):
    n = r.randint(1, 9)
    texto_vazio = ""
    texto_zero = "0"
    return dict(
        titulo="O que vira True e o que vira False?",
        enunciado=(
            "A função `bool()` converte qualquer valor para booleano (`True` ou `False`).\n\n"
            "Lembre que textos não vazios são considerados verdadeiros. Escreva a saída exata do código:"
        ),
        solucao=(
            f"print(bool({n}))\n"
            "print(bool(0))\n"
            f'print(bool("{texto_vazio}"))\n'
            f'print(bool("{texto_zero}"))\n'
        ),
        dicas=[
            "Zero (`0` ou `0.0`) e string vazia (`\"\"`) viram `False`.",
            "Cuidado com `\"0\"`: é uma string que contém um caractere, portanto **não** está vazia!",
        ],
        explicacao=(
            f"`bool({n})` é `True` (número diferente de zero); `bool(0)` é `False`; `bool(\"\")` é `False` (texto vazio); "
            "`bool(\"0\")` é `True`, porque `\"0\"` é uma string de tamanho 1, não o número zero."
        ),
    )


@exercicio(estagio=2, dificuldade=3, tipo="corrigir", conceitos=["tipos", "fstring", "depuracao"])
def corrigir_fstring_e_decimal(r):
    prod = r.choice(PRODUTOS)
    valor = round(r.uniform(12.1, 49.9), 2)
    return dict(
        titulo="F-string esquecida",
        enunciado=(
            f"O código deveria imprimir:\n```\nProduto: {prod} - R$ {valor:.2f}\n```\n"
            "Mas está imprimindo literalmente `{produto}` e `{valor:.2f}`, além de estar com o número como texto. Corrija!"
        ),
        codigo_inicial=(
            f'produto = "{prod}"\n'
            f'valor = "{valor:.2f}"\n'
            'print("Produto: {produto} - R$ {valor:.2f}")\n'
        ),
        solucao=(
            f'produto = "{prod}"\n'
            f"valor = {valor:.2f}\n"
            'print(f"Produto: {produto} - R$ {valor:.2f}")\n'
        ),
        dicas=[
            "Para que `{produto}` seja substituído pelo valor, falta uma letrinha antes das aspas.",
            "O especificador `:.2f` só funciona para números (`float`/`int`), não para `str` — remova as aspas ou converta `valor` com `float()`.",
        ],
        explicacao=(
            "Faltava o prefixo `f` antes das aspas da string (`f\"...\"`), e `valor` estava guardado como `str` "
            "(formatação `:.2f` exige valor numérico)."
        ),
    )


@exercicio(estagio=2, dificuldade=3, tipo="completar", conceitos=["conversao", "tipos"])
def completar_juntar_codigo_numerico(r):
    prefixo = r.choice(["PED", "ID", "NF", "COD"])
    num = r.randint(100, 999)
    return dict(
        titulo="Montando código de pedido com str()",
        enunciado=(
            f"Temos a letra/sigla `\"{prefixo}\"` e o número inteiro `{num}`. Complete as lacunas `___` para juntar os dois "
            "com `+` (usando `str()`) e também mostrar o número seguinte:\n\n"
            f"Saída esperada:\n```\n{prefixo}-{num}\nPróximo: {num + 1}\n```"
        ),
        codigo_inicial=(
            f'prefixo = "{prefixo}"\n'
            f"numero = {num}\n"
            'codigo = prefixo + "-" + ___(numero)\n'
            "proximo = numero + ___\n"
            "print(codigo)\n"
            'print("Próximo:", proximo)\n'
        ),
        solucao=(
            f'prefixo = "{prefixo}"\n'
            f"numero = {num}\n"
            'codigo = prefixo + "-" + str(numero)\n'
            "proximo = numero + 1\n"
            "print(codigo)\n"
            'print("Próximo:", proximo)\n'
        ),
        dicas=[
            "O operador `+` só junta `str` com `str`. Converta `numero` para texto dentro da concatenação.",
            "Para calcular o próximo número, `numero` continua sendo inteiro, então basta somar `1`.",
        ],
        explicacao=(
            "`str(numero)` gera uma cópia em texto apenas para montar `codigo`, mantendo a variável original `numero` "
            "como `int` para podermos somar `1` na linha seguinte."
        ),
    )


@exercicio(estagio=2, dificuldade=3, tipo="codigo", conceitos=["conversao", "fstring"])
def nota_fiscal_conversao(r):
    a = r.randint(10, 35)
    b = round(r.uniform(2.25, 8.75), 2)
    total = int(a) * b
    return dict(
        titulo="Convertendo dados de texto para conta",
        enunciado=(
            f"Imagine que um sistema antigo guardou os dados como texto: `qtd_txt = \"{a}\"` e `preco_txt = \"{b:.2f}\"`.\n\n"
            "Crie essas duas variáveis exatamente como texto, converta cada uma para o tipo numérico adequado (`int` e `float`), "
            "calcule `total` e imprima com uma f-string no formato:\n"
            f"```\nTotal da compra: R$ {total:.2f}\n```"
        ),
        solucao=(
            f'qtd_txt = "{a}"\n'
            f'preco_txt = "{b:.2f}"\n'
            "qtd = int(qtd_txt)\n"
            "preco = float(preco_txt)\n"
            "total = qtd * preco\n"
            'print(f"Total da compra: R$ {total:.2f}")\n'
        ),
        dicas=[
            "Converta `qtd_txt` com `int()` e `preco_txt` com `float()`.",
            "No `print`, use `{total:.2f}` dentro de uma f-string.",
        ],
        explicacao=(
            "Cada texto é convertido para o seu tipo numérico natural (`int` para quantidade inteira, `float` para preço com centavos). "
            "Só então fazemos a multiplicação e formatamos a saída com `:.2f`."
        ),
    )


@exercicio(estagio=2, dificuldade=4, tipo="corrigir", conceitos=["conversao", "tipos", "depuracao"])
def corrigir_int_de_string_decimal(r):
    peso = round(r.uniform(2.5, 9.8), 1)
    fator = r.randint(3, 6)
    return dict(
        titulo="ValueError no int()",
        enunciado=(
            f"O código tenta converter o texto `\"{peso}\"` em número inteiro para multiplicar por `{fator}`, mas quebra com `ValueError`.\n\n"
            "Corrija usando a conversão adequada (convertendo para `float` primeiro e depois para `int` para pegar só a parte inteira do peso) "
            f"de modo a imprimir:\n```\nResultado: {int(peso) * fator}\n```"
        ),
        codigo_inicial=(
            f'peso_txt = "{peso}"\n'
            "peso_inteiro = int(peso_txt)\n"
            f"resultado = peso_inteiro * {fator}\n"
            'print("Resultado:", resultado)\n'
        ),
        solucao=(
            f'peso_txt = "{peso}"\n'
            "peso_inteiro = int(float(peso_txt))\n"
            f"resultado = peso_inteiro * {fator}\n"
            'print("Resultado:", resultado)\n'
        ),
        dicas=[
            "`int(\"3.7\")` falha porque o ponto decimal não é um dígito válido para conversão direta de string em inteiro.",
            "Converta primeiro com `float(peso_txt)` e envolva o resultado em `int(...)`.",
        ],
        explicacao=(
            "`int()` aceita strings apenas quando representam inteiros puros (como `\"42\"`). Ao fazer `int(float(peso_txt))`, "
            "primeiro obtemos o decimal e depois cortamos a parte fracionária."
        ),
    )


@exercicio(estagio=2, dificuldade=4, tipo="prever", conceitos=["tipos", "conversao", "fstring", "teste_de_mesa"])
def prever_concatenacao_vs_soma(r):
    n1 = r.randint(1, 9)
    n2 = r.randint(1, 9)
    return dict(
        titulo="Quando + soma e quando + gruda",
        enunciado=(
            "Atenção ao tipo de cada variável! O operador `+` se comporta de forma diferente para `int` e para `str`.\n\n"
            "Escreva exatamente a saída produzida pelo código:"
        ),
        solucao=(
            f'a = "{n1}"\n'
            f'b = "{n2}"\n'
            "c = int(a) + int(b)\n"
            "d = a + b\n"
            "print(c)\n"
            "print(d)\n"
            'print(f"{c} e {d}")\n'
        ),
        dicas=[
            "`a` e `b` são strings! Somar duas strings (`a + b`) **concatena** (gruda uma na outra).",
            "Já `int(a) + int(b)` soma os valores numéricos.",
        ],
        explicacao=(
            f"`int(\"{n1}\") + int(\"{n2}\")` soma os inteiros dando `{n1 + n2}`. Já `\"{n1}\" + \"{n2}\"` concatena os textos, "
            f"formando `\"{n1}{n2}\"`."
        ),
    )


@exercicio(estagio=2, dificuldade=4, tipo="completar", conceitos=["conversao", "fstring", "tipos"])
def completar_horario_dois_digitos(r):
    h = r.randint(1, 9)
    m = r.randint(0, 9)
    s = r.randint(10, 59)
    return dict(
        titulo="Relógio com zero à esquerda",
        enunciado=(
            f"Queremos mostrar o horário `{h:02d}:{m:02d}:{s:02d}` preenchendo números de 1 dígito com zero à esquerda.\n\n"
            "Complete as lacunas `___` usando o formato `:02d` na f-string:\n"
            f"```\nHora atual: {h:02d}:{m:02d}:{s:02d}\n```"
        ),
        codigo_inicial=(
            f"hora = {h}\n"
            f"minuto = {m}\n"
            f"segundo = {s}\n"
            'print(f"Hora atual: {hora:___}:{minuto:___}:{segundo:___}")\n'
        ),
        solucao=(
            f"hora = {h}\n"
            f"minuto = {m}\n"
            f"segundo = {s}\n"
            'print(f"Hora atual: {hora:02d}:{minuto:02d}:{segundo:02d}")\n'
        ),
        dicas=[
            "Dentro da f-string, `:02d` significa: inteiro (`d`) com largura mínima 2 preenchida com zeros (`02`).",
            "Repita o mesmo especificador `02d` para `hora`, `minuto` e `segundo`.",
        ],
        explicacao=(
            "O formato `:02d` formata inteiros garantindo 2 dígitos: `7` vira `07`, `0` vira `00`, e números que já têm 2 dígitos como `45` permanecem iguais."
        ),
    )


@exercicio(estagio=2, dificuldade=5, tipo="codigo", conceitos=["conversao", "fstring", "tipos"])
def tabela_arredondamento(r):
    v = round(r.uniform(12.345, 89.876), 3)
    return dict(
        titulo="Cortar, arredondar ou formatar?",
        enunciado=(
            f"Crie a variável `valor = {v}`.\n\n"
            "Mostre em três linhas diferentes:\n"
            "1. A parte inteira cortada com `int(valor)` -> `Inteiro: ...`\n"
            "2. O valor arredondado para 1 casa com `round(valor, 1)` -> `1 casa: ...`\n"
            "3. O valor formatado com 2 casas usando f-string -> `2 casas: ...`\n\n"
            f"Saída esperada:\n```\nInteiro: {int(v)}\n1 casa: {round(v, 1)}\n2 casas: {v:.2f}\n```"
        ),
        solucao=(
            f"valor = {v}\n"
            'print("Inteiro:", int(valor))\n'
            'print("1 casa:", round(valor, 1))\n'
            'print(f"2 casas: {valor:.2f}")\n'
        ),
        dicas=[
            "Use `int(valor)` na primeira linha e `round(valor, 1)` na segunda.",
            "Na terceira linha, use `f\"2 casas: {valor:.2f}\"`.",
        ],
        explicacao=(
            "`int()` corta as casas decimais sem arredondar; `round(valor, 1)` arredonda para 1 casa; "
            "e `{valor:.2f}` arredonda na exibição mantendo sempre exatamente duas casas."
        ),
    )


@exercicio(estagio=2, dificuldade=5, tipo="corrigir", conceitos=["tipos", "conversao", "fstring", "depuracao"])
def corrigir_relatorio_tipos(r):
    qtd = r.randint(3, 8)
    unit = round(r.uniform(4.25, 14.75), 2)
    extra = r.randint(2, 7)
    total = qtd * unit + extra
    return dict(
        titulo="Consertando todos os tipos do resumo",
        enunciado=(
            "Este relatório tem vários problemas de tipo e formatação. Ele deveria imprimir exatamente:\n"
            f"```\nItens: {qtd}\nTotal: R$ {total:.2f}\n```\n"
            "Corrija o código mantendo o uso das variáveis iniciais."
        ),
        codigo_inicial=(
            f'qtd_txt = "{qtd}"\n'
            f'unit_txt = "{unit:.2f}"\n'
            f"taxa_extra = {extra}\n"
            "total = qtd_txt * unit_txt + taxa_extra\n"
            'print("Itens:", qtd_txt)\n'
            'print("Total: R$ {total:.2f}")\n'
        ),
        solucao=(
            f'qtd_txt = "{qtd}"\n'
            f'unit_txt = "{unit:.2f}"\n'
            f"taxa_extra = {extra}\n"
            "total = int(qtd_txt) * float(unit_txt) + taxa_extra\n"
            'print("Itens:", qtd_txt)\n'
            'print(f"Total: R$ {total:.2f}")\n'
        ),
        dicas=[
            "Não se pode multiplicar duas strings (`qtd_txt * unit_txt`). Converta uma para `int` e a outra para `float`.",
            "No último `print`, faltou o `f` da f-string!",
        ],
        explicacao=(
            "Corrigimos as conversões (`int(qtd_txt)` e `float(unit_txt)`) para que a conta aritmética funcione, "
            "e adicionamos o `f` antes das aspas no último `print` para formatar `total` com duas casas decimais."
        ),
    )
