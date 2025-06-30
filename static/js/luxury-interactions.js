/* LUXERAZO ULTRA-PREMIUM INTERACTIONS & MICRO-ANIMATIONS */

class LuxuryExperience {
  constructor() {
    this.init();
    this.setupEventListeners();
    this.initializeAnimations();
  }

  init() {
    // Setup performance monitoring
    this.setupPerformanceMonitoring();
    
    // Initialize sound system (muted by default)
    this.initializeSoundSystem();
    
    // Setup scroll-based animations
    // Removed this.setupScrollAnimations() to prevent errors and loader-like behavior
    // this.setupScrollAnimations();
  }

  /* ===== LUXURY SOUND SYSTEM ===== */
  initializeSoundSystem() {
    this.sounds = {
      click: new Audio('/static/sounds/luxury-click.mp3'),
      hover: new Audio('/static/sounds/luxury-hover.mp3'),
      success: new Audio('/static/sounds/luxury-success.mp3')
    };
    
    // Set volume and preload
    Object.values(this.sounds).forEach(sound => {
      sound.volume = 0.3;
      sound.preload = 'auto';
    });
    
    this.soundEnabled = localStorage.getItem('luxe-sound') === 'true';
  }

  playSound(type) {
    if (this.soundEnabled && this.sounds[type]) {
      this.sounds[type].currentTime = 0;
      this.sounds[type].play().catch(() => {
        // Ignore autoplay restrictions
      });
    }
  }

  /* ===== LUXURY HEADER INTERACTIONS ===== */
  setupEventListeners() {
    // Luxury header scroll effect
    this.setupHeaderScroll();
    
    // Search modal interactions
    this.setupSearchModal();
    
    // Mobile menu interactions
    this.setupMobileMenu();
    
    // Cart preview interactions
    this.setupCartPreview();
    
    // Luxury button interactions
    this.setupButtonInteractions();
    
    // Parallax effects
    this.setupParallaxEffects();
    
    // Intersection observer for animations
    this.setupIntersectionObserver();
  }

  setupHeaderScroll() {
    const header = document.querySelector('.luxe-header');
    let lastScrollY = window.scrollY;
    let ticking = false;

    const updateHeader = () => {
      const scrollY = window.scrollY;
      
      if (scrollY > 100) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
      
      // Hide header on scroll down, show on scroll up
      if (scrollY > lastScrollY && scrollY > 200) {
        header.style.transform = 'translateY(-100%)';
      } else {
        header.style.transform = 'translateY(0)';
      }
      
      lastScrollY = scrollY;
      ticking = false;
    };

    window.addEventListener('scroll', () => {
      if (!ticking) {
        requestAnimationFrame(updateHeader);
        ticking = true;
      }
    });
  }

