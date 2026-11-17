import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const raiz = path.resolve(__dirname, "..");
const pastaDojo = path.join(raiz, "dojo-logica");
const pastaWeb = path.join(pastaDojo, "web");
const pastaDist = path.join(raiz, "dist");

function copiarDir(origem, destino) {
  fs.mkdirSync(destino, { recursive: true });
  for (const entrada of fs.readdirSync(origem, { withFileTypes: true })) {
    const src = path.join(origem, entrada.name);
    const dst = path.join(destino, entrada.name);
    if (entrada.isDirectory()) {
      copiarDir(src, dst);
    } else {
      fs.copyFileSync(src, dst);
    }
  }
}

function coletarPython(pastaBase, relPrefix, destinoObj) {
  for (const entrada of fs.readdirSync(pastaBase, { withFileTypes: true })) {
    if (entrada.name === "__pycache__" || entrada.name.startsWith(".")) continue;
    const caminhoCompleto = path.join(pastaBase, entrada.name);
    const caminhoRel = `${relPrefix}/${entrada.name}`;
    if (entrada.isDirectory()) {
      coletarPython(caminhoCompleto, caminhoRel, destinoObj);
    } else if (entrada.name.endsWith(".py")) {
      destinoObj[caminhoRel] = fs.readFileSync(caminhoCompleto, "utf8");
    }
  }
}

fs.rmSync(pastaDist, { recursive: true, force: true });
copiarDir(pastaWeb, pastaDist);

// Ativa o modo estático (Pyodide no navegador) no bundle publicado
fs.writeFileSync(
  path.join(pastaDist, "runtime-config.js"),
  'window.__DOJO_MODO__ = "static";\n',
  "utf8"
);

const bundle = {};
coletarPython(path.join(pastaDojo, "banco"), "banco", bundle);
coletarPython(path.join(pastaDojo, "motor"), "motor", bundle);

const totalArquivos = Object.keys(bundle).length;
if (totalArquivos === 0) {
  throw new Error("Nenhum arquivo Python encontrado em banco/ ou motor/.");
}

const bundlePath = path.join(pastaDist, "dojo_bundle.json");
fs.writeFileSync(bundlePath, JSON.stringify(bundle), "utf8");

const bytes = fs.statSync(bundlePath).size;
console.log(`Build estático gerado em ${pastaDist}`);
console.log(`Bundle Python: ${totalArquivos} arquivos (${(bytes / 1024).toFixed(1)} KB)`);
