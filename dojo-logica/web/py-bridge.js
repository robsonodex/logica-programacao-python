(() => {
  "use strict";

  const STORAGE_KEY = "dojo_logica_progresso_v1";
  const INIT_TIMEOUT_MS = 90000;

  let worker = null;
  let workerReady = false;
  let initInFlight = null;
  let reqSeq = 0;
  let pending = new Map();
  let queue = Promise.resolve();
  let statusListeners = new Set();
  let currentStatus = { stage: "idle", message: "" };

  function emitStatus(next) {
    currentStatus = next;
    for (const fn of statusListeners) {
      try {
        fn(next);
      } catch {
        // Ignora erro de listener isolado
      }
    }
  }

  function isStatic() {
    return window.__DOJO_MODO__ === "static";
  }

  function readSavedProgress() {
    try {
      return window.localStorage.getItem(STORAGE_KEY) || "";
    } catch {
      return "";
    }
  }

  function saveProgressText(txt) {
    if (!txt) return;
    try {
      window.localStorage.setItem(STORAGE_KEY, txt);
    } catch {
      // Ignora erro caso localStorage esteja bloqueado
    }
  }

  function resetWorker(reasonMessage) {
    if (worker) {
      try {
        worker.terminate();
      } catch {
        // Ignore
      }
    }
    worker = null;
    workerReady = false;
    initInFlight = null;
    for (const [id, entry] of pending.entries()) {
      clearTimeout(entry.timer);
      entry.reject(new Error(reasonMessage || "Execução reiniciada."));
      pending.delete(id);
    }
  }

  function ensureWorker() {
    if (worker) return worker;
    worker = new Worker("/py-worker.js");
    workerReady = false;

    worker.onmessage = (event) => {
      const msg = event.data || {};
      if (msg.type === "status") {
        if (msg.stage === "ready") workerReady = true;
        emitStatus({ stage: msg.stage, message: msg.message || "" });
        return;
      }
      if (msg.type === "response") {
        const entry = pending.get(msg.id);
        if (!entry) return;
        clearTimeout(entry.timer);
        pending.delete(msg.id);
        if (msg.ok) {
          entry.resolve(msg.payload);
        } else {
          entry.reject(new Error(msg.error || "Falha no motor Python do navegador."));
        }
      }
    };

    worker.onerror = (err) => {
      const msg = err && err.message ? err.message : "Erro inesperado no ambiente Python.";
      emitStatus({ stage: "error", message: msg });
      resetWorker(msg);
    };

    return worker;
  }

  function sendToWorker(payload, timeoutMs) {
    return new Promise((resolve, reject) => {
      const w = ensureWorker();
      const id = ++reqSeq;
      const timer = setTimeout(() => {
        pending.delete(id);
        resetWorker("Tempo limite excedido na execução.");
        reject(new Error("TIMEOUT_EXECUCAO"));
      }, timeoutMs);

      pending.set(id, { resolve, reject, timer });
      w.postMessage({ id, ...payload });
    });
  }

  function bundleUrl() {
    return new URL("/dojo_bundle.json", window.location.origin).href;
  }

  async function init() {
    if (!isStatic() || workerReady) return;
    if (initInFlight) return initInFlight;
    initInFlight = sendToWorker(
      {
        action: "init",
        bundleUrl: bundleUrl(),
        initialProgress: readSavedProgress(),
      },
      INIT_TIMEOUT_MS
    )
      .then((res) => {
        workerReady = true;
        emitStatus({ stage: "ready", message: "Ambiente Python pronto." });
        return res;
      })
      .finally(() => {
        initInFlight = null;
      });
    return initInFlight;
  }

  function parseUrl(url) {
    const parsed = new URL(url, window.location.origin);
    const query = {};
    for (const [k, v] of parsed.searchParams.entries()) {
      query[k] = v;
    }
    return { path: parsed.pathname, query };
  }

  function timeoutParaRota(path) {
    if (path === "/api/verificar") return 25000;
    if (path === "/api/executar" || path === "/api/rastrear") return 12000;
    return 10000;
  }

  async function executeRequest(url, opcoes = {}) {
    if (!workerReady) {
      await init();
    }
    const { path, query } = parseUrl(url);
    const method = (opcoes.method || "GET").toUpperCase();
    const body = typeof opcoes.body === "string" ? opcoes.body : "{}";

    try {
      const res = await sendToWorker(
        {
          action: "request",
          bundleUrl: bundleUrl(),
          initialProgress: readSavedProgress(),
          method,
          path,
          query,
          body,
        },
        timeoutParaRota(path)
      );

      if (res && res.progresso) {
        saveProgressText(res.progresso);
      }

      const status = res && res.__status ? res.__status : 200;
      const dados = res && "dados" in res ? res.dados : res;
      if (status >= 400 || (dados && dados.falha)) {
        throw new Error((dados && dados.falha) || `Erro ${status}`);
      }
      return dados;
    } catch (err) {
      if (err && err.message === "TIMEOUT_EXECUCAO") {
        const explicacao =
          "Seu programa demorou demais. Confira se há um laço infinito (`while` cuja condição nunca fica falsa).";
        if (path === "/api/executar") {
          return {
            saida: "",
            tempo: 5.0,
            erro: { tipo: "Tempo", mensagem: "O programa passou de 5 segundos.", linha: null, texto: "", explicacao },
          };
        }
        if (path === "/api/rastrear") {
          return {
            passos: [],
            limite: true,
            erro: { tipo: "Tempo", mensagem: "O programa passou do limite de tempo.", linha: null, texto: "", explicacao },
          };
        }
        if (path === "/api/verificar") {
          return {
            passou: false,
            tentativas: 0,
            xp: 0,
            resultados: [
              {
                n: 1,
                entrada: "",
                chamada: "",
                obtido: "",
                esperado: "",
                status: "erro",
                erro: { tipo: "Tempo", mensagem: "O programa passou de 5 segundos.", linha: null, texto: "", explicacao },
              },
            ],
          };
        }
        throw new Error("A operação demorou demais e foi interrompida.");
      }
      throw err;
    }
  }

  function request(url, opcoes = {}) {
    const run = queue.then(() => executeRequest(url, opcoes));
    queue = run.catch(() => {});
    return run;
  }

  function onStatus(fn) {
    statusListeners.add(fn);
    fn(currentStatus);
    return () => statusListeners.delete(fn);
  }

  async function retryInit() {
    resetWorker("Reiniciando ambiente Python...");
    return init();
  }

  window.DojoBridge = {
    isStatic,
    init,
    retryInit,
    request,
    onStatus,
  };
})();
