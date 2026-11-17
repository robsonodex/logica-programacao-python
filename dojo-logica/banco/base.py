"""
Base do banco de exercícios do Dojo de Lógica.

Cada exercício é um *modelo* (template): uma função que recebe um gerador
aleatório ``r`` (random.Random) e devolve um dicionário descrevendo a questão.
Como os valores mudam com a semente, o mesmo modelo gera questões diferentes
a cada dia -- o banco é praticamente infinito.

Campos do dicionário devolvido:

    titulo        (str)  obrigatório - título curto da questão
    enunciado     (str)  obrigatório - texto da questão. Aceita um mini-markdown:
                         `código`, **negrito**, listas com "- ", blocos ```código```
    solucao       (str)  obrigatório - código Python de referência (gabarito).
                         Para o tipo "prever", é o trecho mostrado ao aluno.
    dicas         (list) obrigatório - 2 a 3 dicas progressivas (da mais vaga à mais direta)
    explicacao    (str)  obrigatório - explica por que a solução funciona
    testes        (list) opcional  - lista de dicts {"entrada": "linhas\\nseparadas", "chamada": "print(f(2))"}
                         - "entrada": o que o usuário "digitaria" (cada linha = um input())
                         - "chamada": código executado DEPOIS do código do aluno (útil p/ funções)
                         A saída esperada é calculada executando a ``solucao`` -- nunca escreva à mão.
    codigo_inicial(str)  opcional  - código que já aparece no editor (obrigatório p/ "corrigir" e "completar")
    testes_visiveis (int) opcional - quantos testes aparecem como exemplo (padrão 1)
"""

from __future__ import annotations

import builtins
import io
import random
from dataclasses import dataclass, field
from typing import Callable

TIPOS = {
    "codigo": "Escreva o programa",
    "funcao": "Escreva a função",
    "prever": "Preveja a saída",
    "corrigir": "Caça ao bug",
    "completar": "Complete o código",
}

CONCEITOS_VALIDOS = {
    "variaveis", "print", "tipos", "conversao", "input", "aritmeticos",
    "precedencia", "comparacao", "logicos", "if_else", "elif", "while",
    "contador", "acumulador", "for_range", "strings", "fstring", "listas",
    "funcoes", "return", "depuracao", "teste_de_mesa",
}


@dataclass
class Modelo:
    id: str
    estagio: int
    dificuldade: int
    tipo: str
    conceitos: list[str]
    gerar_fn: Callable = field(repr=False)

    def gerar(self, semente: int) -> dict:
        r = random.Random(f"{self.id}:{semente}")
        dados = self.gerar_fn(r)
        dados.setdefault("testes", [{"entrada": ""}])
        dados.setdefault("codigo_inicial", "")
        dados.setdefault("testes_visiveis", 1)
        for t in dados["testes"]:
            t.setdefault("entrada", "")
            t.setdefault("chamada", "")
        return dados


REGISTRO: dict[str, Modelo] = {}


def exercicio(estagio: int, dificuldade: int, tipo: str, conceitos: list[str]):
    """Decorador que registra um modelo de exercício no banco."""
    if tipo not in TIPOS:
        raise ValueError(f"tipo inválido: {tipo}")
    invalidos = set(conceitos) - CONCEITOS_VALIDOS
    if invalidos:
        raise ValueError(f"conceitos inválidos: {invalidos}")

    def deco(fn):
        modulo = fn.__module__.rsplit(".", 1)[-1]
        mid = f"{modulo}.{fn.__name__}"
        if mid in REGISTRO:
            raise ValueError(f"modelo duplicado: {mid}")
        REGISTRO[mid] = Modelo(mid, estagio, dificuldade, tipo, list(conceitos), fn)
        return fn

    return deco


# ---------------------------------------------------------------------------
# Execução do gabarito (código confiável) dentro do próprio processo.
# Não altera sys.stdout: injeta print/input próprios, então é thread-safe.
# ---------------------------------------------------------------------------

_print_real = builtins.print


def executar_referencia(codigo: str, entrada: str = "", chamada: str = "") -> str:
    buf = io.StringIO()
    linhas = iter(entrada.split("\n")) if entrada != "" else iter(())

    def _print(*args, **kwargs):
        kwargs["file"] = buf
        _print_real(*args, **kwargs)

    def _input(prompt=""):
        try:
            return next(linhas)
        except StopIteration:
            raise EOFError("input() chamado sem dados de entrada") from None

    b = dict(builtins.__dict__)
    b["print"] = _print
    b["input"] = _input
    g = {"__builtins__": b, "__name__": "__main__"}
    exec(compile(codigo, "<gabarito>", "exec"), g)
    if chamada:
        exec(compile(chamada, "<chamada>", "exec"), g)
    return buf.getvalue()
