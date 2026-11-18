"""Estágio 20 - Pipelines de Texto e Dados para LLMs (Chunking RAG, Parsing JSON, Budget de Tokens)."""

from .base import exercicio


@exercicio(estagio=20, dificuldade=2, tipo="funcao", conceitos=["pipelines_llm", "strings", "listas"])
def chunking_com_overlap(r):
    palavras = ["um", "dois", "tres", "quatro", "cinco", "seis", "sete", "oito"]
    tam = r.choice([3, 4])
    ov = r.choice([1, 2])
    texto = " ".join(palavras[: r.randint(6, 8)])
    casos = [(texto, tam, ov), ("a b c", 5, 1), ("", 3, 1), ("um dois tres quatro", 2, 0)]
    return dict(
        titulo="Chunking de texto com sobreposição (base de RAG)",
        enunciado=(
            "Em sistemas RAG (busca com IA), dividimos textos longos em blocos de palavras com sobreposição (*overlap*).\n\n"
            "Escreva `criar_chunks(texto, tamanho, overlap)` que:\n"
            "- Divide `texto` por espaços (`texto.split()`).\n"
            "- Se `texto` estiver vazio ou `tamanho <= 0`, retorna `[]`.\n"
            "- Garante `overlap` seguro (`0 <= overlap < tamanho`; se `overlap >= tamanho`, use `tamanho - 1`).\n"
            "- Avança de `passo = tamanho - overlap` em `passo`, parando assim que o último pedaço cobrir o fim da lista."
        ),
        solucao=(
            "def criar_chunks(texto, tamanho, overlap):\n"
            "    palavras = texto.split()\n"
            "    if not palavras or tamanho <= 0:\n"
            "        return []\n"
            "    overlap = max(0, min(overlap, tamanho - 1))\n"
            "    passo = tamanho - overlap\n"
            "    chunks = []\n"
            "    i = 0\n"
            "    while i < len(palavras):\n"
            "        chunks.append(' '.join(palavras[i:i + tamanho]))\n"
            "        if i + tamanho >= len(palavras):\n"
            "            break\n"
            "        i += passo\n"
            "    return chunks\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(criar_chunks({t!r}, {sz}, {ov_}))"} for t, sz, ov_ in casos],
        testes_visiveis=2,
        dicas=[
            "Calcule `overlap = max(0, min(overlap, tamanho - 1))` para evitar `passo <= 0` (loop infinito).",
            "Interrompa o laço (`break`) quando `i + tamanho >= len(palavras)` para não gerar pedaços redundantes no final.",
        ],
        explicacao=(
            "Esse algoritmo é o coração da indexação vetorial em RAG: mantém contexto entre blocos consecutivos e previne loops infinitos."
        ),
    )


@exercicio(estagio=20, dificuldade=3, tipo="funcao", conceitos=["pipelines_llm", "json_apis", "excecoes"])
def extrair_json_de_resposta_llm(r):
    score = r.randint(70, 99)
    sujo = f'Claro! Segue o resultado:\n```json\n{{"status": "ok", "score": {score}}}\n```\nEspero ter ajudado!'
    puro = f'{{"status": "ok", "score": {score}}}'
    invalido = "Desculpe, não consegui gerar JSON válido."
    casos = [sujo, puro, invalido, 'Texto antes {"a": 1, "b": 2} texto depois']
    return dict(
        titulo="Extrair JSON dentro de resposta suja de LLM",
        enunciado=(
            "Modelos de IA frequentemente respondem texto explicativo em volta de um bloco JSON.\n\n"
            "Escreva `extrair_json(resposta)` que tenta extrair e fazer `json.loads` do primeiro objeto `{...}` "
            "válido contido em `resposta` (inclusive dentro de blocos markdown ```` ```json ````). "
            "Se não houver JSON válido, retorne `None`."
        ),
        solucao=(
            "import json\n"
            "\n"
            "def extrair_json(resposta):\n"
            "    if not isinstance(resposta, str):\n"
            "        return None\n"
            "    ini = resposta.find('{')\n"
            "    fim = resposta.rfind('}')\n"
            "    if ini == -1 or fim == -1 or fim < ini:\n"
            "        return None\n"
            "    try:\n"
            "        return json.loads(resposta[ini:fim + 1])\n"
            "    except json.JSONDecodeError:\n"
            "        return None\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(extrair_json({c!r}))"} for c in casos],
        testes_visiveis=2,
        dicas=[
            "Encontre o primeiro `'{'` com `.find('{')` e o último `'}'` com `.rfind('}')`.",
            "Faça `json.loads(resposta[ini:fim + 1])` dentro de `try/except json.JSONDecodeError`.",
        ],
        explicacao=(
            "Extrair o bloco `{...}` com tratamento de `JSONDecodeError` torna pipelines de saída estruturada de LLM muito mais resilientes."
        ),
    )


