"""Estágio 11 - Listas."""

from .base import exercicio

NOMES = ["Ana", "Bruno", "Carla", "Diego", "Elisa", "Fábio", "Gabi", "Heitor", "Iara", "João",
         "Luna", "Marcos", "Nina", "Otávio", "Paula", "Rafa"]
PRODUTOS = ["arroz", "feijão", "café", "leite", "pão", "ovos", "banana", "macarrão", "queijo",
            "tomate", "açúcar", "manteiga", "iogurte", "alface"]
MUSICAS = ["Aquarela", "Garota de Ipanema", "Evidências", "Tempo Perdido", "Asa Branca",
           "Construção", "Mas que Nada", "Ainda Bem", "Velha Infância", "Sozinho", "Trem-Bala"]
HASHTAGS = ["#praia", "#sol", "#ferias", "#verao", "#amigos", "#viagem", "#mar", "#foto",
            "#natureza", "#trilha"]


def _linha(valores):
    """Junta números numa linha separada por espaços (formato de entrada com split)."""
    return " ".join(str(v) for v in valores)


@exercicio(estagio=11, dificuldade=1, tipo="codigo", conceitos=["listas"])
def lista_de_compras(r):
    itens = r.sample(PRODUTOS, 5)
    iniciais, novo, urgente = itens[:3], itens[3], itens[4]
    final = [urgente] + iniciais + [novo]
    lista_txt = ", ".join(f'"{i}"' for i in iniciais)
    return dict(
        titulo="Lista de compras",
        enunciado=(
            f"Crie uma lista chamada `compras` com os itens {lista_txt}, nessa ordem.\n\n"
            f"Depois:\n"
            f"- use `append` para colocar `\"{novo}\"` no **final** da lista;\n"
            f"- use `insert` para colocar `\"{urgente}\"` no **começo** da lista (posição 0).\n\n"
            "Por fim, mostre a lista inteira e a quantidade de itens (use `len`). Saída esperada:\n"
            f"```\n{final}\nTotal de itens: {len(final)}\n```"
        ),
        solucao=(
            f"compras = [{lista_txt}]\n"
            f'compras.append("{novo}")\n'
            f'compras.insert(0, "{urgente}")\n'
            "print(compras)\n"
            'print("Total de itens:", len(compras))\n'
        ),
        dicas=[
            "Uma lista é criada com colchetes e itens separados por vírgula: `lista = [\"a\", \"b\"]`.",
            "`lista.append(x)` coloca x no fim; `lista.insert(posição, x)` coloca x na posição indicada.",
            f"Use `compras.insert(0, \"{urgente}\")` para o começo e `print(len(compras))` para contar.",
        ],
        explicacao=(
            "`append` sempre adiciona no fim da lista, enquanto `insert(0, ...)` empurra todos os itens "
            "uma posição para a direita e coloca o novo na frente. `len` conta quantos itens a lista tem "
            f"agora: {len(final)}."
        ),
    )


@exercicio(estagio=11, dificuldade=1, tipo="prever", conceitos=["listas", "teste_de_mesa"])
def prever_indices_playlist(r):
    musicas = r.sample(MUSICAS, 5)
    i = r.randint(1, 3)
    return dict(
        titulo="Tocando a playlist",
        enunciado=(
            "Lembre-se: o **primeiro** item de uma lista tem índice 0 e o índice -1 pega o **último**. "
            "Escreva exatamente o que o programa abaixo mostra."
        ),
        solucao=(
            f"playlist = {musicas}\n"
            "print(playlist[0])\n"
            f"print(playlist[{i}])\n"
            "print(playlist[-1])\n"
            "print(len(playlist))\n"
        ),
        dicas=[
            "Conte as posições começando do zero: 0, 1, 2, 3, 4.",
            f"`playlist[{i}]` é o item na posição {i}, ou seja, o {i + 1}º item da lista.",
        ],
        explicacao=(
            f"`playlist[0]` é \"{musicas[0]}\", `playlist[{i}]` é \"{musicas[i]}\" (o {i + 1}º item, já que "
            f"começamos do 0) e `playlist[-1]` é o último, \"{musicas[-1]}\". `len` conta os itens: 5. "
            "Um erro comum é achar que o índice 1 é o primeiro item."
        ),
    )


