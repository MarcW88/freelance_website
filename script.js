// Marc Williame - Consultant SEO orienté Data & IA
// JavaScript pour interactions et animations

document.addEventListener('DOMContentLoaded', function() {
  
  // Initialize AOS (Animate On Scroll)
  AOS.init({
    duration: 800,
    easing: 'ease-out-cubic',
    once: true,
    offset: 100
  });
  
  // Initialize Lucide Icons
  lucide.createIcons();
  
  // Navigation scroll effect
  const nav = document.getElementById('nav');
  let lastScrollY = window.scrollY;
  
  window.addEventListener('scroll', () => {
    const currentScrollY = window.scrollY;
    
    if (currentScrollY > 100) {
      nav.style.background = 'rgba(14, 17, 23, 0.98)';
      nav.style.backdropFilter = 'blur(20px)';
    } else {
      nav.style.background = 'rgba(14, 17, 23, 0.95)';
      nav.style.backdropFilter = 'blur(10px)';
    }
    
    // Hide/show nav on scroll
    if (currentScrollY > lastScrollY && currentScrollY > 200) {
      nav.style.transform = 'translateY(-100%)';
    } else {
      nav.style.transform = 'translateY(0)';
    }
    
    lastScrollY = currentScrollY;
  });
  
  // Mobile navigation toggle
  const navToggle = document.getElementById('nav-toggle');
  const navLinks = document.querySelector('.nav-links');
  
  if (navToggle && navLinks) {
    navToggle.addEventListener('click', () => {
      navLinks.classList.toggle('active');
      navToggle.classList.toggle('active');
    });
  }
  
  // Smooth scroll for navigation links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        const offsetTop = target.offsetTop - 80; // Account for fixed nav
        window.scrollTo({
          top: offsetTop,
          behavior: 'smooth'
        });
      }
    });
  });
  
  // Contact form handling
  const contactForm = document.querySelector('.contact-form');
  if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
      e.preventDefault();
      
      // Get form data
      const formData = new FormData(this);
      const name = formData.get('name');
      const email = formData.get('email');
      const message = formData.get('message');
      
      // Basic validation
      if (!name || !email || !message) {
        alert('Veuillez remplir tous les champs.');
        return;
      }
      
      // Email validation
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email)) {
        alert('Veuillez entrer une adresse email valide.');
        return;
      }
      
      // Simulate form submission
      const submitBtn = this.querySelector('button[type="submit"]');
      const originalText = submitBtn.innerHTML;
      
      submitBtn.innerHTML = '<i data-lucide="loader-2"></i> Envoi en cours...';
      submitBtn.disabled = true;
      
      // Simulate API call
      setTimeout(() => {
        alert('Message envoyé ! Je vous répondrai sous 24h.');
        this.reset();
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
        lucide.createIcons(); // Reinitialize icons
      }, 2000);
    });
  }
  
  // Add hover effects to service cards
  const serviceCards = document.querySelectorAll('.service-card');
  serviceCards.forEach(card => {
    card.addEventListener('mouseenter', function() {
      this.style.transform = 'translateY(-8px) scale(1.02)';
    });
    
    card.addEventListener('mouseleave', function() {
      this.style.transform = 'translateY(0) scale(1)';
    });
  });
  
  // Add pulse effect to data icons on scroll
  const dataIcons = document.querySelectorAll('.data-icon.pulse');
  const observerOptions = {
    threshold: 0.5,
    rootMargin: '0px 0px -100px 0px'
  };
  
  const iconObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.animationPlayState = 'running';
      }
    });
  }, observerOptions);
  
  dataIcons.forEach(icon => {
    icon.style.animationPlayState = 'paused';
    iconObserver.observe(icon);
  });
  
  // Typing effect for hero title (optional enhancement)
  const heroTitle = document.querySelector('.hero h1');
  if (heroTitle) {
    const text = heroTitle.textContent;
    heroTitle.textContent = '';
    
    let i = 0;
    const typeWriter = () => {
      if (i < text.length) {
        heroTitle.textContent += text.charAt(i);
        i++;
        setTimeout(typeWriter, 50);
      }
    };
    
    // Start typing effect after a delay
    setTimeout(typeWriter, 1000);
  }
  
  // Performance optimization: Lazy load images
  const images = document.querySelectorAll('img[data-src]');
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
  
  images.forEach(img => imageObserver.observe(img));
  
  // Add loading states for buttons
  document.querySelectorAll('.btn').forEach(btn => {
    btn.addEventListener('click', function(e) {
      if (this.classList.contains('btn-glow')) {
        this.style.boxShadow = '0 0 40px rgba(24, 212, 183, 0.3)';
        setTimeout(() => {
          this.style.boxShadow = '';
        }, 300);
      }
    });
  });
  
  // Console message for developers
  console.log(`
    🚀 Marc Williame - Consultant SEO orienté Data & IA
    
    Site construit avec :
    - Design System moderne inspiré de Linear.app
    - Animations AOS et micro-interactions
    - Performance optimisée
    - SEO-ready
    
    Contact : marc@marcwilliame.be
  `);
  
});

// Utility functions
const utils = {
  // Debounce function for performance
  debounce: (func, wait) => {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  },
  
  // Check if element is in viewport
  isInViewport: (element) => {
    const rect = element.getBoundingClientRect();
    return (
      rect.top >= 0 &&
      rect.left >= 0 &&
      rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
      rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
  },
  
  // Smooth scroll to element
  scrollTo: (element, offset = 80) => {
    const elementPosition = element.offsetTop - offset;
    window.scrollTo({
      top: elementPosition,
      behavior: 'smooth'
    });
  }
};

// Export utils for potential use in other scripts
window.MarcWilliameUtils = utils;
