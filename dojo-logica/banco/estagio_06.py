"""Estágio 6 - Decisões com if e if/else (sem elif)."""

from .base import exercicio


@exercicio(estagio=6, dificuldade=1, tipo="codigo", conceitos=["if_else", "comparacao", "input"])
def par_ou_impar(r):
    casos = [r.randrange(2, 50, 2), r.randrange(3, 51, 2), 0, -r.randint(1, 15)]
    n0 = casos[0]
    return dict(
        titulo="Par ou ímpar?",
        enunciado=(
            "Leia um número inteiro e use `if` e `else` para imprimir exatamente `Par` se ele for par, "
            "ou `Ímpar` se ele for ímpar.\n\n"
            f"Exemplo para `{n0}`:\n```\n{'Par' if n0 % 2 == 0 else 'Ímpar'}\n```"
        ),
        solucao=(
            'n = int(input("Número: "))\n'
            "if n % 2 == 0:\n"
            '    print("Par")\n'
            "else:\n"
            '    print("Ímpar")\n'
        ),
        testes=[{"entrada": str(x)} for x in casos],
        testes_visiveis=1,
        dicas=[
            "Um número é par quando o resto da divisão por 2 é zero (`n % 2 == 0`).",
            "Não esqueça os dois-pontos `:` no fim da linha do `if` e do `else`, nem a indentação de 4 espaços.",
        ],
        explicacao=(
            "Se `n % 2 == 0` for verdadeiro, o bloco dentro do `if` roda e imprime `Par`. Caso contrário, "
            "o programa vai direto para o bloco do `else` e imprime `Ímpar`."
        ),
    )


@exercicio(estagio=6, dificuldade=1, tipo="completar", conceitos=["if_else", "comparacao"])
def completar_aprovado_reprovado(r):
    media_min = r.choice([5.0, 6.0, 7.0, 7.5])
    casos = [
        media_min,
        round(media_min - r.choice([0.5, 1.0, 1.5]), 1),
        round(media_min + r.choice([0.5, 1.5, 2.0]), 1),
        0.0,
    ]
    n0 = casos[0]
    return dict(
        titulo="Situação da disciplina",
        enunciado=(
            f"A média mínima para aprovação é **{media_min:.1f}**. Complete as lacunas `___` para ler a nota (`float`) "
            "e mostrar `Aprovado` ou `Reprovado`.\n\n"
            f"Exemplo para `{n0}`:\n```\nAprovado\n```"
        ),
        codigo_inicial=(
            'nota = float(input("Nota: "))\n'
            f"___ nota >= {media_min}:\n"
            '    print("Aprovado")\n'
            "___:\n"
            '    print("Reprovado")\n'
        ),
        solucao=(
            'nota = float(input("Nota: "))\n'
            f"if nota >= {media_min}:\n"
            '    print("Aprovado")\n'
            "else:\n"
            '    print("Reprovado")\n'
        ),
        testes=[{"entrada": str(x)} for x in casos],
        testes_visiveis=1,
        dicas=[
            "A palavra que inicia a condição é `if` e a que trata o caso contrário é `else`.",
            "Lembre que `else:` não recebe condição nenhuma.",
        ],
        explicacao=(
            f"Com `if nota >= {media_min}:` garantimos que exatamente `{media_min}` também seja aprovado, "
            "e o `else:` cobre todas as notas abaixo disso."
        ),
    )


@exercicio(estagio=6, dificuldade=2, tipo="prever", conceitos=["if_else", "teste_de_mesa"])
def prever_if_com_linha_fora(r):
    x = r.randint(10, 25)
    limite = x + r.randint(5, 12)
    return dict(
        titulo="O poder da indentação",
        enunciado=(
            "Observe **quais linhas estão recuadas** dentro do `if`/`else` e qual linha está fora.\n\n"
            "Sem executar, escreva exatamente o que o código abaixo vai mostrar:"
        ),
        solucao=(
            f"pontos = {x}\n"
            f"if pontos >= {limite}:\n"
            '    print("Meta batida")\n'
            '    pontos = pontos + 10\n'
            "else:\n"
            '    print("Quase lá")\n'
            'print("Pontos:", pontos)\n'
        ),
        dicas=[
            f"Como `{x} >= {limite}` é falso, o bloco do `if` (inclusive o `+ 10`) não roda!",
            "A última linha `print(\"Pontos:\", pontos)` **não está indentada**, então ela roda de qualquer jeito.",
        ],
        explicacao=(
            f"Como a condição é falsa, executa o `else` (`Quase lá`), e `pontos` não ganha +10. "
            f"Depois do `if/else`, a linha alinhada à margem esquerda sempre executa, imprimindo `Pontos: {x}`."
        ),
    )


