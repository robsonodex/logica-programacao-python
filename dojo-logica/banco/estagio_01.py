"""Estágio 1 - Variáveis e saída (print)."""

from .base import exercicio

NOMES = ["Ana", "Bruno", "Carla", "Diego", "Elisa", "Fábio", "Gabi", "Heitor", "Iara", "João"]
CIDADES = ["Recife", "Curitiba", "Manaus", "Salvador", "Porto Alegre", "Belém", "Natal", "Goiânia"]


@exercicio(estagio=1, dificuldade=1, tipo="codigo", conceitos=["variaveis", "print"])
def cartao_apresentacao(r):
    nome = r.choice(NOMES)
    idade = r.randint(15, 60)
    cidade = r.choice(CIDADES)
    return dict(
        titulo="Cartão de apresentação",
        enunciado=(
            f"Crie três variáveis: `nome` com o valor `\"{nome}\"`, `idade` com o valor `{idade}` "
            f"e `cidade` com o valor `\"{cidade}\"`.\n\n"
            "Depois, usando **as variáveis** (e não os valores escritos direto no print), mostre exatamente:\n"
            f"```\nNome: {nome}\nIdade: {idade}\nCidade: {cidade}\n```"
        ),
        solucao=(
            f'nome = "{nome}"\n'
            f"idade = {idade}\n"
            f'cidade = "{cidade}"\n'
            'print("Nome:", nome)\n'
            'print("Idade:", idade)\n'
            'print("Cidade:", cidade)\n'
        ),
        dicas=[
            "Uma variável é criada com `nome_da_variavel = valor`. Textos ficam entre aspas, números não.",
            "O print aceita vários valores separados por vírgula e coloca um espaço entre eles: `print(\"Nome:\", nome)`.",
        ],
        explicacao=(
            "Cada `=` guarda um valor numa caixinha com nome. Depois, o `print` recebe o texto fixo "
            "e a variável separados por vírgula; o Python troca a variável pelo valor guardado e "
            "coloca um espaço entre os itens automaticamente."
        ),
    )


@exercicio(estagio=1, dificuldade=2, tipo="prever", conceitos=["variaveis", "print", "teste_de_mesa"])
def troca_de_valor(r):
    a = r.randint(2, 9)
    b = r.randint(10, 30)
    return dict(
        titulo="Quem vale quanto?",
        enunciado=(
            "Sem executar, faça o **teste de mesa**: acompanhe linha por linha o valor de cada variável "
            "e escreva exatamente o que o programa abaixo vai mostrar."
        ),
        solucao=(
            f"x = {a}\n"
            f"y = {b}\n"
            "x = y\n"
            f"y = {a + b}\n"
            "print(x)\n"
            "print(y)\n"
        ),
        dicas=[
            "Uma variável guarda só o **último** valor atribuído a ela.",
            "Na linha `x = y`, o x recebe o valor que y tem **naquele momento**. Mudar y depois não muda x.",
        ],
        explicacao=(
            f"x começa com {a} e y com {b}. Em `x = y`, x passa a valer {b}. Depois y recebe {a + b}, "
            f"mas x continua {b}, porque a atribuição copia o valor, não cria um 'link' entre as variáveis."
        ),
    )


@exercicio(estagio=1, dificuldade=2, tipo="corrigir", conceitos=["variaveis", "print", "depuracao"])
def nome_trocado(r):
    produto = r.choice(["caneta", "caderno", "mochila", "garrafa", "fone"])
    preco = r.randint(5, 90)
    return dict(
        titulo="O print que não funciona",
        enunciado=(
            "Este programa deveria mostrar:\n"
            f"```\nProduto: {produto}\nPreço: {preco}\n```\n"
            "mas ele dá erro. Descubra o problema e corrija o código."
        ),
        codigo_inicial=(
            f'produto = "{produto}"\n'
            f"preco = {preco}\n"
            'print("Produto:", produto)\n'
            'print("Preço:", Preco)\n'
        ),
        solucao=(
            f'produto = "{produto}"\n'
            f"preco = {preco}\n"
            'print("Produto:", produto)\n'
            'print("Preço:", preco)\n'
        ),
        dicas=[
            "Leia a mensagem de erro: ela diz o tipo do erro e a linha.",
            "O Python diferencia letras maiúsculas de minúsculas: `preco` e `Preco` são variáveis diferentes.",
        ],
        explicacao=(
            "O erro era um `NameError`: a variável foi criada como `preco` (minúsculo), mas o print usava "
            "`Preco`. Para o Python, são nomes totalmente diferentes."
        ),
    )


