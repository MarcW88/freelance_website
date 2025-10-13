"""Configuration pour l'analyseur LinkedIn SEO"""

import os
from pathlib import Path

# Chemins
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
PROFILES_FILE = BASE_DIR / "seo_profiles.txt"

# Paramètres de collecte
POSTS_PER_PROFILE = 10
MIN_CHARS = 50
SCROLL_DELAY = 1.2
RANDOM_DELAY_MAX = 0.8

# Sélecteurs CSS LinkedIn
SEL_AUTHOR = '[data-test-id="post-author-name"], .update-components-actor__name'
SEL_LIKES = '[data-test-id="social-counts-reactions"], .social-counts-reactions'
SEL_POST_CONTENT = '.feed-shared-update-v2__description, .update-components-text'

# Paramètres d'analyse
MIN_WORD_FREQUENCY = 3
TOP_TRENDS_COUNT = 10
SIMILARITY_THRESHOLD = 0.7

# Mots-clés SEO à surveiller
SEO_KEYWORDS = [
    'seo', 'référencement', 'google', 'serp', 'ranking', 'backlink', 'keyword',
    'content', 'contenu', 'algorithm', 'algorithme', 'core update', 'e-a-t',
    'technical seo', 'seo technique', 'crawl', 'index', 'sitemap', 'robots.txt',
    'page speed', 'vitesse', 'mobile first', 'featured snippet', 'position zéro',
    'local seo', 'seo local', 'analytics', 'search console', 'ga4'
]

# Création des dossiers
DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
