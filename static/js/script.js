document.addEventListener('DOMContentLoaded', function () {
  // Sticky header shrink on scroll
  const header = document.querySelector('.lux-header');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      header.classList.add('shrink');
    } else {
      header.classList.remove('shrink');
    }
  });

  // Search overlay toggle
  const searchIcon = document.getElementById('search-icon');
  const searchOverlay = document.getElementById('search-overlay');
  const searchClose = document.getElementById('search-close');

  searchIcon.addEventListener('click', () => {
    searchOverlay.classList.remove('hidden');
    document.getElementById('search-input').focus();
  });

  searchClose.addEventListener('click', () => {
    searchOverlay.classList.add('hidden');
  });

  // Cart preview toggle on hover
  const cartIcon = document.getElementById('cart-icon');
  const cartPreview = document.getElementById('cart-preview');

  cartIcon.addEventListener('mouseenter', () => {
    cartPreview.classList.remove('hidden');
  });

  cartIcon.addEventListener('mouseleave', () => {
    cartPreview.classList.add('hidden');
  });

  cartPreview.addEventListener('mouseenter', () => {
    cartPreview.classList.remove('hidden');
  });

  cartPreview.addEventListener('mouseleave', () => {
    cartPreview.classList.add('hidden');
  });

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      document.querySelector(this.getAttribute('href')).scrollIntoView({
        behavior: 'smooth'
      });
    });
  });

  // Parallax effect on hero section
  const heroSection = document.querySelector('.hero-section');
  window.addEventListener('scroll', () => {
    if (heroSection) {
      const offset = window.pageYOffset;
      heroSection.style.backgroundPositionY = offset * 0.5 + 'px';
    }
  });

  // Micro-interactions for buttons
  const buttons = document.querySelectorAll('.btn-primary');
  buttons.forEach(button => {
    button.addEventListener('mouseenter', () => {
      button.style.transform = 'scale(1.05)';
      button.style.transition = 'transform 0.3s ease';
    });
    button.addEventListener('mouseleave', () => {
      button.style.transform = 'scale(1)';
    });
  });

  // Loading animation skeleton screens can be implemented as needed in page load
});

// Currency selector change handler
const currencySelector = document.getElementById('currency-selector');
if (currencySelector) {
  currencySelector.addEventListener('change', (event) => {
    const selectedCurrency = event.target.value;
    // TODO: Implement currency change logic, e.g., reload page with selected currency
    alert('Currency changed to ' + selectedCurrency + '. This feature will be implemented.');
  });
}

// Country selector change handler
const countrySelector = document.getElementById('country-selector');
if (countrySelector) {
  countrySelector.addEventListener('change', (event) => {
    const selectedCountry = event.target.value;
    // TODO: Implement country change logic, e.g., reload page with selected country
    alert('Country changed to ' + selectedCountry + '. This feature will be implemented.');
  });
}

// Product detail page image gallery functionality
function changeImage(element) {
  const mainImage = document.getElementById('main-product-image');
  mainImage.src = element.src;
}

// 360° view button click handler (placeholder)
const view360Btn = document.getElementById('view-360-btn');
if (view360Btn) {
  view360Btn.addEventListener('click', () => {
    alert('360° view feature coming soon!');
  });
}