@exercicio(estagio=1, dificuldade=3, tipo="completar", conceitos=["variaveis", "print"])
def troca_entre_variaveis(r):
    a = r.randint(1, 50)
    b = r.randint(51, 99)
    return dict(
        titulo="Trocando os valores de lugar",
        enunciado=(
            f"As variáveis `a` e `b` começam com {a} e {b}. Complete as lacunas `___` para que, no final, "
            f"`a` valha {b} e `b` valha {a}, usando uma variável auxiliar `aux`.\n\n"
            f"Saída esperada:\n```\na = {b}\nb = {a}\n```"
        ),
        codigo_inicial=(
            f"a = {a}\n"
            f"b = {b}\n"
            "aux = ___\n"
            "a = ___\n"
            "b = ___\n"
            'print("a =", a)\n'
            'print("b =", b)\n'
        ),
        solucao=(
            f"a = {a}\n"
            f"b = {b}\n"
            "aux = a\n"
            "a = b\n"
            "b = aux\n"
            'print("a =", a)\n'
            'print("b =", b)\n'
        ),
        dicas=[
            "Pense em dois copos com sucos diferentes: para trocar, você precisa de um terceiro copo vazio.",
            "Primeiro guarde o valor de `a` em `aux`, para não perdê-lo quando `a` receber o valor de `b`.",
        ],
        explicacao=(
            "Se fizéssemos `a = b` direto, o valor original de `a` seria perdido. Por isso guardamos `a` em "
            "`aux`, copiamos `b` para `a` e, por fim, devolvemos o valor guardado para `b`."
        ),
    )


@exercicio(estagio=1, dificuldade=1, tipo="codigo", conceitos=["variaveis", "print"])
def boas_vindas_variavel(r):
    nome = r.choice(NOMES)
    curso = r.choice(["Python", "Lógica", "Algoritmos", "Programação"])
    return dict(
        titulo="Boas-vindas personalizadas",
        enunciado=(
            f"Guarde o nome `\"{nome}\"` em uma variável chamada `aluno` e o tema `\"{curso}\"` em uma variável `curso`.\n\n"
            "Em seguida, usando as variáveis no `print`, exiba exatamente:\n"
            f"```\nBem-vindo(a), {nome} ao curso de {curso}!\n```"
        ),
        solucao=(
            f'aluno = "{nome}"\n'
            f'curso = "{curso}"\n'
            'print("Bem-vindo(a),", aluno, "ao curso de", curso + "!")\n'
        ),
        dicas=[
            "Use `=` para guardar cada texto entre aspas nas variáveis `aluno` e `curso`.",
            "Para evitar um espaço antes da exclamação `!`, você pode juntar `curso + \"!\"` ou usar `sep`.",
        ],
        explicacao=(
            "O `print` separa argumentos por vírgula colocando um espaço entre eles. Como não queremos espaço antes "
            "do `!`, concatenamos `curso + \"!\"` antes de imprimir."
        ),
    )


@exercicio(estagio=1, dificuldade=1, tipo="codigo", conceitos=["variaveis", "print"])
def etiqueta_separador(r):
    dia = r.randint(10, 28)
    mes = r.randint(10, 12)
    ano = r.randint(2024, 2027)
    return dict(
        titulo="Data formatada com sep",
        enunciado=(
            f"Crie as variáveis `dia = {dia}`, `mes = {mes}` e `ano = {ano}`.\n\n"
            "Mostre a data separada por barras usando um **único** `print` com o parâmetro `sep=\"/\"`:\n"
            f"```\n{dia}/{mes}/{ano}\n```"
        ),
        solucao=(
            f"dia = {dia}\n"
            f"mes = {mes}\n"
            f"ano = {ano}\n"
            'print(dia, mes, ano, sep="/")\n'
        ),
        dicas=[
            "Por padrão, `print(a, b, c)` coloca espaços entre os valores.",
            "O parâmetro nomeado `sep=\"/\"` troca esse espaço padrão pela barra `/`.",
        ],
        explicacao=(
            "O `sep` define qual texto o `print` coloca **entre** os itens passados por vírgula. "
            "Com `sep=\"/\"`, os três números ficam unidos por barras sem precisar converter manualmente."
        ),
    )


