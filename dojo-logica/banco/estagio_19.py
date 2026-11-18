"""Estágio 19 - JSON Profundo, Webhooks e APIs (OpenAI, WhatsApp, CRM)."""

from .base import exercicio


@exercicio(estagio=19, dificuldade=1, tipo="funcao", conceitos=["json_apis", "dicionarios", "funcoes"])
def extrair_texto_resposta_llm(r):
    msg = r.choice(["Olá! Como posso ajudar?", "Agendamento confirmado.", "Resumo gerado com sucesso."])
    casos = [
        {"choices": [{"message": {"content": msg}}]},
        {"choices": [{"message": {"content": None}}]},
        {"choices": []},
        {"choices": None},
        {},
    ]
    return dict(
        titulo="Extrair resposta de payload estilo OpenAI",
        enunciado=(
            "Escreva `extrair_texto(payload)` que lê o campo `choices[0]['message']['content']` de um dicionário "
            "estilo resposta de API de LLM.\n\n"
            "- Se qualquer chave faltar, `choices` estiver vazia ou algum nível for `None`, retorne `\"\"` (string vazia) sem lançar erro."
        ),
        solucao=(
            "def extrair_texto(payload):\n"
            "    if not isinstance(payload, dict):\n"
            "        return ''\n"
            "    choices = payload.get('choices') or []\n"
            "    if not choices or not isinstance(choices[0], dict):\n"
            "        return ''\n"
            "    msg = choices[0].get('message') or {}\n"
            "    conteudo = msg.get('content')\n"
            "    return conteudo if isinstance(conteudo, str) else ''\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(repr(extrair_texto({c!r})))"} for c in casos],
        testes_visiveis=2,
        dicas=[
            "Use `payload.get('choices') or []` para proteger tanto contra chave ausente quanto contra `None`.",
            "Valide se `choices` não está vazia antes de acessar `choices[0]`, e use `(choices[0].get('message') or {})`.",
        ],
        explicacao=(
            "Respostas de APIs de IA podem retornar `content: null` (ex.: em chamadas de ferramenta) ou listas vazias. "
            "Proteger cada nível evita `KeyError`, `IndexError` e `AttributeError` em produção."
        ),
    )


@exercicio(estagio=19, dificuldade=2, tipo="funcao", conceitos=["json_apis", "strings", "funcoes"])
def normalizar_telefone_webhook(r):
    ddd = r.choice(["11", "21", "31", "85", "71"])
    num = f"9{r.randint(1000, 9999)}{r.randint(1000, 9999)}"
    casos = [
        f"+55 ({ddd}) {num[:5]}-{num[5:]}",
        f"({ddd}) {num[:5]}-{num[5:]}",
        f"55{ddd}{num}",
        "12345",
        None,
    ]
    return dict(
        titulo="Normalizar telefone de lead (WhatsApp/CRM)",
        enunciado=(
            "Escreva `normalizar_fone(bruto)` que recebe um telefone vindo de webhook/formulário e:\n"
            "1. Remove tudo que não for dígito (`0-9`).\n"
            "2. Se sobrarem **10 ou 11 dígitos**, adiciona o prefixo `'55'` na frente.\n"
            "3. Se o resultado final tiver **12 ou 13 dígitos** começando com `'55'`, retorna a string; caso contrário, retorna `None`.\n\n"
            f"Exemplo: `normalizar_fone('+55 ({ddd}) {num[:5]}-{num[5:]}')` -> `'55{ddd}{num}'`"
        ),
        solucao=(
            "def normalizar_fone(bruto):\n"
            "    if not isinstance(bruto, str):\n"
            "        return None\n"
            "    digitos = ''.join(ch for ch in bruto if ch.isdigit())\n"
            "    if len(digitos) in (10, 11):\n"
            "        digitos = '55' + digitos\n"
            "    if len(digitos) in (12, 13) and digitos.startswith('55'):\n"
            "        return digitos\n"
            "    return None\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(repr(normalizar_fone({c!r})))"} for c in casos],
        testes_visiveis=2,
        dicas=[
            "Filtre os dígitos com `''.join(ch for ch in bruto if ch.isdigit())`.",
            "Se `len(digitos)` for `10` ou `11`, prefixe `'55'` e valide tamanho final `12` ou `13`.",
        ],
        explicacao=(
            "Normalizar telefones na entrada de automações evita duplicar contatos no CRM e falhas de envio na API do WhatsApp."
        ),
    )


