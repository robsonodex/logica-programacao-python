"""Estágio 21 - Lógica de Automação, Idempotência, Rate Limit, Retry e Máquinas de Estado."""

from .base import exercicio


@exercicio(estagio=21, dificuldade=2, tipo="funcao", conceitos=["maquina_estados", "sets", "funcoes"])
def filtrar_eventos_idempotentes(r):
    e1, e2, e3 = f"ev_{r.randint(10, 30)}", f"ev_{r.randint(31, 60)}", f"ev_{r.randint(61, 99)}"
    eventos = [
        {"event_id": e1, "acao": "cobrar"},
        {"event_id": e2, "acao": "notificar"},
        {"event_id": e1, "acao": "cobrar"},
        {"event_id": e3, "acao": "email"},
        {"event_id": e2, "acao": "notificar"},
    ]
    casos = [
        (eventos, [e3]),
        (eventos, []),
        ([], [e1]),
    ]
    return dict(
        titulo="Idempotência de webhooks (nunca processar duas vezes)",
        enunciado=(
            "Webhooks de pagamento e WhatsApp frequentemente chegam repetidos.\n\n"
            "Escreva `eventos_novos(eventos, ja_processados)` onde `eventos` é uma lista de dicts com `'event_id'` e "
            "`ja_processados` é uma lista de IDs já executados no passado. Retorne apenas a lista de `'event_id'`s "
            "**ainda não processados**, sem repetir duplicatas da própria leva, preservando a ordem."
        ),
        solucao=(
            "def eventos_novos(eventos, ja_processados):\n"
            "    vistos = set(ja_processados)\n"
            "    saida = []\n"
            "    for ev in eventos:\n"
            "        eid = ev.get('event_id')\n"
            "        if eid and eid not in vistos:\n"
            "            vistos.add(eid)\n"
            "            saida.append(eid)\n"
            "    return saida\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(eventos_novos({ev!r}, {jp!r}))"} for ev, jp in casos],
        testes_visiveis=2,
        dicas=[
            "Comece com `vistos = set(ja_processados)` para busca `O(1)`.",
            "Ao aceitar um `event_id`, adicione-o imediatamente em `vistos` para bloquear repetições na mesma leva!",
        ],
        explicacao=(
            "Garantir idempotência evita cobranças duplicadas e envio repetido de mensagens quando um webhook sofre retry."
        ),
    )


@exercicio(estagio=21, dificuldade=3, tipo="funcao", conceitos=["maquina_estados", "pilha_fila", "funcoes"])
def rate_limiter_janela_deslizante(r):
    janela = r.choice([10, 60])
    limite = r.choice([2, 3])
    tempos = [1, 2, 3, 5, janela + 2, janela + 3]
    casos = [
        (tempos, limite, janela),
        ([0, 1, 2, 3], 2, 10),
        ([], 3, 10),
    ]
    return dict(
        titulo="Rate Limiter por janela deslizante (proteção de API)",
        enunciado=(
            "Para não estourar o limite de chamadas de uma API externa, implemente `filtrar_rate_limit(timestamps, limite, janela)`:\n"
            "- `timestamps` é uma lista ordenada de instantes (segundos) em que requisições chegaram.\n"
            "- Uma requisição no instante `t` é **permitida (`True`)** se nos últimos `janela` segundos "
            "(`anterior > t - janela`) houve **menos que `limite`** requisições permitidas.\n"
            "- Retorne uma lista de booleanos indicando quais requisições foram permitidas."
        ),
        solucao=(
            "from collections import deque\n"
            "\n"
            "def filtrar_rate_limit(timestamps, limite, janela):\n"
            "    fila = deque()\n"
            "    res = []\n"
            "    for t in timestamps:\n"
            "        while fila and fila[0] <= t - janela:\n"
            "            fila.popleft()\n"
            "        if len(fila) < limite:\n"
            "            fila.append(t)\n"
            "            res.append(True)\n"
            "        else:\n"
            "            res.append(False)\n"
            "    return res\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(filtrar_rate_limit({ts!r}, {lm}, {jn}))"} for ts, lm, jn in casos],
        testes_visiveis=2,
        dicas=[
            "Use uma `deque` guardando apenas os timestamps **permitidos** dentro da janela atual.",
            "Antes de decidir sobre `t`, remova da esquerda (`popleft`) tudo que tiver `fila[0] <= t - janela`.",
        ],
        explicacao=(
            "O Rate Limiter com `deque` é um clássico de entrevistas de backend/sistemas e essencial em automações com APIs limitadas."
        ),
    )


