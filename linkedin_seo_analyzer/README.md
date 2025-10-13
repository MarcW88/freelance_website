# LinkedIn SEO Analyzer 📊

Un outil intelligent pour analyser les tendances SEO sur LinkedIn et générer automatiquement des suggestions de posts basées sur les récurrences détectées.

## 🎯 Objectif

Vous aider à être plus présent sur LinkedIn en :
- Collectant automatiquement les posts des experts SEO
- Identifiant les sujets récurrents et tendances hebdomadaires
- Générant des suggestions de posts pertinents basés sur ces analyses

## 🚀 Fonctionnalités

### 📥 Collecte de données
- Extraction automatique des posts LinkedIn via Playwright
- Support de multiples profils SEO français
- Respect des ToS LinkedIn (login manuel, délais respectés)
- Sauvegarde en CSV pour analyse

### 📊 Analyse des tendances
- Détection des mots-clés récurrents par semaine
- Identification des thèmes porteurs
- Analyse de l'engagement par type de contenu
- Visualisations automatiques (graphiques, word clouds)

### ✍️ Génération de contenu
- Suggestions de posts basées sur les tendances
- 4 types de posts : questions, conseils, analyses, actualités
- Hashtags automatiques et estimation d'engagement
- Plans de contenu hebdomadaires

## 📦 Installation

1. **Cloner le projet**
```bash
cd /Users/marc/Desktop/freelance_website/linkedin_seo_analyzer
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Installer Playwright**
```bash
playwright install chromium
```

4. **Configuration des profils SEO**
Éditez le fichier `seo_profiles.txt` pour ajouter/modifier les profils à analyser :
```
https://www.linkedin.com/in/olivierduffez/
https://www.linkedin.com/in/danielroch/
# Ajoutez vos profils SEO préférés
```

## 🔧 Utilisation

### Mode complet (recommandé pour la première fois)
```bash
python main.py full
```

### Collecte uniquement
```bash
python main.py collect
```

### Analyse des données existantes
```bash
python main.py analyze
```

### Génération de nouveaux posts
```bash
python main.py generate
```

### Programmation automatique
```bash
python main.py schedule
```
- Mercredi 10h : Analyse des tendances
- Vendredi 15h : Génération de posts

### Vérification du statut
```bash
python main.py status
```

## 📁 Structure du projet

```
linkedin_seo_analyzer/
├── main.py                 # Script principal
├── linkedin_collector.py   # Collecteur de posts
├── trend_analyzer.py      # Analyseur de tendances
├── post_generator.py      # Générateur de suggestions
├── config.py             # Configuration
├── requirements.txt      # Dépendances Python
├── seo_profiles.txt     # Liste des profils à analyser
├── data/                # Données collectées
│   └── posts_linkedin.csv
└── output/              # Résultats et rapports
    ├── trend_report.json
    ├── post_suggestions_*.json
    ├── weekly_plan_*.json
    └── visualizations/
```

## 🎨 Exemples de posts générés

### Question engageante
```
🤔 Question du jour : SEO

Le SEO évolue constamment. Avec les dernières mises à jour Google...

Quelle est votre expérience avec seo ?

💬 Partagez vos retours en commentaire !

#SEO #ReferenceNaturel #DigitalMarketing #Google #SEOTips
```

### Conseil pratique
```
💡 Conseil SEO du jour : CONTENU

La stratégie de contenu devient de plus en plus cruciale...

✅ Mon conseil : La qualité prime toujours sur la quantité

🔄 Partagez si ça vous aide !

#SEO #ContentMarketing #StrategieContenu
```

## ⚙️ Configuration avancée

### Personnalisation des mots-clés SEO
Éditez `config.py` pour modifier la liste `SEO_KEYWORDS` :
```python
SEO_KEYWORDS = [
    'seo', 'référencement', 'google', 'serp',
    # Ajoutez vos mots-clés spécifiques
]
```

### Ajustement des paramètres de collecte
```python
POSTS_PER_PROFILE = 10  # Nombre de posts par profil
MIN_CHARS = 50          # Longueur minimale des posts
SCROLL_DELAY = 1.2      # Délai entre les scrolls
```

## 📊 Rapports générés

### Rapport de tendances (`trend_report.json`)
- Résumé global des données
- Tendances hebdomadaires
- Thèmes récurrents
- Mots-clés SEO populaires
- Analyse d'engagement

### Suggestions de posts (`post_suggestions_*.json`)
- Type de post (question, conseil, analyse, actualité)
- Contenu généré
- Hashtags recommandés
- Score d'engagement estimé

### Plan hebdomadaire (`weekly_plan_*.json`)
- Contenu organisé par jour
- Mix équilibré des types de posts
- Basé sur les tendances actuelles

## 🔒 Respect de LinkedIn

Cet outil respecte les conditions d'utilisation de LinkedIn :
- ✅ Login manuel requis
- ✅ Délais respectés entre les requêtes
- ✅ Pas d'automatisation complète
- ✅ Usage personnel/professionnel uniquement

## 🚨 Limitations

- Nécessite une connexion LinkedIn active
- Les sélecteurs CSS peuvent changer (LinkedIn met à jour régulièrement)
- Analyse en français principalement
- Génération basée sur des templates (pas d'IA générative)

## 🛠️ Dépannage

### Erreur "Profils non trouvés"
- Vérifiez que `seo_profiles.txt` existe et contient des URLs valides

### Erreur de collecte LinkedIn
- Assurez-vous d'être connecté à LinkedIn
- Vérifiez que les sélecteurs CSS sont à jour
- Réduisez `POSTS_PER_PROFILE` si timeout

### Erreur d'analyse NLTK
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

## 📈 Roadmap

- [ ] Intégration d'une IA générative (GPT/Claude)
- [ ] Support multilingue complet
- [ ] Interface web pour la gestion
- [ ] Analyse de sentiment des posts
- [ ] Prédiction de viralité
- [ ] Export vers outils de planification (Buffer, Hootsuite)

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Ajouter de nouveaux templates de posts
- Améliorer les algorithmes d'analyse

## 📄 Licence

Usage personnel et professionnel. Respectez les ToS de LinkedIn.

---

**💡 Conseil d'utilisation :** Lancez une collecte complète une fois par semaine, puis utilisez le mode `analyze` et `generate` pour créer du contenu frais régulièrement !
