"""Estágio 8 - Repetição com while, contadores e acumuladores (sem for/listas)."""

from .base import exercicio


@exercicio(estagio=8, dificuldade=1, tipo="codigo", conceitos=["while", "contador", "input"])
def contagem_regressiva_while(r):
    palavra = r.choice(["Lançar!", "Já!", "Fogo!", "Partida!"])
    casos = [r.randint(3, 7), r.randint(2, 5), 1]
    n0 = casos[0]
    linhas0 = "\n".join(str(x) for x in range(n0, 0, -1))
    return dict(
        titulo="Contagem regressiva de foguete",
        enunciado=(
            f"Leia um inteiro positivo `n` e, usando `while`, conte de `n` até `1` (um número por linha). "
            f"Ao terminar o laço, imprima `{palavra}`.\n\n"
            f"Exemplo para `n = {n0}`:\n```\n{linhas0}\n{palavra}\n```"
        ),
        solucao=(
            'n = int(input("Início: "))\n'
            "while n >= 1:\n"
            "    print(n)\n"
            "    n -= 1\n"
            f'print("{palavra}")\n'
        ),
        testes=[{"entrada": str(x)} for x in casos],
        testes_visiveis=1,
        dicas=[
            "Enquanto `n >= 1`, imprima `n` e diminua `n` em 1 (`n -= 1`).",
            f"Deixe `print(\"{palavra}\")` **fora** do `while` (sem recuo), para rodar só quando a contagem acabar.",
        ],
        explicacao=(
            "A variável `n` funciona como um contador decrescente. Quando `n` chega a `0`, a condição `n >= 1` "
            "vira falsa, o laço termina e o programa imprime a mensagem final."
        ),
    )


@exercicio(estagio=8, dificuldade=1, tipo="completar", conceitos=["while", "contador"])
def completar_pares_ate_n(r):
    casos = [r.randrange(6, 14, 2), r.randrange(7, 17, 2), r.randrange(14, 24, 2), 2]
    n0 = casos[0]
    ex0 = "\n".join(str(x) for x in range(2, n0 + 1, 2))
    return dict(
        titulo="Números pares com while",
        enunciado=(
            "Complete as lacunas `___` para ler um inteiro `limite` e imprimir todos os números pares de `2` até `limite`.\n\n"
            f"Exemplo para `limite = {n0}`:\n```\n{ex0}\n```"
        ),
        codigo_inicial=(
            'limite = int(input("Limite: "))\n'
            "atual = 2\n"
            "while atual ___ limite:\n"
            "    print(atual)\n"
            "    atual += ___\n"
        ),
        solucao=(
            'limite = int(input("Limite: "))\n'
            "atual = 2\n"
            "while atual <= limite:\n"
            "    print(atual)\n"
            "    atual += 2\n"
        ),
        testes=[{"entrada": str(x)} for x in casos],
        testes_visiveis=1,
        dicas=[
            "Como queremos incluir o próprio `limite` se ele for par, use `<=`.",
            "Começando no `2`, somando de `2` em `2` só passamos pelos números pares!",
        ],
        explicacao=(
            "Avançar de 2 em 2 a partir do 2 evita até precisar testar `if atual % 2 == 0`, e se `limite` for `1`, "
            "a condição `2 <= 1` já começa falsa e não imprime nada."
        ),
    )


@exercicio(estagio=8, dificuldade=2, tipo="prever", conceitos=["while", "acumulador", "teste_de_mesa"])
def prever_while_soma_passo(r):
    ini = r.randint(1, 3)
    limite = ini + r.randint(5, 8)
    passo = r.randint(2, 3)
    return dict(
        titulo="Tabela de mesa com while",
        enunciado=(
            "Faça o teste de mesa anotando os valores de `i` e `soma` a cada volta do `while`, e escreva a saída exata:"
        ),
        solucao=(
            f"i = {ini}\n"
            "soma = 0\n"
            f"while i <= {limite}:\n"
            "    soma += i\n"
            f"    i += {passo}\n"
            "print(i, soma)\n"
        ),
        dicas=[
            "Só existe um `print` no final, depois que o `while` terminar!",
            f"Anote cada valor de `i` que ainda satisfaz `i <= {limite}`; quando `i` passar desse limite pela primeira vez, pare o laço.",
        ],
        explicacao=(
            "O `while` continua somando `i` em `soma` e avançando `i` até que `i` ultrapasse o limite. "
            "Esse último valor de `i` (que fez a condição falhar) é o que sobra para o `print(i, soma)`."
        ),
    )


