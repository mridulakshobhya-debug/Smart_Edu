/* ============================================================================
   SmartEdu Pro - Advanced JavaScript System
   Theme Management, Animations, and Premium Features
   ============================================================================ */

class ThemeManager {
  constructor() {
    this.theme = localStorage.getItem('theme') || 'light';
    this.init();
  }

  init() {
    this.applyTheme();
    this.createToggleButton();
    this.setupToggleListener();
  }

  applyTheme() {
    const root = document.documentElement;
    root.setAttribute('data-theme', this.theme);
    document.body.style.transition = 'background-color 300ms cubic-bezier(0.4, 0, 0.2, 1)';
  }

  createToggleButton() {
    const nav = document.querySelector('nav ul');
    const authPage = document.querySelector('.auth-page');
    const welcomePage = document.querySelector('.welcome-container');
    
    // Check if we're on a welcome page
    if (welcomePage) {
      const welcomeToggle = document.querySelector('.welcome-theme-toggle');
      if (welcomeToggle) {
        this.toggleButton = welcomeToggle;
        this.updateToggleIcon();
        return;
      }
    }
    
    // Check if we're on an auth page
    if (authPage) {
      const authToggle = document.querySelector('.auth-theme-toggle');
      if (authToggle) {
        this.toggleButton = authToggle;
        this.updateToggleIcon();
        return;
      }
    }
    
    // Regular nav toggle
    if (!nav) return;

    // Check if toggle already exists
    if (document.querySelector('.theme-toggle')) return;

    const toggle = document.createElement('button');
    toggle.className = 'theme-toggle';
    toggle.setAttribute('aria-label', 'Toggle theme');
    toggle.innerHTML = this.theme === 'dark' ? '☀️' : '🌙';
    toggle.style.marginLeft = 'auto';

    nav.appendChild(toggle);
    this.toggleButton = toggle;
  }

  setupToggleListener() {
    if (this.toggleButton) {
      // Use arrow function to preserve 'this' context
      this.toggleButton.onclick = () => {
        this.theme = this.theme === 'light' ? 'dark' : 'light';
        localStorage.setItem('theme', this.theme);
        this.applyTheme();
        this.updateToggleIcon();
      };
    }
  }

  toggle() {
    this.theme = this.theme === 'light' ? 'dark' : 'light';
    localStorage.setItem('theme', this.theme);
    this.applyTheme();
    this.updateToggleIcon();
  }

  updateToggleIcon() {
    if (this.toggleButton) {
      const icon = this.toggleButton.querySelector('.theme-icon') || this.toggleButton;
      icon.innerHTML = this.theme === 'dark' ? '☀️' : '🌙';
    }
  }
}

/* ============================================================================
   Utility Functions
   ============================================================================ */

const debounce = (func, wait = 300) => {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
};

const throttle = (func, limit = 300) => {
  let lastFunc, lastRan;
  return function(...args) {
    if (!lastRan) {
      func.apply(this, args);
      lastRan = Date.now();
    } else {
      clearTimeout(lastFunc);
      lastFunc = setTimeout(() => {
        if ((Date.now() - lastRan) >= limit) {
          func.apply(this, args);
          lastRan = Date.now();
        }
      }, limit - (Date.now() - lastRan));
    }
  };
};

const animate = (element, animationClass) => {
  element.classList.add(animationClass);
  element.addEventListener('animationend', () => {
    element.classList.remove(animationClass);
  }, { once: true });
};

/* ============================================================================
   Notification System
   ============================================================================ */

