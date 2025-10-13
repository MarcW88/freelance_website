"""
Collecteur de posts LinkedIn pour l'analyse des tendances SEO
Basé sur Playwright avec login manuel pour respecter les ToS LinkedIn
"""

import argparse
import csv
import re
import time
import random
from pathlib import Path
from datetime import datetime, timedelta
from playwright.sync_api import sync_playwright
from config import *

def norm_whitespace(text):
    """Normalise les espaces dans le texte"""
    return re.sub(r'\s+', ' ', text).strip()

def read_profiles(profiles_file):
    """Lit la liste des profils depuis un fichier"""
    try:
        with open(profiles_file, 'r', encoding='utf-8') as f:
            profiles = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        return profiles
    except FileNotFoundError:
        print(f"Fichier {profiles_file} non trouvé")
        return []

def extract_posts_from_profile(page, profile_url, posts_limit=10):
    """Extrait les posts d'un profil LinkedIn"""
    print(f"Extraction des posts de: {profile_url}")
    
    # Navigation vers le profil
    page.goto(f"{profile_url}/recent-activity/all/")
    time.sleep(2)
    
    rows = []
    seen = set()
    loaded = 0
    max_scrolls = 10
    scrolls = 0
    
    while loaded < posts_limit and scrolls < max_scrolls:
        scrolls += 1
        
        # Recherche des conteneurs de posts
        containers = page.locator('.feed-shared-update-v2, .update-components-update')
        
        for i in range(containers.count()):
            if loaded >= posts_limit:
                break
                
            container = containers.nth(i)
            
            try:
                # Extraction du texte du post
                text_elem = container.locator(SEL_POST_CONTENT).first
                if not text_elem.is_visible():
                    continue
                    
                text = norm_whitespace(text_elem.inner_text())
                if len(text) < MIN_CHARS:
                    continue
                
                # Extraction de l'auteur
                author = None
                try:
                    author_elem = container.locator(SEL_AUTHOR).first
                    if author_elem.is_visible():
                        author = norm_whitespace(author_elem.inner_text())
                except:
                    pass
                
                if not author:
                    author = profile_url.rstrip("/").split("/")[-1]
                
                # Extraction des likes
                likes = ""
                try:
                    likes_elem = container.locator(SEL_LIKES).first
                    if likes_elem.is_visible():
                        likes_text = likes_elem.inner_text()
                        likes = re.sub(r"\D", "", likes_text)
                except:
                    pass
                
                # Extraction de la date (approximative)
                post_date = datetime.now().strftime("%Y-%m-%d")
                try:
                    # Tentative d'extraction de la date réelle
                    date_elem = container.locator('[data-test-id="feed-shared-update-v2__timestamp"], .update-components-actor__sub-description').first
                    if date_elem.is_visible():
                        date_text = date_elem.inner_text().lower()
                        if 'jour' in date_text or 'day' in date_text:
                            days_ago = 1
                            if any(char.isdigit() for char in date_text):
                                days_ago = int(re.search(r'\d+', date_text).group())
                            post_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
                        elif 'semaine' in date_text or 'week' in date_text:
                            weeks_ago = 1
                            if any(char.isdigit() for char in date_text):
                                weeks_ago = int(re.search(r'\d+', date_text).group())
                            post_date = (datetime.now() - timedelta(weeks=weeks_ago)).strftime("%Y-%m-%d")
                except:
                    pass
                
                # Éviter les doublons
                key = (author, text[:100])
                if key in seen:
                    continue
                seen.add(key)
                
                rows.append([
                    author,
                    post_date,
                    text,
                    "",  # commentaires (à implémenter si nécessaire)
                    likes,
                    profile_url
                ])
                
                loaded += 1
                print(f"  Post collecté: {text[:50]}...")
                
            except Exception as e:
                print(f"  Erreur lors de l'extraction d'un post: {e}")
                continue
        
        if loaded >= posts_limit:
            break
            
        # Scroll pour charger plus de contenu
        page.mouse.wheel(0, 2500)
        time.sleep(SCROLL_DELAY + random.uniform(0, RANDOM_DELAY_MAX))
    
    print(f"  Total collecté: {loaded} posts")
    return rows

def main():
    parser = argparse.ArgumentParser(description="Collecte des posts LinkedIn SEO")
    parser.add_argument("--profiles_file", default=str(PROFILES_FILE), 
                       help="Fichier contenant les URLs des profils")
    parser.add_argument("--posts_per_profile", type=int, default=POSTS_PER_PROFILE)
    parser.add_argument("--outfile", default=str(DATA_DIR / "posts_linkedin.csv"))
    
    args = parser.parse_args()
    
    profiles = read_profiles(args.profiles_file)
    if not profiles:
        raise SystemExit("Aucun profil trouvé dans le fichier.")
    
    print(f"Collecte prévue sur {len(profiles)} profils")
    
    with sync_playwright() as p:
        try:
            # Configuration du navigateur avec options plus robustes
            browser = p.chromium.launch(
                headless=False,
                args=['--no-sandbox', '--disable-dev-shm-usage']
            )
            
            # Création du contexte avec user agent
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            
            page = context.new_page()
            
            # Connexion manuelle LinkedIn
            print("🔗 Ouverture de LinkedIn...")
            page.goto("https://www.linkedin.com/login", wait_until='networkidle')
            
            print("👤 Veuillez vous connecter à LinkedIn dans la fenêtre du navigateur")
            print("⏳ Une fois connecté, appuyez sur Entrée pour continuer...")
            input("➡️ Appuyez sur Entrée quand vous êtes connecté: ")
            
            # Vérification que l'utilisateur est bien connecté
            try:
                page.wait_for_url("**/feed/**", timeout=10000)
                print("✅ Connexion LinkedIn détectée!")
            except:
                print("⚠️ Connexion non détectée, mais on continue...")
                
        except Exception as e:
            print(f"❌ Erreur lors de l'initialisation du navigateur: {e}")
            return
        
        all_rows = []
        
        for idx, profile_url in enumerate(profiles, 1):
            print(f"\n[{idx}/{len(profiles)}] Traitement de: {profile_url}")
            
            try:
                rows = extract_posts_from_profile(page, profile_url, args.posts_per_profile)
                all_rows.extend(rows)
                
                # Pause entre les profils pour éviter la détection
                if idx < len(profiles):
                    delay = 2.0 + random.uniform(1, 3)
                    print(f"  Pause de {delay:.1f}s avant le prochain profil...")
                    time.sleep(delay)
                    
            except Exception as e:
                print(f"  ❌ Erreur sur {profile_url}: {e}")
                continue
        
        # Sauvegarde des données
        print(f"\n💾 Sauvegarde de {len(all_rows)} posts dans {args.outfile}")
        
        with open(args.outfile, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["author", "date", "text", "comments", "likes", "source_url"])
            writer.writerows(all_rows)
        
        # Fermeture propre
        try:
            context.close()
            browser.close()
        except:
            pass
        
        print("✅ Collecte terminée!")

if __name__ == "__main__":
    main()
