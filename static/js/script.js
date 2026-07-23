/**
 * Government Scheme Predictor - Client-side JavaScript
 * Handles form validation, loading states, and UI interactions
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all functionality
    initializeFormValidation();
    initializeSmoothScrolling();
    initializeNavbar();
    initializeAnimations();
    initializeTooltips();
    initializeConditionalFields();
});

/**
 * Initialize form validation for all forms
 */
function initializeFormValidation() {
    const forms = document.querySelectorAll('form[novalidate]');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                form.classList.add('was-validated');
                
                // Scroll to first invalid field
                const firstInvalid = form.querySelector(':invalid');
                if (firstInvalid) {
                    firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    firstInvalid.focus();
                }
            }
        });
        
        // Remove validation styling on input
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('input', function() {
                if (this.checkValidity()) {
                    this.classList.remove('is-invalid');
                }
            });
        });
    });
}

/**
 * Initialize smooth scrolling for anchor links
 */
function initializeSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            if (href !== '#' && href.length > 1) {
                e.preventDefault();
                const target = document.querySelector(href);
                
                if (target) {
                    const headerOffset = 80;
                    const elementPosition = target.getBoundingClientRect().top;
                    const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
                    
                    window.scrollTo({
                        top: offsetPosition,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });
}

/**
 * Initialize navbar behavior
 */
function initializeNavbar() {
    const navbar = document.querySelector('.navbar');
    
    if (navbar) {
        // Add shadow on scroll
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('shadow-lg');
            } else {
                navbar.classList.remove('shadow-lg');
            }
        });
        
        // Close mobile menu on link click
        const navLinks = document.querySelectorAll('.nav-link');
        const navbarCollapse = document.querySelector('.navbar-collapse');
        
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                if (window.innerWidth < 992 && navbarCollapse) {
                    const bsCollapse = bootstrap.Collapse.getInstance(navbarCollapse);
                    if (bsCollapse) {
                        bsCollapse.hide();
                    }
                }
            });
        });
    }
}

/**
 * Initialize scroll animations
 */
function initializeAnimations() {
    // Intersection Observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe cards and sections
    const animatedElements = document.querySelectorAll('.card, section > .container > .row');
    animatedElements.forEach(el => observer.observe(el));
}

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(
        tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl)
    );
}

/**
 * Initialize conditional field visibility based on gender selection
 */
function initializeConditionalFields() {
    const genderSelect = document.getElementById('gender');
    const pregnancySection = document.getElementById('pregnancy-section');
    const pregnantRadios = document.querySelectorAll('input[name="pregnant"]');
    const ageInput = document.getElementById('age');
    const seniorCitizenSection = document.getElementById('senior-citizen-section');

    if (!genderSelect || !pregnancySection) return;

    // Function to toggle pregnancy section
    function togglePregnancySection() {
        const gender = genderSelect.value;

        if (gender === 'Female') {
            // Show pregnancy section with animation
            pregnancySection.classList.remove('d-none');
            // Small delay to allow display:block to apply before opacity transition
            setTimeout(() => {
                pregnancySection.classList.add('show');
                pregnancySection.classList.remove('hide');
            }, 10);
        } else {
            // Hide pregnancy section with animation
            pregnancySection.classList.remove('show');
            pregnancySection.classList.add('hide');
            // Wait for animation to complete before hiding
            setTimeout(() => {
                pregnancySection.classList.add('d-none');
            }, 400);
        }
    }

    // Function to toggle senior citizen section
    function toggleSeniorCitizenSection() {
        if (!ageInput || !seniorCitizenSection) return;

        const age = parseInt(ageInput.value) || 0;

        if (age >= 60) {
            // Show senior citizen section with animation
            seniorCitizenSection.classList.remove('d-none');
            setTimeout(() => {
                seniorCitizenSection.classList.add('show');
                seniorCitizenSection.classList.remove('hide');
            }, 10);
        } else {
            // Hide senior citizen section with animation
            seniorCitizenSection.classList.remove('show');
            seniorCitizenSection.classList.add('hide');
            setTimeout(() => {
                seniorCitizenSection.classList.add('d-none');
            }, 400);
        }
    }

    // Listen for gender changes
    genderSelect.addEventListener('change', togglePregnancySection);

    // Listen for age changes
    if (ageInput) {
        ageInput.addEventListener('input', toggleSeniorCitizenSection);
        ageInput.addEventListener('change', toggleSeniorCitizenSection);
    }

    // Handle form submission - auto-set defaults for hidden sections
    const predictionForm = document.getElementById('predictionForm');
    if (predictionForm) {
        predictionForm.addEventListener('submit', function(e) {
            const gender = genderSelect.value;
            if (gender !== 'Female') {
                // Ensure pregnant field is set to 0 for non-female genders
                const pregnantInput = document.querySelector('input[name="pregnant"][value="0"]');
                if (pregnantInput) {
                    pregnantInput.checked = true;
                }
            }

            const age = parseInt(ageInput.value) || 0;
            if (age < 60) {
                // Ensure senior_citizen field is set to 0 for age < 60
                const seniorCitizenInput = document.querySelector('input[name="senior_citizen"][value="0"]');
                if (seniorCitizenInput) {
                    seniorCitizenInput.checked = true;
                }
            }
        });
    }
}

