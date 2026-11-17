"""Estágio 10 - Strings a fundo: índices, fatias, busca e métodos (sem def)."""

from .base import exercicio

PALAVRAS = ["computador", "algoritmo", "programar", "teclado", "variavel", "logica", "escola"]


@exercicio(estagio=10, dificuldade=1, tipo="codigo", conceitos=["strings", "input", "fstring"])
def primeira_ultima_e_tamanho(r):
    casos = r.sample(PALAVRAS, 3) + ["py"]
    p0 = casos[0]
    return dict(
        titulo="Raio-X da palavra",
        enunciado=(
            "Leia uma palavra (`str`) e mostre:\n"
            "- O tamanho dela (`len()`)\n"
            "- A primeira letra (`[0]`)\n"
            "- A última letra (`[-1]`)\n\n"
            f"Exemplo para `\"{p0}\"`:\n```\nTamanho: {len(p0)}\nPrimeira: {p0[0]}\nÚltima: {p0[-1]}\n```"
        ),
        solucao=(
            'palavra = input("Palavra: ")\n'
            'print("Tamanho:", len(palavra))\n'
            'print("Primeira:", palavra[0])\n'
            'print("Última:", palavra[-1])\n'
        ),
        testes=[{"entrada": p} for p in casos],
        testes_visiveis=1,
        dicas=[
            "Em Python, índices começam em `0` e índices negativos contam do fim (`-1` é o último).",
            "Use `len(palavra)` para obter a quantidade de caracteres.",
        ],
        explicacao=(
            "O índice `-1` evita ter que escrever `palavra[len(palavra) - 1]`, tornando o código mais legível e seguro."
        ),
    )


@exercicio(estagio=10, dificuldade=1, tipo="prever", conceitos=["strings", "teste_de_mesa"])
def prever_fatias_string(r):
    p = r.choice(["PROGRAMA", "ALGORITMO", "PYTHON3", "CADERNO"])
    a = r.randint(1, 2)
    b = a + r.randint(3, 4)
    return dict(
        titulo="Fatiando pedaços do texto",
        enunciado=(
            "Lembre que na fatia `s[inicio:fim]` o índice `inicio` entra, mas o `fim` fica de fora. "
            "E `[::-1]` percorre de trás para frente!\n\nEscreva exatamente a saída:"
        ),
        solucao=(
            f's = "{p}"\n'
            f"print(s[{a}:{b}])\n"
            "print(s[:3])\n"
            "print(s[-2:])\n"
            "print(s[::-1])\n"
        ),
        dicas=[
            f"Conte os índices a partir do `0`: na palavra `\"{p}\"`, `s[0]` é `'{p[0]}'`, `s[1]` é `'{p[1]}'`...",
            "`s[:3]` pega os 3 primeiros caracteres (`0, 1, 2`), e `s[-2:]` pega do penúltimo até o fim.",
        ],
        explicacao=(
            f"Para `\"{p}\"`: `s[{a}:{b}]` dá `\"{p[a:b]}\"`, `s[:3]` dá `\"{p[:3]}\"`, `s[-2:]` dá `\"{p[-2:]}\"` "
            f"e `s[::-1]` inverte a palavra para `\"{p[::-1]}\"`."
        ),
    )


@exercicio(estagio=10, dificuldade=2, tipo="completar", conceitos=["strings", "input"])
def completar_limpar_e_padronizar(r):
    nomes = ["   ana   silva  ", "  BRUNO Costa ", "  pedro ALVES  ", " Carla   Dias ", "  lucas MOURA "]
    casos = r.sample(nomes, 3)
    c0 = casos[0]
    res0 = c0.strip().lower().replace(" ", "_")
    return dict(
        titulo="Gerando nome de usuário limpo",
        enunciado=(
            "Complete as lacunas `___` para ler um nome com espaços extras nas pontas, remover os espaços das pontas (`.strip()`), "
            "converter tudo para minúsculas (`.lower()`) e trocar espaços internos por `_` (`.replace()`):\n\n"
            f"Exemplo para `\"{c0}\"`:\n```\n{res0}\n```"
        ),
        codigo_inicial=(
            'nome = input("Nome: ")\n'
            "usuario = nome.___().___().replace(\" \", ___)\n"
            "print(usuario)\n"
        ),
        solucao=(
            'nome = input("Nome: ")\n'
            'usuario = nome.strip().lower().replace(" ", "_")\n'
            "print(usuario)\n"
        ),
        testes=[{"entrada": c} for c in casos],
        testes_visiveis=1,
        dicas=[
            "`.strip()` remove espaços do início e do fim; `.lower()` coloca em minúsculas.",
            "No `.replace(antigo, novo)`, troque `\" \"` por `\"_\"`.",
        ],
        explicacao=(
            "Podemos encadear métodos de string porque cada método devolve uma nova string pronta para o próximo método atuar."
        ),
    )