@exercicio(estagio=8, dificuldade=2, tipo="codigo", conceitos=["while", "contador", "acumulador"])
def tabuada_com_while(r):
    casos = [r.randint(3, 9), r.randint(2, 8), 10]
    n0 = casos[0]
    ex0 = "\n".join(f"{n0} x {i} = {n0 * i}" for i in range(1, 11))
    return dict(
        titulo="Tabuada de 1 a 10 com while",
        enunciado=(
            "Leia um número inteiro `n` e use `while` para exibir a tabuada dele de `1` até `10`:\n\n"
            f"Exemplo para `n = {n0}`:\n```\n{ex0}\n```"
        ),
        solucao=(
            'n = int(input("Número: "))\n'
            "i = 1\n"
            "while i <= 10:\n"
            '    print(f"{n} x {i} = {n * i}")\n'
            "    i += 1\n"
        ),
        testes=[{"entrada": str(x)} for x in casos],
        testes_visiveis=1,
        dicas=[
            "Comece um contador `i = 1` e repita `while i <= 10:`.",
            "Não esqueça de fazer `i += 1` no final do bloco!",
        ],
        explicacao=(
            "O contador `i` varia de 1 a 10 dentro do laço, e a f-string formata cada linha multiplicando `n * i`."
        ),
    )


@exercicio(estagio=8, dificuldade=2, tipo="corrigir", conceitos=["while", "contador", "depuracao"])
def corrigir_limite_e_passo_while(r):
    casos = [r.randint(4, 8), r.randint(2, 5), 1]
    n0 = casos[0]
    soma0 = n0 * (n0 + 1) // 2
    return dict(
        titulo="Soma de 1 até N deixando o último de fora!",
        enunciado=(
            f"O código deveria ler um inteiro `n` e somar todos os inteiros de `1` até `n` (inclusive).\n"
            f"Para `n = {n0}`, a saída deve ser:\n```\nSoma: {soma0}\n```\n"
            "Mas está sempre faltando somar o próprio `n` (e avançando errado)! Corrija o bug."
        ),
        codigo_inicial=(
            'n = int(input("N: "))\n'
            "i = 1\n"
            "soma = 0\n"
            "while i < n:\n"
            "    soma += i\n"
            "    i += 1\n"
            'print("Soma:", soma)\n'
        ),
        solucao=(
            'n = int(input("N: "))\n'
            "i = 1\n"
            "soma = 0\n"
            "while i <= n:\n"
            "    soma += i\n"
            "    i += 1\n"
            'print("Soma:", soma)\n'
        ),
        testes=[{"entrada": str(x)} for x in casos],
        testes_visiveis=1,
        dicas=[
            "Quando `i` chega exatamente ao valor de `n`, o teste `i < n` é verdadeiro ou falso?",
            "Troque `<` por `<=` para incluir o próprio `n` na soma.",
        ],
        explicacao=(
            "O erro *off-by-one* acontece quando usamos `<` em vez de `<=` no `while`: o laço para uma volta antes e deixa `n` de fora."
        ),
    )


@exercicio(estagio=8, dificuldade=3, tipo="codigo", conceitos=["while", "acumulador", "contador"])
def sentinela_soma_ate_zero(r):
    def seq(k):
        return [r.randint(5, 40) for _ in range(k)] + [0]
    c1, c2, c3 = seq(r.randint(3, 5)), seq(r.randint(2, 4)), [0]
    s1 = sum(c1)
    q1 = len(c1) - 1
    return dict(
        titulo="Somando compras até digitar 0 (sentinela)",
        enunciado=(
            "Leia vários valores inteiros, um por linha, até que o usuário digite `0` (o **sentinela** de parada).\n\n"
            "O `0` não deve ser contado! Ao parar, mostre quantos valores foram digitados e a soma deles:\n"
            f"Exemplo para entrada `{' '.join(map(str, c1))}`:\n"
            f"```\nQuantidade: {q1}\nSoma: {s1}\n```"
        ),
        solucao=(
            "soma = 0\n"
            "qtd = 0\n"
            'valor = int(input("Valor (0 para sair): "))\n'
            "while valor != 0:\n"
            "    soma += valor\n"
            "    qtd += 1\n"
            '    valor = int(input("Valor (0 para sair): "))\n'
            'print("Quantidade:", qtd)\n'
            'print("Soma:", soma)\n'
        ),
        testes=[{"entrada": "\n".join(map(str, c))} for c in (c1, c2, c3)],
        testes_visiveis=1,
        dicas=[
            "Leia o primeiro `valor` **antes** do `while` para poder testar `while valor != 0:`.",
            "Dentro do `while`, some/conte primeiro e leia o próximo `valor` no final do bloco — assim o `0` nunca entra na conta!",
        ],
        explicacao=(
            "O padrão ler-antes / testar / processar / ler-no-fim é a forma mais limpa de trabalhar com sentinela: "
            "se o primeiro número já for `0`, o `while` nem entra e imprime 0 e 0."
        ),
    )