/**
 * Validate individual field
 * @param {HTMLElement} field - The input field to validate
 * @returns {boolean} - Whether the field is valid
 */
function validateField(field) {
    if (field.checkValidity()) {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
        return true;
    } else {
        field.classList.remove('is-valid');
        field.classList.add('is-invalid');
        return false;
    }
}

/**
 * Show loading spinner
 * @param {string} buttonId - ID of the submit button
 * @param {string} spinnerId - ID of the loading spinner
 */
function showLoading(buttonId, spinnerId) {
    const button = document.getElementById(buttonId);
    const spinner = document.getElementById(spinnerId);
    
    if (button) {
        button.disabled = true;
        button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
    }
    
    if (spinner) {
        spinner.classList.remove('d-none');
    }
}

/**
 * Hide loading spinner
 * @param {string} buttonId - ID of the submit button
 * @param {string} spinnerId - ID of the loading spinner
 * @param {string} originalText - Original button text
 */
function hideLoading(buttonId, spinnerId, originalText) {
    const button = document.getElementById(buttonId);
    const spinner = document.getElementById(spinnerId);
    
    if (button) {
        button.disabled = false;
        button.innerHTML = originalText || 'Submit';
    }
    
    if (spinner) {
        spinner.classList.add('d-none');
    }
}

/**
 * Show alert message
 * @param {string} message - Alert message
 * @param {string} type - Alert type (success, danger, warning, info)
 * @param {string} containerId - Container ID to append alert to
 */
function showAlert(message, type = 'info', containerId = 'alert-container') {
    const container = document.getElementById(containerId);
    
    if (container) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.setAttribute('role', 'alert');
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        
        container.appendChild(alertDiv);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alertDiv);
            if (bsAlert) {
                bsAlert.close();
            }
        }, 5000);
    }
}

/**
 * Format number as currency
 * @param {number} amount - Amount to format
 * @param {string} currency - Currency symbol (default: ₹)
 * @returns {string} - Formatted currency string
 */
function formatCurrency(amount, currency = '₹') {
    return currency + amount.toLocaleString('en-IN');
}

/**
 * Validate email format
 * @param {string} email - Email address to validate
 * @returns {boolean} - Whether email is valid
 */
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Validate phone number (Indian format)
 * @param {string} phone - Phone number to validate
 * @returns {boolean} - Whether phone number is valid
 */
function isValidPhone(phone) {
    const phoneRegex = /^[6-9]\d{9}$/;
    return phoneRegex.test(phone);
}

/**
 * Debounce function to limit function calls
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @returns {Function} - Debounced function
 */
function debounce(func, wait = 300) {
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
 * Copy text to clipboard
 * @param {string} text - Text to copy
 * @returns {Promise<boolean>} - Whether copy was successful
 */
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        return true;
    } catch (err) {
        console.error('Failed to copy text: ', err);
        return false;
    }
}

/**
 * Get URL parameter by name
 * @param {string} name - Parameter name
 * @returns {string|null} - Parameter value or null
 */
function getUrlParameter(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}

/**
 * Set URL parameter
 * @param {string} name - Parameter name
 * @param {string} value - Parameter value
 */
function setUrlParameter(name, value) {
    const url = new URL(window.location);
    url.searchParams.set(name, value);
    window.history.replaceState({}, '', url);
}

/**
 * Remove URL parameter
 * @param {string} name - Parameter name
 */
function removeUrlParameter(name) {
    const url = new URL(window.location);
    url.searchParams.delete(name);
    window.history.replaceState({}, '', url);
}

/**
 * Check if element is in viewport
 * @param {HTMLElement} element - Element to check
 * @returns {boolean} - Whether element is in viewport
 */
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

/**
 * Add class to element when in viewport
 * @param {string} selector - CSS selector
 * @param {string} className - Class to add
 */
function addClassOnScroll(selector, className) {
    const element = document.querySelector(selector);
    
    if (element) {
        window.addEventListener('scroll', debounce(() => {
            if (isInViewport(element)) {
                element.classList.add(className);
            }
        }, 100));
    }
}

// Export functions for use in other scripts
window.GovSchemeUtils = {
    validateField,
    showLoading,
    hideLoading,
    showAlert,
    formatCurrency,
    isValidEmail,
    isValidPhone,
    debounce,
    copyToClipboard,
    getUrlParameter,
    setUrlParameter,
    removeUrlParameter,
    isInViewport,
    addClassOnScroll
};