@exercicio(estagio=11, dificuldade=2, tipo="codigo", conceitos=["listas", "input", "for_range"])
def boletim_maior_menor_media(r):
    def gerar_notas(n):
        return [f"{r.randint(0, 20) / 2:g}" for _ in range(n)]

    testes = []
    for n in (r.randint(3, 5), r.randint(4, 6), 1, r.randint(2, 3)):
        notas = gerar_notas(n)
        testes.append({"entrada": "\n".join([str(n)] + notas)})
    ex = testes[0]["entrada"].split("\n")
    notas_ex = [float(x) for x in ex[1:]]
    return dict(
        titulo="Boletim: maior, menor e média",
        enunciado=(
            "O programa lê um número inteiro `N` (quantas notas) e depois `N` notas (números reais), "
            "uma por linha. Guarde as notas numa lista e mostre a maior nota, a menor nota (com 1 casa "
            "decimal) e a média (com 2 casas decimais).\n\n"
            f"Exemplo: para as entradas `{'`, `'.join(ex)}` a saída deve ser:\n"
            f"```\nMaior nota: {max(notas_ex):.1f}\nMenor nota: {min(notas_ex):.1f}\n"
            f"Média: {sum(notas_ex) / len(notas_ex):.2f}\n```"
        ),
        solucao=(
            "quantidade = int(input())\n"
            "notas = []\n"
            "for i in range(quantidade):\n"
            "    nota = float(input())\n"
            "    notas.append(nota)\n"
            "media = sum(notas) / len(notas)\n"
            'print(f"Maior nota: {max(notas):.1f}")\n'
            'print(f"Menor nota: {min(notas):.1f}")\n'
            'print(f"Média: {media:.2f}")\n'
        ),
        testes=testes,
        testes_visiveis=2,
        dicas=[
            "Comece com uma lista vazia `notas = []` e use um `for` com `range(quantidade)` para ler cada nota.",
            "Dentro do laço, converta com `float(input())` e guarde com `notas.append(nota)`.",
            "Depois do laço: `max(notas)`, `min(notas)` e `sum(notas) / len(notas)` dão tudo o que você precisa.",
        ],
        explicacao=(
            "Ler os valores para uma lista permite usá-los várias vezes depois do laço. `max` e `min` "
            "procuram o maior e o menor item, e a média é a soma (`sum`) dividida pela quantidade (`len`). "
            "Note que até com uma única nota tudo funciona: ela é ao mesmo tempo a maior, a menor e a média."
        ),
    )


@exercicio(estagio=11, dificuldade=2, tipo="completar", conceitos=["listas", "for_range", "contador"])
def completar_dias_quentes(r):
    temperaturas = [r.randint(18, 38) for _ in range(7)]
    limite = r.randint(25, 31)
    quentes = sum(1 for t in temperaturas if t > limite)
    return dict(
        titulo="Semana de calor",
        enunciado=(
            f"A lista `temperaturas` guarda a máxima de cada dia da semana. Complete as lacunas `___` para "
            f"contar em quantos dias a temperatura passou de {limite} graus (estritamente maior).\n\n"
            f"Saída esperada:\n```\nDias acima de {limite} graus: {quentes}\n```"
        ),
        codigo_inicial=(
            f"temperaturas = {temperaturas}\n"
            f"limite = {limite}\n"
            "quentes = 0\n"
            "for t in ___:\n"
            "    if ___ > limite:\n"
            "        quentes = ___\n"
            'print("Dias acima de", limite, "graus:", quentes)\n'
        ),
        solucao=(
            f"temperaturas = {temperaturas}\n"
            f"limite = {limite}\n"
            "quentes = 0\n"
            "for t in temperaturas:\n"
            "    if t > limite:\n"
            "        quentes = quentes + 1\n"
            'print("Dias acima de", limite, "graus:", quentes)\n'
        ),
        dicas=[
            "O `for` pode percorrer a lista diretamente: a cada volta, `t` vale um dos itens.",
            "Compare a temperatura do dia (`t`) com o limite.",
            "O contador aumenta de 1 em 1: `quentes = quentes + 1`.",
        ],
        explicacao=(
            "`for t in temperaturas` faz `t` assumir cada valor da lista, um por volta. Sempre que `t` "
            f"passa do limite, somamos 1 ao contador. No fim, {quentes} dias passaram de {limite} graus."
        ),
    )


