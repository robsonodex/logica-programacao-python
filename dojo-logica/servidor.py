"""
Dojo de Lógica — servidor local (só biblioteca padrão do Python).

Execute:  python servidor.py      (ou dê dois cliques em iniciar.bat)
O navegador abre sozinho em http://localhost:8765
"""

import json
import mimetypes
import os
import socket
import sys
import threading
import traceback
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)

from motor import executor, progresso  # noqa: E402
from motor.conceitos import CONCEITOS  # noqa: E402

PASTA_WEB = os.path.join(RAIZ, "web")
PORTA_PADRAO = 8765


class Manipulador(BaseHTTPRequestHandler):
    server_version = "DojoLogica/1.0"

    def log_message(self, fmt, *args):  # silencia o log padrão
        pass

    # --- utilidades -------------------------------------------------------
    def _json(self, dados, status=200):
        corpo = json.dumps(dados, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(corpo)

    def _corpo(self):
        n = int(self.headers.get("Content-Length") or 0)
        if not n:
            return {}
        return json.loads(self.rfile.read(n).decode("utf-8"))

    def _arquivo(self, caminho):
        caminho = os.path.normpath(os.path.join(PASTA_WEB, caminho.lstrip("/")))
        if not caminho.startswith(PASTA_WEB) or not os.path.isfile(caminho):
            self.send_error(404)
            return
        tipo = mimetypes.guess_type(caminho)[0] or "application/octet-stream"
        if tipo.startswith("text/") or tipo.endswith("javascript"):
            tipo += "; charset=utf-8"
        with open(caminho, "rb") as f:
            corpo = f.read()
        self.send_response(200)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(corpo)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(corpo)

    # --- rotas ------------------------------------------------------------
    def do_GET(self):
        url = urlparse(self.path)
        q = parse_qs(url.query)
        try:
            if url.path == "/api/estado":
                return self._json(progresso.estado(q.get("data", [None])[0]))
            if url.path == "/api/questao":
                return self._json(progresso.questao(q["id"][0]))
            if url.path == "/api/conceitos":
                return self._json(CONCEITOS)
            if url.path == "/api/progresso":
                return self._json(progresso.carregar())
            if url.path in ("/", "/index.html"):
                return self._arquivo("index.html")
            return self._arquivo(url.path)
        except Exception as e:  # noqa: BLE001
            traceback.print_exc()
            return self._json({"falha": f"{type(e).__name__}: {e}"}, 500)

    def do_POST(self):
        url = urlparse(self.path)
        try:
            c = self._corpo()
            rotas = {
                "/api/executar": lambda: executor.executar(c.get("codigo", ""), c.get("entrada", ""), "", eco=True),
                "/api/rastrear": lambda: executor.rastrear(c.get("codigo", ""), c.get("entrada", "")),
                "/api/verificar": lambda: progresso.verificar(c["id"], c.get("codigo", ""), c.get("resposta")),
                "/api/dica": lambda: progresso.revelar_dica(c["id"]),
                "/api/solucao": lambda: progresso.revelar_solucao(c["id"]),
                "/api/rascunho": lambda: progresso.salvar_rascunho(c["id"], c.get("codigo", "")) or {"ok": True},
                "/api/estagio": lambda: progresso.mudar_estagio(int(c["estagio"])),
                "/api/regenerar": lambda: progresso.regenerar_hoje(),
                "/api/treino-extra": lambda: progresso.treino_extra(progresso.hoje()),
                "/api/progresso": lambda: progresso.importar(c),
            }
            if url.path not in rotas:
                return self._json({"falha": "rota desconhecida"}, 404)
            return self._json(rotas[url.path]())
        except Exception as e:  # noqa: BLE001
            traceback.print_exc()
            return self._json({"falha": f"{type(e).__name__}: {e}"}, 500)


def porta_livre(inicial):
    for p in range(inicial, inicial + 30):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", p)) != 0:
                return p
    return inicial


def main():
    porta = porta_livre(int(os.environ.get("DOJO_PORTA", PORTA_PADRAO)))
    servidor = ThreadingHTTPServer(("127.0.0.1", porta), Manipulador)
    url = f"http://localhost:{porta}"
    print("=" * 52)
    print("  🥋  DOJO DE LÓGICA — prática diária de Python")
    print(f"  Abra no navegador: {url}")
    print("  Para encerrar: feche esta janela ou Ctrl+C")
    print("=" * 52)
    if "--sem-navegador" not in sys.argv:
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nAté amanhã! Constância vence intensidade. 👋")


if __name__ == "__main__":
    main()