@exercicio(estagio=1, dificuldade=1, tipo="completar", conceitos=["variaveis", "print"])
def completar_placar_jogo(r):
    time_a = r.choice(["Tigres", "Falcões", "Leões", "Lobos", "Águias"])
    time_b = r.choice(["Tubas", "Panteras", "Corvos", "Ursos", "Dragões"])
    gols_a = r.randint(1, 5)
    gols_b = r.randint(0, 4)
    return dict(
        titulo="Placar da partida",
        enunciado=(
            f"Complete as lacunas `___` para que o programa mostre o placar `{time_a} {gols_a} x {gols_b} {time_b}` "
            "usando as variáveis criadas.\n\n"
            f"Saída esperada:\n```\n{time_a} {gols_a} x {gols_b} {time_b}\n```"
        ),
        codigo_inicial=(
            f'time_a = "{time_a}"\n'
            f'time_b = "{time_b}"\n'
            f"gols_a = {gols_a}\n"
            f"gols_b = {gols_b}\n"
            'print(___, ___, "x", ___, ___)\n'
        ),
        solucao=(
            f'time_a = "{time_a}"\n'
            f'time_b = "{time_b}"\n'
            f"gols_a = {gols_a}\n"
            f"gols_b = {gols_b}\n"
            'print(time_a, gols_a, "x", gols_b, time_b)\n'
        ),
        dicas=[
            "Coloque os nomes das variáveis na ordem exata em que devem aparecer no placar.",
            "O `\"x\"` já está no meio; antes dele vão o time A e seus gols, e depois os gols B e o time B.",
        ],
        explicacao=(
            "Passando as quatro variáveis e a letra `\"x\"` separados por vírgula no `print`, o Python substitui "
            "cada variável pelo seu valor e coloca um espaço entre eles automaticamente."
        ),
    )


@exercicio(estagio=1, dificuldade=2, tipo="codigo", conceitos=["variaveis", "print"])
def saldo_apos_compras(r):
    saldo = r.randint(120, 300)
    gasto1 = r.randint(20, 50)
    gasto2 = r.randint(15, 45)
    restante = saldo - gasto1 - gasto2
    return dict(
        titulo="Atualizando a carteira",
        enunciado=(
            f"Você começou o dia com R$ `{saldo}` em uma variável `saldo`. Depois comprou um lanche de `{gasto1}` "
            f"e um livro de `{gasto2}`.\n\n"
            "Crie a variável `saldo` e atualize o valor dela descontando as compras. Mostre exatamente:\n"
            f"```\nSaldo inicial: {saldo}\nSaldo final: {restante}\n```"
        ),
        solucao=(
            f"saldo = {saldo}\n"
            'print("Saldo inicial:", saldo)\n'
            f"saldo = saldo - {gasto1}\n"
            f"saldo = saldo - {gasto2}\n"
            'print("Saldo final:", saldo)\n'
        ),
        dicas=[
            "Primeiro mostre o saldo inicial antes de alterá-lo.",
            "Para atualizar uma variável com base no valor anterior, use `saldo = saldo - valor`.",
        ],
        explicacao=(
            "Como cada `print` executa no momento em que o Python passa por aquela linha, imprimimos `saldo` antes "
            "das subtrações e novamente depois. Em `saldo = saldo - ...`, o lado direito lê o valor atual e guarda o novo."
        ),
    )


@exercicio(estagio=1, dificuldade=2, tipo="prever", conceitos=["variaveis", "print", "teste_de_mesa"])
def prever_reatribuicao_sequencial(r):
    v1 = r.randint(3, 12)
    v2 = r.randint(2, 6)
    v3 = r.randint(1, 5)
    return dict(
        titulo="Seguindo o rastro de pontos",
        enunciado=(
            "Faça o teste de mesa e escreva exatamente o que o trecho abaixo imprime na tela."
        ),
        solucao=(
            f"pontos = {v1}\n"
            f"pontos = pontos + {v2}\n"
            "print(pontos)\n"
            f"pontos = pontos - {v3}\n"
            "pontos = pontos * 2\n"
            "print(pontos)\n"
        ),
        dicas=[
            "Comece anotando `pontos` e atualize o valor na mesma coluna a cada linha.",
            "Lembre-se que o primeiro `print` acontece antes da subtração e da multiplicação.",
        ],
        explicacao=(
            f"Inicialmente `pontos` vale {v1}. Soma-se {v2}, chegando a {v1 + v2} (primeiro print). "
            f"Depois subtrai-se {v3} (ficando {v1 + v2 - v3}) e multiplica-se por 2, resultando em {(v1 + v2 - v3) * 2}."
        ),
    )


