#!/bin/bash
# Script para sincronizar DESTRABAR_BLTOUCH desde el submodule
# Uso: ./scripts/sync-destrabe-bltouch.sh

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

SUBMODULE_SRC="$REPO_ROOT/macros/destrabe-bltouch-src/DESTRABAR_BLTOUCH.cfg"
DEST_MACROS="$REPO_ROOT/macros/DESTRABAR_BLTOUCH.cfg"
DEST_CONFIG="$REPO_ROOT/printer_data/config/macros/DESTRABAR_BLTOUCH.cfg"

echo "📡 Sincronizando DESTRABAR_BLTOUCH desde submodule..."

# Actualizar submodule
cd "$REPO_ROOT"
git submodule update --remote macros/destrabe-bltouch-src
echo "✓ Submodule actualizado"

# Copiar archivo
if [ -f "$SUBMODULE_SRC" ]; then
    cp "$SUBMODULE_SRC" "$DEST_MACROS" 2>/dev/null || true
    cp "$SUBMODULE_SRC" "$DEST_CONFIG" 2>/dev/null || true
    echo "✓ DESTRABAR_BLTOUCH sincronizado"
    echo "  Versión: $(grep -m1 'description:' "$SUBMODULE_SRC" | sed 's/.*description: //')"
else
    echo "❌ Error: archivo no encontrado en $SUBMODULE_SRC"
    exit 1
fi

echo "✅ Sincronización completada"