@exercicio(estagio=10, dificuldade=2, tipo="corrigir", conceitos=["strings", "depuracao"])
def corrigir_string_imutavel(r):
    itens = ["   Python   ", "  Dojo ", " logica ", "  Codigo  ", " Treino "]
    casos = r.sample(itens, 3)
    c0 = casos[0].strip().upper()
    return dict(
        titulo="Os métodos que não mudaram nada!",
        enunciado=(
            "O programa lê uma palavra, tenta remover espaços das pontas e deixá-la toda em MAIÚSCULAS:\n"
            f"Para `\"{casos[0]}\"`, deveria imprimir:\n```\n{c0}\n```\n"
            "Mas está imprimindo a palavra original sem alterações! Por quê? Corrija."
        ),
        codigo_inicial=(
            'texto = input("Texto: ")\n'
            "texto.strip()\n"
            "texto.upper()\n"
            "print(texto)\n"
        ),
        solucao=(
            'texto = input("Texto: ")\n'
            "texto = texto.strip()\n"
            "texto = texto.upper()\n"
            "print(texto)\n"
        ),
        testes=[{"entrada": c} for c in casos],
        testes_visiveis=1,
        dicas=[
            "Strings em Python são **imutáveis**: `texto.upper()` não altera `texto` por dentro!",
            "Guarde o resultado retornado de volta em `texto`: `texto = texto.strip()`.",
        ],
        explicacao=(
            "Esse é um erro clássico: métodos de string devolvem uma **nova string** modificada. Se você não atribuir "
            "a uma variável, o resultado é descartado na mesma hora."
        ),
    )


@exercicio(estagio=10, dificuldade=2, tipo="codigo", conceitos=["strings", "for_range", "contador"])
def contar_vogais_frase(r):
    casos = [
        r.choice(["Programar em Python", "Logica de Programacao", "Aprender todos os dias"]),
        "AEIOUaeiou",
        "xyz",
    ]
    f0 = casos[0]
    v0 = sum(1 for c in f0.lower() if c in "aeiou")
    return dict(
        titulo="Contador de vogais",
        enunciado=(
            "Leia uma frase (`str`) e conte quantas **vogais** (`a, e, i, o, u`, maiúsculas ou minúsculas, sem considerar acentos) ela possui.\n\n"
            f"Exemplo para `\"{f0}\"`:\n```\nVogais: {v0}\n```"
        ),
        solucao=(
            'frase = input("Frase: ")\n'
            "vogais = 0\n"
            "for letra in frase.lower():\n"
            '    if letra in "aeiou":\n'
            "        vogais += 1\n"
            'print("Vogais:", vogais)\n'
        ),
        testes=[{"entrada": c} for c in casos],
        testes_visiveis=1,
        dicas=[
            "Converta a frase para minúsculas com `.lower()` antes (ou dentro) do `for` para não precisar checar `AEIOU` separado.",
            "O operador `in` verifica se um caractere está dentro da string `\"aeiou\"`.",
        ],
        explicacao=(
            "Usar `letra in \"aeiou\"` sobre `frase.lower()` substitui 10 comparações (`== 'a' or == 'A'...`) por uma verificação limpa."
        ),
    )


