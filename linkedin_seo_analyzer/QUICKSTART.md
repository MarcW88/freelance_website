# 🚀 Guide de démarrage rapide

## Installation en 3 minutes

1. **Installation automatique**
```bash
cd /Users/marc/Desktop/freelance_website/linkedin_seo_analyzer
./install.sh
```

2. **Premier lancement**
```bash
python3 main.py status
```

3. **Collecte de test**
```bash
python3 main.py collect
```
*Connectez-vous à LinkedIn quand demandé*

## Utilisation quotidienne

### 🔄 Workflow hebdomadaire recommandé

**Lundi** - Collecte des données
```bash
python3 main.py collect
```

**Mercredi** - Analyse des tendances
```bash
python3 main.py analyze
```

**Vendredi** - Génération de posts
```bash
python3 main.py generate
```

### ⚡ Mode automatique
```bash
python3 main.py schedule
```
Lance l'analyse le mercredi et la génération le vendredi automatiquement.

## 📝 Vos premiers posts

Après la première analyse, vous trouverez dans `/output/` :

- `post_suggestions_*.json` : Vos suggestions de posts
- `weekly_plan_*.json` : Plan de contenu pour la semaine
- `trend_report.json` : Analyse complète des tendances

## 🎯 Personnalisation rapide

### Ajouter vos profils SEO préférés
Éditez `seo_profiles.txt` :
```
https://www.linkedin.com/in/votre-expert-seo-prefere/
```

### Modifier les mots-clés surveillés
Éditez `config.py`, section `SEO_KEYWORDS` :
```python
SEO_KEYWORDS = [
    'seo', 'référencement', 'google',
    'votre-niche-specifique'  # Ajoutez ici
]
```

## 🆘 Problèmes courants

**"Aucune donnée trouvée"**
→ Lancez `python3 main.py collect` d'abord

**"Erreur de connexion LinkedIn"**
→ Vérifiez que vous êtes bien connecté dans le navigateur

**"Module non trouvé"**
→ Relancez `./install.sh`

## 📊 Exemple de résultat

Après analyse, vous obtiendrez des posts comme :

```
🤔 Question du jour : SEO TECHNIQUE

Le SEO technique évolue constamment. Avec les dernières mises à jour Google...

Quelle est votre expérience avec technical seo ?

💬 Partagez vos retours en commentaire !

#SEO #TechnicalSEO #Google #WebPerf
```

**Prêt à dominer LinkedIn ? 🚀**