@exercicio(estagio=21, dificuldade=3, tipo="funcao", conceitos=["maquina_estados", "dicionarios", "funcoes"])
def maquina_estados_lead(r):
    seq1 = r.choice([
        ["responder", "agendar", "comparecer"],
        ["responder", "desistir", "agendar"],
        ["agendar", "responder", "agendar"],
    ])
    casos = [
        seq1,
        ["responder", "agendar", "cancelar", "agendar", "comparecer"],
        ["desistir", "responder"],
        [],
    ]
    return dict(
        titulo="Máquina de Estados de Funil de Atendimento",
        enunciado=(
            "Modele o ciclo de vida de um lead começando em `'novo'` com a tabela de transições válidas:\n"
            "- `'novo'`: `'responder'` -> `'qualificado'`, `'desistir'` -> `'perdido'`\n"
            "- `'qualificado'`: `'agendar'` -> `'agendado'`, `'desistir'` -> `'perdido'`\n"
            "- `'agendado'`: `'comparecer'` -> `'concluido'`, `'cancelar'` -> `'qualificado'`\n"
            "- `'concluido'` e `'perdido'` são estados finais (ignoram eventos).\n\n"
            "Escreva `simular_funil(eventos)` que aplica a lista de eventos na ordem (ignorando eventos inválidos para o estado atual) "
            "e retorna o estado final."
        ),
        solucao=(
            "def simular_funil(eventos):\n"
            "    transicoes = {\n"
            "        'novo': {'responder': 'qualificado', 'desistir': 'perdido'},\n"
            "        'qualificado': {'agendar': 'agendado', 'desistir': 'perdido'},\n"
            "        'agendado': {'comparecer': 'concluido', 'cancelar': 'qualificado'},\n"
            "    }\n"
            "    estado = 'novo'\n"
            "    for ev in eventos:\n"
            "        estado = transicoes.get(estado, {}).get(ev, estado)\n"
            "    return estado\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(simular_funil({c!r}))"} for c in casos],
        testes_visiveis=2,
        dicas=[
            "Represente as transições num dicionário de dicionários `{estado: {evento: novo_estado}}`.",
            "A cada evento, faça `estado = transicoes.get(estado, {}).get(ev, estado)` — uma única linha limpa!",
        ],
        explicacao=(
            "Tabelas de transição eliminam `if/elif` frágeis e garantem que eventos fora de ordem nunca corrompam o estado do negócio."
        ),
    )


@exercicio(estagio=21, dificuldade=2, tipo="funcao", conceitos=["maquina_estados", "aritmeticos", "funcoes"])
def backoff_exponencial_retry(r):
    base = r.choice([1, 2])
    teto = r.choice([10, 16, 30])
    n = r.choice([4, 5])
    casos = [(n, base, teto), (3, 1, 100), (0, 2, 10)]
    return dict(
        titulo="Política de Retry com Backoff Exponencial",
        enunciado=(
            "Quando uma chamada de API falha temporariamente (HTTP 429 ou 503), aguardamos intervalos crescentes "
            "antes de tentar de novo (**backoff exponencial com teto**).\n\n"
            "Escreva `atrasos_retry(tentativas, base, teto)` que retorna uma lista de tamanho `tentativas`, "
            "onde o atraso da tentativa `i` (`0, 1, 2, ...`) é `min(teto, base * (2 ** i))`."
        ),
        solucao=(
            "def atrasos_retry(tentativas, base, teto):\n"
            "    return [min(teto, base * (2 ** i)) for i in range(max(0, tentativas))]\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(atrasos_retry({a}, {b}, {c}))"} for a, b, c in casos],
        testes_visiveis=2,
        dicas=[
            "Para `i` de `0` até `tentativas - 1`, calcule `base * (2 ** i)`.",
            "Limite o valor máximo com `min(teto, ...)`.",
        ],
        explicacao=(
            "Backoff exponencial com teto evita derrubar APIs instáveis com enxurradas de requisições imediatas."
        ),
    )


