"""Gera os JSON Schemas de schemas/ a partir dos modelos Pydantic.

Uso:
    python scripts/gerar_schemas.py              # regrava os arquivos
    python scripts/gerar_schemas.py --verificar  # só confere (usado no CI)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from app.modelos.evidencia import ResultadoAnalise  # noqa: E402
from app.modelos.extracao import EntradaAnalise, ExtracaoOferta, Normalizacao  # noqa: E402

MODELOS = {
    "entrada": EntradaAnalise,
    "extracao": ExtracaoOferta,
    "normalizacao": Normalizacao,
    "resultado": ResultadoAnalise,
}


def conteudo(modelo) -> str:
    return json.dumps(modelo.model_json_schema(), ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    verificar = "--verificar" in sys.argv
    desatualizados = []
    for nome, modelo in MODELOS.items():
        caminho = RAIZ / "schemas" / f"{nome}.schema.json"
        novo = conteudo(modelo)
        if verificar:
            if not caminho.exists() or caminho.read_text(encoding="utf-8") != novo:
                desatualizados.append(caminho.name)
        else:
            caminho.write_text(novo, encoding="utf-8")
            print(f"gerado {caminho.relative_to(RAIZ)}")
    if desatualizados:
        print("Schemas desatualizados: " + ", ".join(desatualizados))
        print("Rode: python scripts/gerar_schemas.py")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
