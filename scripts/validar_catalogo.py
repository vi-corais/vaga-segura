"""Valida catalogo/evidencias.yaml contra app/modelos/catalogo.py.

Uso:
    python scripts/validar_catalogo.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from app.modelos.catalogo import Catalogo  # noqa: E402


def carregar(caminho: Path = RAIZ / "catalogo" / "evidencias.yaml") -> Catalogo:
    with caminho.open(encoding="utf-8") as f:
        return Catalogo(**yaml.safe_load(f))


if __name__ == "__main__":
    catalogo = carregar()
    print(f"Catálogo {catalogo.versao} válido: {len(catalogo.evidencias)} evidências, {len(catalogo.combinacoes)} combinação(ões)")
