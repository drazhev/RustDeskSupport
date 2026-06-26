#!/usr/bin/env bash
# Сборка на rustdesk-drazhev.exe чрез PyInstaller (изпълнява се от GitHub Actions на Windows)

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ASSETS="$PROJECT_ROOT/assets"
SRC="$PROJECT_ROOT/src"
BUILD="$PROJECT_ROOT/build"

if [ ! -f "$ASSETS/rustdesk.exe" ]; then
    echo "ГРЕШКА: Липсва assets/rustdesk.exe"
    exit 1
fi

mkdir -p "$BUILD"

pyinstaller \
    --onefile \
    --windowed \
    --name "rustdesk-drazhev" \
    --distpath "$BUILD" \
    --workpath "$BUILD/.pyinstaller-work" \
    --specpath "$BUILD" \
    --add-data "$ASSETS/rustdesk.exe;." \
    --icon "$ASSETS/icon.ico" \
    "$SRC/launcher.py"

echo "Готово: $BUILD/rustdesk-drazhev.exe"
