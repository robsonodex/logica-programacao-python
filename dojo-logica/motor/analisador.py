"""Análise estática (AST), medição empírica de passos/Big-O e classificação de bugs."""

from __future__ import annotations

import ast
import builtins
import io
import sys
import time

# Catálogo de categorias para o Museu dos Meus Bugs
CATEGORIAS_BUG = {
    "sintaxe_indentacao": {
        "nome": "Sintaxe e indentação",
        "cura": "Antes de rodar, confira os dois-pontos `:` no fim de blocos, parênteses/aspas fechados e alinhamento de 4 espaços.",
    },
    "tipo_conversao": {
        "nome": "Tipos e conversões (str/int/float)",
        "cura": "Lembre que `input()` retorna texto (`str`). Converta explicitamente com `int()` ou `float()` e valide entradas antes de operar.",
    },
    "indice_off_by_one": {
        "nome": "Índices, chaves e off-by-one",
        "cura": "Em sequências de tamanho `n`, índices válidos vão de `0` a `n - 1`. Em dicionários, prefira `.get(chave, padrao)` para evitar `KeyError`.",
    },
    "variavel_escopo": {
        "nome": "Variáveis não definidas ou escopo",
        "cura": "Inicialize acumuladores antes do laço e passe valores como parâmetros em funções em vez de depender de variáveis externas.",
    },
    "return_ausente": {
        "nome": "Esquecer return ou retornar None",
        "cura": "Funções avaliadas por retorno devem encerrar com `return valor` em todos os caminhos possíveis, não apenas `print()`.",
    },
    "loop_infinito": {
        "nome": "Loop infinito ou complexidade excessiva",
        "cura": "No `while`, garanta que a variável de controle avança a cada iteração. Em listas grandes, evite laço aninhado usando `set` ou `dict`.",
    },
    "entrada_eof": {
        "nome": "Leitura excessiva de input()",
        "cura": "Conte exatamente quantas linhas o enunciado especifica para `input()` e nunca chame `input()` dentro de função avaliada por parâmetro.",
    },
    "divisao_zero": {
        "nome": "Divisão por zero",
        "cura": "Sempre trate denominador igual a zero (`if n == 0:`) antes de dividir ou calcular médias de coleções potencialmente vazias.",
    },
    "logica_borda": {
        "nome": "Casos de borda (edge cases)",
        "cura": "Seu código passou nos casos comuns mas falhou na fronteira. Teste mentalmente vazio `[]`/`\"\"`, `0`, negativos, 1 elemento e empates.",
    },
    "logica_geral": {
        "nome": "Lógica do algoritmo ou formato de saída",
        "cura": "Faça o teste de mesa no Laboratório acompanhando cada variável e confira se o formato da saída bate exatamente com o contrato.",
    },
}


def _profundidade_aninhamento(no: ast.AST, atual: int = 0) -> int:
    blocos = (ast.If, ast.For, ast.AsyncFor, ast.While, ast.Try, ast.With, ast.AsyncWith)
    max_p = atual
    for filho in ast.iter_child_nodes(no):
        prox = atual + 1 if isinstance(filho, blocos) else atual
        sub = _profundidade_aninhamento(filho, prox)
        if sub > max_p:
            max_p = sub
    return max_p


def _tem_busca_linear_em_laco(arvore: ast.AST) -> bool:
    """Detecta padrão de risco O(n²): laço aninhado ou `in`/`count`/`index` em coleção dentro de laço."""
    for no in ast.walk(arvore):
        if isinstance(no, (ast.For, ast.While)):
            for corpo_item in no.body:
                for sub in ast.walk(corpo_item):
                    if sub is not no and isinstance(sub, (ast.For, ast.While)):
                        return True
                    if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Attribute):
                        if sub.func.attr in ("count", "index", "remove"):
                            return True
    return False