@exercicio(estagio=20, dificuldade=3, tipo="funcao", conceitos=["pipelines_llm", "dicionarios", "listas"])
def truncar_historico_por_tokens(r):
    lim = r.choice([10, 12, 15, 18])
    msgs = [
        {"role": "system", "content": "Voce e um tutor"},
        {"role": "user", "content": "mensagem antiga numero um dois tres"},
        {"role": "assistant", "content": "resposta antiga curta"},
        {"role": "user", "content": "pergunta atual"},
    ]
    casos = [
        (msgs, lim),
        ([{"role": "system", "content": "sys"}, {"role": "user", "content": "oi"}], 10),
        ([], 10),
    ]
    return dict(
        titulo="Orçamento de contexto (Token Budget) para chat de IA",
        enunciado=(
            "Para economizar custo de API e não estourar a janela de contexto, precisamos podar o histórico de mensagens.\n\n"
            "Considere que cada mensagem custa `len(msg['content'].split())` tokens (1 palavra = 1 token). "
            "Escreva `podar_historico(mensagens, limite)` que:\n"
            "1. Sempre mantém a 1ª mensagem se ela tiver `role == 'system'` (se couber ou como base obrigatória);\n"
            "2. Mantém o máximo possível das mensagens **mais recentes** (do fim para o início) sem ultrapassar `limite` tokens no total;\n"
            "3. Retorna as mensagens selecionadas na **ordem cronológica original**."
        ),
        solucao=(
            "def podar_historico(mensagens, limite):\n"
            "    if not mensagens:\n"
            "        return []\n"
            "    def tokens(m):\n"
            "        return len(m.get('content', '').split())\n"
            "    sistema = []\n"
            "    resto = mensagens\n"
            "    usado = 0\n"
            "    if mensagens[0].get('role') == 'system':\n"
            "        sistema = [mensagens[0]]\n"
            "        usado = tokens(mensagens[0])\n"
            "        resto = mensagens[1:]\n"
            "    mantidas = []\n"
            "    for m in reversed(resto):\n"
            "        custo = tokens(m)\n"
            "        if usado + custo <= limite:\n"
            "            mantidas.append(m)\n"
            "            usado += custo\n"
            "        else:\n"
            "            break\n"
            "    mantidas.reverse()\n"
            "    return sistema + mantidas\n"
        ),
        testes=[{"entrada": "", "chamada": f"print([m['content'] for m in podar_historico({ms!r}, {lm})])"} for ms, lm in casos],
        testes_visiveis=1,
        dicas=[
            "Separe `mensagens[0]` se `role == 'system'` e contabilize os tokens dela primeiro.",
            "Percorra o restante com `reversed(resto)`, acumulando enquanto `usado + custo <= limite`, pare ao estourar (`break`) e inverta de volta!",
        ],
        explicacao=(
            "Preservar o prompt de sistema e priorizar as mensagens mais recentes em ordem cronológica é o padrão real de memória em chatbots de IA."
        ),
    )


@exercicio(estagio=20, dificuldade=2, tipo="funcao", conceitos=["pipelines_llm", "strings", "dicionarios"])
def renderizar_prompt_template(r):
    nome = r.choice(["Ana", "Robson", "Carla"])
    tema = r.choice(["Python", "Automações", "APIs"])
    casos = [
        ("Olá {{nome}}, hoje vamos estudar {{tema}}!", {"nome": nome, "tema": tema}),
        ("Sem variaveis aqui.", {"nome": "X"}),
        ("Oi {{nome}}, plano {{plano}}.", {"nome": nome}),
    ]
    return dict(
        titulo="Motor seguro de template de prompts ({{variavel}})",
        enunciado=(
            "Escreva `render_prompt(template, variaveis)` que substitui todas as ocorrências de `{{chave}}` "
            "pelo respectivo `str(valor)` no dicionário `variaveis`.\n\n"
            "- Se uma chave `{{...}}` no template **não** existir em `variaveis`, mantenha o marcador original intacto "
            "(não quebre com `KeyError`, diferente de `.format()`!)."
        ),
        solucao=(
            "def render_prompt(template, variaveis):\n"
            "    resultado = template\n"
            "    for k, v in variaveis.items():\n"
            "        resultado = resultado.replace('{{' + str(k) + '}}', str(v))\n"
            "    return resultado\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(render_prompt({t!r}, {v!r}))"} for t, v in casos],
        testes_visiveis=2,
        dicas=[
            "Evite `template.format(**variaveis)` porque chaves JSON `{}` dentro do prompt fariam `.format()` falhar!",
            "Substitua explicitamente `'{{' + str(k) + '}}'` usando `.replace()`.",
        ],
        explicacao=(
            "Usar delimitador duplo `{{chave}}` com `.replace()` permite incluir exemplos JSON com `{...}` dentro do prompt sem conflito."
        ),
    )