const showNotification = (message, type = 'info', duration = 3000) => {
  const notification = document.createElement('div');
  notification.className = `alert alert-${type}`;
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 10000;
    max-width: 400px;
    animation: slideInDown 0.3s ease-out;
  `;
  notification.textContent = message;
  
  document.body.appendChild(notification);
  
  setTimeout(() => {
    notification.style.animation = 'slideInUp 0.3s ease-out forwards';
    setTimeout(() => notification.remove(), 300);
  }, duration);
};

/* ============================================================================
   Form Handler
   ============================================================================ */

class FormHandler {
  constructor(formSelector) {
    this.form = document.querySelector(formSelector);
    if (!this.form) return;
    
    // Skip FormHandler for auth forms - they need normal submission for redirects
    if (this.form.classList.contains('auth-form')) {
      return;
    }
    
    this.init();
  }

  init() {
    this.form.addEventListener('submit', (e) => this.handleSubmit(e));
    this.setupFieldValidation();
  }

  handleSubmit(e) {
    e.preventDefault();
    
    if (!this.validate()) {
      showNotification('Please fill in all required fields correctly', 'danger');
      return;
    }

    this.submit();
  }

  validate() {
    const fields = this.form.querySelectorAll('[required]');
    let isValid = true;

    fields.forEach(field => {
      if (!field.value.trim()) {
        this.setFieldError(field, 'This field is required');
        isValid = false;
      } else {
        this.clearFieldError(field);
      }
    });

    return isValid;
  }

  setupFieldValidation() {
    this.form.querySelectorAll('input, textarea').forEach(field => {
      field.addEventListener('blur', () => {
        if (field.required && !field.value.trim()) {
          this.setFieldError(field, 'This field is required');
        } else {
          this.clearFieldError(field);
        }
      });
    });
  }

  setFieldError(field, message) {
    field.style.borderColor = '#ef4444';
    field.title = message;
  }

  clearFieldError(field) {
    field.style.borderColor = '';
    field.title = '';
  }

  submit() {
    const formData = new FormData(this.form);
    const action = this.form.action || window.location.href;

    fetch(action, {
      method: this.form.method || 'POST',
      body: formData
    })
    .then(response => response.ok ? response.text() : Promise.reject(response))
    .then(data => {
      showNotification('Form submitted successfully!', 'success');
      this.form.reset();
    })
    .catch(error => {
      showNotification('Error submitting form. Please try again.', 'danger');
      console.error('Form submission error:', error);
    });
  }
}

/* ============================================================================
   Scroll Animations
   ============================================================================ */

class ScrollAnimator {
  constructor() {
    this.elements = document.querySelectorAll('[data-animate]');
    if (this.elements.length === 0) return;
    this.init();
  }

  init() {
    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('fade-in');
            observer.unobserve(entry.target);
          }
        });
      }, { threshold: 0.1 });

      this.elements.forEach(el => observer.observe(el));
    } else {
      this.elements.forEach(el => el.classList.add('fade-in'));
    }
  }
}

/* ============================================================================
   Lazy Loading Images
   ============================================================================ */

const setupLazyLoading = () => {
  const images = document.querySelectorAll('[data-src]');
  
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          img.removeAttribute('data-src');
          observer.unobserve(img);
        }
      });
    });

    images.forEach(img => observer.observe(img));
  } else {
    images.forEach(img => {
      img.src = img.dataset.src;
    });
  }
};

/* ============================================================================
   Smooth Scrolling
   ============================================================================ */

const setupSmoothScroll = () => {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      e.preventDefault();
      const target = document.querySelector(anchor.getAttribute('href'));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });
};

/* ============================================================================
   Navigation Active State
   ============================================================================ */

const setupActiveNavigation = () => {
  const navLinks = document.querySelectorAll('nav a');
  
  window.addEventListener('scroll', throttle(() => {
    let current = '';
    
    document.querySelectorAll('section').forEach(section => {
      const sectionTop = section.offsetTop;
      const sectionHeight = section.clientHeight;
      if (pageYOffset >= sectionTop - 200) {
        current = section.getAttribute('id');
      }
    });

    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href').slice(1) === current) {
        link.classList.add('active');
      }
    });
  }));
};

/* ============================================================================
   Button Ripple Effect
   ============================================================================ */

const setupRippleEffect = () => {
  const buttons = document.querySelectorAll('button, .btn');
  
  buttons.forEach(button => {
    button.addEventListener('click', function(e) {
      const rect = this.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      const ripple = document.createElement('span');
      ripple.style.position = 'absolute';
      ripple.style.left = x + 'px';
      ripple.style.top = y + 'px';
      ripple.style.width = '20px';
      ripple.style.height = '20px';
      ripple.style.background = 'rgba(255, 255, 255, 0.6)';
      ripple.style.borderRadius = '50%';
      ripple.style.transform = 'scale(0)';
      ripple.style.animation = 'ripple-animation 0.6s ease-out';
      ripple.style.pointerEvents = 'none';
      
      this.appendChild(ripple);
      
      setTimeout(() => ripple.remove(), 600);
    });
  });
};

/* ============================================================================
   Analytics
   ============================================================================ */

const trackEvent = (category, action, label) => {
  if (typeof gtag !== 'undefined') {
    gtag('event', action, {
      'event_category': category,
      'event_label': label
    });
  }
  console.log(`Event: ${category} - ${action} - ${label}`);
};

/* ============================================================================
   Performance Monitoring
   ============================================================================ */

const measurePerformance = () => {
  if ('PerformanceObserver' in window) {
    try {
      const observer = new PerformanceObserver((list) => {
        list.getEntries().forEach((entry) => {
          console.log(`${entry.name}: ${entry.duration.toFixed(2)}ms`);
        });
      });

      observer.observe({ entryTypes: ['measure', 'navigation'] });
    } catch (e) {
      console.log('PerformanceObserver not supported');
    }
  }
};

/* ============================================================================
   Modal Management
   ============================================================================ */

class Modal {
  constructor(modalSelector) {
    this.modal = document.querySelector(modalSelector);
    if (!this.modal) return;
    this.init();
  }

  init() {
    this.setupCloseButtons();
    this.setupClickOutside();
  }

  setupCloseButtons() {
    this.modal.querySelectorAll('[data-close]').forEach(btn => {
      btn.addEventListener('click', () => this.close());
    });
  }

  setupClickOutside() {
    this.modal.addEventListener('click', (e) => {
      if (e.target === this.modal) this.close();
    });
  }

  open() {
    this.modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
    animate(this.modal, 'fade-in');
  }

  close() {
    this.modal.style.display = 'none';
    document.body.style.overflow = 'auto';
  }

  toggle() {
    this.modal.style.display === 'none' ? this.open() : this.close();
  }
}

/* ============================================================================
   Initialize on DOM Ready
   ============================================================================ */

document.addEventListener('DOMContentLoaded', () => {
  console.log('🎓 SmartEdu Pro Platform Initialized');

  // Theme Management
  new ThemeManager();

  // Initialize features
  setupSmoothScroll();
  setupLazyLoading();
  setupActiveNavigation();
  setupRippleEffect();
  measurePerformance();
  new ScrollAnimator();

  // Setup forms
  document.querySelectorAll('form').forEach(form => new FormHandler(form));

  // Setup modals
  document.querySelectorAll('[data-modal]').forEach(modal => new Modal(modal));

  // Add data-animate to cards for scroll animations
  document.querySelectorAll('.card, .feature').forEach(el => {
    el.setAttribute('data-animate', 'true');
  });

  // Log page view
  trackEvent('page_view', 'visit', window.location.pathname);

  // Check for notifications
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(alert => {
    const type = alert.className.includes('success') ? 'success' : 'info';
    const message = alert.textContent;
    if (message) {
      console.log(`Alert: ${message}`);
    }
  });

  // Initialize Chat Widget
  initializeChatWidget();
});

/* ============================================================================
   Chat Widget System
   ============================================================================ */

const initializeChatWidget = () => {
  const toggleBtn = document.getElementById('chat-toggle-btn');
  const chatWidget = document.getElementById('chat-widget');
  const closeBtn = document.getElementById('chat-close-btn');
  const sendBtn = document.getElementById('chat-widget-send');
  const input = document.getElementById('chat-widget-input');
  const messagesContainer = document.getElementById('chat-widget-messages');

  if (!toggleBtn || !chatWidget) return;

  // Toggle widget visibility
  toggleBtn.addEventListener('click', () => {
    const isHidden = chatWidget.style.display === 'none';
    chatWidget.style.display = isHidden ? 'flex' : 'none';
    if (isHidden) input.focus();
  });

  // Close button
  if (closeBtn) {
    closeBtn.addEventListener('click', () => {
      chatWidget.style.display = 'none';
    });
  }

  // Send message
  const sendMessage = async () => {
    const message = input.value.trim();
    if (!message) return;

    // Add user message
    appendChatMessage(message, 'user');
    input.value = '';
    sendBtn.disabled = true;
    sendBtn.textContent = 'Sending...';

    try {
      const response = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      appendChatMessage(data.reply || 'No response received', 'ai');
    } catch (error) {
      console.error('Chat error:', error);
      appendChatMessage(`Error: ${error.message}`, 'ai');
    } finally {
      sendBtn.disabled = false;
      sendBtn.textContent = 'Send';
      input.focus();
    }
  };

  sendBtn.addEventListener('click', sendMessage);
  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  // Add initial greeting
  appendChatMessage("Hello! 👋 I'm your SmartEdu AI Assistant. How can I help you today?", 'ai');

  function appendChatMessage(text, sender) {
    const bubble = document.createElement('div');
    bubble.className = `chat-message-bubble ${sender}`;
    
    const messageText = document.createElement('div');
    messageText.className = 'chat-message-text';
    messageText.textContent = text;
    
    bubble.appendChild(messageText);
    messagesContainer.appendChild(bubble);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }
};

/* ============================================================================
   Service Worker Registration (PWA)
   ============================================================================ */

if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/service-worker.js').catch(err => {
      console.log('Service Worker not available:', err);
    });
  });
}

/* ============================================================================
   Export Global API
   ============================================================================ */

window.SmartEdu = {
  showNotification,
  debounce,
  throttle,
  animate,
  FormHandler,
  Modal,
  ThemeManager,
  TrackEvent: trackEvent
};

console.log('✨ SmartEdu Pro - Premium Educational Platform Ready');
