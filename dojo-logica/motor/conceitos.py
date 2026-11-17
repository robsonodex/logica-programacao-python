"""Mini-lições didáticas para os 22 conceitos fundamentais de Python e lógica."""

CONCEITOS = {
    "variaveis": {
        "nome": "Variáveis",
        "resumo": "Caixinhas com nome na memória usadas para guardar e reaproveitar valores no programa.",
        "explicacao": (
            "Imagine uma estante com várias caixinhas etiquetadas. Em Python, uma **variável** funciona "
            "exatamente assim: você escolhe um nome (a etiqueta) e guarda um valor dentro dela usando o sinal `=`.\n\n"
            "Em programação, o sinal `=` **não significa igualdade matemática**, mas sim **atribuição** (\"recebe\"). "
            "Quando escrevemos `idade = 20`, estamos dizendo ao Python: \"crie a variável `idade` e guarde `20` nela\".\n\n"
            "Cada variável guarda apenas **um valor por vez**. Se você atribuir um novo valor ao mesmo nome, "
            "o valor antigo é substituído pelo novo. Além disso, o Python diferencia letras maiúsculas de minúsculas: "
            "`nome` e `Nome` são variáveis completamente diferentes.\n\n"
            "Dicas para bons nomes de variáveis:\n"
            "- Use nomes claros que expliquem o que está guardado (ex.: `preco_produto`, `pontos`).\n"
            "- Comece com letra ou `_`, sem espaços e sem acentos (use `snake_case`, separando palavras por `_`).\n"
            "- Não comece com número e não use palavras reservadas do Python (`if`, `for`, `print`)."
        ),
        "exemplo": (
            "# Guardando valores em variáveis\n"
            'nome = "Lucas"\n'
            "pontos = 10\n"
            "bonus = 5\n"
            "\n"
            "# Lendo e atualizando valores\n"
            "total = pontos + bonus\n"
            "pontos = total  # substitui o valor antigo de pontos\n"
            "\n"
            'print("Jogador:", nome)\n'
            'print("Pontuação final:", pontos)\n'
        ),
        "erros_comuns": [
            "Escrever `10 = x` em vez de `x = 10`. Quem recebe o valor fica sempre à esquerda do `=`.",
            "Trocar maiúsculas por minúsculas (criar `idade` e tentar ler `Idade`), gerando `NameError`.",
            "Esquecer as aspas ao guardar um texto (`cidade = Recife`), fazendo o Python achar que `Recife` é uma variável.",
        ],
        "dica_de_ouro": "Leia o símbolo `=` como \"recebe\": `x = x + 1` significa \"o novo x recebe o valor antigo de x mais 1\".",
    },
    "print": {
        "nome": "Saída com print()",
        "resumo": "Exibe mensagens, números e valores de variáveis na tela do programa.",
        "explicacao": (
            "Um programa precisa conversar com quem o usa. A função `print()` é o megafone do Python: "
            "tudo o que você colocar dentro dos parênteses aparece na saída.\n\n"
            "Você pode passar vários itens separados por vírgula, como `print(\"Total:\", valor)`. Por padrão, "
            "o `print()` coloca **um espaço** entre cada item e **pula uma linha** ao terminar.\n\n"
            "Também é possível personalizar esse comportamento:\n"
            "- `sep=\"-\"` muda o separador entre os itens (em vez de espaço).\n"
            "- `end=\" \"` muda o que vai no final da linha (evitando pular linha).\n"
            "- `print()` vazio apenas pula uma linha em branco."
        ),
        "exemplo": (
            'produto = "Caderno"\n'
            "preco = 18\n"
            "\n"
            'print("Item:", produto, "| Valor:", preco)\n'
            'print("10", "05", "2026", sep="/")\n'
            'print("Carregando", end="...")\n'
            'print(" pronto!")\n'
        ),
        "erros_comuns": [
            "Colocar aspas em volta do nome da variável (`print(\"idade\")` imprime a palavra idade, não o número guardado).",
            "Esquecer a vírgula entre dois valores dentro do `print()`, causando `SyntaxError`.",
            "Escrever `Print()` com P maiúsculo — em Python o comando é sempre `print` todo em minúsculas.",
        ],
        "dica_de_ouro": "Se quiser ver o conteúdo de uma variável, escreva o nome dela dentro do `print()` **sem aspas**.",
    },
    "tipos": {
        "nome": "Tipos de dados",
        "resumo": "Classificam a natureza de cada valor (inteiro, decimal, texto ou booleano) para o Python saber o que pode fazer com ele.",
        "explicacao": (
            "Nem todo dado é tratado do mesmo jeito: você consegue multiplicar números, mas não faz sentido "
            "dividir dois nomes de pessoas. Por isso, todo valor em Python tem um **tipo**.\n\n"
            "Os quatro tipos fundamentais que você usará o tempo todo são:\n"
            "- `int` (inteiro): números sem vírgula, positivos, negativos ou zero (ex.: `7`, `-3`, `0`).\n"
            "- `float` (ponto flutuante): números com casas decimais, usando **ponto** em vez de vírgula (ex.: `3.14`, `2.0`).\n"
            "- `str` (string / texto): qualquer sequência de caracteres entre aspas simples ou duplas (ex.: `\"Olá\"`, `'42'`).\n"
            "- `bool` (booleano): representa verdadeiro ou falso, usando exatamente `True` ou `False` (com inicial maiúscula).\n\n"
            "Você pode descobrir o tipo de qualquer valor ou variável usando a função `type(valor)`. "
            "Repare que `42` (número) e `\"42\"` (texto) têm tipos diferentes e comportamentos diferentes!"
        ),
        "exemplo": (
            "idade = 25\n"
            "altura = 1.74\n"
            'apelido = "Bia"\n'
            "ativo = True\n"
            "\n"
            "print(idade, type(idade))\n"
            "print(altura, type(altura))\n"
            "print(apelido, type(apelido))\n"
            "print(ativo, type(ativo))\n"
        ),
        "erros_comuns": [
            "Usar vírgula em números decimais (`1,75` em vez de `1.75`). Em Python, vírgula separa itens!",
            "Escrever `true` ou `false` em minúsculas; o correto é sempre `True` e `False`.",
            "Achar que `\"10\"` é igual a `10` para fazer contas (`\"10\" + 5` gera `TypeError`).",
        ],
        "dica_de_ouro": "Aspas transformam qualquer coisa em texto (`str`), e o ponto (`.`) é o separador decimal oficial do Python.",
    },
    "conversao": {
        "nome": "Conversão de tipos",
        "resumo": "Transforma um valor de um tipo em outro usando int(), float(), str() e bool().",
        "explicacao": (
            "Muitas vezes o dado chega num tipo e precisamos dele em outro — por exemplo, um número guardado "
            "como texto (`\"15\"`) que precisa entrar numa conta matemática.\n\n"
            "O Python oferece funções simples para fazer essa conversão (também chamada de *casting*):\n"
            "- `int(x)`: converte para inteiro. Em texto, aceita dígitos como `\"42\"`. Em `float`, **corta** a parte decimal (`int(3.9)` vira `3`).\n"
            "- `float(x)`: converte para número decimal (`float(\"7.5\")` vira `7.5`; `float(4)` vira `4.0`).\n"
            "- `str(x)`: transforma qualquer valor em texto (`str(100)` vira `\"100\"`).\n"
            "- `bool(x)`: converte para lógico (`0`, `0.0` e `\"\"` viram `False`; quase todo o resto vira `True`).\n\n"
            "Quando precisar arredondar um decimal em vez de cortar as casas, use `round(valor, casas)`."
        ),
        "exemplo": (
            'texto_num = "12"\n'
            'texto_preco = "4.50"\n'
            "\n"
            "quantidade = int(texto_num)\n"
            "preco = float(texto_preco)\n"
            "total = quantidade * preco\n"
            "\n"
            'etiqueta = "R$ " + str(total)\n'
            "print(etiqueta)\n"
            "print(\"Arredondado:\", round(3.678, 2))\n"
        ),
        "erros_comuns": [
            "Passar um texto decimal direto para `int(\"3.5\")` — dá `ValueError`. Converta para `float()` primeiro se necessário.",
            "Esquecer de guardar o resultado da conversão: escrever apenas `int(x)` sem `x = int(x)` não muda `x`.",
            "Tentar converter letras como `int(\"abc\")`, o que gera `ValueError`.",
        ],
        "dica_de_ouro": "Sempre pergunte: \"esse dado vai virar conta ou vai só aparecer na tela?\" — para conta, converta para `int` ou `float`.",
    },
    "input": {
        "nome": "Entrada com input()",
        "resumo": "Pausa o programa para ler o que o usuário digitar e guarda como texto (str).",
        "explicacao": (
            "Sem entrada de dados, um programa faria sempre a mesma coisa toda vez que rodasse. "
            "A função `input()` permite receber dados digitados pelo usuário.\n\n"
            "Você pode colocar uma mensagem orientando o que digitar: `nome = input(\"Seu nome: \")`. "
            "O programa espera o usuário digitar e pressionar Enter, e guarda o texto digitado na variável.\n\n"
            "**Regra de ouro do `input()`**: ele **sempre devolve um texto (`str`)**, mesmo que o usuário digite `10` ou `3.5`. "
            "Por isso, sempre que você for fazer cálculos numéricos, combine `input()` com `int()` ou `float()`:\n"
            "- `idade = int(input(\"Idade: \"))`\n"
            "- `nota = float(input(\"Nota: \"))`"
        ),
        "exemplo": (
            "# Exemplo simulando o padrão de leitura e conversão\n"
            'entrada_nome = "Marina"  # imagine que veio de input("Nome: ")\n'
            'entrada_idade = "19"     # imagine que veio de input("Idade: ")\n'
            "\n"
            "idade = int(entrada_idade)\n"
            "ano_que_vem = idade + 1\n"
            'print(f"{entrada_nome} fará {ano_que_vem} anos.")\n'
        ),
        "erros_comuns": [
            "Fazer `idade = input(\"Idade: \")` e depois tentar `idade + 1` (erro `TypeError`, pois `input()` devolve texto).",
            "Chamar `input()` numa ordem diferente da descrita no enunciado dos exercícios.",
            "Usar `int(input())` quando o usuário pode digitar valores com casas decimais como `7.5`.",
        ],
        "dica_de_ouro": "`input()` sempre entrega `str`; se for número para fazer conta, envolva logo com `int(input())` ou `float(input())`.",
    },
    "aritmeticos": {
        "nome": "Operadores aritméticos",
        "resumo": "Símbolos para somar, subtrair, multiplicar, dividir, pegar divisão inteira, resto e potência.",
        "explicacao": (
            "O Python é uma calculadora poderosa. Além das quatro operações básicas, ele traz três operadores "
            "muito úteis em lógica de programação:\n\n"
            "- `+` soma e `-` subtração\n"
            "- `*` multiplicação\n"
            "- `/` divisão comum (sempre retorna `float`, ex.: `10 / 2` dá `5.0`)\n"
            "- `//` **divisão inteira**: devolve apenas a parte inteira do quociente (`7 // 2` dá `3`)\n"
            "- `%` **módulo (resto da divisão)**: devolve o que sobra da divisão inteira (`7 % 2` dá `1`)\n"
            "- `**` **potência**: eleva um número ao outro (`2 ** 3` dá `8`)\n\n"
            "Os operadores `//` e `%` aparecem o tempo todo: para saber se um número é par (`n % 2 == 0`), "
            "para pegar o último dígito (`n % 10`) ou para converter minutos em horas e minutos restantes."
        ),
        "exemplo": (
            "total_minutos = 135\n"
            "horas = total_minutos // 60\n"
            "minutos_restantes = total_minutos % 60\n"
            "\n"
            'print(f"{total_minutos} min = {horas}h e {minutos_restantes}min")\n'
            'print("2 elevado a 5:", 2 ** 5)\n'
            'print("Divisão normal 7 / 2:", 7 / 2)\n'
        ),
        "erros_comuns": [
            "Usar `^` achando que é potência (em Python potência é `**`).",
            "Confundir `/` (divisão com decimal) com `//` (só a parte inteira) e `%` (só o resto).",
            "Dividir por zero (`/`, `//` ou `%` com `0`), o que causa `ZeroDivisionError`.",
        ],
        "dica_de_ouro": "Pense em `//` e `%` como irmãos: `17 // 5` diz quantas caixas completas de 5 cabem em 17 (`3`), e `17 % 5` diz quantos itens sobram fora da caixa (`2`).",
    },
    "precedencia": {
        "nome": "Precedência e parênteses",
        "resumo": "Define a ordem em que as operações de uma expressão são calculadas.",
        "explicacao": (
            "Assim como na matemática, o Python não calcula uma expressão simplesmente da esquerda para a direita. "
            "Existe uma fila de prioridade chamada **precedência**.\n\n"
            "A ordem padrão, da maior prioridade para a menor, é:\n"
            "1. Parênteses `( )` — tudo o que está dentro é resolvido primeiro.\n"
            "2. Potência `**`.\n"
            "3. Multiplicação `*`, divisões `/` e `//`, resto `%` (da esquerda para a direita).\n"
            "4. Soma `+` e subtração `-` (da esquerda para a direita).\n\n"
            "Quando quiser garantir que uma soma aconteça antes de uma divisão (como numa média), **use parênteses**! "
            "Eles deixam sua intenção cristalina tanto para o Python quanto para quem lê o código."
        ),
        "exemplo": (
            "n1 = 8.0\n"
            "n2 = 6.0\n"
            "\n"
            "errado = n1 + n2 / 2       # divide n2 por 2 antes de somar!\n"
            "certo = (n1 + n2) / 2      # soma primeiro, depois divide\n"
            "\n"
            'print("Sem parênteses:", errado)\n'
            'print("Com parênteses:", certo)\n'
        ),
        "erros_comuns": [
            "Calcular média escrevendo `a + b + c / 3` sem parênteses — apenas `c` é dividido por 3.",
            "Escrever potências como `-3 ** 2` esperando `9`: o Python faz `-(3 ** 2) = -9`; use `(-3) ** 2`.",
            "Deixar expressões longas e difíceis de ler sem quebrar em variáveis intermediárias.",
        ],
        "dica_de_ouro": "Na dúvida sobre quem executa primeiro, coloque parênteses: eles nunca atrapalham e evitam bugs silenciosos.",
    },
    "comparacao": {
        "nome": "Operadores de comparação",
        "resumo": "Comparam dois valores e sempre devolvem True ou False.",
        "explicacao": (
            "Para tomar decisões, um programa precisa fazer perguntas cujas respostas sejam sim (`True`) ou não (`False`). "
            "Os operadores de comparação fazem exatamente essas perguntas:\n\n"
            "- `==` igual a (cuidado: são **dois** sinais de igual!)\n"
            "- `!=` diferente de\n"
            "- `>` maior que / `<` menor que\n"
            "- `>=` maior ou igual a / `<=` menor ou igual a\n\n"
            "Uma expressão como `nota >= 7` já tem um valor próprio (`True` ou `False`), que pode ser impresso "
            "ou guardado numa variável booleana antes mesmo de usarmos `if`."
        ),
        "exemplo": (
            "nota = 7.0\n"
            "idade = 16\n"
            "\n"
            "aprovado = nota >= 7.0\n"
            "maior_de_idade = idade >= 18\n"
            "numero_par = (10 % 2) == 0\n"
            "\n"
            'print("Aprovado?", aprovado)\n'
            'print("Maior de idade?", maior_de_idade)\n'
            'print("10 é par?", numero_par)\n'
        ),
        "erros_comuns": [
            "Usar `=` (atribuição) em vez de `==` (comparação).",
            "Confundir `>` com `>=` em limites exatos (\"a partir de 18 anos\" inclui o 18, então é `>= 18`).",
            "Escrever `=<` ou `=>` invertidos — o símbolo de igual vem sempre depois (`<=`, `>=`).",
        ],
        "dica_de_ouro": "Um `=` guarda na caixa; dois `==` espiam a caixa para perguntar se é igual.",
    },
    "logicos": {
        "nome": "Operadores lógicos (and, or, not)",
        "resumo": "Combinam ou invertem condições booleanas para formar regras mais completas.",
        "explicacao": (
            "Muitas regras do mundo real dependem de mais de uma condição ao mesmo tempo. "
            "Os operadores lógicos juntam comparações:\n\n"
            "- `and` (**E**): só é `True` se **todas** as condições forem verdadeiras.\n"
            "- `or` (**OU**): é `True` se **pelo menos uma** condição for verdadeira.\n"
            "- `not` (**NÃO**): inverte o resultado (`not True` vira `False`, `not False` vira `True`).\n\n"
            "Atenção especial ao `or`: em português dizemos \"x é igual a 1 ou 2\", mas em Python é obrigatório "
            "repetir a comparação dos dois lados: `x == 1 or x == 2`."
        ),
        "exemplo": (
            "idade = 20\n"
            "tem_convite = True\n"
            "vip = False\n"
            "\n"
            "pode_entrar = (idade >= 18) and (tem_convite or vip)\n"
            "bloqueado = not pode_entrar\n"
            "\n"
            'print("Pode entrar?", pode_entrar)\n'
            'print("Bloqueado?", bloqueado)\n'
        ),
        "erros_comuns": [
            "Escrever `opcao == \"s\" or \"S\"` achando que compara `opcao` com os dois. Texto não vazio é sempre `True`! O certo é `opcao == \"s\" or opcao == \"S\"`.",
            "Trocar `and` por `or` ao descrever faixas (ex.: \"fora do intervalo 0..10\" usa `or`: `x < 0 or x > 10`; \"dentro\" usa `and`: `x >= 0 and x <= 10`).",
            "Esquecer a ordem de avaliação: `not` executa antes de `and`, que executa antes de `or`. Use parênteses para deixar claro.",
        ],
        "dica_de_ouro": "Sempre escreva comparações completas dos dois lados de `and` e `or` (`a > 0 and a < 10`).",
    },
    "if_else": {
        "nome": "Decisões com if e else",
        "resumo": "Fazem o programa escolher um caminho quando a condição é verdadeira e outro quando é falsa.",
        "explicacao": (
            "Até aqui, todas as linhas rodavam de cima para baixo sem desvio. Com `if` (\"se\") e `else` (\"senão\"), "
            "o código passa a tomar decisões.\n\n"
            "Funcionamento:\n"
            "- O Python testa a condição depois do `if`.\n"
            "- Se ela for `True`, executa o bloco recuado logo abaixo do `if` e **pula** o `else`.\n"
            "- Se ela for `False`, pula o `if` e executa o bloco do `else`.\n\n"
            "Note duas coisas obrigatórias da sintaxe:\n"
            "1. Os **dois-pontos `:`** no fim da linha do `if` e do `else:`.\n"
            "2. A **indentação** (4 espaços à direita) indicando quais linhas pertencem a cada caminho. O `else` é opcional quando você não precisa fazer nada no caso falso."
        ),
        "exemplo": (
            "nota = 6.5\n"
            "\n"
            "if nota >= 7.0:\n"
            '    print("Aprovado!")\n'
            '    print("Parabéns pelo esforço.")\n'
            "else:\n"
            '    print("Precisa de recuperação.")\n'
            "\n"
            'print("Fim da análise.")  # fora do if/else: roda sempre\n'
        ),
        "erros_comuns": [
            "Esquecer os dois-pontos `:` após a condição do `if` ou após `else`.",
            "Errar o recuo (indentação) das linhas dentro do bloco, causando `IndentationError` ou executando linhas fora do `if` sem querer.",
            "Colocar uma condição na linha do `else` (ex.: `else nota < 7:`) — `else` não leva condição.",
        ],
        "dica_de_ouro": "Apenas as linhas recuadas (indentadas) pertencem ao `if` ou ao `else`; quando o recuo volta para a margem, o programa continua normal.",
    },
    "elif": {
        "nome": "Múltiplos caminhos com elif",
        "resumo": "Encadeia várias condições exclusivas em sequência (se / senão se / senão).",
        "explicacao": (
            "Quando existem 3 ou mais cenários possíveis — como classificar faixas de idade, notas em conceitos A/B/C/D "
            "ou menus de opções — usamos `elif` (abreviação de *else if*, \"senão se\").\n\n"
            "Em uma cadeia `if / elif / elif / else`, o Python testa de cima para baixo e **para no primeiro bloco verdadeiro**, "
            "ignorando todos os outros abaixo dele.\n\n"
            "Por causa disso, **a ordem das condições importa muito**! Ao testar faixas numéricas, vá sempre do extremo "
            "para o outro lado em ordem crescente ou decrescente. Como o `elif` só é testado se os anteriores falharam, "
            "você não precisa repetir o limite que já foi descartado acima."
        ),
        "exemplo": (
            "temperatura = 27\n"
            "\n"
            "if temperatura < 15:\n"
            '    print("Frio")\n'
            "elif temperatura <= 25:\n"
            '    print("Agradável")\n'
            "elif temperatura <= 32:\n"
            '    print("Quente")\n'
            "else:\n"
            '    print("Muito quente!")\n'
        ),
        "erros_comuns": [
            "Colocar uma faixa mais abrangente antes de uma mais específica (ex.: testar `nota >= 5` antes de `nota >= 9` faz quem tirou 10 cair no primeiro bloco!).",
            "Usar vários `if` soltos em vez de `elif` quando os casos deveriam ser excludentes.",
            "Escrever `else if` separado (em Python a palavra é junta: `elif`).",
        ],
        "dica_de_ouro": "Numa cadeia `if/elif/else`, exatamente **um** bloco será executado se houver `else` no final — e a ordem dos testes funciona como peneira.",
    },
    "while": {
        "nome": "Repetição com while",
        "resumo": "Repete um bloco de código enquanto uma condição continuar verdadeira.",
        "explicacao": (
            "O `while` (\"enquanto\") funciona como um `if` que, ao terminar seu bloco, volta para o topo e "
            "testa a condição novamente.\n\n"
            "Ele é ideal quando **não sabemos de antemão** quantas vezes vamos repetir: por exemplo, ler números "
            "até o usuário digitar `0` (valor **sentinela**), ou dividir um número até ele chegar a `1`.\n\n"
            "Para que o laço não rode para sempre (o temido **loop infinito**), três peças precisam estar certas:\n"
            "1. **Inicialização**: dar o valor inicial da variável antes do `while`.\n"
            "2. **Condição**: a pergunta que mantém o laço vivo enquanto for `True`.\n"
            "3. **Atualização**: mudar a variável dentro do `while` para que um dia a condição vire `False`."
        ),
        "exemplo": (
            "contagem = 5\n"
            "\n"
            "while contagem >= 1:\n"
            "    print(contagem)\n"
            "    contagem = contagem - 1  # atualização! Sem isso, loop infinito\n"
            "\n"
            'print("Lançar!")\n'
        ),
        "erros_comuns": [
            "Esquecer de atualizar a variável dentro do `while`, travando o programa em loop infinito.",
            "Inicializar a variável de forma que a condição já comece falsa e o `while` nunca execute nenhuma vez.",
            "Usar `while` lendo com sentinela e acabar somando ou contando o próprio valor de parada (`0`) junto.",
        ],
        "dica_de_ouro": "Antes de rodar um `while`, aponte com o dedo a linha dentro dele que faz a condição chegar ao fim.",
    },
    "contador": {
        "nome": "Contadores",
        "resumo": "Variável que registra quantas vezes um evento aconteceu, normalmente crescendo de 1 em 1.",
        "explicacao": (
            "Um **contador** é um padrão clássico dentro de laços: uma variável que começa em zero (ou no início "
            "da contagem) e aumenta de 1 em 1 cada vez que algo acontece.\n\n"
            "Podemos usá-lo de dois jeitos principais:\n"
            "- **Para controlar o laço**: contar de `1` até `N` num `while`.\n"
            "- **Para contar ocorrências**: usar um `if` dentro do laço e fazer `qtd = qtd + 1` (ou `qtd += 1`) "
            "apenas quando uma condição for satisfeita (ex.: contar quantos números foram pares).\n\n"
            "Lembre-se sempre de inicializar o contador com `0` **antes** do laço começar, nunca dentro dele!"
        ),
        "exemplo": (
            "numero = 1\n"
            "qtd_pares = 0  # começa zerado fora do laço\n"
            "\n"
            "while numero <= 10:\n"
            "    if numero % 2 == 0:\n"
            "        qtd_pares += 1\n"
            "    numero += 1\n"
            "\n"
            'print("Pares de 1 a 10:", qtd_pares)\n'
        ),
        "erros_comuns": [
            "Zerar o contador dentro do laço (`qtd = 0` dentro do `while` ou `for`), perdendo a contagem anterior.",
            "Esquecer de criar a variável antes (`NameError` ou `UnboundLocalError`).",
            "Errar o limite por 1 (`< 10` em vez de `<= 10`), o famoso erro *off-by-one*.",
        ],
        "dica_de_ouro": "Contador sempre começa antes do laço (`cont = 0`) e cresce de 1 em 1 (`cont += 1`) no momento certo.",
    },
    "acumulador": {
        "nome": "Acumuladores",
        "resumo": "Variável que vai somando (ou multiplicando) vários valores ao longo de uma repetição.",
        "explicacao": (
            "Enquanto o contador soma sempre `1` para saber *quantos* itens apareceram, o **acumulador** soma "
            "*o valor* de cada item para obter um total.\n\n"
            "O mecanismo é simples:\n"
            "- Para somar valores: comece com `soma = 0` antes do laço e faça `soma += valor` a cada volta.\n"
            "- Para multiplicar valores (como em um fatorial): o elemento neutro da multiplicação é `1`, "
            "então comece com `produto = 1` e faça `produto *= valor`.\n\n"
            "Combinar um acumulador (`soma`) com um contador (`qtd`) permite calcular a média de quantos valores forem digitados."
        ),
        "exemplo": (
            "soma = 0\n"
            "fatorial = 1\n"
            "\n"
            "for n in range(1, 6):\n"
            "    soma += n\n"
            "    fatorial *= n\n"
            "\n"
            'print("Soma de 1 a 5:", soma)\n'
            'print("Fatorial de 5:", fatorial)\n'
        ),
        "erros_comuns": [
            "Inicializar um acumulador de multiplicação com `0` (tudo multiplicado por 0 continua 0!).",
            "Escrever `soma = valor` em vez de `soma = soma + valor` (ou `soma += valor`), substituindo o total em vez de somar.",
            "Calcular a média dentro do laço antes de terminar todas as somas.",
        ],
        "dica_de_ouro": "Soma começa em `0`; produto começa em `1`; e ambos sempre usam `+=` ou `*=` para não perder o que já foi acumulado.",
    },
    "for_range": {
        "nome": "Repetição com for e range()",
        "resumo": "Percorre sequências ou repete um bloco um número exato de vezes usando range().",
        "explicacao": (
            "Quando você já sabe quantas repetições quer fazer — ou quer visitar cada item de uma string ou lista — "
            "o `for` é mais curto e seguro que o `while`, pois ele mesmo cuida da variável de controle.\n\n"
            "A função `range()` gera sequências numéricas sob medida:\n"
            "- `range(5)`: gera `0, 1, 2, 3, 4` (5 números, começando do 0 e **parando antes** do 5).\n"
            "- `range(1, 6)`: gera `1, 2, 3, 4, 5` (começa no 1 e para antes do 6).\n"
            "- `range(0, 10, 2)`: gera `0, 2, 4, 6, 8` (pulando de 2 em 2).\n"
            "- `range(5, 0, -1)`: gera `5, 4, 3, 2, 1` (passo negativo para contagem regressiva).\n\n"
            "Você também pode usar `for letra in texto:` para percorrer um texto caractere por caractere."
        ),
        "exemplo": (
            "numero = 4\n"
            'print(f"Tabuada do {numero}:")\n'
            "for i in range(1, 6):\n"
            '    print(f"{numero} x {i} = {numero * i}")\n'
            "\n"
            'print("Contagem regressiva:")\n'
            "for c in range(3, 0, -1):\n"
            "    print(c)\n"
        ),
        "erros_comuns": [
            "Esquecer que o fim do `range(inicio, fim)` **não é incluído**: para ir até `N`, use `range(1, N + 1)`.",
            "Tentar contagem regressiva com `range(10, 0)` sem colocar o passo `-1` no terceiro argumento.",
            "Alterar a variável do `for` dentro do bloco esperando pular voltas (na próxima volta o `for` assume o próximo item do `range`).",
        ],
        "dica_de_ouro": "Em `range(inicio, fim, passo)`, o `inicio` entra na sequência, mas o `fim` fica de fora (`fim - 1` é o último).",
    },
    "strings": {
        "nome": "Strings (textos)",
        "resumo": "Sequências de caracteres que podem ser acessadas por índice, fatiadas, medidas e transformadas com métodos.",
        "explicacao": (
            "Uma string (`str`) funciona como uma fila numerada de letras. O primeiro caractere está na posição "
            "(**índice**) `0`, o segundo no `1` e assim por diante. Índices negativos contam de trás para frente: "
            "`texto[-1]` é a última letra!\n\n"
            "Recursos essenciais de strings:\n"
            "- `len(texto)`: informa quantos caracteres existem (incluindo espaços).\n"
            "- **Fatiamento** `texto[inicio:fim]`: pega um pedaço (do índice `inicio` até `fim - 1`). `texto[::-1]` inverte o texto!\n"
            "- **Busca**: `\"py\" in texto` verifica se um pedaço existe dentro do texto (`True`/`False`).\n"
            "- **Métodos úteis**: `.upper()` (maiúsculas), `.lower()` (minúsculas), `.strip()` (remove espaços nas pontas), "
            "`.replace(a, b)` (troca pedaços), `.count(x)` (conta ocorrências) e `.split()` (separa em palavras).\n\n"
            "Importante: strings são **imutáveis**. Métodos como `.upper()` não mudam a variável original; eles **devolvem** um novo texto."
        ),
        "exemplo": (
            'frase = "  Python é legal  "\n'
            "limpa = frase.strip()\n"
            "\n"
            'print("Tamanho:", len(limpa))\n'
            'print("Primeira letra:", limpa[0])\n'
            'print("Última letra:", limpa[-1])\n'
            'print("Invertida:", limpa[::-1])\n'
            'print("Maiúscula:", limpa.upper())\n'
        ),
        "erros_comuns": [
            "Chamar `nome.upper()` sozinho sem guardar o retorno (`nome = nome.upper()`), achando que a string mudou.",
            "Tentar mudar uma letra com `texto[0] = \"P\"` — gera `TypeError`, pois strings são imutáveis.",
            "Esquecer que o índice começa em `0` e tentar acessar `texto[len(texto)]`, causando `IndexError`.",
        ],
        "dica_de_ouro": "Índices começam no `0`, `-1` aponta para o fim, e todo método de string devolve uma string nova.",
    },
    "fstring": {
        "nome": "F-strings (formatação)",
        "resumo": "Permitem inserir variáveis e formatar casas decimais diretamente dentro de um texto com f\"...\".",
        "explicacao": (
            "Juntar textos e variáveis com `+` e `str()` funciona, mas fica trabalhoso quando há muitos valores. "
            "Com uma **f-string**, basta colocar a letra `f` antes das aspas e envolver qualquer variável ou cálculo "
            "entre chaves `{ }`.\n\n"
            "Além de deixar o código limpo, as chaves aceitam especificadores de formato após dois-pontos `:`:\n"
            "- `{preco:.2f}`: mostra o número decimal com exatamente **2 casas decimais** (ótimo para dinheiro!).\n"
            "- `{n:02d}`: preenche com zero à esquerda para ter pelo menos 2 dígitos (ex.: `05:09`)."
        ),
        "exemplo": (
            'item = "Café"\n'
            "preco = 7.5\n"
            "qtd = 3\n"
            "horas = 9\n"
            "minutos = 4\n"
            "\n"
            'print(f"{qtd}x {item} = R$ {preco * qtd:.2f}")\n'
            'print(f"Horário: {horas:02d}:{minutos:02d}")\n'
        ),
        "erros_comuns": [
            "Esquecer a letra `f` antes das aspas (`\"Oi {nome}\"` imprime literalmente `{nome}`!).",
            "Escrever `round(x, 2)` esperando ver `10.50` — `round` mostra `10.5`; para fixar zeros no final use `{x:.2f}`.",
            "Colocar espaços errados dentro de `{x : .2f}` ou usar `,` no lugar de `.` em `.2f`.",
        ],
        "dica_de_ouro": "Colocou `f` antes das aspas, tudo entre `{ }` vira código Python calculado na hora — e `:.2f` garante sempre duas casas decimais.",
    },
    "listas": {
        "nome": "Listas",
        "resumo": "Coleções ordenadas e mutáveis que guardam vários valores em uma única variável.",
        "explicacao": (
            "Quando você precisa guardar 5, 10 ou 100 notas, criar variáveis `nota1`, `nota2`, `nota3` não escala. "
            "Uma **lista** guarda quantos elementos você quiser dentro de colchetes `[ ]`, separados por vírgula.\n\n"
            "Diferente das strings, listas são **mutáveis** (podem crescer, encolher e trocar valores por índice):\n"
            "- `lista[0]` acessa o primeiro item; `lista[-1]` acessa o último.\n"
            "- `lista.append(x)` adiciona `x` no final; `lista.insert(i, x)` insere na posição `i`.\n"
            "- `lista.pop()` remove o último (ou `pop(i)` o da posição `i`); `lista.remove(x)` remove o primeiro valor igual a `x`.\n"
            "- `len(lista)`, `sum(lista)`, `max(lista)`, `min(lista)` e `x in lista` facilitam análises.\n"
            "- Use `for item in lista:` para percorrer valores, ou `for i in range(len(lista)):` quando precisar dos índices."
        ),
        "exemplo": (
            "notas = [7.5, 8.0, 6.5]\n"
            "notas.append(9.0)\n"
            "\n"
            "soma = 0\n"
            "for n in notas:\n"
            "    soma += n\n"
            "\n"
            "media = soma / len(notas)\n"
            'print("Notas:", notas)\n'
            'print(f"Média: {media:.2f} | Maior: {max(notas)}")\n'
        ),
        "erros_comuns": [
            "Fazer `lista = lista.append(x)`: o método `.append()` modifica a lista no lugar e devolve `None`, apagando sua variável!",
            "Acessar `lista[len(lista)]` (o último índice válido é `len(lista) - 1`).",
            "Fazer `copia = original` achando que criou uma lista independente (ambas apontam para a mesma lista; use `original.copy()`).",
        ],
        "dica_de_ouro": "`.append()` altera a lista direto e devolve `None` — nunca faça `lista = lista.append(...)`.",
    },
    "funcoes": {
        "nome": "Funções (def)",
        "resumo": "Blocos de código reutilizáveis com nome que recebem dados pelos parâmetros e executam uma tarefa.",
        "explicacao": (
            "Funções evitam repetição de código e dividem um problema grande em peças pequenas e fáceis de testar. "
            "Você cria uma função usando a palavra-chave `def`:\n\n"
            "```python\n"
            "def saudar(nome):\n"
            '    print(f"Olá, {nome}!")\n'
            "```\n\n"
            "Definir a função (`def`) apenas **ensina** o Python a fazer aquela tarefa — nada acontece até você "
            "**chamá-la** pelo nome: `saudar(\"Ana\")`.\n\n"
            "Variáveis criadas dentro de uma função são **locais**: existem somente enquanto a função está rodando. "
            "Você também pode definir **valores padrão** nos parâmetros, como `def calcular(preco, desconto=0.1):`."
        ),
        "exemplo": (
            "def dobro(n):\n"
            "    resultado = n * 2\n"
            "    return resultado\n"
            "\n"
            "def aplicar_desconto(valor, taxa=0.10):\n"
            "    return valor * (1 - taxa)\n"
            "\n"
            'print("Dobro de 7:", dobro(7))\n'
            'print(f"Com 10% off: R$ {aplicar_desconto(100):.2f}")\n'
            'print(f"Com 25% off: R$ {aplicar_desconto(100, 0.25):.2f}")\n'
        ),
        "erros_comuns": [
            "Definir a função com `def` e esquecer de chamá-la em seguida.",
            "Chamar a função passando mais ou menos argumentos do que os parâmetros exigidos.",
            "Tentar acessar fora da função uma variável local criada dentro dela (`NameError`).",
        ],
        "dica_de_ouro": "Dê à função tudo de que ela precisa pelos parâmetros e evite depender de variáveis soltas lá fora.",
    },
    "return": {
        "nome": "Retorno de valores (return)",
        "resumo": "Entrega o resultado calculado pela função de volta para quem a chamou e encerra a função.",
        "explicacao": (
            "Uma das confusões mais comuns no início é entre `print()` e `return`.\n\n"
            "- `print()` apenas **mostra** algo na tela para um humano ler; o programa não consegue reaproveitar esse valor em contas.\n"
            "- `return` **devolve** o valor para a linha que chamou a função, permitindo guardá-lo numa variável (`x = dobro(4)`) "
            "ou combiná-lo em outras expressões (`dobro(4) + 1`).\n\n"
            "Além disso, assim que o Python encontra um `return`, **a função termina imediatamente**. Por isso, dentro de laços "
            "de busca ou validação, nunca dê `return` no `else` antes de terminar de olhar todos os itens!"
        ),
        "exemplo": (
            "def eh_par(numero):\n"
            "    return numero % 2 == 0\n"
            "\n"
            "def primeiro_negativo(lista):\n"
            "    for item in lista:\n"
            "        if item < 0:\n"
            "            return item   # só sai quando acha um negativo\n"
            "    return None           # só roda se nenhum item for negativo\n"
            "\n"
            'print("8 é par?", eh_par(8))\n'
            'print("Primeiro negativo:", primeiro_negativo([4, 2, -5, -1]))\n'
        ),
        "erros_comuns": [
            "Usar `print(resultado)` no lugar de `return resultado` dentro da função — aí `x = minha_funcao()` recebe `None`.",
            "Colocar `return` dentro do `for` com um `if/else` de forma que o laço pare na **primeira** volta antes de checar os demais itens.",
            "Escrever código depois do `return` no mesmo bloco achando que ainda será executado.",
        ],
        "dica_de_ouro": "`print()` fala com a tela; `return` devolve o valor para o seu código continuar trabalhando com ele.",
    },
    "depuracao": {
        "nome": "Depuração (caça a bugs)",
        "resumo": "Técnica de investigar erros de execução e defeitos de lógica até descobrir a causa real.",
        "explicacao": (
            "Errar faz parte do dia a dia de qualquer programador. **Depurar** é agir como um detetive: ler as pistas "
            "e encontrar onde o comportamento real se separou do esperado.\n\n"
            "Quando o Python mostrar um erro, leia sempre **o tipo do erro** e **o número da linha** (e olhe a linha anterior também):\n"
            "- `SyntaxError`: erro de escrita (faltou `:`, aspas ou parêntese sem fechar, `=` em vez de `==`).\n"
            "- `IndentationError`: espaços no início da linha fora do alinhamento.\n"
            "- `NameError`: variável não criada ou digitada com letra errada.\n"
            "- `TypeError`: mistura de tipos incompatíveis (como somar `str` com `int`).\n"
            "- `ValueError`: conversão inválida (como `int(\"abc\")`).\n"
            "- `ZeroDivisionError`: tentativa de dividir por zero.\n\n"
            "Quando o programa roda sem travar mas imprime o **valor errado** (bug de lógica), use o botão "
            "**🔬 Rastrear passo a passo** no Laboratório do Dojo para enxergar cada variável mudando linha por linha!"
        ),
        "exemplo": (
            "# Exemplo: um bug de lógica clássico (média sem parênteses)\n"
            "a = 8\n"
            "b = 6\n"
            "\n"
            "media_errada = a + b / 2\n"
            "media_certa = (a + b) / 2\n"
            "\n"
            "# Prints de depuração ajudam a conferir os valores:\n"
            'print("errada:", media_errada, "| certa:", media_certa)\n'
        ),
        "erros_comuns": [
            "Mudar linhas aleatórias sem ler a mensagem de erro ou sem testar o programa com um exemplo pequeno.",
            "Ignorar a linha **anterior** àquela apontada pelo `SyntaxError` (muitas vezes um parêntese ficou aberto nela).",
            "Testar só um caso fácil e achar que a lógica funciona para zeros, negativos ou empates.",
        ],
        "dica_de_ouro": "Nunca adivinhe o que uma variável vale — inspecione com o rastreador passo a passo ou com um `print()`.",
    },
    "teste_de_mesa": {
        "nome": "Teste de mesa",
        "resumo": "Simular a execução do programa linha por linha no papel, anotando o valor de cada variável.",
        "explicacao": (
            "O **teste de mesa** é a habilidade número um para desenvolver raciocínio lógico. Em vez de rodar o código "
            "no escuro e torcer para dar certo, você finge ser o computador.\n\n"
            "Como fazer um teste de mesa em 3 passos:\n"
            "1. Desenhe uma coluna para cada variável do programa e uma coluna para a **Saída**.\n"
            "2. Leia o programa **uma linha por vez**, de cima para baixo (ou seguindo desvios de `if` e voltas de `while`/`for`).\n"
            "3. Sempre que uma variável mudar de valor, risque o valor antigo e anote o novo na coluna dela.\n\n"
            "Aqui no Dojo, você treina isso nos exercícios **Preveja a saída** e pode conferir seu raciocínio "
            "usando a aba **🔬 Laboratório**, que faz o teste de mesa visual automaticamente para você!"
        ),
        "exemplo": (
            "# Faça o teste de mesa acompanhando a, b e soma:\n"
            "a = 2\n"
            "b = 5\n"
            "soma = 0\n"
            "\n"
            "for i in range(1, 4):\n"
            "    soma = soma + a\n"
            "    a = a + 1\n"
            "\n"
            "print(a, b, soma)\n"
        ),
        "erros_comuns": [
            "Achar que `x = y` conecta `x` e `y` para sempre (na verdade só copia o valor naquele instante).",
            "Pular voltas do laço de cabeça em vez de anotar cada repetição em ordem.",
            "Esquecer que dentro de uma função as variáveis locais não alteram variáveis de fora com o mesmo nome.",
        ],
        "dica_de_ouro": "Quem consegue prever o que o código vai fazer antes de apertar Executar já domina metade da programação.",
    },
}
