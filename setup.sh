#!/bin/sh
set -eu

# Sauvegarder le répertoire de travail (chemin absolu)
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

echo " Configuration de CartoSymTranscoder..."

if ! command -v uv >/dev/null 2>&1; then
    echo " Erreur: uv est requis mais introuvable. Voir https://docs.astral.sh/uv/getting-started/installation/"
    exit 1
fi

echo " Initialisation du submodule de grammaire (vendor/cartosymcss-grammar)..."
git submodule update --init --recursive

echo " Installation des dépendances Python (uv sync)..."
uv sync --all-extras

echo " Setup terminé avec succès!"
echo " Environnement virtuel: .venv (géré par uv)"
echo " Pour l'activer: source .venv/bin/activate"
echo " Ou lancer les commandes directement via: uv run <commande>"
echo ""
echo " Test rapide de l'installation..."
uv run python -c "import cartosym_transcoder; print(' Import réussi!')" || echo " Problème d'import"