@exercicio(estagio=21, dificuldade=4, tipo="funcao", conceitos=["maquina_estados", "ordenacao", "dicionarios"])
def roteador_fila_prioridade(r):
    p_t1 = r.choice([2, 3])
    tarefas = [
        {"id": "t1", "prioridade": p_t1, "ordem": 1},
        {"id": "t2", "prioridade": 1, "ordem": 2},
        {"id": "t3", "prioridade": 1, "ordem": 1},
        {"id": "t4", "prioridade": 2, "ordem": 0},
    ]
    limite = r.choice([1, 2, 3])
    casos = [(tarefas, limite), (tarefas, 10), ([], 3)]
    return dict(
        titulo="Agendador de fila com prioridade e desempate FIFO",
        enunciado=(
            "Um worker de automação recebe uma lista de tarefas `{'id', 'prioridade', 'ordem'}` "
            "(onde prioridade `1` é a mais urgente e `ordem` menor chegou antes).\n\n"
            "Escreva `proximo_lote(tarefas, capacidade)` que retorna a lista de `id`s das até `capacidade` "
            "tarefas que devem rodar primeiro, ordenadas por `(prioridade, ordem)`."
        ),
        solucao=(
            "def proximo_lote(tarefas, capacidade):\n"
            "    if capacidade <= 0:\n"
            "        return []\n"
            "    ordenadas = sorted(tarefas, key=lambda t: (t['prioridade'], t['ordem']))\n"
            "    return [t['id'] for t in ordenadas[:capacidade]]\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(proximo_lote({t!r}, {cap}))"} for t, cap in casos],
        testes_visiveis=1,
        dicas=[
            "Use `sorted(tarefas, key=lambda t: (t['prioridade'], t['ordem']))`.",
            "Retorne os `[:capacidade]` primeiros `id`s (tratando `capacidade <= 0`).",
        ],
        explicacao=(
            "Ordenar por `(prioridade, ordem_de_chegada)` garante urgência sem gerar injustiça entre tarefas de mesma prioridade."
        ),
    )


@exercicio(estagio=21, dificuldade=4, tipo="quebrar", conceitos=["maquina_estados", "depuracao"])
def quebrar_transicao_estado_final(r):
    ev_exemplo = r.choice(["['cancelar', 'pagar']", "['pagar', 'cancelar', 'pagar']", "['pagar', 'enviar', 'pagar']"])
    return dict(
        titulo="Quebre o código: transição ilegal após cancelamento ou envio",
        enunciado=(
            "Um fluxo de pedido começa em `'pendente'`. Ele pode ir para `'pago'` (`pagar`), de `'pago'` para `'enviado'` (`enviar`), "
            "ou ser cancelado (`cancelar` -> `'cancelado'`) se ainda não foi enviado. Uma vez `'cancelado'` ou `'enviado'`, **nunca** pode voltar para `'pago'`.\n\n"
            "**Seu desafio:** forneça uma lista de eventos (ex.: `['cancelar', 'pagar']`) que faça o código bugado abaixo "
            "terminar em um estado proibido!"
        ),
        modo_quebrar="args",
        funcao_quebrar="estado_pedido",
        placeholder_quebrar="Ex.: ['cancelar', 'pagar']",
        codigo_inicial=(
            "def estado_pedido(eventos):\n"
            "    estado = 'pendente'\n"
            "    for ev in eventos:\n"
            "        if ev == 'pagar':\n"
            "            estado = 'pago'\n"
            "        elif ev == 'enviar' and estado == 'pago':\n"
            "            estado = 'enviado'\n"
            "        elif ev == 'cancelar' and estado != 'enviado':\n"
            "            estado = 'cancelado'\n"
            "    return estado\n"
        ),
        solucao=(
            "def estado_pedido(eventos):\n"
            "    transicoes = {\n"
            "        'pendente': {'pagar': 'pago', 'cancelar': 'cancelado'},\n"
            "        'pago': {'enviar': 'enviado', 'cancelar': 'cancelado'},\n"
            "    }\n"
            "    estado = 'pendente'\n"
            "    for ev in eventos:\n"
            "        estado = transicoes.get(estado, {}).get(ev, estado)\n"
            "    return estado\n"
        ),
        testes=[{"entrada": ev_exemplo}],
        testes_visiveis=0,
        dicas=[
            "Veja o `if ev == 'pagar':` no código bugado — ele NÃO verifica qual era o estado atual!",
            "O que acontece se o pedido for cancelado primeiro e depois chegar um webhook atrasado de `'pagar'`?",
        ],
        explicacao=(
            "Sem checar `estado == 'pendente'`, um evento atrasado `'pagar'` ressuscita um pedido `'cancelado'` para `'pago'`."
        ),
    )