@exercicio(estagio=19, dificuldade=3, tipo="funcao", conceitos=["json_apis", "dicionarios", "funcoes"])
def extrair_caminho_seguro(r):
    val = r.randint(100, 999)
    obj = {"cliente": {"plano": {"limite": val}, "ativo": True}, "vazio": None}
    casos = [
        (obj, "cliente.plano.limite", 0),
        (obj, "cliente.plano.inexistente", -1),
        (obj, "vazio.algo", "padrao"),
        (obj, "cliente.ativo", False),
    ]
    return dict(
        titulo="Leitor genérico de caminho em JSON (dot notation)",
        enunciado=(
            "Escreva `obter_caminho(dados, caminho, padrao=None)` que navega por chaves separadas por ponto "
            "(ex.: `'cliente.plano.limite'`) dentro de dicionários aninhados.\n\n"
            "- Se qualquer etapa não for um `dict` ou a chave não existir, retorne `padrao`.\n"
            "- Atenção: se o valor encontrado for `0` ou `False`, retorne o valor encontrado (não `padrao`!)."
        ),
        solucao=(
            "def obter_caminho(dados, caminho, padrao=None):\n"
            "    atual = dados\n"
            "    for chave in caminho.split('.'):\n"
            "        if not isinstance(atual, dict) or chave not in atual:\n"
            "            return padrao\n"
            "        atual = atual[chave]\n"
            "    return atual\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(repr(obter_caminho({d!r}, {p!r}, {df!r})))"} for d, p, df in casos],
        testes_visiveis=2,
        dicas=[
            "Comece com `atual = dados` e percorra `for chave in caminho.split('.'):`.",
            "Em cada passo verifique `if not isinstance(atual, dict) or chave not in atual: return padrao`.",
        ],
        explicacao=(
            "Esse helper reutilizável substitui cadeias frágeis de `d['a']['b']['c']` ao integrar APIs e webhooks."
        ),
    )


@exercicio(estagio=19, dificuldade=3, tipo="funcao", conceitos=["json_apis", "dicionarios", "listas"])
def mesclar_registros_por_id(r):
    v_novo = r.randint(200, 500)
    base = [
        {"id": "u1", "nome": "Ana", "valor": 100},
        {"id": "u2", "nome": "Bruno", "valor": 150},
    ]
    updates = [
        {"id": "u2", "valor": v_novo},
        {"id": "u3", "nome": "Carla", "valor": 300},
    ]
    casos = [(base, updates), ([], [{"id": "a", "x": 1}]), ([{"id": "a", "x": 1}], [])]
    return dict(
        titulo="Sincronizar e mesclar registros por ID (upsert)",
        enunciado=(
            "Escreva `mesclar_por_id(base, atualizacoes)` que recebe duas listas de dicionários (cada um com chave `'id'`) "
            "e retorna uma nova lista ordenada por `'id'` onde:\n"
            "- Se o `'id'` já existe em `base`, mescla os campos (os campos de `atualizacoes` sobrescrevem os antigos, mantendo os demais);\n"
            "- Se o `'id'` é novo, inclui o registro;\n"
            "- Não modifique os dicionários originais."
        ),
        solucao=(
            "def mesclar_por_id(base, atualizacoes):\n"
            "    mapa = {item['id']: dict(item) for item in base}\n"
            "    for upd in atualizacoes:\n"
            "        uid = upd['id']\n"
            "        if uid in mapa:\n"
            "            mapa[uid].update(upd)\n"
            "        else:\n"
            "            mapa[uid] = dict(upd)\n"
            "    return [mapa[k] for k in sorted(mapa)]\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(mesclar_por_id({b!r}, {u!r}))"} for b, u in casos],
        testes_visiveis=1,
        dicas=[
            "Indexe `base` em um dicionário por `'id'` fazendo cópia (`dict(item)`) para não mutar a entrada.",
            "Para cada item em `atualizacoes`, use `.update(upd)` se o ID existir ou crie novo registro; no fim retorne ordenado por chave.",
        ],
        explicacao=(
            "Indexar por ID transforma uma sincronização de CRM/API de `O(n * m)` em `O(n + m)` sem perder campos antigos."
        ),
    )


