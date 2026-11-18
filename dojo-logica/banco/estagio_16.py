"""Estágio 16 - Programação Defensiva, Validação e Exceções (try/except, None)."""

from .base import exercicio


@exercicio(estagio=16, dificuldade=1, tipo="funcao", conceitos=["excecoes", "funcoes", "return"])
def divisao_segura(r):
    a = r.randint(10, 50)
    b = r.randint(2, 9)
    casos = [(a, b), (a, 0), ("20", "4"), ("abc", 2), (None, 5)]
    return dict(
        titulo="Divisão segura com validação",
        enunciado=(
            "Escreva a função `dividir_seguro(a, b)` que converte `a` e `b` para `float` e retorna "
            "`round(a / b, 2)`.\n\n"
            "- Se `b` for zero ou se `a`/`b` não puderem ser convertidos em número (ex.: texto inválido ou `None`), "
            "retorne `None` sem lançar exceção.\n\n"
            f"Exemplo: `dividir_seguro({a}, {b})` -> `{round(a / b, 2)}`, `dividir_seguro({a}, 0)` -> `None`"
        ),
        solucao=(
            "def dividir_seguro(a, b):\n"
            "    try:\n"
            "        num = float(a)\n"
            "        den = float(b)\n"
            "        if den == 0:\n"
            "            return None\n"
            "        return round(num / den, 2)\n"
            "    except (ValueError, TypeError):\n"
            "        return None\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(dividir_seguro({x!r}, {y!r}))"} for x, y in casos],
        testes_visiveis=2,
        dicas=[
            "Converta `a` e `b` com `float()` dentro de `try:` e capture `(ValueError, TypeError)`.",
            "Verifique `if den == 0: return None` antes de dividir (ou capture `ZeroDivisionError`).",
        ],
        explicacao=(
            "Capturar apenas as exceções esperadas (`ValueError`, `TypeError`, `ZeroDivisionError`) protege contra dados sujos sem mascarar bugs."
        ),
    )


@exercicio(estagio=16, dificuldade=2, tipo="funcao", conceitos=["excecoes", "listas", "funcoes"])
def media_resiliente(r):
    v1 = r.randint(10, 30)
    v2 = r.randint(20, 40)
    suja = [str(v1), "erro", None, v2, "", "  10 "]
    casos = [suja, ["x", None], [], [5, "5.0", 5]]
    return dict(
        titulo="Média ignorando registros corrompidos",
        enunciado=(
            "Escreva a função `media_limpa(valores)` que recebe uma lista com dados mistos (números, strings numéricas, "
            "textos inválidos e `None`) e retorna a média dos valores numéricos válidos arredondada em 2 casas.\n\n"
            "- Ignore valores `bool` (`True`/`False`), `None` e textos que não viram `float`.\n"
            "- Se não sobrar nenhum número válido, retorne `0.0`."
        ),
        solucao=(
            "def media_limpa(valores):\n"
            "    validos = []\n"
            "    for v in valores:\n"
            "        if isinstance(v, bool) or v is None:\n"
            "            continue\n"
            "        try:\n"
            "            validos.append(float(v))\n"
            "        except (ValueError, TypeError):\n"
            "            continue\n"
            "    if not validos:\n"
            "        return 0.0\n"
            "    return round(sum(validos) / len(validos), 2)\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(media_limpa({c!r}))"} for c in casos],
        testes_visiveis=1,
        dicas=[
            "Em Python `bool` é subclasse de `int` (`float(True) == 1.0`), então descarte `isinstance(v, bool)` antes!",
            "Tente converter cada item com `float(v)` em `try/except (ValueError, TypeError)` e trate lista vazia retornando `0.0`.",
        ],
        explicacao=(
            "Planilhas e APIs trazem valores nulos, espaços e textos misturados. Filtrar explicitamente `bool`/`None` e proteger contra lista vazia evita falhas em produção."
        ),
    )


@exercicio(estagio=16, dificuldade=2, tipo="completar", conceitos=["excecoes", "dicionarios", "funcoes"])
def completar_obter_inteiro_config(r):
    padrao = r.randint(3, 10)
    casos = [
        ({"tentativas": "5"}, "tentativas", padrao),
        ({"tentativas": "abc"}, "tentativas", padrao),
        ({}, "tentativas", padrao),
        ({"tentativas": None}, "tentativas", padrao),
    ]
    return dict(
        titulo="Ler configuração inteira com fallback",
        enunciado=(
            "Complete as lacunas `___` para ler uma chave inteira de um dicionário de configurações "
            "retornando `padrao` se a chave faltar ou não for conversível em inteiro."
        ),
        codigo_inicial=(
            "def ler_int(cfg, chave, padrao):\n"
            "    bruto = cfg.___(chave)\n"
            "    if bruto is ___:\n"
            "        return padrao\n"
            "    ___:\n"
            "        return int(bruto)\n"
            "    except (___, TypeError):\n"
            "        return padrao\n"
        ),
        solucao=(
            "def ler_int(cfg, chave, padrao):\n"
            "    bruto = cfg.get(chave)\n"
            "    if bruto is None:\n"
            "        return padrao\n"
            "    try:\n"
            "        return int(bruto)\n"
            "    except (ValueError, TypeError):\n"
            "        return padrao\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(ler_int({cfg!r}, {ch!r}, {p}))"} for cfg, ch, p in casos],
        testes_visiveis=2,
        dicas=[
            "Use `.get(chave)` e compare com `is None`.",
            "A exceção lançada por `int('abc')` é `ValueError`.",
        ],
        explicacao=(
            "Ler variáveis de ambiente ou configs de API com fallback seguro impede que uma configuração malformada derrube o serviço."
        ),
    )


