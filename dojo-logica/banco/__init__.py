"""Carrega automaticamente todos os arquivos banco/estagio_XX.py."""

import importlib
import pkgutil

from .base import REGISTRO, TIPOS, Modelo, executar_referencia  # noqa: F401

for _info in sorted(pkgutil.iter_modules(__path__), key=lambda m: m.name):
    if _info.name.startswith("estagio_"):
        importlib.import_module(f"{__name__}.{_info.name}")


def modelos_do_estagio(n: int) -> list[Modelo]:
    return [m for m in REGISTRO.values() if m.estagio == n]