@exercicio(estagio=6, dificuldade=2, tipo="codigo", conceitos=["if_else", "input", "fstring"])
def frete_gratis_loja(r):
    minimo = r.choice([100, 120, 150, 200])
    frete = r.choice([15, 18, 22])
    casos = [
        round(minimo - 15.5, 2),
        float(minimo),
        round(minimo + 42.3, 2),
    ]
    c0 = casos[0]
    t0 = c0 if c0 >= minimo else c0 + frete
    return dict(
        titulo="Frete grátis acima do mínimo",
        enunciado=(
            f"Uma loja dá **frete grátis** para compras a partir de **R$ {minimo:.2f}**. "
            f"Abaixo disso, cobra **R$ {frete:.2f}** de frete.\n\n"
            "Leia o valor da compra (`float`) e mostre o total final com 2 casas decimais:\n"
            f"Exemplo para `{c0:.2f}`:\n```\nTotal: R$ {t0:.2f}\n```"
        ),
        solucao=(
            'compra = float(input("Valor da compra: "))\n'
            f"if compra >= {minimo}:\n"
            "    total = compra\n"
            "else:\n"
            f"    total = compra + {frete}\n"
            'print(f"Total: R$ {total:.2f}")\n'
        ),
        testes=[{"entrada": f"{x:.2f}"} for x in casos],
        testes_visiveis=1,
        dicas=[
            f"Teste `if compra >= {minimo}:` — nesse caso o total é a própria `compra`.",
            f"No `else:`, some `{frete}` ao valor da compra.",
        ],
        explicacao=(
            f"Definimos `total` em ambos os caminhos (`if` e `else`) e deixamos o `print` fora da decisão, "
            "evitando escrever dois `print`s parecidos."
        ),
    )


@exercicio(estagio=6, dificuldade=2, tipo="corrigir", conceitos=["if_else", "comparacao", "depuracao"])
def corrigir_atribuicao_no_if(r):
    senha_certa = r.choice(["python123", "dojo2026", "segredo", "alfa99"])
    casos = [senha_certa, "errada", "1234", senha_certa.upper()]
    return dict(
        titulo="Cofre trancado por um =",
        enunciado=(
            f"O programa deveria ler uma senha (`str`) e compará-la com `\"{senha_certa}\"`, imprimindo "
            "`Acesso liberado` se for igual ou `Senha incorreta` se for diferente.\n\n"
            "Mas dá erro de sintaxe logo na linha do `if`! Corrija o código."
        ),
        codigo_inicial=(
            'senha = input("Senha: ")\n'
            f'if senha = "{senha_certa}":\n'
            '    print("Acesso liberado")\n'
            "else:\n"
            '    print("Senha incorreta")\n'
        ),
        solucao=(
            'senha = input("Senha: ")\n'
            f'if senha == "{senha_certa}":\n'
            '    print("Acesso liberado")\n'
            "else:\n"
            '    print("Senha incorreta")\n'
        ),
        testes=[{"entrada": s} for s in casos],
        testes_visiveis=2,
        dicas=[
            "Um único `=` tenta guardar um valor dentro de uma variável; dentro de um `if`, queremos **comparar**!",
            "Troque `=` por `==` na condição.",
        ],
        explicacao=(
            "Em Python, atribuição (`=`) não é permitida como condição do `if`. Para verificar igualdade, usamos sempre `==`."
        ),
    )


@exercicio(estagio=6, dificuldade=3, tipo="codigo", conceitos=["if_else", "input"])
def maior_de_dois_numeros(r):
    casos = [
        (r.randint(20, 80), r.randint(1, 19)),
        (r.randint(1, 19), r.randint(20, 80)),
        (15, 15),
        (-5, -12),
    ]
    a0, b0 = casos[0]
    return dict(
        titulo="Maior entre dois valores",
        enunciado=(
            "Leia dois números inteiros (um por linha). Mostre o maior deles no formato abaixo "
            "(se forem iguais, o maior valor é o próprio número):\n\n"
            f"Exemplo para `{a0}` e `{b0}`:\n```\nMaior: {max(a0, b0)}\n```"
        ),
        solucao=(
            'a = int(input("Primeiro: "))\n'
            'b = int(input("Segundo: "))\n'
            "if a >= b:\n"
            "    maior = a\n"
            "else:\n"
            "    maior = b\n"
            'print("Maior:", maior)\n'
        ),
        testes=[{"entrada": f"{x}\n{y}"} for x, y in casos],
        testes_visiveis=1,
        dicas=[
            "Compare `a >= b`: se for verdade, `maior = a`; senão, `maior = b`.",
            "Depois do `if/else`, imprima `print(\"Maior:\", maior)`.",
        ],
        explicacao=(
            "Com `if a >= b:` tratamos tanto quando `a` é maior quanto o empate (já que em caso de empate os dois são iguais)."
        ),
    )