def analisar_codigo(codigo: str, tipo: str = "codigo") -> dict:
    """Faz code review automático usando AST (biblioteca padrão do Python)."""
    linhas_uteis = [l for l in codigo.splitlines() if l.strip() and not l.strip().startswith("#")]
    try:
        arvore = ast.parse(codigo)
    except SyntaxError:
        return {
            "nota": 0,
            "nivel": "Erro de sintaxe",
            "metricas": {"linhas": len(linhas_uteis), "funcoes": 0, "aninhamento": 0, "desvios": 0},
            "observacoes": [],
        }

    funcoes = [n for n in ast.walk(arvore) if isinstance(n, ast.FunctionDef)]
    aninhamento = _profundidade_aninhamento(arvore)
    desvios = sum(
        1 for n in ast.walk(arvore)
        if isinstance(n, (ast.If, ast.For, ast.While, ast.ExceptHandler, ast.IfExp, ast.BoolOp))
    )

    nota = 100
    obs: list[dict] = []

    def add_obs(severidade: str, titulo: str, detalhe: str, penalidade: int = 0):
        nonlocal nota
        nota = max(20, nota - penalidade)
        obs.append({"severidade": severidade, "titulo": titulo, "detalhe": detalhe})

    # 1. Comparação explícita com True/False/None
    for no in ast.walk(arvore):
        if isinstance(no, ast.Compare):
            for op, comp in zip(no.ops, no.comparators):
                if isinstance(comp, ast.Constant) and isinstance(comp.value, bool) and isinstance(op, (ast.Eq, ast.NotEq)):
                    add_obs(
                        "melhoria",
                        "Comparação redundante com booleano",
                        "Em vez de `if cond == True:` ou `== False:`, escreva diretamente `if cond:` ou `if not cond:`.",
                        6,
                    )
                    break
                if isinstance(comp, ast.Constant) and comp.value is None and isinstance(op, (ast.Eq, ast.NotEq)):
                    add_obs(
                        "melhoria",
                        "Comparação com None usando ==/!=",
                        "Em Python idiomático, compare com `is None` ou `is not None`.",
                        4,
                    )
                    break

    # 2. except nu (engolir qualquer erro)
    for no in ast.walk(arvore):
        if isinstance(no, ast.ExceptHandler) and no.type is None:
            add_obs(
                "aviso",
                "Cláusula except sem tipo de exceção",
                "Evite `except:` genérico em produção; capture erros específicos como `except (ValueError, KeyError):`.",
                10,
            )
            break

    # 3. Argumento mutável padrão (bug clássico em Python e em código gerado por IA)
    for fn in funcoes:
        for default in fn.args.defaults + [d for d in fn.args.kw_defaults if d is not None]:
            if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                add_obs(
                    "aviso",
                    f"Argumento padrão mutável em `{fn.name}()`",
                    "Usar `=[]` ou `={}` como valor padrão compartilha o mesmo objeto entre chamadas. Use `None` e crie dentro da função.",
                    12,
                )
                break

    # 4. Aninhamento profundo
    if aninhamento >= 4:
        add_obs(
            "melhoria",
            f"Aninhamento profundo (nível {aninhamento})",
            "Muitos níveis de `if`/`for` dificultam leitura e testes. Use retorno antecipado (`return`/`continue`) ou extraia uma função auxiliar.",
            8,
        )

    # 5. Função longa
    for fn in funcoes:
        fim = getattr(fn, "end_lineno", fn.lineno) or fn.lineno
        comp = fim - fn.lineno + 1
        if comp > 28:
            add_obs(
                "melhoria",
                f"Função `{fn.name}()` extensa ({comp} linhas)",
                "Em entrevistas e sistemas reais, quebre funções longas em subfunções com responsabilidade única.",
                6,
            )

    # 6. Padrão range(len(...)) desnecessário
    for no in ast.walk(arvore):
        if (
            isinstance(no, ast.For)
            and isinstance(no.iter, ast.Call)
            and isinstance(no.iter.func, ast.Name)
            and no.iter.func.id == "range"
            and len(no.iter.args) == 1
            and isinstance(no.iter.args[0], ast.Call)
            and isinstance(no.iter.args[0].func, ast.Name)
            and no.iter.args[0].func.id == "len"
        ):
            add_obs(
                "melhoria",
                "Laço com `range(len(...))`",
                "Quando não precisar alterar por índice, prefira `for item in colecao:` ou `for i, item in enumerate(colecao):`.",
                4,
            )
            break

    # 7. Risco de complexidade quadrática
    if _tem_busca_linear_em_laco(arvore):
        add_obs(
            "melhoria",
            "Possível custo quadrático O(n²)",
            "Há laços aninhados ou buscas lineares (`.count`/`.index`/`.remove`) dentro de laço. Avalie se um `dict` ou `set` reduz para `O(n)`.",
            6,
        )

    # 8. Código inatingível após return
    for fn in funcoes:
        for i, stmt in enumerate(fn.body[:-1]):
            if isinstance(stmt, ast.Return):
                add_obs(
                    "aviso",
                    f"Código inatingível após `return` em `{fn.name}()`",
                    "Linhas depois de um `return` no mesmo bloco nunca são executadas.",
                    8,
                )
                break

    if not obs:
        obs.append({
            "severidade": "ok",
            "titulo": "Código limpo e legível",
            "detalhe": "Boa estrutura, sem anti-padrões detectados pelo analisador estático.",
        })

    nivel = "Excelente" if nota >= 90 else ("Bom" if nota >= 75 else "Pode melhorar")
    return {
        "nota": nota,
        "nivel": nivel,
        "metricas": {
            "linhas": len(linhas_uteis),
            "funcoes": len(funcoes),
            "aninhamento": aninhamento,
            "desvios": desvios,
        },
        "observacoes": obs[:5],
    }