@exercicio(estagio=1, dificuldade=2, tipo="corrigir", conceitos=["variaveis", "print", "depuracao"])
def corrigir_aspas_variavel(r):
    item = r.choice(["teclado", "mouse", "monitor", "webcam", "pendrive"])
    qtd = r.randint(2, 9)
    return dict(
        titulo="Imprimiu o texto errado!",
        enunciado=(
            "O programador queria mostrar o conteúdo das variáveis `item` e `quantidade`, produzindo:\n"
            f"```\nItem: {item}\nQuantidade: {qtd}\n```\n"
            "Mas o programa está imprimindo os nomes literais das variáveis. Corrija o bug."
        ),
        codigo_inicial=(
            f'item = "{item}"\n'
            f"quantidade = {qtd}\n"
            'print("Item:", "item")\n'
            'print("Quantidade:", "quantidade")\n'
        ),
        solucao=(
            f'item = "{item}"\n'
            f"quantidade = {qtd}\n"
            'print("Item:", item)\n'
            'print("Quantidade:", quantidade)\n'
        ),
        dicas=[
            "Qual é a diferença entre `\"item\"` (com aspas) e `item` (sem aspas)?",
            "Aspas criam um texto literal; para acessar uma variável, escreva o nome dela **sem aspas**.",
        ],
        explicacao=(
            "Colocar aspas em `\"item\"` e `\"quantidade\"` faz o Python imprimir essas palavras literalmente, "
            "ignorando as variáveis criadas acima. Removendo as aspas, os valores guardados são exibidos."
        ),
    )


@exercicio(estagio=1, dificuldade=2, tipo="codigo", conceitos=["variaveis", "print"])
def duas_palavras_mesma_linha(r):
    p1 = r.choice(["Olá", "Bom dia", "Foco", "Treino", "Avante"])
    p2 = r.choice(["Python", "Lógica", "Código", "Dojo", "Mundo"])
    return dict(
        titulo="Juntando na mesma linha com end",
        enunciado=(
            f"Guarde `\"{p1}\"` na variável `inicio` e `\"{p2}\"` na variável `fim`.\n\n"
            "Use **dois** comandos `print()`, mas faça os dois aparecerem na **mesma linha**, separados por ` -> `, "
            "usando o parâmetro `end` no primeiro `print`:\n"
            f"```\n{p1} -> {p2}\n```"
        ),
        solucao=(
            f'inicio = "{p1}"\n'
            f'fim = "{p2}"\n'
            'print(inicio, end=" -> ")\n'
            "print(fim)\n"
        ),
        dicas=[
            "Normalmente, todo `print()` termina pulando uma linha (`\\n`).",
            "Use `end=\" -> \"` no primeiro `print` para trocar a quebra de linha pela setinha.",
        ],
        explicacao=(
            "O parâmetro `end` controla o que o `print` coloca no final. Ao definir `end=\" -> \"`, ele não pula "
            "para a linha de baixo, e o próximo `print(fim)` continua logo em seguida."
        ),
    )


@exercicio(estagio=1, dificuldade=3, tipo="prever", conceitos=["variaveis", "print", "teste_de_mesa"])
def prever_copia_independente(r):
    a = r.randint(4, 15)
    b = r.randint(16, 30)
    c = r.randint(1, 5)
    return dict(
        titulo="Cópia ou espelho?",
        enunciado=(
            "Acompanhe atentamente cada linha e escreva exatamente a saída gerada pelo código."
        ),
        solucao=(
            f"a = {a}\n"
            f"b = {b}\n"
            "c = a + b\n"
            f"a = {c}\n"
            "print(a, b, c)\n"
        ),
        dicas=[
            "Quando `c = a + b` roda, qual é o valor de `a` naquele momento?",
            "Mudar `a` na linha seguinte altera o valor que já foi guardado em `c`?",
        ],
        explicacao=(
            f"`c` é calculado quando `a` vale {a} e `b` vale {b}, então `c` recebe {a + b}. "
            f"Depois `a` passa a valer {c}, mas `c` não é recalculado automaticamente — continua valendo {a + b}."
        ),
    )


