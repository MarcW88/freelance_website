#!/usr/bin/env python3
"""
LinkedIn SEO Analyzer - Script principal
Orchestre la collecte, l'analyse et la génération de contenu
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime
import schedule
import time

from linkedin_collector import main as collect_posts
from trend_analyzer import TrendAnalyzer
from post_generator import PostGenerator
from config import *

class LinkedInSEOAnalyzer:
    def __init__(self):
        """Initialise l'analyseur principal"""
        self.data_file = DATA_DIR / "posts_linkedin.csv"
        self.last_collection = None
        
    def run_full_pipeline(self):
        """Exécute le pipeline complet"""
        print("🚀 Démarrage du pipeline LinkedIn SEO Analyzer")
        print("=" * 60)
        
        # 1. Collecte des posts
        print("\n📥 ÉTAPE 1: Collecte des posts LinkedIn")
        print("-" * 40)
        
        try:
            # Sauvegarde de sys.argv pour éviter les conflits
            original_argv = sys.argv.copy()
            sys.argv = ['linkedin_collector.py', '--posts_per_profile', str(POSTS_PER_PROFILE)]
            
            collect_posts()
            self.last_collection = datetime.now()
            
            # Restauration de sys.argv
            sys.argv = original_argv
            
        except Exception as e:
            print(f"❌ Erreur lors de la collecte: {e}")
            return False
        
        # 2. Analyse des tendances
        print("\n📊 ÉTAPE 2: Analyse des tendances")
        print("-" * 40)
        
        if not self.data_file.exists():
            print(f"❌ Fichier de données non trouvé: {self.data_file}")
            return False
        
        try:
            analyzer = TrendAnalyzer(self.data_file)
            if analyzer.load_data():
                report = analyzer.generate_trend_report()
                analyzer.create_visualizations()
                
                # Sauvegarde du rapport
                import json
                with open(OUTPUT_DIR / 'trend_report.json', 'w', encoding='utf-8') as f:
                    json.dump(report, f, ensure_ascii=False, indent=2, default=str)
                
                print("✅ Analyse des tendances terminée")
            else:
                return False
                
        except Exception as e:
            print(f"❌ Erreur lors de l'analyse: {e}")
            return False
        
        # 3. Génération de suggestions
        print("\n✍️ ÉTAPE 3: Génération de suggestions de posts")
        print("-" * 40)
        
        try:
            generator = PostGenerator()
            suggestions = generator.generate_post_suggestions(count=5)
            weekly_plan = generator.generate_weekly_content_plan()
            
            # Sauvegarde des suggestions
            generator.save_suggestions(suggestions)
            
            print("✅ Génération de contenu terminée")
            
        except Exception as e:
            print(f"❌ Erreur lors de la génération: {e}")
            return False
        
        print("\n🎉 Pipeline terminé avec succès!")
        print(f"📁 Résultats disponibles dans: {OUTPUT_DIR}")
        return True
    
    def run_analysis_only(self):
        """Exécute uniquement l'analyse et la génération (sans collecte)"""
        print("📊 Analyse des données existantes...")
        
        if not self.data_file.exists():
            print(f"❌ Aucune donnée trouvée. Lancez d'abord la collecte.")
            return False
        
        # Analyse
        analyzer = TrendAnalyzer(self.data_file)
        if not analyzer.load_data():
            return False
        
        report = analyzer.generate_trend_report()
        analyzer.create_visualizations()
        
        # Génération
        generator = PostGenerator()
        suggestions = generator.generate_post_suggestions(count=3)
        generator.save_suggestions(suggestions)
        
        print("✅ Analyse terminée!")
        return True
    
    def run_generation_only(self):
        """Exécute uniquement la génération de posts"""
        print("✍️ Génération de nouveaux posts...")
        
        generator = PostGenerator()
        if generator.trend_data is None:
            print("❌ Aucune donnée de tendance. Lancez d'abord l'analyse.")
            return False
        
        suggestions = generator.generate_post_suggestions(count=5)
        generator.save_suggestions(suggestions)
        
        # Affichage des suggestions
        print("\n📝 NOUVELLES SUGGESTIONS:")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"\n{i}. {suggestion['type'].upper()} - {suggestion['keyword']}")
            print(f"   Engagement: {suggestion['estimated_engagement']}/10")
            print(f"   Extrait: {suggestion['content'][:100]}...")
        
        return True
    
    def schedule_weekly_run(self):
        """Programme l'exécution hebdomadaire"""
        print("⏰ Programmation de l'exécution hebdomadaire...")
        
        # Programmation pour le mercredi à 10h (milieu de semaine)
        schedule.every().wednesday.at("10:00").do(self.run_analysis_only)
        
        # Programmation pour le vendredi à 15h (fin de semaine)
        schedule.every().friday.at("15:00").do(self.run_generation_only)
        
        print("📅 Programmé:")
        print("  - Mercredi 10h: Analyse des tendances")
        print("  - Vendredi 15h: Génération de posts")
        print("\n⏳ En attente... (Ctrl+C pour arrêter)")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Vérification chaque minute
        except KeyboardInterrupt:
            print("\n👋 Arrêt du scheduler")
    
    def show_status(self):
        """Affiche le statut du système"""
        print("📊 STATUT DU SYSTÈME")
        print("=" * 30)
        
        # Vérification des fichiers
        print(f"📁 Dossier de données: {DATA_DIR}")
        print(f"   Existe: {'✅' if DATA_DIR.exists() else '❌'}")
        
        print(f"📄 Fichier de posts: {self.data_file}")
        print(f"   Existe: {'✅' if self.data_file.exists() else '❌'}")
        
        if self.data_file.exists():
            import pandas as pd
            try:
                df = pd.read_csv(self.data_file)
                print(f"   Posts: {len(df)}")
                print(f"   Auteurs: {df['author'].nunique()}")
                print(f"   Dernière date: {df['date'].max()}")
            except:
                print("   ❌ Erreur de lecture")
        
        # Vérification des rapports
        report_file = OUTPUT_DIR / 'trend_report.json'
        print(f"📊 Rapport de tendances: {'✅' if report_file.exists() else '❌'}")
        
        # Vérification des profils
        print(f"👥 Profils SEO: {'✅' if PROFILES_FILE.exists() else '❌'}")
        if PROFILES_FILE.exists():
            with open(PROFILES_FILE, 'r') as f:
                profiles = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            print(f"   Nombre: {len(profiles)}")

def main():
    parser = argparse.ArgumentParser(description="LinkedIn SEO Analyzer - Analyseur de tendances et générateur de contenu")
    parser.add_argument('action', choices=['full', 'collect', 'analyze', 'generate', 'schedule', 'status'],
                       help='Action à exécuter')
    parser.add_argument('--posts-per-profile', type=int, default=POSTS_PER_PROFILE,
                       help='Nombre de posts à collecter par profil')
    
    args = parser.parse_args()
    
    analyzer = LinkedInSEOAnalyzer()
    
    if args.action == 'full':
        analyzer.run_full_pipeline()
    elif args.action == 'collect':
        # Collecte uniquement
        original_argv = sys.argv.copy()
        sys.argv = ['linkedin_collector.py', '--posts_per_profile', str(args.posts_per_profile)]
        collect_posts()
        sys.argv = original_argv
    elif args.action == 'analyze':
        analyzer.run_analysis_only()
    elif args.action == 'generate':
        analyzer.run_generation_only()
    elif args.action == 'schedule':
        analyzer.schedule_weekly_run()
    elif args.action == 'status':
        analyzer.show_status()

if __name__ == "__main__":
    main()