@exercicio(estagio=10, dificuldade=3, tipo="codigo", conceitos=["strings", "if_else"])
def verificar_palindromo(r):
    palindromos = ["arara", "Radar", "osso", "Ana", "reviver"]
    nao_pal = ["python", "casa", "janela", "codigo"]
    casos = [r.choice(palindromos), r.choice(nao_pal), "Aba", "ovo"]
    p0 = casos[0]
    return dict(
        titulo="Detector de palíndromo",
        enunciado=(
            "Um **palíndromo** é uma palavra que se lê igual de trás para frente (ex.: `arara`, `Radar`), "
            "ignorando diferença entre maiúsculas e minúsculas.\n\n"
            "Leia uma palavra (sem espaços) e imprima `Palíndromo` ou `Não é palíndromo`.\n"
            f"Exemplo para `\"{p0}\"`:\n```\nPalíndromo\n```"
        ),
        solucao=(
            'palavra = input("Palavra: ").strip().lower()\n'
            "if palavra == palavra[::-1]:\n"
            '    print("Palíndromo")\n'
            "else:\n"
            '    print("Não é palíndromo")\n'
        ),
        testes=[{"entrada": c} for c in casos],
        testes_visiveis=2,
        dicas=[
            "Normalizar para `.lower()` garante que `Radar` seja igual a `radar`.",
            "Compare `palavra` com sua versão invertida `palavra[::-1]`.",
        ],
        explicacao=(
            "A fatia `[::-1]` cria a string invertida; comparando com a versão em minúsculas `.lower()`, detectamos qualquer palíndromo em uma linha."
        ),
    )


@exercicio(estagio=10, dificuldade=3, tipo="codigo", conceitos=["strings", "input"])
def extrair_usuario_e_dominio_email(r):
    casos = [
        f"{r.choice(['ana', 'lucas', 'bia', 'pedro'])}.{r.choice(['silva', 'lima'])}@{r.choice(['gmail.com', 'outlook.com', 'dojo.org'])}",
        "suporte@empresa.com.br",
        "dev@python.org",
    ]
    e0 = casos[0]
    u0, d0 = e0.split("@")
    return dict(
        titulo="Separando usuário e domínio do e-mail",
        enunciado=(
            "Leia um endereço de e-mail válido contendo exatamente um `@`.\n\n"
            "Separe e mostre o nome de **usuário** (antes do `@`) e o **domínio** (depois do `@`) usando `.find(\"@\")` e fatiamento (ou `.split(\"@\")`):\n"
            f"Exemplo para `\"{e0}\"`:\n```\nUsuário: {u0}\nDomínio: {d0}\n```"
        ),
        solucao=(
            'email = input("E-mail: ").strip()\n'
            'pos = email.find("@")\n'
            "usuario = email[:pos]\n"
            "dominio = email[pos + 1:]\n"
            'print("Usuário:", usuario)\n'
            'print("Domínio:", dominio)\n'
        ),
        testes=[{"entrada": c} for c in casos],
        testes_visiveis=1,
        dicas=[
            "`email.find(\"@\")` devolve o índice onde está o `@`.",
            "Tudo antes é `email[:pos]` e tudo depois é `email[pos + 1:]` (o `+ 1` pula o `@`).",
        ],
        explicacao=(
            "Localizar o índice separador com `.find()` e fatiar antes e depois dele funciona para qualquer tamanho de e-mail."
        ),
    )


@exercicio(estagio=10, dificuldade=3, tipo="prever", conceitos=["strings", "teste_de_mesa"])
def prever_metodos_count_find(r):
    frase = r.choice(["banana nanica", "casa da arvore", "arara azul"])
    alvo = "a"
    return dict(
        titulo="Caçando letras com count e find",
        enunciado=(
            "Lembre que `.find(sub)` devolve o índice da **primeira** ocorrência (ou `-1` se não achar).\n\n"
            "Escreva exatamente a saída do trecho:"
        ),
        solucao=(
            f's = "{frase}"\n'
            f'print(s.count("{alvo}"))\n'
            f'print(s.find("{alvo}"))\n'
            'print(s.find("z"))\n'
        ),
        dicas=[
            f"`count(\"{alvo}\")` conta quantos `'{alvo}'` há na string inteira.",
            "`find` devolve a posição do primeiro encontro, e `-1` quando não encontra o texto procurado.",
        ],
        explicacao=(
            f"Em `\"{frase}\"`, `'{alvo}'` aparece {frase.count(alvo)} vezes; a primeira posição é `{frase.find(alvo)}`; "
            f"e `'z'` {'não existe (-1)' if frase.find('z') == -1 else 'está no índice ' + str(frase.find('z'))}."
        ),
    )


