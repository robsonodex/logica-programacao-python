# Especificação para autores de exercícios — Dojo de Lógica

Projeto: `c:\Users\RobsonOliveira\Curso-Python\dojo-logica` — sistema local de prática diária de lógica com Python para um **iniciante absoluto** brasileiro. Todo texto voltado ao aluno deve estar em **português do Brasil, com acentuação correta**, tom amigável e didático.

## Como funciona o banco
- Leia `banco/base.py` (formato dos modelos, campos, decorador `@exercicio`) e `banco/estagio_01.py` (4 exemplos completos, um de cada tipo: codigo, prever, corrigir, completar). **Siga exatamente esse estilo.**
- A trilha de estágios está em `motor/estagios.py`. Cada estágio introduz poucos conceitos.
- Cada modelo é uma função `def nome(r):` decorada com `@exercicio(estagio=N, dificuldade=1..5, tipo="...", conceitos=[...])`, que usa **somente** o gerador `r` (r.randint, r.choice, r.sample, r.shuffle...) para variar números, nomes, contextos — nunca use `random` global, data/hora, etc. A geração precisa ser determinística a partir de `r`.
- A saída esperada é calculada automaticamente executando `solucao` com cada teste. **Nunca escreva saídas esperadas à mão** além do texto do enunciado (que você deve gerar com as mesmas variáveis Python, para bater com a solução).
- Conceitos válidos (ids): variaveis, print, tipos, conversao, input, aritmeticos, precedencia, comparacao, logicos, if_else, elif, while, contador, acumulador, for_range, strings, fstring, listas, funcoes, return, depuracao, teste_de_mesa. Use `depuracao` em todo "corrigir" e `teste_de_mesa` em todo "prever".

## Tipos
- `codigo`: aluno escreve o programa do zero (lendo `input()` quando houver entrada). Pode ter `codigo_inicial` com comentários-guia opcionais.
- `funcao`: aluno escreve uma função; os testes usam `"chamada"` (ex.: `{"entrada": "", "chamada": "print(dobro(4))"}`). Só a partir do estágio 12 (antes disso o aluno não conhece def).
- `prever`: `solucao` é o trecho mostrado; o aluno digita a saída exata. Ótimo para treinar teste de mesa. Se o trecho usar input(), forneça a entrada em `testes=[{"entrada": "..."}]` e mencione no enunciado o que foi digitado.
- `corrigir`: `codigo_inicial` tem um bug (erro de sintaxe, de lógica, de tipo, de indentação, nome errado, condição invertida, off-by-one, conversão esquecida...). O validador exige que o código com bug **falhe** em pelo menos um teste. Prefira bugs **de lógica** (que rodam mas dão resultado errado) com frequência, pois treinam raciocínio. Descreva no enunciado o comportamento esperado.
- `completar`: `codigo_inicial` com lacunas `___` que o aluno troca por código.

## Regras pedagógicas (importantíssimas)
1. **Só use conceitos do estágio atual e dos anteriores.** Ex.: no estágio 3 não existe if; no estágio 6 não existe laço; listas só a partir do 11; def só a partir do 12. Strings: print/concatenação/f-string desde o 2, mas índices/métodos só no 10 (exceto `len()` e `.upper()/.lower()` a partir do 9 se for natural). `round()`, `int()`, `float()`, `str()`, `abs()`, `type()` liberados a partir do 2. `max/min/sum` em listas só a partir do 11.
2. **Dificuldade progressiva dentro do estágio**: distribua os modelos de 1 a 5 (1 = aplicação direta do conceito; 3 = exige combinar 2 ideias; 5 = problema de raciocínio que pede planejamento). Cerca de 25% fáceis (1-2), 45% médios (3), 30% difíceis (4-5).
3. **Mistura de tipos** por estágio: ~40% codigo (ou funcao no 12+), ~20% prever, ~20% corrigir, ~20% completar.
4. **Problemas com contexto real e criativo** (mercado, jogo, notas, conta de luz, viagem, receitas, academia, games, pix, temperatura...), variando os contextos. Nada de questões repetidas com outra roupagem — cada modelo deve exercitar uma ideia diferente.
5. **Formato de saída exato no enunciado**, mostrado num bloco ``` com os valores do exemplo. Evite ambiguidades: diga quantas casas decimais (`f"{x:.2f}"`), separadores, maiúsculas. Evite floats sem formatação (ex.: 0.1+0.2). Entrada: diga a ordem dos input() e o tipo (ex.: "o programa lê dois números inteiros, um por linha").
6. `input("Mensagem: ")` com mensagem é permitido e recomendado — na correção as mensagens do input **não** aparecem na saída, então não as mostre na saída esperada.
7. **Testes**: para programas com input() ou funções, use de 3 a 6 testes, incluindo casos-limite (zero, negativo, igualdade, fronteiras de faixas, valor mínimo). `testes_visiveis=1` ou 2. Os valores dos testes também devem variar com `r`.
8. **Dicas**: 2 a 3, progressivas (1ª lembra o conceito; 2ª sugere a estratégia; 3ª quase entrega, ex.: mostra a estrutura sem a resposta).
9. **Explicação**: 2 a 5 frases explicando o raciocínio da solução e *por que* funciona (não só o que faz). Pode citar erro comum.
10. A `solucao` deve ser o código mais **simples e didático** possível para o nível, com nomes de variáveis em português, sem truques avançados.
11. Enunciados claros e curtos. Use `código` com crases para nomes de variáveis/funções.

## Arquivo e validação
- Cada estágio fica em `banco/estagio_NN.py` (NN com 2 dígitos), começando com docstring e `from .base import exercicio`. Nomes de funções únicos dentro do arquivo, descritivos, em snake_case.
- Rode a partir da pasta `dojo-logica`: `python ferramentas/validar_banco.py N` (N = número do estágio) até sair `OK` e **sem avisos de pouca variedade**.
- Inspecione algumas questões geradas: `python ferramentas/validar_banco.py --mostrar estagio_NN.nome_da_funcao 3` e confira se enunciado, saída e solução batem e fazem sentido para um iniciante.
- Não edite arquivos fora dos seus (base.py, validador, outros estágios). Se achar um problema na base, relate na resposta final.
- Resposta final: curta — lista de modelos criados (id, dificuldade, tipo) e qualquer observação.