@exercicio(estagio=6, dificuldade=3, tipo="codigo", conceitos=["if_else", "aritmeticos"])
def diferenca_absoluta(r):
    casos = [
        (r.randint(20, 50), r.randint(5, 18)),
        (r.randint(5, 18), r.randint(20, 50)),
        (10, 10),
        (-3, 7),
    ]
    a0, b0 = casos[0]
    return dict(
        titulo="Distância positiva entre dois números",
        enunciado=(
            "Leia dois números inteiros `a` e `b`. Sem usar a função `abs()`, use `if/else` para calcular a "
            "**diferença positiva** entre eles (o maior menos o menor).\n\n"
            f"Exemplo para `{a0}` e `{b0}`:\n```\nDiferença: {abs(a0 - b0)}\n```"
        ),
        solucao=(
            'a = int(input("A: "))\n'
            'b = int(input("B: "))\n'
            "if a >= b:\n"
            "    diff = a - b\n"
            "else:\n"
            "    diff = b - a\n"
            'print("Diferença:", diff)\n'
        ),
        testes=[{"entrada": f"{x}\n{y}"} for x, y in casos],
        testes_visiveis=2,
        dicas=[
            "Se `a >= b`, faça `a - b`; caso contrário (`b` é maior), faça `b - a`.",
            "Assim o resultado nunca fica negativo!",
        ],
        explicacao=(
            "Subtraindo sempre o menor do maior garantimos um número >= 0, reproduzindo exatamente a lógica do valor absoluto `|a - b|`."
        ),
    )


@exercicio(estagio=6, dificuldade=3, tipo="corrigir", conceitos=["if_else", "aritmeticos", "depuracao"])
def corrigir_divisao_por_zero(r):
    casos = [
        (r.randint(20, 90), r.randint(2, 9)),
        (r.randint(10, 40), 0),
        (0, r.randint(2, 6)),
    ]
    a0, b0 = casos[0]
    return dict(
        titulo="Protegendo contra divisão por zero",
        enunciado=(
            "O programa lê numerador e denominador (`int`). Se o denominador for diferente de zero, imprime o resultado "
            "com 2 casas (`Resultado: X.XX`); se for zero, deve imprimir `Não é possível dividir por zero`.\n\n"
            "Mas do jeito atual a divisão acontece **antes** do `if`, quebrando quando o divisor é 0! Corrija."
        ),
        codigo_inicial=(
            'a = int(input("Numerador: "))\n'
            'b = int(input("Denominador: "))\n'
            "res = a / b\n"
            "if b == 0:\n"
            '    print("Não é possível dividir por zero")\n'
            "else:\n"
            '    print(f"Resultado: {res:.2f}")\n'
        ),
        solucao=(
            'a = int(input("Numerador: "))\n'
            'b = int(input("Denominador: "))\n'
            "if b == 0:\n"
            '    print("Não é possível dividir por zero")\n'
            "else:\n"
            "    res = a / b\n"
            '    print(f"Resultado: {res:.2f}")\n'
        ),
        testes=[{"entrada": f"{x}\n{y}"} for x, y in casos],
        testes_visiveis=2,
        dicas=[
            "Se `res = a / b` fica antes do `if`, quando `b` vale 0 o Python já quebra ali mesmo!",
            "Mova o cálculo `res = a / b` para **dentro** do bloco `else:`.",
        ],
        explicacao=(
            "Testamos `if b == 0:` antes de dividir e só executamos `a / b` dentro do `else:`, onde já temos certeza de que `b` não é zero."
        ),
    )


