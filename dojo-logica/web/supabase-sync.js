(() => {
  "use strict";

  const SESSION_KEY = "dojo_supabase_session_v1";
  let session = null;
  let syncTimer = null;
  let listeners = new Set();
  let syncState = { configured: false, loggedIn: false, email: "", status: "local", detail: "" };

  function getConfig() {
    const cfg = window.__DOJO_SUPABASE__ || {};
    const url = (cfg.url || "").replace(/\/+$/, "");
    const key = (cfg.key || "").trim();
    return { url, key, ok: Boolean(url && key) };
  }

  function emit() {
    const cfg = getConfig();
    syncState = {
      ...syncState,
      configured: cfg.ok,
      loggedIn: Boolean(session && session.access_token && session.user),
      email: session && session.user ? session.user.email || "" : "",
    };
    for (const fn of listeners) {
      try {
        fn({ ...syncState });
      } catch {
        // Ignore
      }
    }
  }

  function saveSession(s) {
    session = s;
    try {
      if (s) window.localStorage.setItem(SESSION_KEY, JSON.stringify(s));
      else window.localStorage.removeItem(SESSION_KEY);
    } catch {
      // Ignore
    }
    emit();
  }

  function loadSession() {
    try {
      const raw = window.localStorage.getItem(SESSION_KEY);
      if (raw) session = JSON.parse(raw);
    } catch {
      session = null;
    }
    emit();
  }

  async function authFetch(path, body, withBearer = false) {
    const cfg = getConfig();
    if (!cfg.ok) throw new Error("Supabase não configurado neste ambiente.");
    const headers = {
      apikey: cfg.key,
      "Content-Type": "application/json",
    };
    if (withBearer && session && session.access_token) {
      headers.Authorization = `Bearer ${session.access_token}`;
    }
    const resp = await fetch(`${cfg.url}${path}`, {
      method: "POST",
      headers,
      body: body !== undefined ? JSON.stringify(body) : undefined,
    });
    const text = await resp.text();
    let data = {};
    try {
      data = text ? JSON.parse(text) : {};
    } catch {
      data = { message: text };
    }
    if (!resp.ok) {
      const msg = data.error_description || data.msg || data.message || `Erro HTTP ${resp.status}`;
      throw new Error(msg);
    }
    return data;
  }

  async function ensureValidToken() {
    if (!session || !session.access_token) return false;
    const nowSec = Math.floor(Date.now() / 1000);
    if (session.expires_at && session.expires_at - nowSec > 60) {
      return true;
    }
    if (!session.refresh_token) return false;
    try {
      const data = await authFetch("/auth/v1/token?grant_type=refresh_token", {
        refresh_token: session.refresh_token,
      });
      saveSession({
        access_token: data.access_token,
        refresh_token: data.refresh_token || session.refresh_token,
        expires_at: data.expires_at || nowSec + (data.expires_in || 3600),
        user: data.user || session.user,
      });
      return true;
    } catch {
      saveSession(null);
      return false;
    }
  }

  async function restFetch(path, options = {}) {
    const cfg = getConfig();
    if (!cfg.ok) return null;
    const ok = await ensureValidToken();
    if (!ok) return null;

    const headers = {
      apikey: cfg.key,
      Authorization: `Bearer ${session.access_token}`,
      "Content-Type": "application/json",
      ...(options.headers || {}),
    };
    const resp = await fetch(`${cfg.url}${path}`, {
      ...options,
      headers,
    });
    const text = await resp.text();
    let data = null;
    try {
      data = text ? JSON.parse(text) : null;
    } catch {
      data = text;
    }
    if (!resp.ok) {
      const errMsg =
        (data && (data.message || data.hint || data.error)) || `Erro Supabase HTTP ${resp.status}`;
      const err = new Error(errMsg);
      err.status = resp.status;
      err.code = data && data.code;
      throw err;
    }
    return data;
  }

  function friendlyTableError(err) {
    if (!err) return "";
    if (err.code === "42P01" || err.status === 404 || String(err.message).includes("dojo_progresso")) {
      return "Execute o SQL 001_dojo_inicial.sql no SQL Editor do Supabase para ativar as tabelas.";
    }
    return err.message || "Falha na sincronização com a nuvem.";
  }

  async function ensureProfile() {
    if (!session || !session.user) return;
    const nome = (session.user.user_metadata && session.user.user_metadata.nome) || "";
    try {
      await restFetch("/rest/v1/dojo_perfis?on_conflict=user_id", {
        method: "POST",
        headers: { Prefer: "resolution=merge-duplicates,return=minimal" },
        body: JSON.stringify({ user_id: session.user.id, nome }),
      });
    } catch {
      // Silencioso caso tabela ainda não exista; erro principal aparece no sync de progresso
    }
  }

  async function signUp(email, password, nome = "") {
    const data = await authFetch("/auth/v1/signup", {
      email: email.trim(),
      password,
      data: { nome: nome.trim() },
    });
    if (data.access_token && data.user) {
      saveSession({
        access_token: data.access_token,
        refresh_token: data.refresh_token,
        expires_at: data.expires_at || Math.floor(Date.now() / 1000) + (data.expires_in || 3600),
        user: data.user,
      });
      await ensureProfile();
      return { needsConfirmation: false, user: data.user };
    }
    return { needsConfirmation: true, user: data.user || null };
  }

  async function signIn(email, password) {
    const data = await authFetch("/auth/v1/token?grant_type=password", {
      email: email.trim(),
      password,
    });
    saveSession({
      access_token: data.access_token,
      refresh_token: data.refresh_token,
      expires_at: data.expires_at || Math.floor(Date.now() / 1000) + (data.expires_in || 3600),
      user: data.user,
    });
    await ensureProfile();
    return data.user;
  }

  async function sendPasswordReset(email) {
    await authFetch("/auth/v1/recover", { email: email.trim() });
  }

  async function signOut() {
    try {
      if (session && session.access_token) {
        await authFetch("/auth/v1/logout", {}, true);
      }
    } catch {
      // Mesmo se o token já expirou, encerra localmente
    }
    clearTimeout(syncTimer);
    syncState.status = "local";
    syncState.detail = "";
    saveSession(null);
  }

  async function pullAndMerge(apiFn) {
    if (!session || !session.user) return { changed: false };
    syncState.status = "syncing";
    syncState.detail = "Sincronizando com a nuvem...";
    emit();

    try {
      const uid = encodeURIComponent(session.user.id);
      const rows = await restFetch(`/rest/v1/dojo_progresso?user_id=eq.${uid}&select=dados,xp,atualizado_em`);
      const localProg = await apiFn("/api/progresso");

      if (!rows || !rows.length || !rows[0].dados || !Object.keys(rows[0].dados).length) {
        await pushProgressNow(localProg);
        return { changed: false, direction: "uploaded" };
      }

      const cloudRow = rows[0];
      const cloudProg = cloudRow.dados;
      const cloudXp = Number(cloudProg.xp || cloudRow.xp || 0);
      const localXp = Number(localProg.xp || 0);
      const cloudTs = String(cloudProg.atualizado_em || cloudRow.atualizado_em || "");
      const localTs = String(localProg.atualizado_em || "");

      const cloudWins = cloudXp > localXp || (cloudXp === localXp && cloudTs > localTs);
      if (cloudWins) {
        await apiFn("/api/progresso", { method: "POST", body: JSON.stringify(cloudProg) });
        syncState.status = "synced";
        syncState.detail = "Progresso carregado da nuvem.";
        emit();
        return { changed: true, direction: "downloaded" };
      }

      await pushProgressNow(localProg);
      return { changed: false, direction: "uploaded" };
    } catch (err) {
      syncState.status = "error";
      syncState.detail = friendlyTableError(err);
      emit();
      throw new Error(syncState.detail);
    }
  }

  async function pushProgressNow(progObj) {
    if (!session || !session.user || !progObj) return;
    syncState.status = "syncing";
    syncState.detail = "Salvando na nuvem...";
    emit();
    try {
      await restFetch("/rest/v1/dojo_progresso?on_conflict=user_id", {
        method: "POST",
        headers: { Prefer: "resolution=merge-duplicates,return=minimal" },
        body: JSON.stringify({
          user_id: session.user.id,
          dados: progObj,
          versao: progObj.versao || 2,
          xp: progObj.xp || 0,
          estagio_atual: progObj.estagio_atual || 1,
          estagio_max: progObj.estagio_max || 1,
        }),
      });
      syncState.status = "synced";
      syncState.detail = "Sincronizado na nuvem";
      emit();
    } catch (err) {
      syncState.status = "error";
      syncState.detail = friendlyTableError(err);
      emit();
    }
  }

  function schedulePush(apiFn) {
    if (!session || !session.user) return;
    clearTimeout(syncTimer);
    syncTimer = setTimeout(async () => {
      try {
        const prog = await apiFn("/api/progresso");
        await pushProgressNow(prog);
      } catch {
        // Silencioso em background
      }
    }, 1200);
  }

  async function syncPadrao(padrao) {
    if (!session || !session.user || !padrao) return;
    try {
      await restFetch("/rest/v1/dojo_padroes?on_conflict=user_id,questao_id", {
        method: "POST",
        headers: { Prefer: "resolution=merge-duplicates,return=minimal" },
        body: JSON.stringify({
          user_id: session.user.id,
          questao_id: padrao.questao_id,
          modelo_id: padrao.modelo_id,
          titulo: padrao.titulo,
          estagio: padrao.estagio,
          contrato: padrao.contrato || "",
          edge_cases: padrao.edge_cases || "",
          plano: padrao.plano || "",
          feynman: padrao.feynman || "",
        }),
      });
    } catch {
      // Silencioso; progresso principal ainda é sincronizado
    }
  }

  async function deletePadrao(questaoId) {
    if (!session || !session.user || !questaoId) return;
    try {
      const uid = encodeURIComponent(session.user.id);
      const qid = encodeURIComponent(questaoId);
      await restFetch(`/rest/v1/dojo_padroes?user_id=eq.${uid}&questao_id=eq.${qid}`, {
        method: "DELETE",
      });
    } catch {
      // Silencioso
    }
  }

  async function syncBug(bug) {
    if (!session || !session.user || !bug) return;
    try {
      await restFetch("/rest/v1/dojo_bugs", {
        method: "POST",
        headers: { Prefer: "return=minimal" },
        body: JSON.stringify({
          user_id: session.user.id,
          categoria: bug.categoria,
          tipo_erro: bug.tipo_erro || "",
          modelo_id: bug.modelo_id || "",
          estagio: bug.estagio || 1,
          detalhe: bug.detalhe || "",
        }),
      });
    } catch {
      // Silencioso
    }
  }

  async function syncSimulado(boletim) {
    if (!session || !session.user || !boletim) return;
    try {
      await restFetch("/rest/v1/dojo_simulados?on_conflict=user_id,simulado_local_id", {
        method: "POST",
        headers: { Prefer: "resolution=merge-duplicates,return=minimal" },
        body: JSON.stringify({
          user_id: session.user.id,
          simulado_local_id: boletim.id,
          trilha: boletim.trilha,
          duracao_seg: boletim.duracao_seg || 0,
          nota_geral: boletim.nota_geral || 0,
          nota_correcao: boletim.nota_correcao || 0,
          nota_eficiencia: boletim.nota_eficiencia || 0,
          nota_qualidade: boletim.nota_qualidade || 0,
          nota_edge_cases: boletim.nota_edge_cases || 0,
          veredito: boletim.veredito || "",
          resumo: { resolvidas: boletim.resolvidas, total: boletim.total },
        }),
      });
    } catch {
      // Silencioso
    }
  }

  function onChange(fn) {
    listeners.add(fn);
    fn({ ...syncState });
    return () => listeners.delete(fn);
  }

  loadSession();

  window.DojoCloud = {
    isConfigured: () => getConfig().ok,
    isLoggedIn: () => Boolean(session && session.access_token && session.user),
    getState: () => ({ ...syncState }),
    onChange,
    signUp,
    signIn,
    signOut,
    sendPasswordReset,
    pullAndMerge,
    schedulePush,
    pushProgressNow,
    syncPadrao,
    deletePadrao,
    syncBug,
    syncSimulado,
  };
})();