  setupSearchModal() {
    const searchBtn = document.querySelector('[data-search-toggle]');
    const searchModal = document.querySelector('.luxe-search-modal');
    const searchClose = document.querySelector('.luxe-search-close');
    const searchInput = document.querySelector('.luxe-search-input');

    if (searchBtn && searchModal) {
      searchBtn.addEventListener('click', (e) => {
        e.preventDefault();
        searchModal.classList.add('active');
        setTimeout(() => searchInput?.focus(), 300);
        this.playSound('click');
      });

      searchClose?.addEventListener('click', () => {
        searchModal.classList.remove('active');
        this.playSound('click');
      });

      // Close on escape key
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && searchModal.classList.contains('active')) {
          searchModal.classList.remove('active');
        }
      });

      // Close on backdrop click
      searchModal.addEventListener('click', (e) => {
        if (e.target === searchModal) {
          searchModal.classList.remove('active');
        }
      });
    }
  }

  setupMobileMenu() {
    const mobileToggle = document.querySelector('.luxe-mobile-toggle');
    const mobileMenu = document.querySelector('.luxe-mobile-menu');
    const mobileClose = document.querySelector('.luxe-mobile-menu-close');

    if (mobileToggle && mobileMenu) {
      mobileToggle.addEventListener('click', () => {
        mobileMenu.classList.add('active');
        document.body.style.overflow = 'hidden';
        this.playSound('click');
      });

      mobileClose?.addEventListener('click', () => {
        mobileMenu.classList.remove('active');
        document.body.style.overflow = '';
        this.playSound('click');
      });
    }
  }

  setupCartPreview() {
    const cartBtn = document.querySelector('[data-cart-toggle]');
    const cartPreview = document.querySelector('.luxe-cart-preview');
    let cartTimeout;

    if (cartBtn && cartPreview) {
      cartBtn.addEventListener('mouseenter', () => {
        clearTimeout(cartTimeout);
        cartPreview.classList.add('active');
      });

      cartBtn.addEventListener('mouseleave', () => {
        cartTimeout = setTimeout(() => {
          cartPreview.classList.remove('active');
        }, 300);
      });

      cartPreview.addEventListener('mouseenter', () => {
        clearTimeout(cartTimeout);
      });

      cartPreview.addEventListener('mouseleave', () => {
        cartPreview.classList.remove('active');
      });
    }
  }

  /* ===== LUXURY BUTTON INTERACTIONS ===== */
  setupButtonInteractions() {
    // Ripple effect for buttons
    document.addEventListener('click', (e) => {
      if (e.target.classList.contains('luxe-ripple') || e.target.closest('.luxe-ripple')) {
        this.createRippleEffect(e);
        this.playSound('click');
      }
    });

    // Hover sound effects
    document.querySelectorAll('.luxe-btn, .luxe-action-btn').forEach(btn => {
      btn.addEventListener('mouseenter', () => {
        this.playSound('hover');
      });
    });
  }

  createRippleEffect(e) {
    const button = e.target.classList.contains('luxe-ripple') ? e.target : e.target.closest('.luxe-ripple');
    const rect = button.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = e.clientX - rect.left - size / 2;
    const y = e.clientY - rect.top - size / 2;

    const ripple = document.createElement('span');
    ripple.className = 'luxe-ripple-effect';
    ripple.style.cssText = `
      position: absolute;
      width: ${size}px;
      height: ${size}px;
      left: ${x}px;
      top: ${y}px;
      background: radial-gradient(circle, rgba(212, 175, 55, 0.3) 0%, transparent 70%);
      border-radius: 50%;
      transform: scale(0);
      animation: luxe-ripple-animation 0.6s ease-out;
      pointer-events: none;
      z-index: 1;
    `;

    button.appendChild(ripple);

    setTimeout(() => ripple.remove(), 600);
  }

  /* ===== PARALLAX EFFECTS ===== */
  setupParallaxEffects() {
    const parallaxElements = document.querySelectorAll('[data-parallax]');
    
    if (parallaxElements.length === 0) return;

    let ticking = false;

    const updateParallax = () => {
      const scrollY = window.scrollY;

      parallaxElements.forEach(element => {
        const speed = parseFloat(element.dataset.parallax) || 0.5;
        const yPos = -(scrollY * speed);
        element.style.transform = `translateY(${yPos}px)`;
      });

      ticking = false;
    };

    window.addEventListener('scroll', () => {
      if (!ticking) {
        requestAnimationFrame(updateParallax);
        ticking = true;
      }
    });
  }

  /* ===== SCROLL ANIMATIONS ===== */
  setupIntersectionObserver() {
    const observerOptions = {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('luxe-animate-in');
          
          // Stagger animations for child elements
          const children = entry.target.querySelectorAll('[data-animate-delay]');
          children.forEach((child, index) => {
            const delay = child.dataset.animateDelay || (index * 100);
            setTimeout(() => {
              child.classList.add('luxe-animate-in');
            }, parseInt(delay));
          });
        }
      });
    }, observerOptions);

    // Observe elements with animation classes
    document.querySelectorAll('[data-animate]').forEach(el => {
      observer.observe(el);
    });
  }

  /* ===== PERFORMANCE MONITORING ===== */
  setupPerformanceMonitoring() {
    // Monitor Core Web Vitals
    if ('web-vital' in window) {
      import('web-vitals').then(({ getCLS, getFID, getFCP, getLCP, getTTFB }) => {
        getCLS(console.log);
        getFID(console.log);
        getFCP(console.log);
        getLCP(console.log);
        getTTFB(console.log);
      });
    }

    // Preload critical resources
    this.preloadCriticalResources();
  }

  preloadCriticalResources() {
    const criticalImages = [
      '/static/img/hero1.jpg',
      '/static/img/hero2.jpg',
      '/static/img/luxerazo-logo.png'
    ];

    criticalImages.forEach(src => {
      const link = document.createElement('link');
      link.rel = 'preload';
      link.as = 'image';
      link.href = src;
      document.head.appendChild(link);
    });
  }

  /* ===== LUXURY ANIMATIONS INITIALIZATION ===== */
  initializeAnimations() {
    // Add CSS for animations
    const style = document.createElement('style');
    style.textContent = `
      @keyframes luxe-ripple-animation {
        to {
          transform: scale(4);
          opacity: 0;
        }
      }

      [data-animate] {
        opacity: 0;
        transform: translateY(30px);
        transition: all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
      }

      [data-animate].luxe-animate-in {
        opacity: 1;
        transform: translateY(0);
      }
    `;
    document.head.appendChild(style);
  }

  /* ===== UTILITY METHODS ===== */
  toggleSound() {
    this.soundEnabled = !this.soundEnabled;
    localStorage.setItem('luxe-sound', this.soundEnabled.toString());
    
    if (this.soundEnabled) {
      this.playSound('success');
    }
  }

  // Smooth scroll to element
  scrollToElement(selector, offset = 0) {
    const element = document.querySelector(selector);
    if (element) {
      const elementPosition = element.getBoundingClientRect().top + window.pageYOffset;
      const offsetPosition = elementPosition - offset;

      window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
      });
    }
  }

  // Add to cart with luxury animation
  addToCart(productId, callback) {
    // Create floating animation
    const cartIcon = document.querySelector('[data-cart-toggle]');
    if (cartIcon) {
      const floatingIcon = document.createElement('div');
      floatingIcon.innerHTML = '<i class="fas fa-shopping-bag"></i>';
      floatingIcon.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 2rem;
        color: var(--luxe-gold);
        pointer-events: none;
        z-index: 9999;
        animation: luxe-float-to-cart 1s ease-out forwards;
      `;

      document.body.appendChild(floatingIcon);

      setTimeout(() => {
        floatingIcon.remove();
        this.playSound('success');
        if (callback) callback();
      }, 1000);
    }
  }
}

/* ===== INITIALIZE LUXURY EXPERIENCE ===== */
document.addEventListener('DOMContentLoaded', () => {
  window.luxeExperience = new LuxuryExperience();
  
  // Add floating animation keyframes
  const floatAnimation = document.createElement('style');
  floatAnimation.textContent = `
    @keyframes luxe-float-to-cart {
      0% {
        transform: translate(-50%, -50%) scale(1);
        opacity: 1;
      }
      50% {
        transform: translate(-50%, -60%) scale(1.2);
        opacity: 0.8;
      }
      100% {
        transform: translate(calc(100vw - 100px), -90%) scale(0.5);
        opacity: 0;
      }
    }
  `;
  document.head.appendChild(floatAnimation);
});

/* ===== EXPORT FOR MODULE USAGE ===== */
if (typeof module !== 'undefined' && module.exports) {
  module.exports = LuxuryExperience;
}