@exercicio(estagio=16, dificuldade=3, tipo="prever", conceitos=["excecoes", "teste_de_mesa"])
def prever_try_except_else_finally(r):
    n = r.randint(2, 9)
    return dict(
        titulo="Teste de mesa: try, except, else e finally",
        enunciado="Acompanhe quais blocos executam em cada chamada e escreva exatamente a saída:",
        solucao=(
            "def testar(x):\n"
            "    try:\n"
            f"        res = {n * 10} // x\n"
            "    except ZeroDivisionError:\n"
            "        print('erro')\n"
            "    else:\n"
            "        print('ok', res)\n"
            "    finally:\n"
            "        print('fim')\n"
            "\n"
            f"testar({n})\n"
            "testar(0)\n"
        ),
        dicas=[
            "O bloco `else:` só executa quando **nenhuma** exceção aconteceu no `try:`.",
            "O bloco `finally:` executa **sempre**, dando certo ou dando erro.",
        ],
        explicacao=(
            f"Na primeira chamada (`x={n}`), roda `else` (`ok 10`) e `finally` (`fim`). Na segunda (`x=0`), roda `except` (`erro`) e `finally` (`fim`)."
        ),
    )


@exercicio(estagio=16, dificuldade=3, tipo="corrigir", conceitos=["excecoes", "depuracao", "funcoes"])
def corrigir_validar_idade_cadastro(r):
    min_id = r.choice([16, 18, 21])
    max_id = r.choice([100, 110, 120])
    casos = [str(min_id), str(min_id - 1), str(max_id + 10), "-5", "vinte", ""]
    return dict(
        titulo="Bug na validação defensiva de cadastro",
        enunciado=(
            f"A função `validar_idade(texto)` deve retornar `True` apenas quando `texto` representar um "
            f"inteiro entre `{min_id}` e `{max_id}` (inclusive), e `False` para qualquer outro valor (inclusive texto inválido).\n\n"
            f"O código atual quebra com `ValueError` em textos não numéricos e aceita idades acima de {max_id}. Corrija-o!"
        ),
        codigo_inicial=(
            "def validar_idade(texto):\n"
            "    idade = int(texto)\n"
            f"    return idade >= {min_id}\n"
        ),
        solucao=(
            "def validar_idade(texto):\n"
            "    try:\n"
            "        idade = int(texto)\n"
            "    except (ValueError, TypeError):\n"
            "        return False\n"
            f"    return {min_id} <= idade <= {max_id}\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(validar_idade({c!r}))"} for c in casos],
        testes_visiveis=2,
        dicas=[
            "Envolva `int(texto)` em `try/except (ValueError, TypeError)` retornando `False`.",
            f"Valide o limite superior também: `{min_id} <= idade <= {max_id}`.",
        ],
        explicacao=(
            "Validar tipo, faixa mínima e faixa máxima na entrada protege o resto do sistema contra dados fora de contrato."
        ),
    )