def medir_passos(codigo: str, entrada: str = "", chamada: str = "", max_passos: int = 120000) -> dict:
    """Conta quantas linhas Python o código executou de fato (sem ruído de CPU)."""
    buf_in = io.StringIO(entrada + ("\n" if entrada and not entrada.endswith("\n") else ""))
    buf_out = io.StringIO()

    def _input(prompt=""):
        linha = buf_in.readline()
        if linha == "":
            raise EOFError("SEM_ENTRADA")
        return linha.rstrip("\r\n")

    b = dict(builtins.__dict__)
    b["input"] = _input
    g = {"__name__": "__main__", "__builtins__": b}

    passos = 0
    excedeu = False

    class _Parar(BaseException):
        pass

    def _contar(frame, evento, arg):
        nonlocal passos, excedeu
        if frame.f_code.co_filename == "seu_codigo.py" and evento == "line":
            passos += 1
            if passos >= max_passos:
                excedeu = True
                raise _Parar()
        return _contar

    orig_stdout = sys.stdout
    orig_trace = sys.gettrace()
    inicio = time.perf_counter()
    try:
        sys.stdout = buf_out
        cod = compile(codigo, "seu_codigo.py", "exec")
        sys.settrace(_contar)
        exec(cod, g)
        if chamada:
            exec(compile(chamada, "teste_bench.py", "exec"), g)
    except (_Parar, SystemExit):
        pass
    except BaseException:
        return {"passos": passos, "ms": round((time.perf_counter() - inicio) * 1000, 2), "ok": False, "excedeu": excedeu}
    finally:
        sys.settrace(orig_trace)
        sys.stdout = orig_stdout

    return {
        "passos": passos,
        "ms": round((time.perf_counter() - inicio) * 1000, 2),
        "ok": True,
        "excedeu": excedeu,
    }