@exercicio(estagio=6, dificuldade=3, tipo="completar", conceitos=["if_else", "logicos"])
def completar_desconto_clube(r):
    desconto = r.choice([10, 15, 20])
    casos = [
        (250.0, "nao"),
        (120.0, "sim"),
        (120.0, "nao"),
        (200.0, "nao"),
    ]
    v0, s0 = casos[0]
    tot0 = v0 * (1 - desconto / 100) if (v0 >= 200 or s0 == "sim") else v0
    return dict(
        titulo="Desconto de VIP ou compra alta",
        enunciado=(
            f"Um cliente ganha **{desconto}% de desconto** se a compra for **a partir de R$ 200.00** OU se ele responder `\"sim\"` "
            "para ser sócio do clube.\n\n"
            "Complete as lacunas `___` para ler o valor (`float`) e se é sócio (`\"sim\"` ou `\"nao\"`) e imprimir o total:\n"
            f"Exemplo (`{v0:.2f}`, `\"{s0}\"`):\n```\nTotal a pagar: R$ {tot0:.2f}\n```"
        ),
        codigo_inicial=(
            'valor = float(input("Valor: "))\n'
            'socio = input("É sócio? (sim/nao): ")\n'
            'if valor >= 200 ___ socio == "sim":\n'
            f"    valor = valor * (1 - {desconto} / 100)\n"
            'print(f"Total a pagar: R$ {valor:___}")\n'
        ),
        solucao=(
            'valor = float(input("Valor: "))\n'
            'socio = input("É sócio? (sim/nao): ")\n'
            'if valor >= 200 or socio == "sim":\n'
            f"    valor = valor * (1 - {desconto} / 100)\n"
            'print(f"Total a pagar: R$ {valor:.2f}")\n'
        ),
        testes=[{"entrada": f"{v}\n{s}"} for v, s in casos],
        testes_visiveis=1,
        dicas=[
            "Basta atender a **uma** das duas condições -> operador lógico `or`.",
            "Para exibir 2 casas decimais na f-string, use `.2f`.",
        ],
        explicacao=(
            "Aqui usamos um `if` **sem `else`**: se o cliente tiver direito ao desconto, atualizamos `valor`; "
            "senão, `valor` permanece intacto até o `print` final."
        ),
    )


@exercicio(estagio=6, dificuldade=3, tipo="prever", conceitos=["if_else", "logicos", "teste_de_mesa"])
def prever_if_sequencial_vs_else(r):
    a = r.randint(6, 12)
    return dict(
        titulo="Dois ifs seguidos são diferentes de if/else!",
        enunciado=(
            "Preste muita atenção: abaixo há **dois `if`s independentes**, e não um `if/else`.\n\n"
            "Faça o teste de mesa e escreva exatamente a saída:"
        ),
        solucao=(
            f"n = {a}\n"
            "if n > 5:\n"
            "    n = n + 4\n"
            "if n > 10:\n"
            '    print("Grande")\n'
            "else:\n"
            '    print("Pequeno")\n'
            "print(n)\n"
        ),
        dicas=[
            "O primeiro `if` muda o valor de `n` antes do segundo `if` ser testado!",
            f"Com `n` começando em {a}, `n > 5` é verdadeiro, então `n` passa a valer {a + 4}.",
        ],
        explicacao=(
            f"`{a} > 5` é verdadeiro, logo `n` vira `{a + 4}`. Em seguida o segundo `if` testa `{a + 4} > 10` "
            f"({'verdadeiro' if a + 4 > 10 else 'falso'}), imprimindo `{'Grande' if a + 4 > 10 else 'Pequeno'}` e depois `{a + 4}`."
        ),
    )


@exercicio(estagio=6, dificuldade=4, tipo="codigo", conceitos=["if_else", "aritmeticos", "input"])
def horas_extras_trabalho(r):
    taxa = r.randint(20, 40)
    casos = [
        (46, taxa),
        (40, taxa),
        (32, taxa),
        (50, 30),
    ]
    h0, t0 = casos[0]
    sal0 = 40 * t0 + (h0 - 40) * t0 * 1.5
    return dict(
        titulo="Salário com horas extras",
        enunciado=(
            "Um funcionário trabalha até **40 horas** semanais ganhando o valor normal por hora. "
            "Cada hora **acima de 40** vale **50% a mais** (1.5x o valor da hora).\n\n"
            "Leia as `horas` trabalhadas (`int`) e o `valor_hora` (`float`), e mostre o pagamento semanal com 2 casas:\n"
            f"Exemplo (`{h0}` horas a `R$ {t0:.2f}`):\n```\nPagamento: R$ {sal0:.2f}\n```"
        ),
        solucao=(
            'horas = int(input("Horas: "))\n'
            'valor_hora = float(input("Valor/hora: "))\n'
            "if horas <= 40:\n"
            "    salario = horas * valor_hora\n"
            "else:\n"
            "    extras = horas - 40\n"
            "    salario = 40 * valor_hora + extras * valor_hora * 1.5\n"
            'print(f"Pagamento: R$ {salario:.2f}")\n'
        ),
        testes=[{"entrada": f"{h}\n{t:.2f}"} for h, t in casos],
        testes_visiveis=2,
        dicas=[
            "Se `horas <= 40`, todas as horas são pagas no valor normal.",
            "No `else:`, apenas `extras = horas - 40` horas ganham `1.5 * valor_hora`; as primeiras 40 ganham o valor normal.",
        ],
        explicacao=(
            "Um erro comum é multiplicar **todas** as horas por 1.5 quando passa de 40. O correto é pagar 40 horas normais "
            "mais o excedente (`horas - 40`) com o adicional de 50%."
        ),
    )