@exercicio(estagio=11, dificuldade=3, tipo="prever", conceitos=["listas", "teste_de_mesa"])
def prever_fila_de_atendimento(r):
    a, b, c, d, e = r.sample(NOMES, 5)
    sai = r.choice([b, c, d])
    fila = [a, b, c]
    fila.append(d)
    fila.insert(1, e)
    atendido = fila.pop(0)
    fila.remove(sai)
    return dict(
        titulo="Fila do banco",
        enunciado=(
            "Faça o teste de mesa: anote como a lista `fila` fica depois de **cada** linha e escreva "
            "exatamente o que o programa mostra."
        ),
        solucao=(
            f'fila = ["{a}", "{b}", "{c}"]\n'
            f'fila.append("{d}")\n'
            f'fila.insert(1, "{e}")\n'
            "atendido = fila.pop(0)\n"
            f'fila.remove("{sai}")\n'
            "print(atendido)\n"
            "print(fila)\n"
            "print(len(fila))\n"
        ),
        dicas=[
            "`append` coloca no fim, `insert(1, x)` coloca na posição 1 (a segunda), empurrando os outros.",
            "`pop(0)` **tira** o primeiro item da lista e devolve ele; `remove(x)` apaga o item com aquele valor.",
            f"Depois do insert, a fila é {[a, e, b, c, d]}.",
        ],
        explicacao=(
            f"Após `append` e `insert`, a fila fica {[a, e, b, c, d]}. `pop(0)` remove e devolve "
            f"\"{atendido}\", que fica guardado em `atendido`. Depois `remove(\"{sai}\")` apaga esse nome, "
            f"sobrando {fila}, com {len(fila)} pessoas."
        ),
    )


@exercicio(estagio=11, dificuldade=3, tipo="codigo", conceitos=["listas", "input", "if_else"])
def filtrar_pontuacoes(r):
    testes = []
    for caso in range(4):
        meta = r.randint(40, 80)
        n = r.randint(4, 8)
        if caso == 2:
            pontos = [r.randint(0, meta - 1) for _ in range(n)]
        else:
            pontos = [r.randint(10, 100) for _ in range(n)]
            pontos[r.randrange(n)] = meta
        testes.append({"entrada": f"{meta}\n{_linha(pontos)}"})
    meta_ex, linha_ex = testes[0]["entrada"].split("\n")
    pontos_ex = [int(p) for p in linha_ex.split()]
    bateram_ex = [p for p in pontos_ex if p >= int(meta_ex)]
    return dict(
        titulo="Quem bateu a meta?",
        enunciado=(
            "Num jogo, você quer ver só as partidas em que atingiu a meta de pontos. O programa lê:\n"
            "- na 1ª linha, a meta (inteiro);\n"
            "- na 2ª linha, as pontuações das partidas, separadas por espaço.\n\n"
            "Monte uma **nova lista** só com as pontuações **maiores ou iguais** à meta (na mesma ordem) "
            "e mostre-a, seguida de quantas partidas bateram a meta e do total de partidas.\n\n"
            f"Exemplo: para a entrada\n```\n{meta_ex}\n{linha_ex}\n```\na saída deve ser:\n"
            f"```\nBateram a meta: {bateram_ex}\n{len(bateram_ex)} de {len(pontos_ex)} partidas\n```"
        ),
        solucao=(
            "meta = int(input())\n"
            "pontos = input().split()\n"
            "bateram = []\n"
            "for p in pontos:\n"
            "    valor = int(p)\n"
            "    if valor >= meta:\n"
            "        bateram.append(valor)\n"
            'print("Bateram a meta:", bateram)\n'
            'print(len(bateram), "de", len(pontos), "partidas")\n'
        ),
        testes=testes,
        testes_visiveis=2,
        dicas=[
            "`input().split()` transforma a linha numa lista de textos, um para cada pontuação.",
            "Comece com `bateram = []` e percorra as pontuações; converta cada uma com `int` antes de comparar.",
            "Dentro do `for`: `if valor >= meta:` e então `bateram.append(valor)`.",
        ],
        explicacao=(
            "Filtrar é percorrer a lista original e copiar para uma lista nova só os itens que passam no "
            "teste. É preciso converter cada texto com `int`, senão a comparação seria entre textos. "
            "Usamos `>=` porque empatar com a meta também conta como bater."
        ),
    )


@exercicio(estagio=11, dificuldade=3, tipo="corrigir", conceitos=["listas", "acumulador", "depuracao"])
def corrigir_media_de_gastos(r):
    gastos = [r.randint(12, 90) for _ in range(r.randint(4, 6))]
    total = sum(gastos)
    media = total / len(gastos)
    return dict(
        titulo="O total que sempre dá errado",
        enunciado=(
            "Este programa deveria somar os gastos da semana com lanche e mostrar o total e a média por dia:\n"
            f"```\nTotal gasto: {total}\nMédia por dia: {media:.2f}\n```\n"
            "Mas o total sai errado. Encontre o bug e corrija."
        ),
        codigo_inicial=(
            f"gastos = {gastos}\n"
            "for g in gastos:\n"
            "    total = 0\n"
            "    total = total + g\n"
            "media = total / len(gastos)\n"
            'print("Total gasto:", total)\n'
            'print(f"Média por dia: {media:.2f}")\n'
        ),
        solucao=(
            f"gastos = {gastos}\n"
            "total = 0\n"
            "for g in gastos:\n"
            "    total = total + g\n"
            "media = total / len(gastos)\n"
            'print("Total gasto:", total)\n'
            'print(f"Média por dia: {media:.2f}")\n'
        ),
        dicas=[
            "Faça o teste de mesa: quanto vale `total` depois da 1ª volta? E da 2ª?",
            "A linha `total = 0` está sendo executada em **toda** volta do laço.",
            "O acumulador deve ser zerado **uma vez só**, antes do `for`.",
        ],
        explicacao=(
            "Como `total = 0` estava dentro do laço, a cada volta a soma era apagada e só sobrava o último "
            f"gasto ({gastos[-1]}). Movendo a inicialização para antes do `for`, o total acumula todos os "
            f"valores: {total}."
        ),
    )