@exercicio(estagio=8, dificuldade=3, tipo="codigo", conceitos=["while", "contador", "if_else"])
def contar_positivos_e_negativos_sentinela(r):
    def gerar_seq():
        vals = [r.choice([-1, 1]) * r.randint(1, 25) for _ in range(r.randint(4, 7))]
        return vals + [0]
    casos = [gerar_seq(), gerar_seq(), [5, 10, 0], [-3, -8, 0]]
    c0 = casos[0]
    pos0 = sum(1 for x in c0 if x > 0)
    neg0 = sum(1 for x in c0 if x < 0)
    return dict(
        titulo="Balanço de positivos e negativos",
        enunciado=(
            "Leia números inteiros um por linha até que seja digitado `0` (pare no zero).\n\n"
            "Conte quantos números **positivos** e quantos **negativos** foram digitados:\n"
            f"Exemplo para `{' '.join(map(str, c0))}`:\n"
            f"```\nPositivos: {pos0}\nNegativos: {neg0}\n```"
        ),
        solucao=(
            "pos = 0\n"
            "neg = 0\n"
            "n = int(input())\n"
            "while n != 0:\n"
            "    if n > 0:\n"
            "        pos += 1\n"
            "    else:\n"
            "        neg += 1\n"
            "    n = int(input())\n"
            'print("Positivos:", pos)\n'
            'print("Negativos:", neg)\n'
        ),
        testes=[{"entrada": "\n".join(map(str, c))} for c in casos],
        testes_visiveis=1,
        dicas=[
            "Como `0` faz sair do `while`, todo número dentro do laço é positivo (`> 0`) ou negativo (`else`).",
            "Mantenha dois contadores (`pos` e `neg`) iniciados em `0` antes do laço.",
        ],
        explicacao=(
            "Dentro do `while n != 0:`, garantimos que `n` não é zero, então basta um `if n > 0` / `else` "
            "para classificar e incrementar o contador certo antes de ler o próximo número."
        ),
    )


@exercicio(estagio=8, dificuldade=3, tipo="corrigir", conceitos=["while", "acumulador", "depuracao"])
def corrigir_media_sentinela_conta_zero(r):
    casos = [
        [r.randint(6, 10), r.randint(4, 9), r.randint(5, 10), -1],
        [10, 8, -1],
        [7, -1],
    ]
    c0 = casos[0][:-1]
    m0 = sum(c0) / len(c0)
    return dict(
        titulo="O -1 estragou a média!",
        enunciado=(
            "O programa lê notas inteiras até digitar `-1` e deveria mostrar a média das notas válidas com 2 casas:\n"
            f"Para `{' '.join(map(str, casos[0]))}`:\n```\nMédia: {m0:.2f}\n```\n"
            "Mas está incluindo o `-1` na soma e na contagem! Descubra onde está o erro e corrija."
        ),
        codigo_inicial=(
            "soma = 0\n"
            "qtd = 0\n"
            "nota = 0\n"
            "while nota != -1:\n"
            "    nota = int(input())\n"
            "    soma += nota\n"
            "    qtd += 1\n"
            "media = soma / qtd\n"
            'print(f"Média: {media:.2f}")\n'
        ),
        solucao=(
            "soma = 0\n"
            "qtd = 0\n"
            "nota = int(input())\n"
            "while nota != -1:\n"
            "    soma += nota\n"
            "    qtd += 1\n"
            "    nota = int(input())\n"
            "media = soma / qtd\n"
            'print(f"Média: {media:.2f}")\n'
        ),
        testes=[{"entrada": "\n".join(map(str, c))} for c in casos],
        testes_visiveis=1,
        dicas=[
            "Quando o usuário digita `-1` dentro do `while`, o código soma `-1` e aumenta `qtd` antes de testar `while nota != -1` de novo!",
            "Leia a primeira `nota` antes do `while` e mova a próxima leitura para o **fim** do bloco do `while`.",
        ],
        explicacao=(
            "Ler no começo do corpo do `while` sem testar em seguida faz o sentinela ser processado como se fosse dado válido. "
            "Lendo antes do laço e ao final de cada repetição, o `-1` interrompe o laço antes de entrar na soma."
        ),
    )