@exercicio(estagio=20, dificuldade=4, tipo="funcao", conceitos=["pipelines_llm", "sets", "ordenacao"])
def deduplicar_e_ranquear_rag(r):
    s1 = round(r.uniform(0.75, 0.95), 2)
    docs = [
        {"doc_id": "d1", "score": s1, "texto": "A"},
        {"doc_id": "d2", "score": 0.80, "texto": "B"},
        {"doc_id": "d1", "score": round(s1 - 0.1, 2), "texto": "A duplicado"},
        {"doc_id": "d3", "score": 0.99, "texto": "C"},
    ]
    casos = [(docs, 2), (docs, 5), ([], 3)]
    return dict(
        titulo="Reranking e deduplicação de documentos em RAG",
        enunciado=(
            "Uma busca vetorial retornou vários trechos candidatos (`{'doc_id', 'score', 'texto'}`), alguns com o mesmo `doc_id`.\n\n"
            "Escreva `selecionar_contexto(docs, k)` que:\n"
            "1. Mantém apenas o trecho de **maior `score`** para cada `doc_id`;\n"
            "2. Ordena do maior para o menor `score` (desempate por `doc_id` crescente);\n"
            "3. Retorna a lista dos `k` melhores `doc_id`s."
        ),
        solucao=(
            "def selecionar_contexto(docs, k):\n"
            "    melhores = {}\n"
            "    for d in docs:\n"
            "        did = d['doc_id']\n"
            "        if did not in melhores or d['score'] > melhores[did]:\n"
            "            melhores[did] = d['score']\n"
            "    ordenados = sorted(melhores.items(), key=lambda par: (-par[1], par[0]))\n"
            "    return [did for did, _ in ordenados[:k]]\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(selecionar_contexto({d!r}, {kv}))"} for d, kv in casos],
        testes_visiveis=1,
        dicas=[
            "Use um dicionário `melhores = {}` mapeando `doc_id -> maior_score`.",
            "Ordene `melhores.items()` por `(-par[1], par[0])` e retorne os `[:k]` IDs.",
        ],
        explicacao=(
            "Evitar enviar o mesmo documento repetido para o prompt economiza tokens e melhora a diversidade do contexto no RAG."
        ),
    )


@exercicio(estagio=20, dificuldade=4, tipo="quebrar", conceitos=["pipelines_llm", "depuracao"])
def quebrar_chunking_overlap_invalido(r):
    tam = r.choice([2, 3, 4])
    return dict(
        titulo="Quebre o código: chunker vulnerável a overlap >= tamanho",
        enunciado=(
            "A função `fatiar(palavras, tamanho, overlap)` divide uma lista de palavras em blocos de tamanho `tamanho` "
            "com sobreposição `overlap` (com `tamanho >= 1`, `overlap >= 0`).\n\n"
            f"**Seu desafio:** forneça `palavras, tamanho, overlap` (ex.: `['a', 'b', 'c'], {tam}, {tam}`) que faça o código "
            "abaixo entrar em erro ou gerar resultado incorreto!"
        ),
        modo_quebrar="args",
        funcao_quebrar="fatiar",
        placeholder_quebrar=f"Ex.: ['a', 'b', 'c'], {tam}, {tam}",
        codigo_inicial=(
            "def fatiar(palavras, tamanho, overlap):\n"
            "    passo = tamanho - overlap\n"
            "    return [palavras[i:i + tamanho] for i in range(0, len(palavras), passo)]\n"
        ),
        solucao=(
            "def fatiar(palavras, tamanho, overlap):\n"
            "    overlap = max(0, min(overlap, tamanho - 1))\n"
            "    passo = tamanho - overlap\n"
            "    return [palavras[i:i + tamanho] for i in range(0, len(palavras), passo)]\n"
        ),
        testes=[{"entrada": f"['a', 'b', 'c'], {tam}, {tam}"}],
        testes_visiveis=0,
        dicas=[
            "O que acontece com `passo = tamanho - overlap` quando `overlap == tamanho`?",
            "`range(0, n, 0)` lança `ValueError: range() arg 3 must not be zero`!",
        ],
        explicacao=(
            "Quando `overlap == tamanho` (ex.: `['a', 'b', 'c'], 2, 2`), `passo` vira `0` e `range()` explode com `ValueError`. "
            "Sempre limite `overlap` a no máximo `tamanho - 1`."
        ),
    )