@exercicio(estagio=11, dificuldade=4, tipo="codigo", conceitos=["listas", "input", "for_range", "if_else"])
def posicao_da_maior_venda(r):
    testes = []
    for caso in range(5):
        n = r.randint(5, 8)
        vendas = r.sample(range(100, 990, 10), n)
        if caso == 1:  # maior no primeiro dia
            vendas.sort(reverse=True)
            r.shuffle(vendas[1:])
        elif caso == 2:  # empate no maior valor
            i, j = sorted(r.sample(range(n), 2))
            vendas[j] = max(vendas)
            vendas[i] = vendas[j]
        elif caso == 3:  # maior no último dia
            vendas.sort()
        elif caso == 4:
            vendas = [r.randint(100, 900)]
        testes.append({"entrada": _linha(vendas)})
    ex = [int(v) for v in testes[0]["entrada"].split()]
    maior = max(ex)
    return dict(
        titulo="O melhor dia de vendas",
        enunciado=(
            "O programa lê **uma linha** com as vendas de cada dia (inteiros separados por espaço). "
            "Descubra a maior venda e em qual dia ela aconteceu (o 1º valor é o dia 1). "
            "**Não use `max()`** nem ordene a lista: percorra com `range(len(...))`. "
            "Se houver empate, mostre o **primeiro** dia com o maior valor.\n\n"
            f"Exemplo: para a entrada `{testes[0]['entrada']}` a saída deve ser:\n"
            f"```\nMaior venda: {maior}\nDia: {ex.index(maior) + 1}\n```"
        ),
        solucao=(
            "textos = input().split()\n"
            "vendas = []\n"
            "for t in textos:\n"
            "    vendas.append(int(t))\n"
            "maior = vendas[0]\n"
            "posicao = 0\n"
            "for i in range(len(vendas)):\n"
            "    if vendas[i] > maior:\n"
            "        maior = vendas[i]\n"
            "        posicao = i\n"
            'print("Maior venda:", maior)\n'
            'print("Dia:", posicao + 1)\n'
        ),
        testes=testes,
        testes_visiveis=2,
        dicas=[
            "Primeiro converta os textos da linha para uma lista de inteiros.",
            "Guarde o 'campeão até agora': comece com `maior = vendas[0]` e `posicao = 0`.",
            "Percorra com `for i in range(len(vendas))`; se `vendas[i] > maior`, atualize `maior` e `posicao`. "
            "No fim, o dia é `posicao + 1`.",
        ],
        explicacao=(
            "Começar com o primeiro valor como 'maior até agora' garante que funciona até com números "
            "pequenos. Percorrer pelos índices permite guardar **onde** o maior está. Usar `>` (e não `>=`) "
            "faz o primeiro dia vencer os empates, e somamos 1 porque os índices começam em 0, mas os dias em 1."
        ),
    )


@exercicio(estagio=11, dificuldade=3, tipo="completar", conceitos=["listas", "for_range"])
def completar_inverter_ordem(r):
    nomes = r.sample(NOMES, r.randint(4, 6))
    return dict(
        titulo="Ordem de chegada ao contrário",
        enunciado=(
            "A lista `chegada` tem os corredores na ordem em que cruzaram a linha. Complete as lacunas para "
            "criar a lista `invertida`, com os nomes do último para o primeiro, **sem usar** `[::-1]` nem "
            "`reverse()`: percorra os índices de trás para frente.\n\n"
            f"Saída esperada:\n```\n{nomes[::-1]}\n```"
        ),
        codigo_inicial=(
            f"chegada = {nomes}\n"
            "invertida = []\n"
            "for i in range(___, ___, ___):\n"
            "    invertida.___(chegada[i])\n"
            "print(invertida)\n"
        ),
        solucao=(
            f"chegada = {nomes}\n"
            "invertida = []\n"
            "for i in range(len(chegada) - 1, -1, -1):\n"
            "    invertida.append(chegada[i])\n"
            "print(invertida)\n"
        ),
        dicas=[
            "O último índice de uma lista é `len(lista) - 1`.",
            "`range(início, fim, passo)` para **antes** do fim. Para chegar até o índice 0 andando para trás, "
            "o fim precisa ser -1 e o passo, -1.",
            "Fica `range(len(chegada) - 1, -1, -1)` e, dentro do laço, `invertida.append(chegada[i])`.",
        ],
        explicacao=(
            f"Com {len(nomes)} nomes, os índices vão de 0 a {len(nomes) - 1}. O `range` começa em "
            f"{len(nomes) - 1}, desce de 1 em 1 e para antes de -1, ou seja, passa pelo 0. Cada nome visitado "
            "é colocado no fim da lista nova, que fica invertida."
        ),
    )


