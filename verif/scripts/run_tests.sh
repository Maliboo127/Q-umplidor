#!/usr/bin/env bash
# run_tests.sh — Script inicial de verificación (RNF-20).
# Ejecuta todas las pruebas automatizadas con un único comando.
#
# Uso:
#   bash verif/scripts/run_tests.sh

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

echo "== Q-umplidor: ejecutando pruebas automatizadas =="
echo "Commit: $(git rev-parse --short HEAD 2>/dev/null || echo 'sin-git')"
echo "Fecha:  $(date)"
echo ""

python3 -m pip install --quiet pytest --break-system-packages 2>/dev/null || \
    python3 -m pip install --quiet pytest 2>/dev/null || true

python3 -m pytest tests/ -v

echo ""
echo "== Fin de la verificación =="