@exercicio(estagio=1, dificuldade=3, tipo="corrigir", conceitos=["variaveis", "print", "depuracao"])
def corrigir_ordem_variavel(r):
    preco = r.randint(15, 60)
    frete = r.randint(8, 20)
    return dict(
        titulo="Variável antes da hora",
        enunciado=(
            "O programa tenta calcular o total de uma compra somando `preco` e `frete` para mostrar:\n"
            f"```\nTotal a pagar: {preco + frete}\n```\n"
            "Mas está dando `NameError`. Corrija o código mantendo o cálculo com as variáveis."
        ),
        codigo_inicial=(
            f"preco = {preco}\n"
            "total = preco + frete\n"
            f"frete = {frete}\n"
            'print("Total a pagar:", total)\n'
        ),
        solucao=(
            f"preco = {preco}\n"
            f"frete = {frete}\n"
            "total = preco + frete\n"
            'print("Total a pagar:", total)\n'
        ),
        dicas=[
            "O Python executa o código de cima para baixo, uma linha de cada vez.",
            "A variável `frete` está sendo usada na soma antes de ter sido criada!",
        ],
        explicacao=(
            "Em Python não podemos usar uma variável antes da linha em que ela recebe um valor. "
            "Movendo `frete = ...` para antes de `total = preco + frete`, todas as variáveis já existem na hora da soma."
        ),
    )


@exercicio(estagio=1, dificuldade=3, tipo="completar", conceitos=["variaveis", "print"])
def completar_etiqueta_produto(r):
    nome = r.choice(["Caderno", "Mochila", "Estojo", "Agenda", "Lapiseira"])
    unidades = r.randint(3, 8)
    unitario = r.randint(10, 40)
    return dict(
        titulo="Resumo do pedido",
        enunciado=(
            f"Complete as lacunas `___` para calcular `total` multiplicando `unidades` por `unitario` e "
            "exibir o resumo com um separador ` | `:\n\n"
            f"Saída esperada:\n```\n{nome} | {unidades} un | R$ {unidades * unitario}\n```"
        ),
        codigo_inicial=(
            f'item = "{nome}"\n'
            f"unidades = {unidades}\n"
            f"unitario = {unitario}\n"
            "total = ___\n"
            'print(item, str(unidades) + " un", "R$ " + str(total), sep=___)\n'
        ),
        solucao=(
            f'item = "{nome}"\n'
            f"unidades = {unidades}\n"
            f"unitario = {unitario}\n"
            "total = unidades * unitario\n"
            'print(item, str(unidades) + " un", "R$ " + str(total), sep=" | ")\n'
        ),
        dicas=[
            "O total é a multiplicação `unidades * unitario`.",
            "Observe o que separa os três blocos na saída esperada: espaço, barra vertical, espaço (`\" | \"`).",
        ],
        explicacao=(
            "Calculamos `total` primeiro e depois usamos `sep=\" | \"` para unir os três textos no formato exato pedido."
        ),
    )


@exercicio(estagio=1, dificuldade=3, tipo="codigo", conceitos=["variaveis", "print"])
def cartaz_com_bordas(r):
    titulo_msg = r.choice(["AVISO IMPORTANTE", "REUNIÃO HOJE", "TREINO DIÁRIO", "META CUMPRIDA"])
    borda = r.choice(["=", "*", "-", "#"]) * (len(titulo_msg) + 4)
    return dict(
        titulo="Cartaz emoldurado",
        enunciado=(
            f"Crie uma variável `borda` com o valor `\"{borda}\"` e uma variável `mensagem` com `\"{titulo_msg}\"`.\n\n"
            "Imprima a borda em cima, a mensagem com dois espaços antes (use `\"  \"` ou texto formatado), "
            "e a borda novamente embaixo:\n"
            f"```\n{borda}\n  {titulo_msg}\n{borda}\n```"
        ),
        solucao=(
            f'borda = "{borda}"\n'
            f'mensagem = "{titulo_msg}"\n'
            "print(borda)\n"
            'print("  " + mensagem)\n'
            "print(borda)\n"
        ),
        dicas=[
            "Reutilize a variável `borda` no primeiro e no terceiro `print`.",
            "Para colocar exatamente dois espaços antes do texto, faça `print(\"  \" + mensagem)` (com vírgula, `\" \"` já adicionaria um espaço extra!).",
        ],
        explicacao=(
            "Guardar a borda numa variável evita repetir os símbolos e garante que topo e base tenham o mesmo tamanho. "
            "Usar `+` com `\"  \"` garante exatamente dois espaços à esquerda."
        ),
    )