@exercicio(estagio=10, dificuldade=3, tipo="corrigir", conceitos=["strings", "for_range", "depuracao"])
def corrigir_indice_fora_do_limite(r):
    casos = r.sample(PALAVRAS, 3)
    p0 = casos[0]
    ex0 = "\n".join(f"{i}: {p0[i]}" for i in range(len(p0)))
    return dict(
        titulo="IndexError na última letra!",
        enunciado=(
            "O programa deveria imprimir cada índice e sua respectiva letra:\n"
            f"Exemplo para `\"{p0}\"`:\n```\n{ex0}\n```\n"
            "Mas está dando `IndexError: string index out of range`! Descubra o motivo e corrija."
        ),
        codigo_inicial=(
            'palavra = input("Palavra: ")\n'
            "for i in range(len(palavra) + 1):\n"
            '    print(f"{i}: {palavra[i]}")\n'
        ),
        solucao=(
            'palavra = input("Palavra: ")\n'
            "for i in range(len(palavra)):\n"
            '    print(f"{i}: {palavra[i]}")\n'
        ),
        testes=[{"entrada": p} for p in casos],
        testes_visiveis=1,
        dicas=[
            "Se uma palavra tem `5` letras, quais são os índices válidos?",
            "Os índices vão de `0` até `len(palavra) - 1`, então `range(len(palavra))` já para no lugar certo — o `+ 1` passa do limite!",
        ],
        explicacao=(
            "Como a contagem começa no `0`, `range(len(palavra))` já gera exatamente todos os índices válidos (`0` até `len - 1`)."
        ),
    )


@exercicio(estagio=10, dificuldade=3, tipo="completar", conceitos=["strings", "for_range"])
def completar_contar_palavras_frase(r):
    frases = [
        "  aprender python todos os dias  ",
        "logica e pratica constante",
        "estudar algoritmos com calma",
        "  cada exercicio conta  ",
    ]
    casos = r.sample(frases, 3)
    f0 = casos[0]
    p0 = len(f0.split())
    return dict(
        titulo="Contando palavras com split()",
        enunciado=(
            "O método `.split()` separa uma frase pelos espaços em uma sequência de palavras (ignorando espaços extras nas pontas!).\n\n"
            "Complete as lacunas `___` para contar quantas palavras tem a frase e imprimir cada uma em maiúsculas:\n"
            f"Exemplo para `\"{f0}\"`:\n```\nTotal de palavras: {p0}\n" + "\n".join(w.upper() for w in f0.split()) + "\n```"
        ),
        codigo_inicial=(
            'frase = input("Frase: ")\n'
            "palavras = frase.___()\n"
            'print("Total de palavras:", ___(palavras))\n'
            "for p in palavras:\n"
            "    print(p.___())\n"
        ),
        solucao=(
            'frase = input("Frase: ")\n'
            "palavras = frase.split()\n"
            'print("Total de palavras:", len(palavras))\n'
            "for p in palavras:\n"
            "    print(p.upper())\n"
        ),
        testes=[{"entrada": c} for c in casos],
        testes_visiveis=1,
        dicas=[
            "`frase.split()` sem argumentos quebra em qualquer quantidade de espaços.",
            "Use `len(palavras)` para saber quantas palavras foram separadas e `p.upper()` dentro do `for`.",
        ],
        explicacao=(
            "`split()` é extremamente útil para lidar com frases porque elimina automaticamente espaços duplicados ou nas bordas."
        ),
    )


@exercicio(estagio=10, dificuldade=4, tipo="codigo", conceitos=["strings", "for_range", "if_else"])
def construir_iniciais_nome(r):
    nomes = [
        "Maria Clara Souza",
        "joao pedro lima",
        "Ana Beatriz Costa",
        "carlos eduardo silva",
        "rafaela macedo",
    ]
    casos = r.sample(nomes, 3)
    n0 = casos[0]
    ini0 = ".".join(p[0].upper() for p in n0.split()) + "."
    return dict(
        titulo="Gerador de iniciais",
        enunciado=(
            "Leia um nome completo (`str`). Pegue a primeira letra de cada palavra, transforme em maiúscula, "
            "e monte as iniciais separadas por ponto (terminando também com ponto).\n\n"
            f"Exemplo para `\"{n0}\"`:\n```\n{ini0}\n```"
        ),
        solucao=(
            'nome = input("Nome completo: ")\n'
            'resultado = ""\n'
            "for parte in nome.split():\n"
            '    resultado += parte[0].upper() + "."\n'
            "print(resultado)\n"
        ),
        testes=[{"entrada": c} for c in casos],
        testes_visiveis=1,
        dicas=[
            "Separe o nome em palavras com `nome.split()` e percorra cada `parte` com `for`.",
            "Comece `resultado = \"\"` e vá concatenando `parte[0].upper() + \".\"`.",
        ],
        explicacao=(
            "Usamos uma string vazia como acumulador de texto (`resultado += ...`), somando a primeira letra maiúscula "
            "de cada palavra seguida de ponto."
        ),
    )