@exercicio(estagio=8, dificuldade=3, tipo="completar", conceitos=["while", "contador", "aritmeticos"])
def completar_quantas_vezes_divide_por_2(r):
    casos = [r.randint(16, 128), r.randint(9, 45), 1, 64]
    n0 = casos[0]
    tmp, cnt = n0, 0
    while tmp >= 2:
        tmp //= 2
        cnt += 1
    return dict(
        titulo="Dividindo até não dar mais",
        enunciado=(
            "Leia um inteiro positivo `n`. Quantas vezes podemos dividir `n` inteiramente por `2` (`n = n // 2`) "
            "enquanto `n` for maior ou igual a `2`?\n\n"
            f"Complete as lacunas `___`. Exemplo para `n = {n0}`:\n```\nDivisões: {cnt}\n```"
        ),
        codigo_inicial=(
            'n = int(input("N: "))\n'
            "vezes = ___\n"
            "while n >= 2:\n"
            "    n = n ___ 2\n"
            "    vezes += ___\n"
            'print("Divisões:", vezes)\n'
        ),
        solucao=(
            'n = int(input("N: "))\n'
            "vezes = 0\n"
            "while n >= 2:\n"
            "    n = n // 2\n"
            "    vezes += 1\n"
            'print("Divisões:", vezes)\n'
        ),
        testes=[{"entrada": str(x)} for x in casos],
        testes_visiveis=1,
        dicas=[
            "O contador `vezes` começa zerado e soma `1` a cada divisão.",
            "Para divisão inteira em Python, use `//`.",
        ],
        explicacao=(
            "A cada repetição `n` cai pela metade inteira (`// 2`) até ficar menor que 2, e `vezes` conta exatamente quantos passos foram necessários."
        ),
    )


@exercicio(estagio=8, dificuldade=4, tipo="codigo", conceitos=["while", "acumulador", "aritmeticos"])
def soma_dos_digitos_while(r):
    casos = [r.randint(123, 9876), r.randint(1000, 99999), 7, 1005]
    n0 = casos[0]
    s0 = sum(int(d) for d in str(n0))
    return dict(
        titulo="Somando os algarismos de qualquer número",
        enunciado=(
            "Leia um número inteiro positivo `n` (de qualquer tamanho!).\n\n"
            "Usando apenas `while`, `% 10` (último dígito) e `// 10` (corta último dígito), "
            "calcule a soma de todos os seus algarismos.\n\n"
            f"Exemplo para `{n0}`:\n```\nSoma dos dígitos: {s0}\n```"
        ),
        solucao=(
            'n = int(input("Número: "))\n'
            "soma = 0\n"
            "while n > 0:\n"
            "    digito = n % 10\n"
            "    soma += digito\n"
            "    n //= 10\n"
            'print("Soma dos dígitos:", soma)\n'
        ),
        testes=[{"entrada": str(x)} for x in casos],
        testes_visiveis=1,
        dicas=[
            "Enquanto `n > 0`, pegue o último dígito com `n % 10`, some em `soma`, e remova esse dígito fazendo `n = n // 10`.",
            "Quando sobrar só 1 dígito (ex.: `4`), `4 // 10` dá `0`, encerrando o `while`!",
        ],
        explicacao=(
            "Essa é uma técnica fundamental da lógica: `% 10` lê o algarismo das unidades e `//= 10` desliza o número "
            "uma casa para a direita até zerar."
        ),
    )