@exercicio(estagio=1, dificuldade=3, tipo="prever", conceitos=["variaveis", "print", "teste_de_mesa"])
def prever_sep_e_end(r):
    a = r.randint(1, 5)
    b = r.randint(6, 10)
    c = r.randint(11, 15)
    return dict(
        titulo="Combinação de sep e end",
        enunciado=(
            "Observe atentamente os parâmetros `sep` e `end` e escreva exatamente o que será impresso."
        ),
        solucao=(
            f"x = {a}\n"
            f"y = {b}\n"
            f"z = {c}\n"
            'print(x, y, sep="-", end=" | ")\n'
            "print(z)\n"
            "print(x + y)\n"
        ),
        dicas=[
            "`sep` atua **entre** `x` e `y`. `end` atua **depois** de `y`.",
            "O segundo `print(z)` não tem `end`, então ele quebra a linha normalmente antes do último `print`.",
        ],
        explicacao=(
            f"A primeira linha imprime `{a}-{b} | ` sem pular linha; logo `z` ({c}) aparece na mesma linha: `{a}-{b} | {c}`. "
            f"Na linha de baixo aparece a soma `{a + b}`."
        ),
    )


@exercicio(estagio=1, dificuldade=4, tipo="codigo", conceitos=["variaveis", "print"])
def soma_e_produto_tres_variaveis(r):
    a = r.randint(2, 9)
    b = r.randint(2, 9)
    c = r.randint(2, 9)
    return dict(
        titulo="Duas contas, três variáveis",
        enunciado=(
            f"Crie as variáveis `a = {a}`, `b = {b}` e `c = {c}`.\n\n"
            "Guarde em `soma` a soma dos três valores e em `produto` a multiplicação dos três. "
            "Depois mostre exatamente:\n"
            f"```\nValores: {a} {b} {c}\nSoma: {a + b + c}\nProduto: {a * b * c}\n```"
        ),
        solucao=(
            f"a = {a}\n"
            f"b = {b}\n"
            f"c = {c}\n"
            "soma = a + b + c\n"
            "produto = a * b * c\n"
            'print("Valores:", a, b, c)\n'
            'print("Soma:", soma)\n'
            'print("Produto:", produto)\n'
        ),
        dicas=[
            "Use `+` para `soma` e `*` para `produto`.",
            "No primeiro `print`, passe `\"Valores:\"`, `a`, `b`, `c` separados por vírgula.",
        ],
        explicacao=(
            "Podemos combinar várias variáveis na mesma expressão matemática e guardar o resultado em novas variáveis (`soma` e `produto`) "
            "para manter o código legível."
        ),
    )


@exercicio(estagio=1, dificuldade=4, tipo="corrigir", conceitos=["variaveis", "print", "depuracao"])
def corrigir_nome_reservado_e_sintaxe(r):
    aluno = r.choice(NOMES)
    nota1 = r.randint(6, 10)
    nota2 = r.randint(5, 9)
    return dict(
        titulo="Dois erros escondidos",
        enunciado=(
            "O código abaixo deveria imprimir o nome do aluno e a soma das duas notas:\n"
            f"```\nAluno: {aluno}\nTotal de pontos: {nota1 + nota2}\n```\n"
            "Mas ele possui erros. Encontre-os e corrija o código."
        ),
        codigo_inicial=(
            f'nome_aluno = "{aluno}"\n'
            f"nota_1 = {nota1}\n"
            f"nota_2 = {nota2}\n"
            "soma = nota_1 + nota_2\n"
            'print("Aluno:" nome_aluno)\n'
            'print("Total de pontos:", Soma)\n'
        ),
        solucao=(
            f'nome_aluno = "{aluno}"\n'
            f"nota_1 = {nota1}\n"
            f"nota_2 = {nota2}\n"
            "soma = nota_1 + nota_2\n"
            'print("Aluno:", nome_aluno)\n'
            'print("Total de pontos:", soma)\n'
        ),
        dicas=[
            "Faltou algo separando os dois itens do primeiro `print`.",
            "Depois de corrigir a sintaxe do primeiro `print`, observe o nome da variável no segundo (`soma` vs `Soma`).",
        ],
        explicacao=(
            "Havia dois bugs: falta de vírgula entre `\"Aluno:\"` e `nome_aluno` (que causava `SyntaxError`) "
            "e o uso de `Soma` com S maiúsculo quando a variável se chamava `soma` (`NameError`)."
        ),
    )


