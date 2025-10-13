// Blog JavaScript - Marc Williame
// Interactions et filtres pour le blog

document.addEventListener('DOMContentLoaded', function() {
  
  // Article filtering functionality
  const filterButtons = document.querySelectorAll('.filter-btn');
  const articleCards = document.querySelectorAll('.article-card');
  const categoryCards = document.querySelectorAll('.category-card');
  
  // Filter articles by category
  function filterArticles(category) {
    articleCards.forEach(card => {
      const cardCategory = card.getAttribute('data-category');
      
      if (category === 'all' || cardCategory === category) {
        card.classList.remove('hidden');
        card.classList.add('show');
      } else {
        card.classList.add('hidden');
        card.classList.remove('show');
      }
    });
  }
  
  // Handle filter button clicks
  filterButtons.forEach(button => {
    button.addEventListener('click', function() {
      const category = this.getAttribute('data-filter');
      
      // Update active button
      filterButtons.forEach(btn => btn.classList.remove('active'));
      this.classList.add('active');
      
      // Filter articles
      filterArticles(category);
      
      // Update URL without page reload
      const url = new URL(window.location);
      if (category === 'all') {
        url.searchParams.delete('category');
      } else {
        url.searchParams.set('category', category);
      }
      window.history.pushState({}, '', url);
    });
  });
  
  // Handle category card clicks
  categoryCards.forEach(card => {
    card.addEventListener('click', function() {
      const category = this.getAttribute('data-category');
      
      // Update filter buttons
      filterButtons.forEach(btn => btn.classList.remove('active'));
      const targetButton = document.querySelector(`[data-filter="${category}"]`);
      if (targetButton) {
        targetButton.classList.add('active');
      }
      
      // Filter articles
      filterArticles(category);
      
      // Scroll to articles section
      const articlesSection = document.querySelector('.articles-grid');
      if (articlesSection) {
        articlesSection.scrollIntoView({ 
          behavior: 'smooth', 
          block: 'start' 
        });
      }
      
      // Update URL
      const url = new URL(window.location);
      url.searchParams.set('category', category);
      window.history.pushState({}, '', url);
    });
  });
  
  // Initialize filter from URL parameter
  function initializeFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    const category = urlParams.get('category');
    
    if (category) {
      // Update active button
      filterButtons.forEach(btn => btn.classList.remove('active'));
      const targetButton = document.querySelector(`[data-filter="${category}"]`);
      if (targetButton) {
        targetButton.classList.add('active');
        filterArticles(category);
      }
    }
  }
  
  // Newsletter form handling
  const newsletterForm = document.querySelector('.newsletter-form');
  if (newsletterForm) {
    newsletterForm.addEventListener('submit', function(e) {
      e.preventDefault();
      
      const emailInput = this.querySelector('input[type="email"]');
      const submitBtn = this.querySelector('button[type="submit"]');
      const email = emailInput.value;
      
      // Basic email validation
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email)) {
        alert('Veuillez entrer une adresse email valide.');
        return;
      }
      
      // Simulate subscription
      const originalText = submitBtn.innerHTML;
      submitBtn.innerHTML = '<i data-lucide="loader-2"></i> Inscription...';
      submitBtn.disabled = true;
      
      setTimeout(() => {
        alert('Merci ! Vous êtes maintenant abonné aux updates.');
        emailInput.value = '';
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
        lucide.createIcons(); // Reinitialize icons
      }, 2000);
    });
  }
  
  // Article card hover effects
  articleCards.forEach(card => {
    card.addEventListener('mouseenter', function() {
      this.style.transform = 'translateY(-8px)';
    });
    
    card.addEventListener('mouseleave', function() {
      this.style.transform = 'translateY(0)';
    });
  });
  
  // Category card hover effects
  categoryCards.forEach(card => {
    card.addEventListener('mouseenter', function() {
      this.style.transform = 'translateY(-6px)';
    });
    
    card.addEventListener('mouseleave', function() {
      this.style.transform = 'translateY(0)';
    });
  });
  
  // Reading time estimation for articles
  function estimateReadingTime(text) {
    const wordsPerMinute = 200;
    const words = text.trim().split(/\s+/).length;
    const minutes = Math.ceil(words / wordsPerMinute);
    return minutes;
  }
  
  // Add reading progress indicator (for individual article pages)
  function addReadingProgress() {
    const article = document.querySelector('article.blog-post');
    if (!article) return;
    
    const progressBar = document.createElement('div');
    progressBar.className = 'reading-progress';
    progressBar.innerHTML = '<div class="progress-fill"></div>';
    document.body.appendChild(progressBar);
    
    const progressFill = progressBar.querySelector('.progress-fill');
    
    window.addEventListener('scroll', () => {
      const articleHeight = article.offsetHeight;
      const articleTop = article.offsetTop;
      const scrolled = window.scrollY - articleTop;
      const progress = Math.max(0, Math.min(100, (scrolled / articleHeight) * 100));
      
      progressFill.style.width = progress + '%';
    });
  }
  
  // Search functionality (basic)
  function addSearchFunctionality() {
    const searchInput = document.querySelector('.blog-search');
    if (!searchInput) return;
    
    searchInput.addEventListener('input', function() {
      const searchTerm = this.value.toLowerCase();
      
      articleCards.forEach(card => {
        const title = card.querySelector('h3').textContent.toLowerCase();
        const excerpt = card.querySelector('.article-excerpt').textContent.toLowerCase();
        const tags = Array.from(card.querySelectorAll('.tag')).map(tag => tag.textContent.toLowerCase());
        
        const matches = title.includes(searchTerm) || 
                       excerpt.includes(searchTerm) || 
                       tags.some(tag => tag.includes(searchTerm));
        
        if (matches || searchTerm === '') {
          card.classList.remove('hidden');
          card.classList.add('show');
        } else {
          card.classList.add('hidden');
          card.classList.remove('show');
        }
      });
    });
  }
  
  // Social sharing (for individual articles)
  function addSocialSharing() {
    const shareButtons = document.querySelectorAll('.share-btn');
    
    shareButtons.forEach(button => {
      button.addEventListener('click', function(e) {
        e.preventDefault();
        
        const platform = this.getAttribute('data-platform');
        const url = encodeURIComponent(window.location.href);
        const title = encodeURIComponent(document.title);
        
        let shareUrl = '';
        
        switch (platform) {
          case 'twitter':
            shareUrl = `https://twitter.com/intent/tweet?url=${url}&text=${title}`;
            break;
          case 'linkedin':
            shareUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${url}`;
            break;
          case 'facebook':
            shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${url}`;
            break;
        }
        
        if (shareUrl) {
          window.open(shareUrl, '_blank', 'width=600,height=400');
        }
      });
    });
  }
  
  // Copy link functionality
  function addCopyLinkFunctionality() {
    const copyButtons = document.querySelectorAll('.copy-link-btn');
    
    copyButtons.forEach(button => {
      button.addEventListener('click', function() {
        navigator.clipboard.writeText(window.location.href).then(() => {
          const originalText = this.textContent;
          this.textContent = 'Copié !';
          this.style.color = 'var(--color-accent)';
          
          setTimeout(() => {
            this.textContent = originalText;
            this.style.color = '';
          }, 2000);
        });
      });
    });
  }
  
  // Article view tracking (basic analytics)
  function trackArticleView() {
    const article = document.querySelector('article.blog-post');
    if (!article) return;
    
    const articleId = article.getAttribute('data-article-id');
    if (!articleId) return;
    
    // Track when user has read 50% of the article
    let tracked = false;
    
    window.addEventListener('scroll', () => {
      if (tracked) return;
      
      const articleHeight = article.offsetHeight;
      const articleTop = article.offsetTop;
      const scrolled = window.scrollY - articleTop;
      const progress = (scrolled / articleHeight) * 100;
      
      if (progress >= 50) {
        tracked = true;
        
        // Send analytics event (replace with your analytics service)
        console.log(`Article ${articleId} read 50%`);
        
        // Example: Google Analytics 4
        if (typeof gtag !== 'undefined') {
          gtag('event', 'article_read_50', {
            'article_id': articleId,
            'article_title': document.title
          });
        }
      }
    });
  }
  
  // Initialize all functionality
  initializeFromURL();
  addReadingProgress();
  addSearchFunctionality();
  addSocialSharing();
  addCopyLinkFunctionality();
  trackArticleView();
  
  // Handle browser back/forward buttons
  window.addEventListener('popstate', function() {
    initializeFromURL();
  });
  
  // Lazy loading for article images (if any)
  const articleImages = document.querySelectorAll('img[data-src]');
  if (articleImages.length > 0) {
    const imageObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          img.removeAttribute('data-src');
          imageObserver.unobserve(img);
        }
      });
    });
    
    articleImages.forEach(img => imageObserver.observe(img));
  }
  
  console.log('Blog functionality initialized');
});
