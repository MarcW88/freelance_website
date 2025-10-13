"""
Analyseur de tendances pour les posts LinkedIn SEO
Identifie les sujets récurrents et les tendances par semaine
"""

import pandas as pd
import numpy as np
import re
from collections import Counter, defaultdict
from datetime import datetime, timedelta
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from pathlib import Path
from config import *

class TrendAnalyzer:
    def __init__(self, csv_file_path):
        """Initialise l'analyseur avec les données CSV"""
        self.csv_file = csv_file_path
        self.df = None
        self.weekly_trends = {}
        self.global_trends = {}
        
        # Configuration NLTK
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
        
        self.french_stopwords = set(stopwords.words('french'))
        self.english_stopwords = set(stopwords.words('english'))
        self.custom_stopwords = {
            'linkedin', 'post', 'partage', 'share', 'merci', 'thanks', 
            'like', 'comment', 'commentaire', 'https', 'http', 'www'
        }
        self.all_stopwords = self.french_stopwords | self.english_stopwords | self.custom_stopwords
        
        self.stemmer = SnowballStemmer('french')
    
    def load_data(self):
        """Charge et préprocesse les données"""
        try:
            self.df = pd.read_csv(self.csv_file, encoding='utf-8')
            self.df['date'] = pd.to_datetime(self.df['date'])
            self.df['week'] = self.df['date'].dt.isocalendar().week
            self.df['year'] = self.df['date'].dt.year
            self.df['week_year'] = self.df['year'].astype(str) + '-W' + self.df['week'].astype(str).str.zfill(2)
            
            print(f"✅ Données chargées: {len(self.df)} posts")
            print(f"📅 Période: {self.df['date'].min()} à {self.df['date'].max()}")
            print(f"👥 Auteurs: {self.df['author'].nunique()}")
            
            return True
        except Exception as e:
            print(f"❌ Erreur lors du chargement: {e}")
            return False
    
    def preprocess_text(self, text):
        """Préprocesse le texte pour l'analyse"""
        if pd.isna(text):
            return ""
        
        # Nettoyage de base
        text = str(text).lower()
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\d+', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Tokenisation et suppression des stopwords
        tokens = word_tokenize(text, language='french')
        tokens = [token for token in tokens if len(token) > 2 and token not in self.all_stopwords]
        
        # Stemming
        tokens = [self.stemmer.stem(token) for token in tokens]
        
        return ' '.join(tokens)
    
    def extract_seo_keywords(self, text):
        """Extrait les mots-clés SEO spécifiques du texte"""
        if pd.isna(text):
            return []
        
        text_lower = str(text).lower()
        found_keywords = []
        
        for keyword in SEO_KEYWORDS:
            if keyword.lower() in text_lower:
                found_keywords.append(keyword)
        
        return found_keywords
    
    def analyze_weekly_trends(self):
        """Analyse les tendances par semaine"""
        if self.df is None:
            print("❌ Aucune donnée chargée")
            return
        
        print("🔍 Analyse des tendances hebdomadaires...")
        
        # Préprocessing des textes
        self.df['processed_text'] = self.df['text'].apply(self.preprocess_text)
        self.df['seo_keywords'] = self.df['text'].apply(self.extract_seo_keywords)
        
        weekly_data = {}
        
        for week_year in self.df['week_year'].unique():
            week_posts = self.df[self.df['week_year'] == week_year]
            
            # Analyse des mots-clés
            all_text = ' '.join(week_posts['processed_text'].dropna())
            words = all_text.split()
            word_freq = Counter(words)
            top_words = dict(word_freq.most_common(20))
            
            # Analyse des mots-clés SEO spécifiques
            seo_keywords_week = []
            for keywords_list in week_posts['seo_keywords']:
                seo_keywords_week.extend(keywords_list)
            seo_freq = Counter(seo_keywords_week)
            
            # Calcul de l'engagement moyen
            avg_likes = week_posts['likes'].apply(lambda x: int(x) if str(x).isdigit() else 0).mean()
            
            weekly_data[week_year] = {
                'posts_count': len(week_posts),
                'top_words': top_words,
                'seo_keywords': dict(seo_freq.most_common(10)),
                'avg_likes': avg_likes,
                'authors': list(week_posts['author'].unique()),
                'sample_posts': week_posts['text'].head(3).tolist()
            }
        
        self.weekly_trends = weekly_data
        return weekly_data
    
    def find_recurring_themes(self, min_weeks=2):
        """Identifie les thèmes récurrents sur plusieurs semaines"""
        if not self.weekly_trends:
            self.analyze_weekly_trends()
        
        print("🔄 Recherche des thèmes récurrents...")
        
        # Collecte de tous les mots-clés par semaine
        all_keywords = defaultdict(list)
        
        for week, data in self.weekly_trends.items():
            for word, freq in data['top_words'].items():
                if freq >= MIN_WORD_FREQUENCY:
                    all_keywords[word].append((week, freq))
        
        # Identification des mots récurrents
        recurring_themes = {}
        for word, occurrences in all_keywords.items():
            if len(occurrences) >= min_weeks:
                total_freq = sum(freq for _, freq in occurrences)
                weeks = [week for week, _ in occurrences]
                recurring_themes[word] = {
                    'frequency': total_freq,
                    'weeks_count': len(weeks),
                    'weeks': weeks,
                    'avg_frequency': total_freq / len(weeks)
                }
        
        # Tri par pertinence
        sorted_themes = dict(sorted(recurring_themes.items(), 
                                  key=lambda x: (x[1]['weeks_count'], x[1]['frequency']), 
                                  reverse=True))
        
        return sorted_themes
    
    def generate_trend_report(self):
        """Génère un rapport complet des tendances"""
        if not self.weekly_trends:
            self.analyze_weekly_trends()
        
        recurring_themes = self.find_recurring_themes()
        
        report = {
            'summary': {
                'total_posts': len(self.df),
                'weeks_analyzed': len(self.weekly_trends),
                'unique_authors': self.df['author'].nunique(),
                'date_range': f"{self.df['date'].min().strftime('%Y-%m-%d')} à {self.df['date'].max().strftime('%Y-%m-%d')}"
            },
            'weekly_trends': self.weekly_trends,
            'recurring_themes': recurring_themes,
            'top_seo_keywords': self._get_top_seo_keywords(),
            'engagement_analysis': self._analyze_engagement()
        }
        
        return report
    
    def _get_top_seo_keywords(self):
        """Analyse les mots-clés SEO les plus fréquents"""
        all_seo_keywords = []
        for keywords_list in self.df['seo_keywords']:
            all_seo_keywords.extend(keywords_list)
        
        return dict(Counter(all_seo_keywords).most_common(15))
    
    def _analyze_engagement(self):
        """Analyse l'engagement par type de contenu"""
        engagement_data = {}
        
        for week, data in self.weekly_trends.items():
            engagement_data[week] = {
                'avg_likes': data['avg_likes'],
                'posts_count': data['posts_count']
            }
        
        return engagement_data
    
    def create_visualizations(self):
        """Crée des visualisations des tendances"""
        if not self.weekly_trends:
            self.analyze_weekly_trends()
        
        output_dir = OUTPUT_DIR
        
        # 1. WordCloud des mots les plus fréquents
        all_text = ' '.join(self.df['processed_text'].dropna())
        if all_text:
            wordcloud = WordCloud(width=800, height=400, 
                                background_color='white',
                                colormap='viridis').generate(all_text)
            
            plt.figure(figsize=(12, 6))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.title('Mots-clés les plus fréquents dans les posts SEO')
            plt.tight_layout()
            plt.savefig(output_dir / 'wordcloud_seo.png', dpi=300, bbox_inches='tight')
            plt.close()
        
        # 2. Évolution des posts par semaine
        weeks = list(self.weekly_trends.keys())
        posts_counts = [data['posts_count'] for data in self.weekly_trends.values()]
        
        plt.figure(figsize=(12, 6))
        plt.plot(range(len(weeks)), posts_counts, marker='o', linewidth=2, markersize=6)
        plt.title('Évolution du nombre de posts par semaine')
        plt.xlabel('Semaines')
        plt.ylabel('Nombre de posts')
        plt.xticks(range(len(weeks)), [w.split('-W')[1] for w in weeks], rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_dir / 'posts_evolution.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 3. Top mots-clés SEO
        seo_keywords = self._get_top_seo_keywords()
        if seo_keywords:
            plt.figure(figsize=(12, 8))
            keywords = list(seo_keywords.keys())[:10]
            frequencies = list(seo_keywords.values())[:10]
            
            bars = plt.barh(keywords, frequencies, color='skyblue')
            plt.title('Top 10 des mots-clés SEO les plus mentionnés')
            plt.xlabel('Fréquence')
            
            # Ajouter les valeurs sur les barres
            for bar, freq in zip(bars, frequencies):
                plt.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                        str(freq), ha='left', va='center')
            
            plt.tight_layout()
            plt.savefig(output_dir / 'top_seo_keywords.png', dpi=300, bbox_inches='tight')
            plt.close()
        
        print(f"📊 Visualisations sauvegardées dans {output_dir}")