@exercicio(estagio=10, dificuldade=4, tipo="codigo", conceitos=["strings", "for_range", "elif"])
def validar_forca_senha(r):
    fortes = ["Python12", "Segura99", "Dojo2026", "Chave77A"]
    fracas = ["python12", "Py12", "PYTHON12", "SenhaForte", "abc123"]
    casos = [r.choice(fortes), r.choice(fracas), r.choice(fracas), "Ab12cd34"]
    return dict(
        titulo="Validador de senha forte",
        enunciado=(
            "Leia uma senha (`str`) e verifique se ela é **Forte** atendendo a TODOS os critérios abaixo:\n"
            "- Pelo menos **8 caracteres** (`len(senha) >= 8`)\n"
            "- Pelo menos uma letra **maiúscula** (`c.isupper()`)\n"
            "- Pelo menos uma letra **minúscula** (`c.islower()`)\n"
            "- Pelo menos um **dígito** (`c.isdigit()`)\n\n"
            "Imprima `Forte` se cumprir tudo, ou `Fraca` caso falte algum critério."
        ),
        solucao=(
            'senha = input("Senha: ")\n'
            "tem_maiuscula = False\n"
            "tem_minuscula = False\n"
            "tem_digito = False\n"
            "for c in senha:\n"
            "    if c.isupper():\n"
            "        tem_maiuscula = True\n"
            "    elif c.islower():\n"
            "        tem_minuscula = True\n"
            "    elif c.isdigit():\n"
            "        tem_digito = True\n"
            "if len(senha) >= 8 and tem_maiuscula and tem_minuscula and tem_digito:\n"
            '    print("Forte")\n'
            "else:\n"
            '    print("Fraca")\n'
        ),
        testes=[{"entrada": s} for s in casos],
        testes_visiveis=2,
        dicas=[
            "Crie três variáveis booleanas (*bandeiras* / *flags*) começando em `False`: `tem_maiuscula`, `tem_minuscula`, `tem_digito`.",
            "Percorra `senha` caractere por caractere: se achar um tipo, ligue a flag correspondente para `True`.",
        ],
        explicacao=(
            "O padrão de *flags* booleanas é ideal aqui: cada característica começa desligada (`False`) e é ativada assim que um caractere "
            "daquele tipo aparece durante a varredura."
        ),
    )


@exercicio(estagio=10, dificuldade=4, tipo="corrigir", conceitos=["strings", "if_else", "depuracao"])
def corrigir_palindromo_espacos_maiusculas(r):
    frases_pal = [
        "A base do teto desaba",
        "Socorram me subi no onibus em Marrocos",
        "Anotaram a data da maratona",
        "A sacada da casa",
    ]
    casos = [r.choice(frases_pal), "A grama e amarga", "Ola mundo grande"]
    return dict(
        titulo="Palíndromo de frase inteira falhou!",
        enunciado=(
            "Queremos detectar palíndromos de **frases inteiras** (ex.: `\"A base do teto desaba\"`), "
            "ignorando **espaços** e **maiúsculas/minúsculas**.\n"
            "Mas o código atual não remove os espaços nem padroniza as letras, dando resultado errado! Corrija."
        ),
        codigo_inicial=(
            'frase = input("Frase: ")\n'
            "if frase == frase[::-1]:\n"
            '    print("Palíndromo")\n'
            "else:\n"
            '    print("Não é palíndromo")\n'
        ),
        solucao=(
            'frase = input("Frase: ")\n'
            'limpa = frase.replace(" ", "").lower()\n'
            "if limpa == limpa[::-1]:\n"
            '    print("Palíndromo")\n'
            "else:\n"
            '    print("Não é palíndromo")\n'
        ),
        testes=[{"entrada": c} for c in casos],
        testes_visiveis=1,
        dicas=[
            "`\"a base\"` ao contrário tem o espaço em posição diferente (`\"esab a\"`)!",
            "Use `.replace(\" \", \"\")` para remover todos os espaços e `.lower()` para igualar maiúsculas e minúsculas.",
        ],
        explicacao=(
            "Ao contrário de `.strip()` (que tira espaços só das pontas), `.replace(\" \", \"\")` apaga os espaços do meio também, "
            "permitindo comparar a frase limpa com seu inverso."
        ),
    )


