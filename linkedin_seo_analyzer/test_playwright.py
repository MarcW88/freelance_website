#!/usr/bin/env python3
"""
Test simple de Playwright pour vérifier que tout fonctionne
"""

from playwright.sync_api import sync_playwright
import time

def test_playwright():
    print("🧪 Test de Playwright...")
    
    with sync_playwright() as p:
        try:
            print("🚀 Lancement du navigateur...")
            browser = p.chromium.launch(headless=False, slow_mo=1000)
            
            print("📄 Création d'une nouvelle page...")
            page = browser.new_page()
            
            print("🌐 Navigation vers Google...")
            page.goto("https://www.google.com")
            
            print("⏳ Attente de 3 secondes...")
            time.sleep(3)
            
            title = page.title()
            print(f"📋 Titre de la page: {title}")
            
            print("🔍 Test de recherche...")
            page.fill('textarea[name="q"]', 'LinkedIn SEO')
            page.press('textarea[name="q"]', 'Enter')
            
            print("⏳ Attente des résultats...")
            page.wait_for_load_state('networkidle')
            
            print("✅ Test réussi!")
            
            input("Appuyez sur Entrée pour fermer le navigateur...")
            
            browser.close()
            
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return False
    
    return True

if __name__ == "__main__":
    success = test_playwright()
    if success:
        print("🎉 Playwright fonctionne correctement!")
    else:
        print("💥 Problème avec Playwright")