@exercicio(estagio=6, dificuldade=4, tipo="corrigir", conceitos=["if_else", "comparacao", "depuracao"])
def corrigir_desconto_condicao_invertida(r):
    casos = [
        (r.randint(2, 5), 10.0),
        (r.randint(10, 15), 10.0),
        (9, 10.0),
    ]
    q0, p0 = casos[0]
    return dict(
        titulo="Desconto para o lado errado!",
        enunciado=(
            "Um atacadão dá **15% de desconto** quando o cliente compra **10 ou mais unidades**; abaixo de 10 unidades paga o preço cheio.\n"
            "Mas o programa está dando desconto justamente para quem compra menos de 10, e cobrando cheio de quem leva 10+!\n\n"
            f"Exemplo (`{q0}` un a `R$ {p0:.2f}`):\n```\nTotal: R$ {q0 * p0:.2f}\n```\n"
            "Encontre o bug na condição e corrija."
        ),
        codigo_inicial=(
            'qtd = int(input("Quantidade: "))\n'
            'preco = float(input("Preço unitário: "))\n'
            "total = qtd * preco\n"
            "if qtd < 10:\n"
            "    total = total * 0.85\n"
            'print(f"Total: R$ {total:.2f}")\n'
        ),
        solucao=(
            'qtd = int(input("Quantidade: "))\n'
            'preco = float(input("Preço unitário: "))\n'
            "total = qtd * preco\n"
            "if qtd >= 10:\n"
            "    total = total * 0.85\n"
            'print(f"Total: R$ {total:.2f}")\n'
        ),
        testes=[{"entrada": f"{q}\n{p:.2f}"} for q, p in casos],
        testes_visiveis=2,
        dicas=[
            "Leia com atenção a condição do `if`: `qtd < 10` está aplicando 15% de desconto quando é menor que 10.",
            "\"10 ou mais unidades\" significa `qtd >= 10`.",
        ],
        explicacao=(
            "A condição estava invertida (`<` em vez de `>=`). Inverter um sinal de comparação é um bug de lógica silencioso: "
            "o código roda sem mensagens de erro, mas cobra errado!"
        ),
    )


@exercicio(estagio=6, dificuldade=4, tipo="completar", conceitos=["if_else", "logicos"])
def completar_multiplo_com_if(r):
    d1 = r.choice([3, 4, 5])
    d2 = r.choice([7, 8, 9])
    casos = [d1 * d2, d1 * d2 * 2, d1 * 2, d2 * 2, d1 + 1]
    return dict(
        titulo=f"Múltiplo de {d1} e {d2} ao mesmo tempo",
        enunciado=(
            f"Leia um inteiro `n`. Complete as lacunas `___` para verificar se `n` é divisível por **{d1}** e por **{d2}** ao mesmo tempo.\n\n"
            f"Exemplo para `{casos[0]}`:\n```\nDivisível pelos dois\n```"
        ),
        codigo_inicial=(
            'n = int(input("Número: "))\n'
            f"if n % {d1} == ___ and n % {d2} == ___:\n"
            '    print("Divisível pelos dois")\n'
            "else:\n"
            '    print("Não é divisível pelos dois")\n'
        ),
        solucao=(
            'n = int(input("Número: "))\n'
            f"if n % {d1} == 0 and n % {d2} == 0:\n"
            '    print("Divisível pelos dois")\n'
            "else:\n"
            '    print("Não é divisível pelos dois")\n'
        ),
        testes=[{"entrada": str(x)} for x in casos],
        testes_visiveis=1,
        dicas=[
            "Um número é divisível por outro quando o resto da divisão (`%`) é `0`.",
            "Como precisa atender aos dois ao mesmo tempo, usamos `and`.",
        ],
        explicacao=(
            f"Testamos ambos os restos com `== 0` ligados por `and`. Se falhar em apenas um deles, cai no `else`."
        ),
    )


