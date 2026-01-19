/**
 * Clear Choice Restoration - Main JavaScript
 * Handles site-wide functionality: navigation, animations, forms
 */

document.addEventListener('DOMContentLoaded', function() {
  // Initialize all modules
  initMobileNav();
  initScrollReveal();
  initHeaderScroll();
  initSmoothScroll();
  initFAQAccordion();
  initLightbox();
});

/**
 * Mobile Navigation
 */
function initMobileNav() {
  const toggle = document.querySelector('.mobile-menu-toggle');
  const mobileNav = document.querySelector('.mobile-nav');

  if (!toggle || !mobileNav) return;

  toggle.addEventListener('click', function() {
    this.classList.toggle('active');
    mobileNav.classList.toggle('active');
    document.body.style.overflow = mobileNav.classList.contains('active') ? 'hidden' : '';
  });

  // Close menu when clicking a link
  mobileNav.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', function() {
      toggle.classList.remove('active');
      mobileNav.classList.remove('active');
      document.body.style.overflow = '';
    });
  });

  // Close menu on escape key
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && mobileNav.classList.contains('active')) {
      toggle.classList.remove('active');
      mobileNav.classList.remove('active');
      document.body.style.overflow = '';
    }
  });
}

/**
 * Scroll Reveal Animations
 */
function initScrollReveal() {
  const reveals = document.querySelectorAll('[data-reveal]');

  if (!reveals.length) return;

  const revealOnScroll = () => {
    const windowHeight = window.innerHeight;
    const revealPoint = 100;

    reveals.forEach(element => {
      const elementTop = element.getBoundingClientRect().top;

      if (elementTop < windowHeight - revealPoint) {
        element.classList.add('revealed');
      }
    });
  };

  // Initial check
  revealOnScroll();

  // Throttled scroll listener
  let ticking = false;
  window.addEventListener('scroll', function() {
    if (!ticking) {
      window.requestAnimationFrame(function() {
        revealOnScroll();
        ticking = false;
      });
      ticking = true;
    }
  });
}

/**
 * Header Scroll Effect
 */
function initHeaderScroll() {
  const header = document.querySelector('.site-header');

  if (!header) return;

  const scrollThreshold = 50;

  const updateHeader = () => {
    if (window.scrollY > scrollThreshold) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  };

  // Initial check
  updateHeader();

  // Throttled scroll listener
  let ticking = false;
  window.addEventListener('scroll', function() {
    if (!ticking) {
      window.requestAnimationFrame(function() {
        updateHeader();
        ticking = false;
      });
      ticking = true;
    }
  });
}

/**
 * Smooth Scroll for Anchor Links
 */
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const targetId = this.getAttribute('href');

      if (targetId === '#') return;

      const target = document.querySelector(targetId);

      if (target) {
        e.preventDefault();
        const headerOffset = 100;
        const elementPosition = target.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

        window.scrollTo({
          top: offsetPosition,
          behavior: 'smooth'
        });
      }
    });
  });
}

/**
 * FAQ Accordion
 */
function initFAQAccordion() {
  const faqItems = document.querySelectorAll('.faq-item');

  if (!faqItems.length) return;

  faqItems.forEach(item => {
    const question = item.querySelector('.faq-question');

    if (question) {
      question.addEventListener('click', function() {
        const isActive = item.classList.contains('active');

        // Close all other items
        faqItems.forEach(otherItem => {
          if (otherItem !== item) {
            otherItem.classList.remove('active');
          }
        });

        // Toggle current item
        item.classList.toggle('active', !isActive);
      });
    }
  });
}

/**
 * Lightbox for Gallery
 */
function initLightbox() {
  const galleryItems = document.querySelectorAll('.gallery-item');
  const lightbox = document.querySelector('.lightbox');

  if (!galleryItems.length || !lightbox) return;

  const lightboxImg = lightbox.querySelector('img');
  const lightboxClose = lightbox.querySelector('.lightbox-close');

  galleryItems.forEach(item => {
    item.addEventListener('click', function() {
      const img = this.querySelector('img');
      if (img) {
        lightboxImg.src = img.src;
        lightboxImg.alt = img.alt;
        lightbox.classList.add('active');
        document.body.style.overflow = 'hidden';
      }
    });
  });

  // Close lightbox
  const closeLightbox = () => {
    lightbox.classList.remove('active');
    document.body.style.overflow = '';
  };

  if (lightboxClose) {
    lightboxClose.addEventListener('click', closeLightbox);
  }

  lightbox.addEventListener('click', function(e) {
    if (e.target === lightbox) {
      closeLightbox();
    }
  });

  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && lightbox.classList.contains('active')) {
      closeLightbox();
    }
  });
}

/**
 * Form Validation
 */
function initFormValidation(formSelector) {
  const form = document.querySelector(formSelector);

  if (!form) return;

  form.addEventListener('submit', function(e) {
    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');

    requiredFields.forEach(field => {
      const errorEl = field.parentNode.querySelector('.form-error');

      // Clear previous error
      field.classList.remove('error');
      if (errorEl) errorEl.remove();

      // Check if empty
      if (!field.value.trim()) {
        isValid = false;
        field.classList.add('error');
        const error = document.createElement('span');
        error.className = 'form-error';
        error.textContent = 'This field is required';
        field.parentNode.appendChild(error);
      }

      // Email validation
      if (field.type === 'email' && field.value.trim()) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(field.value)) {
          isValid = false;
          field.classList.add('error');
          const error = document.createElement('span');
          error.className = 'form-error';
          error.textContent = 'Please enter a valid email address';
          field.parentNode.appendChild(error);
        }
      }

      // Phone validation
      if (field.type === 'tel' && field.value.trim()) {
        const phoneRegex = /^[\d\s\-\(\)]+$/;
        if (!phoneRegex.test(field.value) || field.value.replace(/\D/g, '').length < 10) {
          isValid = false;
          field.classList.add('error');
          const error = document.createElement('span');
          error.className = 'form-error';
          error.textContent = 'Please enter a valid phone number';
          field.parentNode.appendChild(error);
        }
      }
    });

    if (!isValid) {
      e.preventDefault();
      // Scroll to first error
      const firstError = form.querySelector('.error');
      if (firstError) {
        firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
        firstError.focus();
      }
    }
  });

  // Real-time validation on blur
  form.querySelectorAll('input, textarea, select').forEach(field => {
    field.addEventListener('blur', function() {
      const errorEl = this.parentNode.querySelector('.form-error');
      if (errorEl) {
        this.classList.remove('error');
        errorEl.remove();
      }
    });
  });
}

/**
 * Phone Number Formatting
 */
function formatPhoneInput(input) {
  if (!input) return;

  input.addEventListener('input', function(e) {
    let value = e.target.value.replace(/\D/g, '');

    if (value.length > 10) {
      value = value.slice(0, 10);
    }

    if (value.length >= 6) {
      value = `(${value.slice(0, 3)}) ${value.slice(3, 6)}-${value.slice(6)}`;
    } else if (value.length >= 3) {
      value = `(${value.slice(0, 3)}) ${value.slice(3)}`;
    }

    e.target.value = value;
  });
}

/**
 * Utility: Debounce function
 */
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

/**
 * Utility: Throttle function
 */
function throttle(func, limit) {
  let inThrottle;
  return function(...args) {
    if (!inThrottle) {
      func.apply(this, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

// Expose utilities for use in other scripts
window.CCR = {
  initFormValidation,
  formatPhoneInput,
  debounce,
  throttle
};