@exercicio(estagio=11, dificuldade=2, tipo="corrigir", conceitos=["listas", "for_range", "depuracao"])
def corrigir_ranking_sem_campeao(r):
    nomes = r.sample(NOMES, r.randint(3, 5))
    esperado = "\n".join(f"{i + 1}º lugar: {n}" for i, n in enumerate(nomes))
    return dict(
        titulo="Cadê o campeão?",
        enunciado=(
            "A lista `ranking` já está em ordem de classificação. O programa deveria mostrar:\n"
            f"```\n{esperado}\n```\n"
            "Mas o campeão sumiu e as posições estão erradas. Corrija o código."
        ),
        codigo_inicial=(
            f"ranking = {nomes}\n"
            "for i in range(1, len(ranking)):\n"
            '    print(f"{i}º lugar: {ranking[i]}")\n'
        ),
        solucao=(
            f"ranking = {nomes}\n"
            "for i in range(len(ranking)):\n"
            '    print(f"{i + 1}º lugar: {ranking[i]}")\n'
        ),
        dicas=[
            "Qual é o índice do primeiro item de uma lista?",
            "`range(1, len(ranking))` começa no índice 1, pulando o índice 0.",
            "Percorra a partir do 0 e, para mostrar a posição para humanos, use `i + 1`.",
        ],
        explicacao=(
            "Índices começam em 0, mas posições de pódio começam em 1. O código começava o `range` em 1 e "
            "pulava o campeão. O certo é percorrer todos os índices (`range(len(ranking))`) e mostrar `i + 1` "
            "como posição."
        ),
    )


@exercicio(estagio=11, dificuldade=4, tipo="codigo", conceitos=["listas", "input", "if_else"])
def hashtags_sem_repeticao(r):
    testes = []
    for caso in range(4):
        if caso == 2:
            tags = r.sample(HASHTAGS, r.randint(3, 5))
        elif caso == 3:
            tags = [r.choice(HASHTAGS)] * r.randint(2, 4)
        else:
            base = r.sample(HASHTAGS, r.randint(3, 4))
            tags = base + [r.choice(base) for _ in range(r.randint(2, 4))]
            r.shuffle(tags)
        testes.append({"entrada": " ".join(tags)})
    ex = testes[0]["entrada"].split()
    unicas = []
    for t in ex:
        if t not in unicas:
            unicas.append(t)
    return dict(
        titulo="Hashtags repetidas",
        enunciado=(
            "Você colou as hashtags de um post, mas algumas vieram repetidas. O programa lê **uma linha** "
            "com as hashtags separadas por espaço. Crie uma nova lista **sem repetições**, mantendo a ordem "
            "em que cada hashtag apareceu pela primeira vez. Mostre a lista e quantas repetições foram removidas.\n\n"
            f"Exemplo: para a entrada `{testes[0]['entrada']}` a saída deve ser:\n"
            f"```\n{unicas}\nRepetidas removidas: {len(ex) - len(unicas)}\n```"
        ),
        solucao=(
            "hashtags = input().split()\n"
            "unicas = []\n"
            "for h in hashtags:\n"
            "    if h not in unicas:\n"
            "        unicas.append(h)\n"
            "print(unicas)\n"
            'print("Repetidas removidas:", len(hashtags) - len(unicas))\n'
        ),
        testes=testes,
        testes_visiveis=2,
        dicas=[
            "O operador `in` responde se um valor já está numa lista: `\"#sol\" in lista` dá True ou False.",
            "Comece com uma lista vazia e só adicione uma hashtag se ela **ainda não** estiver lá (`not in`).",
            "Quantas foram removidas? É a diferença entre os tamanhos das duas listas.",
        ],
        explicacao=(
            "Percorrendo as hashtags na ordem original e adicionando cada uma só se ela não estiver em "
            "`unicas`, a primeira aparição fica e as seguintes são ignoradas. Como cada repetição ignorada "
            "deixa a lista nova menor, a diferença `len(hashtags) - len(unicas)` conta as removidas."
        ),
    )