@exercicio(estagio=8, dificuldade=4, tipo="prever", conceitos=["while", "contador", "teste_de_mesa"])
def prever_while_dobrando_ate_meta(r):
    inicio = r.randint(2, 5)
    meta = inicio * r.randint(10, 20)
    return dict(
        titulo="Quando o dobro alcança a meta?",
        enunciado=(
            "Acompanhe o crescimento de `valor` e de `passos` no teste de mesa e escreva exatamente a saída:"
        ),
        solucao=(
            f"valor = {inicio}\n"
            f"meta = {meta}\n"
            "passos = 0\n"
            "while valor < meta:\n"
            "    valor *= 2\n"
            "    passos += 1\n"
            "print(passos, valor)\n"
        ),
        dicas=[
            "Simule volta por volta: enquanto `valor < meta`, dobre `valor` e aumente `passos` em 1.",
            "Assim que `valor >= meta`, o laço para imediatamente.",
        ],
        explicacao=(
            "Esse padrão encontra quantas duplicações são necessárias para atingir uma meta exponencialmente, "
            "parando na primeira vez em que `valor` iguala ou supera `meta`."
        ),
    )


@exercicio(estagio=8, dificuldade=4, tipo="codigo", conceitos=["while", "if_else", "input"])
def maior_e_menor_sentinela(r):
    def seq():
        return [r.randint(1, 99) for _ in range(r.randint(4, 6))] + [0]
    casos = [seq(), seq(), [42, 0], [10, 5, 30, 2, 0]]
    c0 = casos[0][:-1]
    return dict(
        titulo="Maior e menor até digitar 0",
        enunciado=(
            "Leia números inteiros **positivos** um por linha até que o usuário digite `0` (garantido que haverá pelo menos um número antes do 0).\n\n"
            "Sem usar listas, descubra e mostre o **maior** e o **menor** número digitado:\n"
            f"Exemplo para `{' '.join(map(str, casos[0]))}`:\n"
            f"```\nMaior: {max(c0)}\nMenor: {min(c0)}\n```"
        ),
        solucao=(
            "n = int(input())\n"
            "maior = n\n"
            "menor = n\n"
            "while n != 0:\n"
            "    if n > maior:\n"
            "        maior = n\n"
            "    if n < menor:\n"
            "        menor = n\n"
            "    n = int(input())\n"
            'print("Maior:", maior)\n'
            'print("Menor:", menor)\n'
        ),
        testes=[{"entrada": "\n".join(map(str, c))} for c in casos],
        testes_visiveis=1,
        dicas=[
            "Inicialize `maior` e `menor` com o **primeiro número lido** (não com 0 — pois todos poderiam ser maiores que 0!).",
            "A cada novo número antes do `0`, atualize `maior` se `n > maior` e `menor` se `n < menor`.",
        ],
        explicacao=(
            "Iniciar `maior` e `menor` com o primeiro valor válido evita bugs clássicos (como `menor = 0` nunca ser atualizado "
            "por números positivos). Depois, cada novo valor é comparado com os recordes atuais."
        ),
    )


@exercicio(estagio=8, dificuldade=4, tipo="corrigir", conceitos=["while", "if_else", "depuracao"])
def corrigir_menor_inicializado_zero(r):
    casos = [
        [r.randint(12, 30), r.randint(5, 11), r.randint(15, 40), 0],
        [50, 20, 35, 0],
        [8, 0],
    ]
    c0 = casos[0][:-1]
    return dict(
        titulo="O menor sempre dá zero!",
        enunciado=(
            "O programa deveria ler inteiros positivos até `0` e mostrar o **menor** valor digitado (sem contar o 0).\n"
            f"Para `{' '.join(map(str, casos[0]))}`, deveria mostrar:\n```\nMenor: {min(c0)}\n```\n"
            "Mas está sempre imprimindo `Menor: 0`! Descubra por quê e corrija."
        ),
        codigo_inicial=(
            "menor = 0\n"
            "n = int(input())\n"
            "while n != 0:\n"
            "    if n < menor:\n"
            "        menor = n\n"
            "    n = int(input())\n"
            'print("Menor:", menor)\n'
        ),
        solucao=(
            "n = int(input())\n"
            "menor = n\n"
            "while n != 0:\n"
            "    if n < menor:\n"
            "        menor = n\n"
            "    n = int(input())\n"
            'print("Menor:", menor)\n'
        ),
        testes=[{"entrada": "\n".join(map(str, c))} for c in casos],
        testes_visiveis=1,
        dicas=[
            "Se `menor` começa valendo `0` e só entram números positivos, a condição `n < 0` alguma vez será verdadeira?",
            "Leia o primeiro `n` e faça `menor = n`!",
        ],
        explicacao=(
            "Começar `menor = 0` faz `0` vencer qualquer número positivo na comparação `<`. Ao inicializar `menor` com o "
            "primeiro dado válido, a comparação passa a funcionar para qualquer faixa de valores."
        ),
    )