@exercicio(estagio=1, dificuldade=4, tipo="completar", conceitos=["variaveis", "print"])
def completar_troca_sem_perder(r):
    x = r.randint(10, 40)
    y = r.randint(41, 80)
    z = r.randint(81, 99)
    return dict(
        titulo="Rodízio de três variáveis",
        enunciado=(
            f"Temos `x = {x}`, `y = {y}` e `z = {z}`. Queremos fazer um rodízio para a direita:\n"
            f"- `y` recebe o antigo `x` ({x})\n"
            f"- `z` recebe o antigo `y` ({y})\n"
            f"- `x` recebe o antigo `z` ({z})\n\n"
            "Complete as lacunas `___` usando `aux` para não perder nenhum valor!\n\n"
            f"Saída esperada:\n```\n{z} {x} {y}\n```"
        ),
        codigo_inicial=(
            f"x = {x}\n"
            f"y = {y}\n"
            f"z = {z}\n"
            "aux = z\n"
            "z = ___\n"
            "y = ___\n"
            "x = ___\n"
            "print(x, y, z)\n"
        ),
        solucao=(
            f"x = {x}\n"
            f"y = {y}\n"
            f"z = {z}\n"
            "aux = z\n"
            "z = y\n"
            "y = x\n"
            "x = aux\n"
            "print(x, y, z)\n"
        ),
        dicas=[
            "`aux` já salvou o valor original de `z`, então `z` já pode ser sobrescrito sem medo!",
            "Depois que `z = y` copia `y`, quem está livre para receber o valor de `x` é `y`.",
        ],
        explicacao=(
            "Ao salvar `z` em `aux`, liberamos `z` para receber `y`; em seguida `y` fica livre para receber `x`; "
            "por fim `x` recebe o valor original de `z` guardado em `aux`."
        ),
    )


@exercicio(estagio=1, dificuldade=4, tipo="prever", conceitos=["variaveis", "print", "teste_de_mesa"])
def prever_duas_linhas_mesma_variavel(r):
    a = r.randint(2, 7)
    b = r.randint(3, 8)
    return dict(
        titulo="O truque da soma e subtração",
        enunciado=(
            "Existe um jeito clássico de trocar dois números sem usar variável auxiliar. "
            "Faça o teste de mesa linha por linha e escreva o que o código imprime!"
        ),
        solucao=(
            f"a = {a}\n"
            f"b = {b}\n"
            "a = a + b\n"
            "b = a - b\n"
            "a = a - b\n"
            "print(a, b)\n"
        ),
        dicas=[
            "Calcule com calma: na linha 3, `a` passa a guardar a soma dos dois.",
            "Na linha 4, subtraia o `b` antigo dessa soma — o que sobra?",
        ],
        explicacao=(
            f"Primeiro `a` vira `{a} + {b} = {a + b}`. Depois `b` recebe `{a + b} - {b} = {a}` (o antigo `a`!). "
            f"Por fim `a` recebe `{a + b} - {a} = {b}` (o antigo `b`!). Os valores trocaram de lugar."
        ),
    )


@exercicio(estagio=1, dificuldade=5, tipo="codigo", conceitos=["variaveis", "print"])
def progresso_dobrando_variavel(r):
    inicio = r.randint(2, 5)
    return dict(
        titulo="Crescimento dobrado",
        enunciado=(
            f"Crie uma variável `energia` começando com `{inicio}`.\n\n"
            "Mostre o valor inicial na 1ª linha, depois dobre o valor da variável (`energia = energia * 2`) "
            "e mostre na 2ª linha, dobre novamente e mostre na 3ª linha, e dobre uma última vez mostrando na 4ª linha.\n\n"
            f"Saída esperada:\n```\n{inicio}\n{inicio * 2}\n{inicio * 4}\n{inicio * 8}\n```"
        ),
        solucao=(
            f"energia = {inicio}\n"
            "print(energia)\n"
            "energia = energia * 2\n"
            "print(energia)\n"
            "energia = energia * 2\n"
            "print(energia)\n"
            "energia = energia * 2\n"
            "print(energia)\n"
        ),
        dicas=[
            "Você só precisa de uma única variável `energia`.",
            "A cada passo, faça `energia = energia * 2` seguido de `print(energia)`.",
        ],
        explicacao=(
            "Este exercício mostra o poder de atualizar uma variável a partir dela mesma: cada `energia = energia * 2` "
            "lê o valor atual e guarda o dobro, preparando o terreno para laços de repetição no futuro."
        ),
    )