@exercicio(estagio=19, dificuldade=4, tipo="funcao", conceitos=["json_apis", "recursao", "dicionarios"])
def achatar_json_aninhado(r):
    porta = r.choice([5432, 8080, 3000])
    d1 = {"app": {"nome": "dojo", "db": {"porta": porta}}, "debug": False}
    casos = [d1, {"a": {"b": 1}, "c": 2}, {"vazio": {}}, {}]
    return dict(
        titulo="Achatar JSON aninhado (flatten dict)",
        enunciado=(
            "Escreva `achatar_json(dados, prefixo='')` que transforma um dicionário aninhado em um dicionário plano "
            "unindo as chaves por ponto `.`.\n\n"
            f"- Exemplo: `{d1!r}` -> `{{'app.nome': 'dojo', 'app.db.porta': {porta}, 'debug': False}}`\n"
            "- Se um subdicionário estiver vazio (`{}`), ignore-o."
        ),
        solucao=(
            "def achatar_json(dados, prefixo=''):\n"
            "    saida = {}\n"
            "    for k, v in dados.items():\n"
            "        chave = f'{prefixo}.{k}' if prefixo else k\n"
            "        if isinstance(v, dict):\n"
            "            saida.update(achatar_json(v, chave))\n"
            "        else:\n"
            "            saida[chave] = v\n"
            "    return saida\n"
        ),
        testes=[{"entrada": "", "chamada": f"print(sorted(achatar_json({c!r}).items()))"} for c in casos],
        testes_visiveis=2,
        dicas=[
            "Monte `chave = f'{prefixo}.{k}' if prefixo else k`.",
            "Se `isinstance(v, dict)`, chame recursivamente `achatar_json(v, chave)` e junte com `saida.update(...)`.",
        ],
        explicacao=(
            "Achatar payloads JSON é rotina em pipelines de ETL, logs estruturados e exportação de dados de API para planilhas/bancos."
        ),
    )


@exercicio(estagio=19, dificuldade=4, tipo="quebrar", conceitos=["json_apis", "depuracao"])
def quebrar_get_com_none(r):
    chave = r.choice(["cliente", "usuario", "paciente", "lead"])
    return dict(
        titulo="Quebre o código: a armadilha clássica do .get(chave, {})",
        enunciado=(
            f"Um dev escreveu `nome_registro(payload)` para retornar o nome em `payload[{chave!r}]['nome']` "
            "(ou `'Desconhecido'` se não existir).\n\n"
            f"**Seu desafio:** envie um dicionário válido (ex.: `{{{chave!r}: ...}}`) que faça o código abaixo "
            "**quebrar com exceção** ou devolver resposta errada!"
        ),
        modo_quebrar="args",
        funcao_quebrar="nome_registro",
        placeholder_quebrar=f"Ex.: {{{chave!r}: None}}",
        codigo_inicial=(
            "def nome_registro(payload):\n"
            f"    item = payload.get({chave!r}, {{}})\n"
            "    return item.get('nome', 'Desconhecido')\n"
        ),
        solucao=(
            "def nome_registro(payload):\n"
            f"    item = payload.get({chave!r}) or {{}}\n"
            "    if not isinstance(item, dict):\n"
            "        return 'Desconhecido'\n"
            "    return item.get('nome') or 'Desconhecido'\n"
        ),
        testes=[{"entrada": f"{{{chave!r}: None}}"}],
        testes_visiveis=0,
        dicas=[
            f"`.get({chave!r}, {{}})` só usa `{{}}` quando a chave `{chave!r}` **não existe** no dicionário.",
            f"O que acontece se a chave `{chave!r}` existir, mas o valor vindo do JSON for `None` (`null`)?",
        ],
        explicacao=(
            f"Com `{{{chave!r}: None}}`, `payload.get({chave!r}, {{}})` devolve `None`, e `None.get('nome')` explode com `AttributeError`. "
            f"Use `(payload.get({chave!r}) or {{}})`!"
        ),
    )