@exercicio(estagio=8, dificuldade=5, tipo="codigo", conceitos=["while", "contador", "if_else"])
def sequencia_collatz_passos(r):
    casos = [r.randint(6, 15), r.randint(18, 30), 1, 7]
    n0 = casos[0]
    x, p0 = n0, 0
    while x != 1:
        x = x // 2 if x % 2 == 0 else 3 * x + 1
        p0 += 1
    return dict(
        titulo="Conjectura de Collatz",
        enunciado=(
            "Na famosa sequência de Collatz, partindo de um inteiro positivo `n`, repetimos até `n` chegar a `1`:\n"
            "- Se `n` for **par**: `n = n // 2`\n"
            "- Se `n` for **ímpar**: `n = 3 * n + 1`\n\n"
            "Leia `n` e conte quantos **passos** foram necessários até `n` virar `1`:\n"
            f"Exemplo para `n = {n0}`:\n```\nPassos: {p0}\n```"
        ),
        solucao=(
            'n = int(input("N: "))\n'
            "passos = 0\n"
            "while n != 1:\n"
            "    if n % 2 == 0:\n"
            "        n = n // 2\n"
            "    else:\n"
            "        n = 3 * n + 1\n"
            "    passos += 1\n"
            'print("Passos:", passos)\n'
        ),
        testes=[{"entrada": str(x)} for x in casos],
        testes_visiveis=1,
        dicas=[
            "Use `while n != 1:` (se começar em `1`, já termina com 0 passos!).",
            "Dentro do laço, use `if n % 2 == 0:` / `else:` para atualizar `n` e depois some `1` em `passos`.",
        ],
        explicacao=(
            "Ninguém sabe exatamente quantas voltas um número levará para chegar a 1 antes de simular — por isso "
            "`while n != 1:` é a ferramenta perfeita."
        ),
    )


@exercicio(estagio=8, dificuldade=5, tipo="codigo", conceitos=["while", "acumulador", "contador"])
def meses_para_juntar_meta(r):
    casos = [
        (round(r.uniform(800.0, 2000.0), 2), round(r.uniform(150.0, 350.0), 2), round(r.uniform(2500.0, 4500.0), 2)),
        (1000.00, 200.00, 1500.00),
        (500.00, 100.00, 500.00),
    ]
    ini0, dep0, meta0 = casos[0]
    saldo, m0 = ini0, 0
    while saldo < meta0:
        saldo = saldo * 1.01 + dep0
        m0 += 1
    return dict(
        titulo="Simulando poupança mês a mês",
        enunciado=(
            "Leia três valores (`float`, um por linha): `saldo_inicial`, `deposito_mensal` e `meta`.\n\n"
            "A cada mês, o saldo atual **rende 1%** (`saldo * 1.01`) e depois recebe o `deposito_mensal`.\n"
            "Simule mês a mês com `while` até `saldo >= meta` e mostre quantos meses levou e o saldo final:\n\n"
            f"Exemplo (`{ini0:.2f}`, `{dep0:.2f}`, `{meta0:.2f}`):\n"
            f"```\nMeses: {m0}\nSaldo final: R$ {saldo:.2f}\n```"
        ),
        solucao=(
            'saldo = float(input("Saldo inicial: "))\n'
            'deposito = float(input("Depósito mensal: "))\n'
            'meta = float(input("Meta: "))\n'
            "meses = 0\n"
            "while saldo < meta:\n"
            "    saldo = saldo * 1.01 + deposito\n"
            "    meses += 1\n"
            'print("Meses:", meses)\n'
            'print(f"Saldo final: R$ {saldo:.2f}")\n'
        ),
        testes=[{"entrada": f"{a:.2f}\n{b:.2f}\n{c:.2f}"} for a, b, c in casos],
        testes_visiveis=1,
        dicas=[
            "Enquanto `saldo < meta`, atualize `saldo = saldo * 1.01 + deposito` e some `1` em `meses`.",
            "Se o saldo inicial já for maior ou igual à meta, o laço nem roda (`Meses: 0`).",
        ],
        explicacao=(
            "Simular passo a passo dentro do `while` resolve naturalmente problemas com juros compostos e aportes mensais "
            "sem precisar de fórmulas matemáticas complexas."
        ),
    )