@exercicio(estagio=1, dificuldade=5, tipo="corrigir", conceitos=["variaveis", "print", "depuracao"])
def corrigir_troca_sem_aux(r):
    a = r.randint(10, 40)
    b = r.randint(60, 95)
    return dict(
        titulo="O valor que sumiu na troca",
        enunciado=(
            f"O código deveria trocar os valores de `x` ({a}) e `y` ({b}) para imprimir:\n"
            f"```\nx = {b}\ny = {a}\n```\n"
            "Mas está imprimindo os dois iguais! Descubra o erro de lógica e corrija."
        ),
        codigo_inicial=(
            f"x = {a}\n"
            f"y = {b}\n"
            "x = y\n"
            "y = x\n"
            'print("x =", x)\n'
            'print("y =", y)\n'
        ),
        solucao=(
            f"x = {a}\n"
            f"y = {b}\n"
            "aux = x\n"
            "x = y\n"
            "y = aux\n"
            'print("x =", x)\n'
            'print("y =", y)\n'
        ),
        dicas=[
            "Quando `x = y` executa, o que acontece com o valor antigo de `x`?",
            "Guarde o valor original de `x` em uma variável `aux` antes de sobrescrever `x`.",
        ],
        explicacao=(
            "Fazer `x = y` e depois `y = x` apenas copia `y` para `x` e copia esse mesmo valor de volta para `y`, "
            "apagando o valor original de `x`. Uma variável auxiliar `aux` resolve preservando `x` antes da troca."
        ),
    )


@exercicio(estagio=1, dificuldade=5, tipo="completar", conceitos=["variaveis", "print"])
def completar_tabela_simples(r):
    p1 = r.choice(["Arroz", "Feijão", "Café"])
    p2 = r.choice(["Leite", "Açúcar", "Pão"])
    v1 = r.randint(10, 28)
    v2 = r.randint(5, 19)
    return dict(
        titulo="Cupom alinhado com duas variáveis de linha",
        enunciado=(
            "Complete as lacunas `___` para montar um mini-cupom imprimindo os dois itens e a soma deles no final:\n\n"
            f"Saída esperada:\n```\n{p1}: R$ {v1}\n{p2}: R$ {v2}\n---\nTotal: R$ {v1 + v2}\n```"
        ),
        codigo_inicial=(
            f'p1 = "{p1}"\n'
            f"v1 = {v1}\n"
            f'p2 = "{p2}"\n'
            f"v2 = {v2}\n"
            "total = ___\n"
            'print(p1 + ":", "R$", v1)\n'
            'print(p2 + ":", "R$", ___)\n'
            'print("---")\n'
            'print("Total:", ___, ___)\n'
        ),
        solucao=(
            f'p1 = "{p1}"\n'
            f"v1 = {v1}\n"
            f'p2 = "{p2}"\n'
            f"v2 = {v2}\n"
            "total = v1 + v2\n"
            'print(p1 + ":", "R$", v1)\n'
            'print(p2 + ":", "R$", v2)\n'
            'print("---")\n'
            'print("Total:", "R$", total)\n'
        ),
        dicas=[
            "`total` deve somar as variáveis `v1` e `v2`.",
            "Na última linha, antes do valor `total`, falta a string `\"R$\"`.",
        ],
        explicacao=(
            "Concatenamos `p1 + \":\"` para os dois-pontos ficarem colados ao nome do item, enquanto a vírgula coloca "
            "espaço entre o rótulo, o cifrão `R$` e o valor numérico."
        ),
    )


@exercicio(estagio=1, dificuldade=5, tipo="codigo", conceitos=["variaveis", "print"])
def sequencia_soma_anterior(r):
    a = r.randint(1, 4)
    b = r.randint(2, 6)
    c = a + b
    d = b + c
    e = c + d
    return dict(
        titulo="Cada termo soma os dois anteriores",
        enunciado=(
            f"Comece com duas variáveis: `a = {a}` e `b = {b}`.\n\n"
            "Calcule os próximos três termos usando **apenas somas das variáveis anteriores** "
            "(`c = a + b`, `d = b + c`, `e = c + d`) e mostre os 5 números numa mesma linha separados por espaço:\n"
            f"```\n{a} {b} {c} {d} {e}\n```"
        ),
        solucao=(
            f"a = {a}\n"
            f"b = {b}\n"
            "c = a + b\n"
            "d = b + c\n"
            "e = c + d\n"
            "print(a, b, c, d, e)\n"
        ),
        dicas=[
            "Crie `c`, `d` e `e` em ordem — cada uma usa as duas anteriores.",
            "No final, use `print(a, b, c, d, e)`.",
        ],
        explicacao=(
            "Cada variável guarda o resultado da soma das duas imediatamente anteriores — essa é a famosa ideia da "
            "sequência de Fibonacci, que depois você automatizará usando laços."
        ),
    )

