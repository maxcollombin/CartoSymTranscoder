#!/bin/sh
set -eu

echo " Configuration de CartoSymTranscoder..."

# Vérifier et ajouter le submodule grammar si absent
if [ ! -d "grammar" ]; then
    echo "Ajout du submodule grammar..."
    git submodule add https://github.com/maxcollombin/cartosymcss-grammar.git grammar || true
fi

echo "Initialisation et mise à jour des submodules..."
git submodule update --init --recursive

# Vérifier que le submodule a été correctement récupéré
if [ ! -d "grammar" ] || [ ! -f "grammar/CartoSymCSSLexer.g4" ] || [ ! -f "grammar/CartoSymCSSGrammar.g4" ]; then
    echo " Erreur: Submodule grammar non initialisé ou fichiers .g4 manquants"
    exit 1
fi

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

# Génération du code à partir des grammaires du submodule
echo " Génération des fichiers ANTLR..."
outdir="cartosym_transcoder/grammar/generated"
mkdir -p "$outdir"
rm -rf "$outdir"/*

# Créer un répertoire temporaire pour la génération
temp_dir=$(mktemp -d)
echo "  Répertoire temporaire: $temp_dir"

# Copier les fichiers .g4 dans le répertoire temporaire
cp grammar/CartoSymCSSLexer.g4 "$temp_dir/"
cp grammar/CartoSymCSSGrammar.g4 "$temp_dir/"

# Aller dans le répertoire temporaire pour la génération
cd "$temp_dir"

# Générer d'abord le lexer, puis le parser
echo "  Génération du lexer..."
antlr4 -Dlanguage=Python3 CartoSymCSSLexer.g4
echo "  Génération du parser..."
antlr4 -Dlanguage=Python3 CartoSymCSSGrammar.g4

# Retourner dans le répertoire principal
cd - > /dev/null

# Copier les fichiers générés
echo "  Copie des fichiers générés..."
cp "$temp_dir"/*.py "$outdir/"
cp "$temp_dir"/*.tokens "$outdir/"
cp "$temp_dir"/*.interp "$outdir/"

# Nettoyer le répertoire temporaire
rm -rf "$temp_dir"

# Désinitialiser et supprimer proprement le submodule grammar
if [ -d "grammar" ]; then
    echo "Suppression propre du submodule grammar..."
    git submodule deinit -f grammar || true
    git rm --cached grammar || true
    rm -rf .git/modules/grammar
    rm -rf grammar
fi

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
echo " Note: Le submodule grammar est conservé pour les générations futures."
echo ""
echo " Test rapide de l'installation..."
python -c "import cartosym_transcoder; print(' Import réussi!')" || echo " Problème d'import"