def main():
    """Fonction principale pour tester l'analyseur"""
    csv_file = DATA_DIR / "posts_linkedin.csv"
    
    if not csv_file.exists():
        print(f"❌ Fichier {csv_file} non trouvé. Lancez d'abord linkedin_collector.py")
        return
    
    analyzer = TrendAnalyzer(csv_file)
    
    if analyzer.load_data():
        report = analyzer.generate_trend_report()
        
        # Sauvegarde du rapport
        import json
        with open(OUTPUT_DIR / 'trend_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2, default=str)
        
        # Création des visualisations
        analyzer.create_visualizations()
        
        # Affichage du résumé
        print("\n" + "="*50)
        print("📊 RAPPORT D'ANALYSE DES TENDANCES")
        print("="*50)
        print(f"Posts analysés: {report['summary']['total_posts']}")
        print(f"Semaines: {report['summary']['weeks_analyzed']}")
        print(f"Auteurs: {report['summary']['unique_authors']}")
        print(f"Période: {report['summary']['date_range']}")
        
        print("\n🔥 TOP THÈMES RÉCURRENTS:")
        for theme, data in list(report['recurring_themes'].items())[:5]:
            print(f"  • {theme}: {data['weeks_count']} semaines, {data['frequency']} mentions")
        
        print("\n🎯 TOP MOTS-CLÉS SEO:")
        for keyword, freq in list(report['top_seo_keywords'].items())[:5]:
            print(f"  • {keyword}: {freq} mentions")
        
        print(f"\n💾 Rapport complet sauvegardé: {OUTPUT_DIR / 'trend_report.json'}")

if __name__ == "__main__":
    main()