@exercicio(estagio=16, dificuldade=4, tipo="funcao", conceitos=["excecoes", "dicionarios", "funcoes"])
def validar_pedido_api(r):
    preco = r.randint(20, 100)
    casos = [
        {"produto": "Curso", "qtd": 2, "preco": preco},
        {"produto": "", "qtd": 2, "preco": preco},
        {"produto": "Curso", "qtd": 0, "preco": preco},
        {"produto": "Curso", "qtd": "3", "preco": -10},
        {"qtd": 1, "preco": 50},
    ]
    return dict(
        titulo="Validador de contrato de pedido",
        enunciado=(
            "Escreva `validar_pedido(p)` que recebe um dicionário e retorna uma **lista ordenada de erros** encontrados:\n"
            "- Se `'produto'` faltar ou for string vazia/só espaços: adicione `'produto_invalido'`\n"
            "- Se `'qtd'` não for inteiro positivo (`> 0`, descartando `bool`): adicione `'qtd_invalida'`\n"
            "- Se `'preco'` não for número `> 0` (`int`/`float`, descartando `bool`): adicione `'preco_invalido'`\n\n"
            "Se tudo estiver válido, retorne `[]`."
        ),
        solucao=(
            "def validar_pedido(p):\n"
            "    erros = []\n"
            "    if not isinstance(p, dict):\n"
            "        return ['pedido_invalido']\n"
            "    prod = p.get('produto')\n"
            "    if not isinstance(prod, str) or not prod.strip():\n"
            "        erros.append('produto_invalido')\n"
            "    qtd = p.get('qtd')\n"
            "    if isinstance(qtd, bool) or not isinstance(qtd, int) or qtd <= 0:\n"
            "        erros.append('qtd_invalida')\n"
            "    preco = p.get('preco')\n"
            "    if isinstance(preco, bool) or not isinstance(preco, (int, float)) or preco <= 0:\n"
            "        erros.append('preco_invalido')\n"
            "    return sorted(erros)\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(validar_pedido({c!r}))"} for c in casos],
        testes_visiveis=2,
        dicas=[
            "Use `p.get(...)` para nunca lançar `KeyError` se um campo vier ausente.",
            "Lembre que `isinstance(True, int)` é `True` em Python, então verifique `isinstance(x, bool)` antes!",
        ],
        explicacao=(
            "Validar contratos de entrada retornando todos os erros de uma vez é a base de APIs e agentes confiáveis."
        ),
    )


@exercicio(estagio=16, dificuldade=4, tipo="quebrar", conceitos=["excecoes", "depuracao"])
def quebrar_maior_numero_inicial_zero(r):
    a = -r.randint(2, 10)
    b = -r.randint(11, 25)
    return dict(
        titulo="Quebre o código: maior elemento da lista",
        enunciado=(
            "A função `maior_elemento(nums)` deveria retornar o maior número de qualquer lista não vazia de inteiros.\n\n"
            "**Seu desafio:** forneça uma lista não vazia de inteiros que faça o código abaixo retornar o resultado **errado**!"
        ),
        modo_quebrar="args",
        funcao_quebrar="maior_elemento",
        placeholder_quebrar="Ex.: [-5, -2, -9]",
        codigo_inicial=(
            "def maior_elemento(nums):\n"
            "    maior = 0\n"
            "    for x in nums:\n"
            "        if x > maior:\n"
            "            maior = x\n"
            "    return maior\n"
        ),
        solucao=(
            "def maior_elemento(nums):\n"
            "    maior = nums[0]\n"
            "    for x in nums[1:]:\n"
            "        if x > maior:\n"
            "            maior = x\n"
            "    return maior\n"
        ),
        testes=[{"entrada": f"[{a}, {b}]"}],
        testes_visiveis=0,
        dicas=[
            "Olhe para o valor inicial da variável: `maior = 0`.",
            "O que acontece se TODOS os números da lista forem menores que zero?",
        ],
        explicacao=(
            f"Inicializar `maior = 0` falha sempre que todos os itens são negativos (como `[{a}, {b}]`): "
            f"a função devolve `0` em vez de `{a}`. Sempre inicialize com `nums[0]`."
        ),
    )


@exercicio(estagio=16, dificuldade=5, tipo="quebrar", conceitos=["excecoes", "depuracao", "strings"])
def quebrar_normalizar_email(r):
    ex = r.choice(["'@.com'", "'a@b@c.com'", "'user @dom.com'", "'a.b@dom'"])
    return dict(
        titulo="Quebre o código: validador simplista de e-mail",
        enunciado=(
            "Um dev escreveu `email_valido(s)` para checar se `s` tem um formato básico `usuario@dominio.ext` "
            "(sem espaços, exatamente um `@`, texto antes do `@` e ponto no domínio após o `@`).\n\n"
            "**Seu desafio:** forneça uma string (entre aspas) que o código bugado aceite ou rejeite de forma **errada**!"
        ),
        modo_quebrar="args",
        funcao_quebrar="email_valido",
        placeholder_quebrar="Ex.: '@.com' ou 'a@b@c.com'",
        codigo_inicial=(
            "def email_valido(s):\n"
            "    return '@' in s and '.' in s\n"
        ),
        solucao=(
            "def email_valido(s):\n"
            "    if not isinstance(s, str) or ' ' in s or s.count('@') != 1:\n"
            "        return False\n"
            "    usuario, dominio = s.split('@')\n"
            "    if not usuario or '.' not in dominio:\n"
            "        return False\n"
            "    partes = dominio.split('.')\n"
            "    return all(len(p) > 0 for p in partes)\n"
        ),
        testes=[{"entrada": ex}],
        testes_visiveis=0,
        dicas=[
            "O código só checa se existe `@` e `.` em qualquer lugar da string.",
            "Tente uma string sem usuário antes do `@`, com espaço, com dois `@` ou com ponto antes do `@` (ex.: `'@.com'`).",
        ],
        explicacao=(
            "Testar apenas `'@' in s and '.' in s` aceita entradas inválidas como `'@.com'`, `'a.b@c'` ou `'a @b.com'`."
        ),
    )
