# 🥋 Dojo de Lógica — Prática Diária de Python

Sistema local, 100% offline e sem dependências externas para praticar lógica de programação e Python do zero todos os dias, com **20 questões diárias de dificuldade progressiva**.

---

## Como iniciar

1. Dê dois cliques em **`iniciar_dojo.bat`** (na pasta raiz) ou em **`dojo-logica/iniciar.bat`**.
   - Ou, pelo terminal, execute:
     ```bash
     cd dojo-logica
     python servidor.py
     ```
2. O navegador abrirá automaticamente em `http://localhost:8765`.
3. Seu progresso fica salvo automaticamente em `dojo-logica/dados/progresso.json`.

---

## Metodologia diária (20 questões por dia)

Cada dia gera automaticamente um plano de **20 questões novas** (com valores, contextos e testes gerados dinamicamente) seguindo uma curva pedagógica progressiva:

1. **Aquecimento**: questões rápidas de estágios anteriores para consolidar a memória.
2. **Revisão espaçada**: questões com conceitos em que você teve mais dificuldade nos últimos dias voltam após 1, 3 e 7 dias.
3. **Conceitos do Estágio Atual**: o núcleo da sua prática do dia, indo da aplicação direta até problemas de raciocínio.
4. **Desafios**: problemas finais combinando vários conceitos.

Quer praticar mais no mesmo dia? Clique em **`+20 Questões Extras`** para gerar um novo conjunto no mesmo dia.

---

## Os 13 Estágios do Nível Básico

| Estágio | Tema | Conceitos principais |
| :---: | :--- | :--- |
| 1 | 📦 Variáveis e saída | Variáveis, atribuição, `print()`, `sep`, `end` |
| 2 | 🔤 Tipos de dados | `int`, `float`, `str`, `bool`, `type()`, conversões, f-strings |
| 3 | ⌨️ Entrada de dados | `input()`, leitura e conversão numérica |
| 4 | ➗ Operadores matemáticos | `+ - * / // % **`, precedência e parênteses |
| 5 | ⚖️ Comparação e lógica | `== != < > <= >=`, `and`, `or`, `not` |
| 6 | 🔀 Decisões com if/else | Condicionais simples e compostas |
| 7 | 🧭 Vários caminhos: elif | Cadeias `if/elif/else` e faixas de valores |
| 8 | 🔁 Repetição com while | Laços condicionais, contadores, acumuladores, sentinela |
| 9 | 🔂 Repetição com for | `range()`, somatórios, iteração em texto, laços aninhados |
| 10 | 🧵 Strings a fundo | Índices, fatias, `len()`, métodos e busca |
| 11 | 📋 Listas | Coleções, índices, `append`, `pop`, filtros e ordenação |
| 12 | 🧩 Funções | `def`, parâmetros, `return` vs `print`, escopo local |
| 13 | 🏆 Desafios de lógica | Integração completa de todo o nível básico |

Resolva **20 questões de um estágio** para desbloquear o próximo automaticamente.

---

## Os 5 formatos de exercícios

- **Escreva o programa**: construir a solução completa do zero lendo `input()` quando necessário.
- **Escreva a função**: implementar funções reutilizáveis usando `def` e `return` (estágios 12 e 13).
- **Preveja a saída**: fazer o **teste de mesa** linha por linha antes de rodar.
- **Caça ao bug**: investigar códigos com erros de sintaxe, tipo ou lógica silenciosa e corrigi-los.
- **Complete o código**: preencher lacunas estratégicas (`___`) entendendo a estrutura da solução.

---

## Recursos de apoio no painel

- **Mini-lições integradas**: toda questão exibe chips clicáveis com os conceitos exigidos; clique para ver explicação, exemplo executável e erros comuns.
- **Erros traduzidos para o português**: se algo falhar, o sistema explica a causa provável (como `TypeError`, `NameError`, `IndentationError`, `SyntaxError`) em linguagem clara.
- **Laboratório (Teste de Mesa Visual)**: execute qualquer código **passo a passo**, acompanhando a linha ativa, os valores e tipos de cada variável na memória (destacando o que mudou em cada passo) e a saída acumulada.

---

## Quando evoluir para o Nível Intermediário?

Ao dominar os 13 estágios do nível básico, você poderá voltar e solicitar a evolução para a trilha **Intermediária**, escolhendo quais novos conteúdos incluir (dicionários, tuplas, conjuntos, list comprehensions, manipulação de arquivos, tratamento de exceções, módulos e programação orientada a objetos).
