/* global importScripts, loadPyodide */
const PYODIDE_INDEX = "https://cdn.jsdelivr.net/pyodide/v0.27.7/full/";

let pyodide = null;
let initPromise = null;

function notify(type, payload) {
  self.postMessage({ type, ...payload });
}

async function initEngine(bundleUrl, initialProgressJson) {
  if (pyodide) return pyodide;
  if (initPromise) return initPromise;

  initPromise = (async () => {
    try {
      notify("status", { stage: "loading", message: "Baixando interpretador Python..." });
      importScripts(`${PYODIDE_INDEX}pyodide.js`);

      const py = await loadPyodide({ indexURL: PYODIDE_INDEX });

      notify("status", { stage: "loading", message: "Carregando módulos, 22 estágios e analisador..." });
      const resp = await fetch(bundleUrl, { cache: "no-store" });
      if (!resp.ok) {
        throw new Error(`Falha ao carregar o pacote de exercícios (HTTP ${resp.status}).`);
      }
      const bundle = await resp.json();

      py.FS.mkdirTree("/dojo/dados");
      for (const [relPath, content] of Object.entries(bundle)) {
        const fullPath = `/dojo/${relPath}`;
        const lastSlash = fullPath.lastIndexOf("/");
        if (lastSlash > 0) {
          py.FS.mkdirTree(fullPath.slice(0, lastSlash));
        }
        py.FS.writeFile(fullPath, content, { encoding: "utf8" });
      }

      if (initialProgressJson) {
        py.FS.writeFile("/dojo/dados/progresso.json", initialProgressJson, { encoding: "utf8" });
      }

      await py.runPythonAsync(`
import json
import os
import sys

if "/dojo" not in sys.path:
    sys.path.insert(0, "/dojo")

from motor import executor, progresso
from motor.conceitos import CONCEITOS

def _dojo_dispatch(method, path, query_json, body_json):
    try:
        q = json.loads(query_json or "{}")
        c = json.loads(body_json or "{}")
        if method == "GET":
            if path == "/api/estado":
                res = progresso.estado(q.get("data"))
            elif path == "/api/questao":
                res = progresso.questao(q["id"])
            elif path == "/api/conceitos":
                res = CONCEITOS
            elif path == "/api/progresso":
                res = progresso.carregar()
            else:
                return json.dumps({"__status": 404, "dados": {"falha": "rota desconhecida"}}, ensure_ascii=False)
        else:
            rotas = {
                "/api/executar": lambda: executor.executar(c.get("codigo", ""), c.get("entrada", ""), "", eco=True),
                "/api/rastrear": lambda: executor.rastrear(c.get("codigo", ""), c.get("entrada", "")),
                "/api/verificar": lambda: progresso.verificar(c["id"], c.get("codigo", ""), c.get("resposta")),
                "/api/dica": lambda: progresso.revelar_dica(c["id"]),
                "/api/solucao": lambda: progresso.revelar_solucao(c["id"]),
                "/api/rascunho": lambda: progresso.salvar_rascunho(c["id"], c.get("codigo", "")) or {"ok": True},
                "/api/estagio": lambda: progresso.mudar_estagio(int(c["estagio"])),
                "/api/desbloquear": lambda: progresso.desbloquear(c.get("estagio"), c.get("modo_livre")),
                "/api/regenerar": lambda: progresso.regenerar_hoje(),
                "/api/treino-extra": lambda: progresso.treino_extra(progresso.hoje()),
                "/api/treino-bugs": lambda: progresso.treino_bugs(),
                "/api/padrao": lambda: progresso.salvar_padrao(
                    c["id"], c.get("contrato", ""), c.get("edge_cases", ""), c.get("plano", ""), c.get("feynman", "")
                ),
                "/api/padrao/excluir": lambda: progresso.excluir_padrao(c["id"]),
                "/api/simulado/iniciar": lambda: progresso.iniciar_simulado(
                    c.get("trilha", "entrevista"), int(c.get("duracao_min", 30))
                ),
                "/api/simulado/avaliar": lambda: progresso.avaliar_simulado(
                    c["id"], c.get("respostas", []), int(c.get("duracao_usada_seg", 0))
                ),
                "/api/progresso": lambda: progresso.importar(c),
            }
            if path not in rotas:
                return json.dumps({"__status": 404, "dados": {"falha": "rota desconhecida"}}, ensure_ascii=False)
            res = rotas[path]()

        prog_txt = None
        if os.path.exists(progresso.ARQ_PROGRESSO):
            with open(progresso.ARQ_PROGRESSO, encoding="utf-8") as f:
                prog_txt = f.read()
        return json.dumps({"__status": 200, "dados": res, "progresso": prog_txt}, ensure_ascii=False)
    except ValueError as e:
        return json.dumps({"__status": 400, "dados": {"falha": str(e)}}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"__status": 500, "dados": {"falha": f"{type(e).__name__}: {e}"}}, ensure_ascii=False)
`);

      pyodide = py;
      notify("status", { stage: "ready", message: "Ambiente Python pronto." });
      return py;
    } catch (err) {
      initPromise = null;
      throw err;
    }
  })();

  return initPromise;
}

self.onmessage = async (event) => {
  const msg = event.data || {};
  const { id, action } = msg;

  try {
    if (action === "init") {
      await initEngine(msg.bundleUrl, msg.initialProgress || "");
      self.postMessage({ type: "response", id, ok: true, payload: { ready: true } });
      return;
    }

    if (action === "request") {
      const py = await initEngine(msg.bundleUrl, msg.initialProgress || "");
      const dispatch = py.globals.get("_dojo_dispatch");
      const raw = dispatch(
        msg.method || "GET",
        msg.path || "/",
        JSON.stringify(msg.query || {}),
        msg.body || "{}"
      );
      const parsed = JSON.parse(raw);
      self.postMessage({ type: "response", id, ok: true, payload: parsed });
      return;
    }

    self.postMessage({ type: "response", id, ok: false, error: "Ação desconhecida no worker." });
  } catch (err) {
    self.postMessage({
      type: "response",
      id,
      ok: false,
      error: err && err.message ? err.message : String(err),
    });
  }
};
