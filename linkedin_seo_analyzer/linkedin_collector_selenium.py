"""
Collecteur de posts LinkedIn avec Selenium (alternative à Playwright)
Plus stable sur certains systèmes macOS
"""

import argparse
import csv
import re
import time
import random
from pathlib import Path
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
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

def setup_driver():
    """Configure et lance le driver Chrome"""
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # User agent pour éviter la détection
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    try:
        print("🔧 Configuration du driver Chrome...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        print("✅ Driver Chrome initialisé")
        return driver
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation du driver Chrome: {e}")
        print("💡 Assurez-vous que Chrome est installé")
        return None

def extract_posts_from_profile_selenium(driver, profile_url, posts_limit=10):
    """Extrait les posts d'un profil LinkedIn avec Selenium"""
    print(f"Extraction des posts de: {profile_url}")
    
    # Navigation vers le profil
    activity_url = f"{profile_url}/recent-activity/all/"
    driver.get(activity_url)
    time.sleep(3)
    
    rows = []
    seen = set()
    loaded = 0
    max_scrolls = 10
    scrolls = 0
    
    while loaded < posts_limit and scrolls < max_scrolls:
        scrolls += 1
        
        try:
            # Recherche des conteneurs de posts
            post_containers = driver.find_elements(By.CSS_SELECTOR, '.feed-shared-update-v2, .update-components-update')
            
            for container in post_containers:
                if loaded >= posts_limit:
                    break
                
                try:
                    # Extraction du texte du post
                    text_elements = container.find_elements(By.CSS_SELECTOR, '.feed-shared-update-v2__description, .update-components-text')
                    
                    if not text_elements:
                        continue
                    
                    text = norm_whitespace(text_elements[0].text)
                    if len(text) < MIN_CHARS:
                        continue
                    
                    # Extraction de l'auteur
                    author = None
                    try:
                        author_elements = container.find_elements(By.CSS_SELECTOR, '[data-test-id="post-author-name"], .update-components-actor__name')
                        if author_elements:
                            author = norm_whitespace(author_elements[0].text)
                    except:
                        pass
                    
                    if not author:
                        author = profile_url.rstrip("/").split("/")[-1]
                    
                    # Extraction des likes
                    likes = ""
                    try:
                        likes_elements = container.find_elements(By.CSS_SELECTOR, '[data-test-id="social-counts-reactions"], .social-counts-reactions')
                        if likes_elements:
                            likes_text = likes_elements[0].text
                            likes = re.sub(r"\D", "", likes_text)
                    except:
                        pass
                    
                    # Date approximative
                    post_date = datetime.now().strftime("%Y-%m-%d")
                    
                    # Éviter les doublons
                    key = (author, text[:100])
                    if key in seen:
                        continue
                    seen.add(key)
                    
                    rows.append([
                        author,
                        post_date,
                        text,
                        "",  # commentaires
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
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_DELAY + random.uniform(0, RANDOM_DELAY_MAX))
            
        except Exception as e:
            print(f"  Erreur lors du scroll: {e}")
            break
    
    print(f"  Total collecté: {loaded} posts")
    return rows

def main():
    parser = argparse.ArgumentParser(description="Collecte des posts LinkedIn SEO avec Selenium")
    parser.add_argument("--profiles_file", default=str(PROFILES_FILE), 
                       help="Fichier contenant les URLs des profils")
    parser.add_argument("--posts_per_profile", type=int, default=POSTS_PER_PROFILE)
    parser.add_argument("--outfile", default=str(DATA_DIR / "posts_linkedin.csv"))
    
    args = parser.parse_args()
    
    profiles = read_profiles(args.profiles_file)
    if not profiles:
        raise SystemExit("Aucun profil trouvé dans le fichier.")
    
    print(f"Collecte prévue sur {len(profiles)} profils")
    
    # Configuration du driver
    driver = setup_driver()
    if not driver:
        return
    
    try:
        # Connexion manuelle LinkedIn
        print("🔗 Ouverture de LinkedIn...")
        driver.get("https://www.linkedin.com/login")
        
        print("👤 Veuillez vous connecter à LinkedIn dans la fenêtre du navigateur")
        print("⏳ Une fois connecté, appuyez sur Entrée pour continuer...")
        input("➡️ Appuyez sur Entrée quand vous êtes connecté: ")
        
        all_rows = []
        
        for idx, profile_url in enumerate(profiles, 1):
            print(f"\n[{idx}/{len(profiles)}] Traitement de: {profile_url}")
            
            try:
                rows = extract_posts_from_profile_selenium(driver, profile_url, args.posts_per_profile)
                all_rows.extend(rows)
                
                # Pause entre les profils
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
        
        print("✅ Collecte terminée!")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
