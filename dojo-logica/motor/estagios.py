"""Trilha do nível básico: cada estágio introduz poucos conceitos novos."""

ESTAGIOS = [
    {"n": 1, "nome": "Variáveis e saída", "icone": "📦",
     "resumo": "Guardar valores em variáveis e mostrar resultados com print().",
     "conceitos": ["variaveis", "print"]},
    {"n": 2, "nome": "Tipos de dados", "icone": "🔤",
     "resumo": "int, float, str e bool: o que cada tipo é e como converter entre eles.",
     "conceitos": ["tipos", "conversao", "fstring"]},
    {"n": 3, "nome": "Entrada de dados", "icone": "⌨️",
     "resumo": "Ler valores do usuário com input() e convertê-los para o tipo certo.",
     "conceitos": ["input", "conversao"]},
    {"n": 4, "nome": "Operadores matemáticos", "icone": "➗",
     "resumo": "+ - * / // % ** e a ordem em que o Python faz as contas.",
     "conceitos": ["aritmeticos", "precedencia"]},
    {"n": 5, "nome": "Comparação e lógica", "icone": "⚖️",
     "resumo": "==, !=, <, >, and, or, not: perguntas que respondem True ou False.",
     "conceitos": ["comparacao", "logicos"]},
    {"n": 6, "nome": "Decisões com if/else", "icone": "🔀",
     "resumo": "Fazer o programa escolher entre dois caminhos.",
     "conceitos": ["if_else"]},
    {"n": 7, "nome": "Vários caminhos: elif", "icone": "🧭",
     "resumo": "Encadear condições com if/elif/else e condições compostas.",
     "conceitos": ["elif", "logicos"]},
    {"n": 8, "nome": "Repetição com while", "icone": "🔁",
     "resumo": "Repetir enquanto uma condição for verdadeira: contadores e acumuladores.",
     "conceitos": ["while", "contador", "acumulador"]},
    {"n": 9, "nome": "Repetição com for", "icone": "🔂",
     "resumo": "Percorrer sequências e usar range() para repetir um número exato de vezes.",
     "conceitos": ["for_range", "acumulador"]},
    {"n": 10, "nome": "Strings a fundo", "icone": "🧵",
     "resumo": "Índices, fatias, len(), métodos e percorrer texto letra por letra.",
     "conceitos": ["strings"]},
    {"n": 11, "nome": "Listas", "icone": "📋",
     "resumo": "Guardar vários valores, percorrer, somar, buscar e modificar listas.",
     "conceitos": ["listas"]},
    {"n": 12, "nome": "Funções", "icone": "🧩",
     "resumo": "Criar blocos reutilizáveis com def, parâmetros e return.",
     "conceitos": ["funcoes", "return"]},
    {"n": 13, "nome": "Desafios de lógica", "icone": "🏆",
     "resumo": "Problemas que combinam tudo o que você aprendeu no nível básico.",
     "conceitos": ["teste_de_mesa", "depuracao"]},
]

TOTAL_ESTAGIOS = len(ESTAGIOS)


def estagio(n: int) -> dict:
    return ESTAGIOS[n - 1]