@exercicio(estagio=11, dificuldade=3, tipo="codigo", conceitos=["listas", "input", "if_else"])
def lista_de_convidados(r):
    convidados = r.sample(NOMES, 5)
    fora = [n for n in NOMES if n not in convidados]
    escolhidos = r.sample(convidados, 3) + r.sample(fora, 2)
    r.shuffle(escolhidos)
    testes = [{"entrada": n} for n in escolhidos]
    dentro = next(n for n in escolhidos if n in convidados)
    resto = [n for n in convidados if n != dentro]
    nao_esta = next(n for n in escolhidos if n not in convidados)
    return dict(
        titulo="Saiu da lista de convidados",
        enunciado=(
            "Comece seu programa com a lista abaixo (ela já está no editor):\n"
            f"```\nconvidados = {convidados}\n```\n"
            "O programa lê um nome. Se ele estiver na lista, remova-o e mostre `<nome> foi removido(a).`; "
            "se não estiver, mostre `<nome> não está na lista.`. Em seguida, sempre mostre a lista e "
            "quantos convidados restam.\n\n"
            f"Exemplo com a entrada `{dentro}`:\n"
            f"```\n{dentro} foi removido(a).\n{resto}\nConvidados: {len(resto)}\n```\n"
            f"Exemplo com a entrada `{nao_esta}`:\n"
            f"```\n{nao_esta} não está na lista.\n{convidados}\nConvidados: {len(convidados)}\n```"
        ),
        codigo_inicial=f"convidados = {convidados}\n",
        solucao=(
            f"convidados = {convidados}\n"
            'nome = input("Nome: ")\n'
            "if nome in convidados:\n"
            "    convidados.remove(nome)\n"
            '    print(nome, "foi removido(a).")\n'
            "else:\n"
            '    print(nome, "não está na lista.")\n'
            "print(convidados)\n"
            'print("Convidados:", len(convidados))\n'
        ),
        testes=testes,
        testes_visiveis=1,
        dicas=[
            "Use `if nome in convidados:` para saber se o nome está na lista.",
            "`convidados.remove(nome)` apaga o item. Cuidado: chamar `remove` com um nome que não existe dá erro!",
            "Os dois `print` finais (lista e `len`) ficam **fora** do if/else, para rodar sempre.",
        ],
        explicacao=(
            "Testar com `in` antes de remover evita o erro `ValueError`, que acontece quando pedimos para "
            "remover algo que não está na lista. Como a lista e o total devem aparecer nos dois casos, esses "
            "prints ficam depois do if/else."
        ),
    )


@exercicio(estagio=11, dificuldade=4, tipo="prever", conceitos=["listas", "for_range", "teste_de_mesa"])
def prever_subidas_de_preco(r):
    valores = [r.randint(3, 15) for _ in range(r.randint(5, 6))]
    resultado = []
    for i in range(1, len(valores)):
        dif = valores[i] - valores[i - 1]
        if dif > 0:
            resultado.append(dif)
    return dict(
        titulo="Quanto o preço subiu?",
        enunciado=(
            "A lista guarda o preço de um lanche em meses seguidos. Faça o teste de mesa (anote `i`, "
            "`valores[i - 1]`, `valores[i]` e `diferenca` em cada volta) e escreva exatamente o que é mostrado."
        ),
        solucao=(
            f"valores = {valores}\n"
            "resultado = []\n"
            "for i in range(1, len(valores)):\n"
            "    diferenca = valores[i] - valores[i - 1]\n"
            "    if diferenca > 0:\n"
            "        resultado.append(diferenca)\n"
            "print(resultado)\n"
            "print(len(resultado))\n"
        ),
        dicas=[
            f"O laço começa em `i = 1` e vai até `i = {len(valores) - 1}`; em cada volta compara um item com o anterior.",
            "Só entram na lista as diferenças **positivas** (quando o preço subiu). Diferença 0 não entra.",
            f"Na 1ª volta: `diferenca = {valores[1]} - {valores[0]} = {valores[1] - valores[0]}`.",
        ],
        explicacao=(
            "Começar o `range` em 1 permite usar `valores[i - 1]` sem sair da lista. A cada volta calculamos "
            "quanto o preço mudou em relação ao mês anterior e guardamos só as subidas. "
            f"Resultado: {resultado}, com {len(resultado)} subida(s)."
        ),
    )


