// Theme Toggle - Dark/Light Mode
// Marc Williame - Consultant SEO Data & IA

class ThemeToggle {
  constructor() {
    this.currentTheme = this.getStoredTheme() || this.getPreferredTheme();
    this.init();
  }
  
  init() {
    // Apply initial theme
    this.applyTheme(this.currentTheme);
    
    // Create toggle button
    this.createToggleButton();
    
    // Listen for system theme changes
    this.watchSystemTheme();
  }
  
  getStoredTheme() {
    return localStorage.getItem('theme');
  }
  
  getPreferredTheme() {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  
  setStoredTheme(theme) {
    localStorage.setItem('theme', theme);
  }
  
  applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    this.updateToggleButton(theme);
    
    // Update meta theme-color for mobile browsers
    const metaThemeColor = document.querySelector('meta[name="theme-color"]');
    if (metaThemeColor) {
      metaThemeColor.setAttribute('content', theme === 'dark' ? '#0E1117' : '#FFFFFF');
    }
  }
  
  createToggleButton() {
    // Check if button already exists
    if (document.querySelector('.theme-toggle')) return;
    
    const toggleButton = document.createElement('button');
    toggleButton.className = 'theme-toggle';
    toggleButton.setAttribute('aria-label', 'Basculer le thème');
    toggleButton.innerHTML = `
      <div class="toggle-icon">
        <i data-lucide="sun" class="sun-icon"></i>
        <i data-lucide="moon" class="moon-icon"></i>
      </div>
    `;
    
    // Add to navigation
    const nav = document.querySelector('.nav .container');
    if (nav) {
      nav.appendChild(toggleButton);
    }
    
    // Add event listener
    toggleButton.addEventListener('click', () => this.toggleTheme());
    
    // Initialize icons
    if (typeof lucide !== 'undefined') {
      lucide.createIcons();
    }
  }
  
  updateToggleButton(theme) {
    const toggleButton = document.querySelector('.theme-toggle');
    if (toggleButton) {
      toggleButton.setAttribute('data-theme', theme);
    }
  }
  
  toggleTheme() {
    const newTheme = this.currentTheme === 'light' ? 'dark' : 'light';
    this.currentTheme = newTheme;
    this.setStoredTheme(newTheme);
    this.applyTheme(newTheme);
    
    // Trigger custom event for other components
    window.dispatchEvent(new CustomEvent('themeChanged', { 
      detail: { theme: newTheme } 
    }));
  }
  
  watchSystemTheme() {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    mediaQuery.addEventListener('change', (e) => {
      // Only update if user hasn't manually set a preference
      if (!this.getStoredTheme()) {
        const newTheme = e.matches ? 'dark' : 'light';
        this.currentTheme = newTheme;
        this.applyTheme(newTheme);
      }
    });
  }
}

// Initialize theme toggle when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
  new ThemeToggle();
});