@exercicio(estagio=6, dificuldade=5, tipo="codigo", conceitos=["if_else", "logicos", "input"])
def validar_emprestimo_bancario(r):
    max_parcela_pct = r.choice([25, 30, 35])
    sal = r.choice([2500.0, 3000.0, 4000.0, 5000.0])
    casos = [
        (sal, round(sal * (max_parcela_pct / 100) * 12 * 0.7, 2), 12),
        (sal, round(sal * (max_parcela_pct / 100) * 10 * 1.4, 2), 10),
        (sal, round(sal * (max_parcela_pct / 100) * 10, 2), 10),
        (sal + 500, 15000.00, 12),
    ]
    s0, v0, m0 = casos[0]
    p0 = v0 / m0
    return dict(
        titulo="Análise de empréstimo",
        enunciado=(
            "Leia, um por linha:\n"
            "1. Salário mensal (`float`)\n"
            "2. Valor do empréstimo desejado (`float`)\n"
            "3. Quantidade de meses para pagar (`int`)\n\n"
            f"Calcule o valor da parcela (`emprestimo / meses`). Se a parcela for **menor ou igual a {max_parcela_pct}% do salário**, "
            "mostre `Empréstimo aprovado` e o valor da parcela; caso contrário, mostre `Empréstimo negado`.\n\n"
            f"Exemplo (`{s0:.2f}`, `{v0:.2f}`, `{m0}`):\n"
            f"```\nParcela: R$ {p0:.2f}\nEmpréstimo aprovado\n```"
        ),
        solucao=(
            'salario = float(input("Salário: "))\n'
            'emprestimo = float(input("Empréstimo: "))\n'
            'meses = int(input("Meses: "))\n'
            "parcela = emprestimo / meses\n"
            f"limite = salario * {max_parcela_pct / 100}\n"
            'print(f"Parcela: R$ {parcela:.2f}")\n'
            "if parcela <= limite:\n"
            '    print("Empréstimo aprovado")\n'
            "else:\n"
            '    print("Empréstimo negado")\n'
        ),
        testes=[{"entrada": f"{s:.2f}\n{v:.2f}\n{m}"} for s, v, m in casos],
        testes_visiveis=1,
        dicas=[
            f"Calcule `parcela = emprestimo / meses` e `limite = salario * {max_parcela_pct / 100}` antes do `if`.",
            f"Compare `if parcela <= limite:` (menor ou igual permite exatamente {max_parcela_pct}%).",
        ],
        explicacao=(
            "Imprimimos o valor da parcela antes da decisão (pois aparece nos dois casos) e então comparamos "
            "`parcela <= limite` para aprovar ou negar."
        ),
    )


@exercicio(estagio=6, dificuldade=5, tipo="prever", conceitos=["if_else", "teste_de_mesa"])
def prever_if_aninhado_dentro_else(r):
    a = r.randint(10, 20)
    b = r.randint(5, 15)
    c = r.randint(21, 30)
    return dict(
        titulo="If dentro de outro if (aninhado)",
        enunciado=(
            "Quando queremos comparar três variáveis usando apenas `if` e `else` (sem `elif`), podemos colocar "
            "um `if/else` dentro do bloco de outro `if/else`. Faça o teste de mesa e escreva a saída exata:"
        ),
        solucao=(
            f"a = {a}\n"
            f"b = {b}\n"
            f"c = {c}\n"
            "if a > b:\n"
            "    if a > c:\n"
            "        print(a)\n"
            "    else:\n"
            "        print(c)\n"
            "else:\n"
            "    if b > c:\n"
            "        print(b)\n"
            "    else:\n"
            "        print(c)\n"
        ),
        dicas=[
            f"Comece testando `{a} > {b}`. Como é {'verdadeiro' if a > b else 'falso'}, entre no ramo correspondente.",
            "Dentro do ramo escolhido, teste apenas o `if/else` interno.",
        ],
        explicacao=(
            f"Esse aninhamento sempre encontra o maior entre três números: como `a={a}`, `b={b}` e `c={c}`, "
            f"ele percorre os desvios corretos e imprime `{max(a, b, c)}`."
        ),
    )
