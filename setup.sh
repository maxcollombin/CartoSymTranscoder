#!/bin/sh
set -eu

# Sauvegarder le répertoire de travail (chemin absolu)
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

GRAMMAR_REPO="https://github.com/maxcollombin/cartosymcss-grammar.git"

echo " Configuration de CartoSymTranscoder..."

# Création de l'environnement virtuel si nécessaire
if [ ! -d "CartoSym" ]; then
    echo " Création de l'environnement virtuel..."
    python3 -m venv CartoSym
fi

echo " Activation de l'environnement virtuel..."
. CartoSym/bin/activate

# Vérifier que nous sommes bien dans l'environnement virtuel
if [ -z "${VIRTUAL_ENV:-}" ]; then
    echo " Erreur: L'environnement virtuel n'a pas été activé correctement"
    exit 1
fi
echo "   Environnement virtuel actif: $VIRTUAL_ENV"

echo "Installation des dépendances Python..."

# Installation des dépendances ANTLR (runtime + tools pour génération)
pip install -q antlr4-python3-runtime antlr4-tools
# Installation du validateur JSON
pip install -q jsonschema
# Installation de pytest pour les tests unitaires
pip install -q pytest

# Génération du code à partir des grammaires
echo " Génération des fichiers ANTLR..."
outdir="$PROJECT_DIR/cartosym_transcoder/grammar/generated"
mkdir -p "$outdir"
rm -rf "$outdir"/*

# Créer un répertoire temporaire et cloner la grammaire dedans
temp_dir=$(mktemp -d)
trap 'rm -rf "$temp_dir"' EXIT
echo "  Clonage de la grammaire..."
git clone --quiet --depth 1 "$GRAMMAR_REPO" "$temp_dir/grammar"
cp "$temp_dir/grammar/"*.g4 "$temp_dir/"

# Générer d'abord le lexer, puis le parser (sans changer de répertoire)
echo "  Génération du lexer..."
antlr4 -Dlanguage=Python3 -o "$temp_dir" "$temp_dir/CartoSymCSSLexer.g4"
echo "  Génération du parser..."
antlr4 -Dlanguage=Python3 -o "$temp_dir" "$temp_dir/CartoSymCSSGrammar.g4"

# Copier les fichiers générés
echo "  Copie des fichiers générés..."
cp "$temp_dir"/*.py "$outdir/"
cp "$temp_dir"/*.tokens "$outdir/"
cp "$temp_dir"/*.interp "$outdir/"

# Création de __init__.py
cat > "$outdir/__init__.py" << 'EOF'
from .CartoSymCSSLexer import CartoSymCSSLexer
from .CartoSymCSSGrammar import CartoSymCSSGrammar
from .CartoSymCSSGrammarListener import CartoSymCSSGrammarListener
__all__ = ["CartoSymCSSLexer", "CartoSymCSSGrammar", "CartoSymCSSGrammarListener"]
EOF

echo "Installation du package en mode développement..."
pip install -e .

echo "Désinstallation d'antlr4-tools (plus nécessaire)..."
pip uninstall -y antlr4-tools

echo " Setup terminé avec succès!"
echo " Environnement virtuel: CartoSym"
echo " Pour l'activer: source CartoSym/bin/activate"
echo ""
echo " Test rapide de l'installation..."
python -c "import cartosym_transcoder; print(' Import réussi!')" || echo " Problème d'import"