@exercicio(estagio=11, dificuldade=4, tipo="corrigir", conceitos=["listas", "comparacao", "depuracao"])
def corrigir_maior_temperatura_freezer(r):
    temps = [r.randint(-25, -3) for _ in range(r.randint(5, 7))]
    return dict(
        titulo="O freezer que esquentou",
        enunciado=(
            "A lista guarda as leituras do termômetro de um freezer (todas negativas). O programa deveria "
            "mostrar a temperatura **mais alta** registrada, percorrendo a lista com `for`:\n"
            f"```\nTemperatura mais alta: {max(temps)}\n```\n"
            "Mas ele mostra um valor que nem está na lista! Corrija o bug mantendo a lógica do laço."
        ),
        codigo_inicial=(
            f"temperaturas = {temps}\n"
            "maior = 0\n"
            "for t in temperaturas:\n"
            "    if t > maior:\n"
            "        maior = t\n"
            'print("Temperatura mais alta:", maior)\n'
        ),
        solucao=(
            f"temperaturas = {temps}\n"
            "maior = temperaturas[0]\n"
            "for t in temperaturas:\n"
            "    if t > maior:\n"
            "        maior = t\n"
            'print("Temperatura mais alta:", maior)\n'
        ),
        dicas=[
            "Faça o teste de mesa: alguma temperatura da lista é maior que o valor inicial de `maior`?",
            "Começar com 0 só funciona se existir algum número positivo na lista.",
            "Comece `maior` com um valor que esteja **na lista**, por exemplo o primeiro: `temperaturas[0]`.",
        ],
        explicacao=(
            "Como todas as temperaturas são negativas, nenhuma é maior que 0, então o `if` nunca era "
            "verdadeiro e `maior` continuava 0. Iniciando com o primeiro item da lista, o 'campeão inicial' é "
            "um valor real e o laço consegue compará-lo com os demais."
        ),
    )


@exercicio(estagio=11, dificuldade=3, tipo="codigo", conceitos=["listas", "input", "for_range"])
def ranking_e_podio(r):
    testes = []
    for caso in range(4):
        n = 3 if caso == 2 else r.randint(4, 7)
        pontos = [r.randint(10, 99) for _ in range(n)]
        if caso == 1:
            pontos[1] = pontos[0]
        testes.append({"entrada": _linha(pontos)})
    ex = [int(p) for p in testes[0]["entrada"].split()]
    dec = sorted(ex, reverse=True)
    return dict(
        titulo="Ranking e pódio",
        enunciado=(
            "O programa lê **uma linha** com as pontuações de um campeonato (pelo menos 3 inteiros separados "
            "por espaço). Mostre a lista em ordem crescente e, depois, as três maiores pontuações (pódio), "
            "da maior para a menor, separadas por vírgula e espaço. Use `sorted`.\n\n"
            f"Exemplo: para a entrada `{testes[0]['entrada']}` a saída deve ser:\n"
            f"```\nEm ordem crescente: {sorted(ex)}\nPódio: {dec[0]}, {dec[1]}, {dec[2]}\n```"
        ),
        solucao=(
            "textos = input().split()\n"
            "pontos = []\n"
            "for t in textos:\n"
            "    pontos.append(int(t))\n"
            "crescente = sorted(pontos)\n"
            "decrescente = sorted(pontos, reverse=True)\n"
            'print("Em ordem crescente:", crescente)\n'
            'print(f"Pódio: {decrescente[0]}, {decrescente[1]}, {decrescente[2]}")\n'
        ),
        testes=testes,
        testes_visiveis=2,
        dicas=[
            "Converta os textos para inteiros antes de ordenar: textos são ordenados como palavras (\"100\" < \"9\")!",
            "`sorted(lista)` devolve uma nova lista em ordem crescente; `sorted(lista, reverse=True)`, decrescente.",
            "Na lista decrescente, o pódio são os índices 0, 1 e 2.",
        ],
        explicacao=(
            "`sorted` cria uma cópia ordenada sem mexer na lista original. Ordenando ao contrário "
            "(`reverse=True`), as maiores pontuações ficam nas primeiras posições, então o pódio são os "
            "índices 0, 1 e 2. Empates aparecem repetidos, como é justo num ranking."
        ),
    )


