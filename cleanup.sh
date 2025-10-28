#!/bin/bash

#!/bin/bash

# Script de nettoyage complet pour CartoSymTranscoder
# Supprime tous les fichiers intermédiaires et temporaires

echo " Nettoyage du projet CartoSymTranscoder..."

# Fonction de suppression sécurisée
safe_remove() {
    if [ -e "$1" ]; then
        echo "    Suppression: $1"
        rm -rf "$1"
    else
        echo "   Déjà supprimé: $1"
    fi
}

# Suppression des fichiers de grammaire ANTLR générés (dans le dossier grammar)
echo ""
echo " Suppression des fichiers de grammaire ANTLR générés dans grammar/..."
safe_remove "grammar/.antlr"
safe_remove "grammar/.git"
safe_remove "grammar/CartoSymCSSGrammar.interp"
safe_remove "grammar/CartoSymCSSGrammar.py"
safe_remove "grammar/CartoSymCSSGrammar.tokens"
safe_remove "grammar/CartoSymCSSGrammarListener.py"
safe_remove "grammar/CartoSymCSSLexer.interp"
safe_remove "grammar/CartoSymCSSLexer.py"
safe_remove "grammar/CartoSymCSSLexer.tokens"

# Suppression des caches Python
echo ""
echo " Suppression des caches Python..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "*.pyo" -delete 2>/dev/null || true

# Suppression de l'environnement virtuel    
echo ""
echo " Suppression de l'environnement virtuel..."
safe_remove "CartoSym"
safe_remove "venv"
safe_remove ".venv"

# Suppression des fichiers de build et distribution
echo ""
echo " Suppression des fichiers de build..."
safe_remove "build"
safe_remove "dist"
safe_remove "*.egg-info"
safe_remove "cartosym_transcoder.egg-info"

# Suppression des fichiers de log
echo ""
echo " Suppression des fichiers de log..."
safe_remove "*.log"
safe_remove "logs"

# Suppression du dossier output
echo ""
echo " Suppression du dossier output..."
if [ -d "output" ]; then
    echo "   Contenu actuel du dossier output:"
    ls -la output/
    echo "   Conservation uniquement des fichiers .cs.json finaux..."
    # On garde seulement les .cs.json qui semblent être des résultats finaux
    find output/ -name "*.tmp" -delete 2>/dev/null || true
    find output/ -name "*.debug" -delete 2>/dev/null || true
    # Supprimer les fichiers de test avec des noms temporaires
    safe_remove "output/2-vector-polygon-units-fixed.cs.json"
fi

# Suppression des submodules git inutilisés
echo ""
echo " Nettoyage des submodules git..."
if [ -f ".gitmodules" ]; then
    echo "   Fichier .gitmodules trouvé - vérification..."
    # Si le dossier grammar n'a plus de contenu utile, on peut nettoyer
    if [ -d "grammar" ] && [ ! -f "grammar/CartoSymCSSGrammar.g4" ] && [ ! -f "grammar/CartoSymCSSLexer.g4" ]; then
        echo "     Suppression du dossier grammar vide..."
        safe_remove "grammar"
        echo "   Nettoyage des références de submodule..."
        git submodule deinit --force grammar 2>/dev/null || true
        git rm --cached grammar 2>/dev/null || true
        safe_remove ".gitmodules"
    fi
fi