@exercicio(estagio=10, dificuldade=5, tipo="codigo", conceitos=["strings", "for_range", "aritmeticos"])
def cifra_cesar_simples(r):
    desloc = r.randint(2, 5)
    casos = ["abc", "xyz", "python", "dojo"]
    p0 = casos[0]
    cif0 = "".join(chr((ord(c) - ord("a") + desloc) % 26 + ord("a")) for c in p0)
    return dict(
        titulo=f"Cifra de César (+{desloc} letras)",
        enunciado=(
            f"Leia uma palavra contendo **apenas letras minúsculas** (`a` a `z`, sem acentos). "
            f"Desloque cada letra **{desloc} posições à frente** no alfabeto (dando a volta após `z` -> `a`, usando `% 26`).\n\n"
            "Dica: `ord('a')` dá o código numérico de `'a'`, e `chr(codigo)` volta para letra.\n"
            f"Exemplo para `\"{p0}\"`:\n```\n{cif0}\n```"
        ),
        solucao=(
            'palavra = input("Palavra: ").strip()\n'
            'cifrada = ""\n'
            "for c in palavra:\n"
            '    pos = ord(c) - ord("a")\n'
            f"    nova_pos = (pos + {desloc}) % 26\n"
            '    cifrada += chr(nova_pos + ord("a"))\n'
            "print(cifrada)\n"
        ),
        testes=[{"entrada": c} for c in casos],
        testes_visiveis=2,
        dicas=[
            "Transforme a letra numa posição `0..25` fazendo `pos = ord(c) - ord('a')`.",
            f"Some `{desloc}` e tire `% 26` para dar a volta quando passar de `'z'`; depois some `ord('a')` e converta com `chr()`.",
        ],
        explicacao=(
            "A aritmética modular `% 26` faz o alfabeto virar um círculo: depois da posição 25 (`'z'`), o resto volta para 0 (`'a'`)."
        ),
    )


@exercicio(estagio=10, dificuldade=5, tipo="codigo", conceitos=["strings", "for_range", "if_else"])
def mascara_cpf_ou_cartao(r):
    n1 = "".join(str(r.randint(0, 9)) for _ in range(16))
    n2 = "".join(str(r.randint(0, 9)) for _ in range(12))
    casos = [
        n1,
        n2,
        str(r.randint(1000, 9999)),
        str(r.randint(10, 99)),
    ]
    c0 = casos[0]
    m0 = "*" * max(0, len(c0) - 4) + c0[-4:]
    return dict(
        titulo="Mascarando cartão de crédito",
        enunciado=(
            "Por segurança, sites ocultam os primeiros dígitos do cartão com `*` e mostram apenas os **4 últimos**.\n\n"
            "Leia uma string numérica `cartao` (de qualquer tamanho; se tiver 4 dígitos ou menos, mostre ela inteira sem `*`) "
            "e imprima a versão mascarada:\n"
            f"Exemplo para `\"{c0}\"`:\n```\n{m0}\n```"
        ),
        solucao=(
            'cartao = input("Número: ").strip()\n'
            "if len(cartao) <= 4:\n"
            "    print(cartao)\n"
            "else:\n"
            '    ocultos = "*" * (len(cartao) - 4)\n'
            "    print(ocultos + cartao[-4:])\n"
        ),
        testes=[{"entrada": c} for c in casos],
        testes_visiveis=2,
        dicas=[
            "Se `len(cartao) <= 4`, não precisa ocultar nada.",
            "Para tamanhos maiores, precisamos de `len(cartao) - 4` asteriscos colados aos 4 últimos dígitos (`cartao[-4:]`).",
        ],
        explicacao=(
            "Fatiamento negativo `cartao[-4:]` pega os 4 caracteres finais independentemente do tamanho da string, "
            "e `\"*\" * (len(cartao) - 4)` cria exatamente o restante em asteriscos."
        ),
    )