@exercicio(estagio=11, dificuldade=3, tipo="completar", conceitos=["listas", "input", "for_range"])
def completar_consumo_acima_da_media(r):
    testes = []
    for caso in range(4):
        n = r.randint(3, 6)
        if caso == 2:
            v = r.randint(100, 300)
            consumo = [v] * n
        else:
            consumo = [r.randint(80, 400) for _ in range(n)]
        testes.append({"entrada": "\n".join([str(n)] + [str(c) for c in consumo])})
    ex = [int(x) for x in testes[0]["entrada"].split("\n")]
    valores = ex[1:]
    media = sum(valores) / len(valores)
    acima = sum(1 for v in valores if v > media)
    return dict(
        titulo="Consumo de água acima da média",
        enunciado=(
            "O programa lê quantos dias foram medidos (`N`) e depois o consumo de água de cada dia, em litros "
            "(inteiros, um por linha). Complete as lacunas para guardar os valores numa lista, calcular a "
            "média e contar quantos dias ficaram **acima** da média.\n\n"
            f"Exemplo: para as entradas `{'`, `'.join(str(x) for x in ex)}` a saída é:\n"
            f"```\nMédia: {media:.1f}\nDias acima da média: {acima}\n```"
        ),
        codigo_inicial=(
            "quantidade = int(input())\n"
            "consumos = []\n"
            "for i in range(___):\n"
            "    valor = int(input())\n"
            "    consumos.___(valor)\n"
            "media = ___ / len(consumos)\n"
            "acima = 0\n"
            "for c in consumos:\n"
            "    if ___:\n"
            "        acima = acima + 1\n"
            'print(f"Média: {media:.1f}")\n'
            'print("Dias acima da média:", acima)\n'
        ),
        solucao=(
            "quantidade = int(input())\n"
            "consumos = []\n"
            "for i in range(quantidade):\n"
            "    valor = int(input())\n"
            "    consumos.append(valor)\n"
            "media = sum(consumos) / len(consumos)\n"
            "acima = 0\n"
            "for c in consumos:\n"
            "    if c > media:\n"
            "        acima = acima + 1\n"
            'print(f"Média: {media:.1f}")\n'
            'print("Dias acima da média:", acima)\n'
        ),
        testes=testes,
        testes_visiveis=2,
        dicas=[
            "O primeiro laço repete uma vez para cada dia lido.",
            "Para guardar cada valor na lista use `append`; a soma de todos é `sum(consumos)`.",
            "Só dá para saber quem está acima da média **depois** de calculá-la — por isso há um segundo laço com `if c > media:`.",
        ],
        explicacao=(
            "Esse problema mostra por que listas são úteis: a média só é conhecida depois de ler tudo, e só "
            "então podemos comparar cada dia com ela. Sem a lista, os valores lidos já teriam sido perdidos. "
            "Quando todos os dias são iguais, ninguém fica acima da média."
        ),
    )


@exercicio(estagio=11, dificuldade=5, tipo="codigo", conceitos=["listas", "input", "contador", "if_else"])
def maior_sequencia_de_passos(r):
    testes = []
    for caso in range(5):
        meta = r.choice([6000, 7000, 8000, 10000])
        n = r.randint(6, 10)
        if caso == 2:
            passos = [r.randint(meta, meta + 4000) for _ in range(n)]
        elif caso == 3:
            passos = [r.randint(1000, meta - 1) for _ in range(n)]
        else:
            passos = [r.choice([r.randint(2000, meta - 1), r.randint(meta, meta + 5000)]) for _ in range(n)]
            passos[r.randrange(n)] = meta
        testes.append({"entrada": f"{meta}\n{_linha(passos)}"})
    meta_ex, linha_ex = testes[0]["entrada"].split("\n")
    atual = melhor = 0
    for p in linha_ex.split():
        if int(p) >= int(meta_ex):
            atual += 1
            melhor = max(melhor, atual)
        else:
            atual = 0
    return dict(
        titulo="Sequência de dias ativos",
        enunciado=(
            "Um app de academia quer mostrar a **maior sequência de dias seguidos** em que você bateu a meta "
            "de passos (passos **maiores ou iguais** à meta). O programa lê:\n"
            "- na 1ª linha, a meta (inteiro);\n"
            "- na 2ª linha, os passos de cada dia, separados por espaço.\n\n"
            f"Exemplo: para a entrada\n```\n{meta_ex}\n{linha_ex}\n```\na saída deve ser:\n"
            f"```\nMaior sequência: {melhor} dias\n```"
        ),
        solucao=(
            "meta = int(input())\n"
            "passos = input().split()\n"
            "atual = 0\n"
            "melhor = 0\n"
            "for p in passos:\n"
            "    if int(p) >= meta:\n"
            "        atual = atual + 1\n"
            "        if atual > melhor:\n"
            "            melhor = atual\n"
            "    else:\n"
            "        atual = 0\n"
            'print("Maior sequência:", melhor, "dias")\n'
        ),
        testes=testes,
        testes_visiveis=2,
        dicas=[
            "Você precisa de dois contadores: a sequência **atual** e a **melhor** já vista.",
            "Quando o dia bate a meta, a sequência atual cresce; quando não bate, ela volta a zero.",
            "Sempre que `atual` crescer, confira se passou de `melhor` e, se sim, atualize `melhor = atual`.",
        ],
        explicacao=(
            "A ideia é andar pelos dias mantendo o tamanho da sequência que está acontecendo agora (`atual`) "
            "e o recorde (`melhor`). Um dia ruim quebra a sequência (`atual = 0`), mas o recorde fica guardado. "
            "Atualizar o recorde dentro do laço garante que uma sequência no final da lista também seja contada."
        ),
    )