def medir_complexidade(codigo: str, benchmark: dict | None, testes: list[dict] | None = None) -> dict:
    """Mede passos reais; quando há ``benchmark`` com múltiplos tamanhos N, estima o Big-O empírico."""
    if benchmark and benchmark.get("chamadas"):
        amostras = []
        for n, chamada in benchmark["chamadas"]:
            m = medir_passos(codigo, "", chamada)
            amostras.append({"n": n, "passos": m["passos"], "excedeu": m["excedeu"]})

        esperado = benchmark.get("esperado", "O(n)")
        classe = "O(n)"
        if len(amostras) >= 2:
            n1, p1 = amostras[0]["n"], max(1, amostras[0]["passos"])
            n2, p2 = amostras[-1]["n"], max(1, amostras[-1]["passos"])
            fator_n = max(1.0, n2 / max(1, n1))
            razao = p2 / p1
            if amostras[-1]["excedeu"] or razao >= (fator_n ** 1.55):
                classe = "O(n²)"
            elif razao <= 1.8:
                classe = "O(1)"
            elif razao <= fator_n * 1.45:
                classe = "O(n)"
            else:
                classe = "O(n log n)"

        ordem = {"O(1)": 1, "O(log n)": 2, "O(n)": 3, "O(n log n)": 4, "O(n²)": 5}
        otimo = ordem.get(classe, 3) <= ordem.get(esperado, 3)
        if otimo:
            feedback = f"Crescimento empírico compatível com {classe} (meta da questão: {esperado})."
        else:
            feedback = (
                f"Seu algoritmo cresceu como {classe} ({amostras[0]['passos']} passos em N={amostras[0]['n']} "
                f"para {amostras[-1]['passos']} em N={amostras[-1]['n']}). A meta ótima é {esperado}."
            )
        return {
            "tem_benchmark": True,
            "classe": classe,
            "esperado": esperado,
            "otimo": otimo,
            "amostras": amostras,
            "feedback": feedback,
        }

    # Sem benchmark específico: mede passos no primeiro teste apenas como telemetria
    if testes:
        t0 = testes[0]
        m = medir_passos(codigo, t0.get("entrada", ""), t0.get("chamada", ""))
        return {
            "tem_benchmark": False,
            "classe": None,
            "esperado": None,
            "otimo": True,
            "passos": m["passos"],
            "ms": m["ms"],
            "feedback": f"Executou {m['passos']} passo(s) no caso principal.",
        }
    return {"tem_benchmark": False, "classe": None, "otimo": True, "passos": 0, "feedback": ""}


def classificar_bug(resultados: list[dict], codigo: str, tipo_questao: str) -> dict:
    """Classifica a causa raiz de uma tentativa incorreta para o Museu dos Meus Bugs."""
    erros = [r["erro"] for r in resultados if r.get("erro")]
    if erros:
        e = erros[0]
        tipo = e.get("tipo", "")
        msg = e.get("mensagem", "") or ""
        if tipo in ("SyntaxError", "IndentationError", "TabError"):
            cat = "sintaxe_indentacao"
        elif tipo in ("TypeError", "ValueError"):
            cat = "tipo_conversao"
        elif tipo in ("IndexError", "KeyError"):
            cat = "indice_off_by_one"
        elif tipo in ("NameError", "UnboundLocalError"):
            cat = "variavel_escopo"
        elif tipo == "Tempo":
            cat = "loop_infinito"
        elif tipo == "EOFError" or "SEM_ENTRADA" in msg:
            cat = "entrada_eof"
        elif tipo == "ZeroDivisionError":
            cat = "divisao_zero"
        else:
            cat = "logica_geral"
        return {"categoria": cat, "tipo_erro": tipo, "detalhe": msg[:140]}

    # Sem exceção: erro de saída ou retorno
    if tipo_questao == "funcao":
        if any((r.get("obtido") or "").strip() == "None" for r in resultados) and "return" not in codigo:
            return {"categoria": "return_ausente", "tipo_erro": "NoneReturn", "detalhe": "Função retornou None (faltou return)."}

    acertos = sum(1 for r in resultados if r.get("status") in ("exato", "quase"))
    if acertos > 0 and acertos < len(resultados):
        return {
            "categoria": "logica_borda",
            "tipo_erro": "EdgeCase",
            "detalhe": f"Passou em {acertos}/{len(resultados)} casos e falhou em caso de borda.",
        }
    return {"categoria": "logica_geral", "tipo_erro": "OutputMismatch", "detalhe": "Saída diferente do esperado."}
