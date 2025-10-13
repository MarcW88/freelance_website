"""
Générateur de suggestions de posts LinkedIn basé sur les tendances SEO
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from config import *

class PostGenerator:
    def __init__(self, trend_report_path=None):
        """Initialise le générateur avec le rapport de tendances"""
        if trend_report_path is None:
            trend_report_path = OUTPUT_DIR / 'trend_report.json'
        
        self.trend_report_path = trend_report_path
        self.trend_data = None
        self.load_trend_data()
        
        # Templates de posts par type
        self.post_templates = {
            'question': [
                "🤔 Question du jour : {topic}\n\nQuelle est votre expérience avec {keyword} ?\n\n{context}\n\n💬 Partagez vos retours en commentaire !",
                "❓ {topic} : êtes-vous d'accord ?\n\n{context}\n\nJ'aimerais connaître votre point de vue sur {keyword}.\n\n👇 Dites-moi tout !",
                "🎯 Sondage SEO : {topic}\n\n{context}\n\nEt vous, comment gérez-vous {keyword} ?\n\n📊 Votez et commentez !"
            ],
            'conseil': [
                "💡 Conseil SEO du jour : {topic}\n\n{context}\n\n✅ Mon conseil : {advice}\n\n🔄 Partagez si ça vous aide !",
                "🚀 Astuce {keyword} :\n\n{context}\n\n💪 Voici ce qui fonctionne pour moi :\n{advice}\n\n📈 Et vous, quelle est votre méthode ?",
                "⚡ Quick tip {topic} :\n\n{context}\n\n🎯 {advice}\n\n💬 Ça vous parle ?"
            ],
            'analyse': [
                "📊 Analyse de tendance : {topic}\n\n{context}\n\nCe que j'observe :\n{analysis}\n\n🤝 Qu'en pensez-vous ?",
                "🔍 Focus sur {keyword} :\n\n{context}\n\n📈 Mon analyse :\n{analysis}\n\n💭 Votre avis ?",
                "📋 Retour d'expérience {topic} :\n\n{context}\n\n✨ {analysis}\n\n🗣️ Partagez votre expérience !"
            ],
            'actualite': [
                "🔥 Actualité SEO : {topic}\n\n{context}\n\nImpact sur votre stratégie :\n{impact}\n\n📢 Restez informés !",
                "⚠️ Mise à jour importante : {keyword}\n\n{context}\n\n🎯 {impact}\n\n💡 Adaptez votre stratégie !",
                "📰 News SEO : {topic}\n\n{context}\n\n🔄 {impact}\n\n👥 Tagguez vos collègues !"
            ]
        }
        
        # Conseils génériques par mot-clé
        self.generic_advice = {
            'seo': "Concentrez-vous sur l'intention utilisateur avant tout",
            'contenu': "La qualité prime toujours sur la quantité",
            'google': "Suivez les guidelines, pas les rumeurs",
            'ranking': "La patience est la clé du référencement",
            'backlink': "Privilégiez la qualité à la quantité",
            'technical seo': "Un site rapide est un site qui convertit",
            'analytics': "Mesurez ce qui compte vraiment",
            'mobile': "Mobile-first n'est plus une option",
            'core update': "Restez zen et continuez à bien faire"
        }
    
    def load_trend_data(self):
        """Charge les données de tendances"""
        try:
            with open(self.trend_report_path, 'r', encoding='utf-8') as f:
                self.trend_data = json.load(f)
            print(f"✅ Données de tendances chargées depuis {self.trend_report_path}")
        except FileNotFoundError:
            print(f"❌ Fichier de tendances non trouvé: {self.trend_report_path}")
            print("💡 Lancez d'abord trend_analyzer.py pour générer les tendances")
        except Exception as e:
            print(f"❌ Erreur lors du chargement: {e}")
    
    def get_weekly_hot_topics(self, week_count=2):
        """Récupère les sujets chauds des dernières semaines"""
        if not self.trend_data:
            return []
        
        # Récupère les dernières semaines
        weekly_trends = self.trend_data.get('weekly_trends', {})
        recent_weeks = sorted(weekly_trends.keys())[-week_count:]
        
        hot_topics = []
        for week in recent_weeks:
            week_data = weekly_trends[week]
            
            # Combine mots-clés généraux et SEO
            topics = {}
            topics.update(week_data.get('top_words', {}))
            topics.update(week_data.get('seo_keywords', {}))
            
            # Filtre et score les topics
            for topic, freq in topics.items():
                if freq >= 2 and len(topic) > 3:  # Filtre basique
                    hot_topics.append({
                        'keyword': topic,
                        'frequency': freq,
                        'week': week,
                        'sample_posts': week_data.get('sample_posts', [])
                    })
        
        # Tri par fréquence
        hot_topics.sort(key=lambda x: x['frequency'], reverse=True)
        return hot_topics[:10]
    
    def get_recurring_themes(self, min_weeks=2):
        """Récupère les thèmes récurrents"""
        if not self.trend_data:
            return []
        
        recurring = self.trend_data.get('recurring_themes', {})
        
        themes = []
        for theme, data in recurring.items():
            if data['weeks_count'] >= min_weeks:
                themes.append({
                    'keyword': theme,
                    'frequency': data['frequency'],
                    'weeks_count': data['weeks_count'],
                    'relevance_score': data['weeks_count'] * data['avg_frequency']
                })
        
        themes.sort(key=lambda x: x['relevance_score'], reverse=True)
        return themes[:8]
    
    def generate_post_suggestions(self, count=5):
        """Génère des suggestions de posts"""
        if not self.trend_data:
            print("❌ Aucune donnée de tendance disponible")
            return []
        
        suggestions = []
        
        # Récupère les données
        hot_topics = self.get_weekly_hot_topics()
        recurring_themes = self.get_recurring_themes()
        top_seo_keywords = list(self.trend_data.get('top_seo_keywords', {}).keys())[:5]
        
        # Génère les suggestions
        for i in range(count):
            # Choix du type de post
            post_type = random.choice(list(self.post_templates.keys()))
            
            # Choix du sujet (mix entre hot topics et thèmes récurrents)
            if i % 2 == 0 and hot_topics:
                topic_data = random.choice(hot_topics)
                keyword = topic_data['keyword']
                context_source = "tendance récente"
            elif recurring_themes:
                topic_data = random.choice(recurring_themes)
                keyword = topic_data['keyword']
                context_source = "thème récurrent"
            else:
                keyword = random.choice(top_seo_keywords) if top_seo_keywords else "seo"
                topic_data = {'keyword': keyword, 'frequency': 1}
                context_source = "mot-clé populaire"
            
            # Génération du contenu
            suggestion = self._create_post_content(post_type, keyword, topic_data, context_source)
            suggestions.append(suggestion)
        
        return suggestions
    
    def _create_post_content(self, post_type, keyword, topic_data, context_source):
        """Crée le contenu d'un post"""
        # Sélection du template
        template = random.choice(self.post_templates[post_type])
        
        # Génération du contexte
        context = self._generate_context(keyword, context_source)
        
        # Génération du contenu spécifique au type
        if post_type == 'conseil':
            specific_content = self._get_advice(keyword)
        elif post_type == 'analyse':
            specific_content = self._get_analysis(keyword)
        elif post_type == 'actualite':
            specific_content = self._get_impact_analysis(keyword)
        else:
            specific_content = ""
        
        # Formatage du post
        post_content = template.format(
            topic=keyword.upper(),
            keyword=keyword,
            context=context,
            advice=specific_content,
            analysis=specific_content,
            impact=specific_content
        )
        
        return {
            'type': post_type,
            'keyword': keyword,
            'content': post_content,
            'hashtags': self._generate_hashtags(keyword),
            'context_source': context_source,
            'estimated_engagement': self._estimate_engagement(post_type, keyword)
        }
    
    def _generate_context(self, keyword, source):
        """Génère le contexte pour un mot-clé"""
        contexts = {
            'seo': f"Le {keyword.upper()} évolue constamment. Avec les dernières mises à jour Google...",
            'contenu': f"La stratégie de {keyword} devient de plus en plus cruciale...",
            'google': f"Les derniers changements de {keyword.title()} impactent notre façon de travailler...",
            'analytics': f"L'analyse des données {keyword} révèle des insights intéressants...",
            'technical': f"L'aspect {keyword} est souvent négligé, pourtant...",
            'mobile': f"L'optimisation {keyword} n'est plus optionnelle en 2024...",
            'backlink': f"La stratégie de {keyword} a évolué ces dernières années..."
        }
        
        # Contexte par défaut ou spécifique
        for key, context in contexts.items():
            if key in keyword.lower():
                return context
        
        return f"J'observe une tendance intéressante autour de {keyword}..."
    
    def _get_advice(self, keyword):
        """Génère un conseil pour un mot-clé"""
        return self.generic_advice.get(keyword.lower(), 
                                     f"Testez, mesurez, ajustez. C'est la base du {keyword} efficace.")
    
    def _get_analysis(self, keyword):
        """Génère une analyse pour un mot-clé"""
        analyses = {
            'seo': "Les sites qui réussissent combinent technique et contenu de qualité",
            'contenu': "L'IA change la donne, mais l'expertise humaine reste irremplaçable",
            'google': "Chaque update nous rappelle l'importance de la qualité",
            'analytics': "Les métriques vanity ne servent à rien sans contexte business"
        }
        
        return analyses.get(keyword.lower(), 
                          f"Le {keyword} demande une approche méthodique et patiente")
    
    def _get_impact_analysis(self, keyword):
        """Génère une analyse d'impact"""
        return f"Cela va changer notre approche du {keyword}. Préparez-vous dès maintenant !"
    
    def _generate_hashtags(self, keyword):
        """Génère des hashtags pertinents"""
        base_hashtags = ['#SEO', '#ReferenceNaturel', '#DigitalMarketing', '#Google']
        
        keyword_hashtags = {
            'seo': ['#SEOTips', '#SearchEngineOptimization'],
            'contenu': ['#ContentMarketing', '#StrategieContenu'],
            'google': ['#GoogleUpdate', '#SearchConsole'],
            'analytics': ['#Analytics', '#DataDriven', '#GA4'],
            'technical': ['#TechnicalSEO', '#WebPerf'],
            'mobile': ['#MobileFirst', '#ResponsiveDesign'],
            'backlink': ['#LinkBuilding', '#NetLinking']
        }
        
        # Ajoute des hashtags spécifiques
        for key, tags in keyword_hashtags.items():
            if key in keyword.lower():
                base_hashtags.extend(tags)
                break
        
        return base_hashtags[:6]  # Limite à 6 hashtags
    
    def _estimate_engagement(self, post_type, keyword):
        """Estime l'engagement potentiel"""
        base_scores = {
            'question': 8,
            'conseil': 7,
            'analyse': 6,
            'actualite': 9
        }
        
        keyword_bonus = 1 if keyword.lower() in ['google', 'seo', 'ia'] else 0
        
        return min(10, base_scores.get(post_type, 5) + keyword_bonus)
    
    def save_suggestions(self, suggestions, filename=None):
        """Sauvegarde les suggestions dans un fichier"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            filename = OUTPUT_DIR / f"post_suggestions_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(suggestions, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Suggestions sauvegardées: {filename}")
        return filename
    
    def generate_weekly_content_plan(self):
        """Génère un plan de contenu pour la semaine"""
        suggestions = self.generate_post_suggestions(count=7)
        
        # Organisation par jour
        days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
        weekly_plan = {}
        
        for i, suggestion in enumerate(suggestions):
            day = days[i] if i < len(days) else f"Extra_{i-6}"
            weekly_plan[day] = suggestion
        
        # Sauvegarde
        timestamp = datetime.now().strftime("%Y%m%d")
        filename = OUTPUT_DIR / f"weekly_plan_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(weekly_plan, f, ensure_ascii=False, indent=2)
        
        print(f"📅 Plan hebdomadaire généré: {filename}")
        return weekly_plan

def main():
    """Fonction principale pour tester le générateur"""
    generator = PostGenerator()
    
    if generator.trend_data is None:
        print("❌ Impossible de charger les données de tendances")
        print("💡 Assurez-vous d'avoir lancé trend_analyzer.py d'abord")
        return
    
    print("🚀 Génération de suggestions de posts...")
    
    # Génère des suggestions
    suggestions = generator.generate_post_suggestions(count=5)
    
    # Affiche les suggestions
    print("\n" + "="*60)
    print("📝 SUGGESTIONS DE POSTS LINKEDIN")
    print("="*60)
    
    for i, suggestion in enumerate(suggestions, 1):
        print(f"\n📌 SUGGESTION #{i} - {suggestion['type'].upper()}")
        print(f"🎯 Mot-clé: {suggestion['keyword']}")
        print(f"📊 Engagement estimé: {suggestion['estimated_engagement']}/10")
        print(f"📄 Contenu:")
        print("-" * 40)
        print(suggestion['content'])
        print("-" * 40)
        print(f"🏷️ Hashtags: {' '.join(suggestion['hashtags'])}")
        print()
    
    # Sauvegarde
    generator.save_suggestions(suggestions)
    
    # Génère un plan hebdomadaire
    print("\n📅 Génération du plan hebdomadaire...")
    weekly_plan = generator.generate_weekly_content_plan()
    
    print("✅ Génération terminée !")

if __name__ == "__main__":
    main()
