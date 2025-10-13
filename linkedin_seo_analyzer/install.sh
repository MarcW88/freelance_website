#!/bin/bash

# Script d'installation pour LinkedIn SEO Analyzer
# Usage: ./install.sh

echo "🚀 Installation de LinkedIn SEO Analyzer"
echo "========================================"

# Vérification de Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

echo "✅ Python 3 détecté: $(python3 --version)"

# Vérification de pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

echo "✅ pip3 détecté"

# Installation des dépendances Python
echo ""
echo "📦 Installation des dépendances Python..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Erreur lors de l'installation des dépendances Python"
    exit 1
fi

echo "✅ Dépendances Python installées"

# Installation de Playwright
echo ""
echo "🎭 Installation de Playwright..."
playwright install chromium

if [ $? -ne 0 ]; then
    echo "❌ Erreur lors de l'installation de Playwright"
    exit 1
fi

echo "✅ Playwright installé"

# Téléchargement des données NLTK
echo ""
echo "📚 Téléchargement des données NLTK..."
python3 -c "
import nltk
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    print('✅ Données NLTK téléchargées')
except Exception as e:
    print(f'❌ Erreur NLTK: {e}')
"

# Création des dossiers nécessaires
echo ""
echo "📁 Création des dossiers..."
mkdir -p data output

echo "✅ Dossiers créés"

# Vérification des permissions
echo ""
echo "🔐 Vérification des permissions..."
chmod +x main.py
chmod +x install.sh

echo "✅ Permissions configurées"

# Test rapide
echo ""
echo "🧪 Test de l'installation..."
python3 main.py status

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Installation terminée avec succès !"
    echo ""
    echo "📋 Prochaines étapes :"
    echo "1. Éditez seo_profiles.txt pour ajouter vos profils SEO préférés"
    echo "2. Lancez: python3 main.py full"
    echo "3. Consultez le README.md pour plus d'informations"
    echo ""
    echo "💡 Conseil: Commencez par 'python3 main.py collect' pour tester la collecte"
else
    echo "❌ Erreur lors du test. Vérifiez l'installation."
    exit 1
fi
