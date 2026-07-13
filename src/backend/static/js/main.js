/**
 * GPC ERP - Main JavaScript
 * Government Polytechnic College - Production Ready Frontend
 * Standards: ES6+, Accessible, Performance Optimized
 */

(function () {
    'use strict';

    // =============================================================================
    // Utilities
    // =============================================================================
    const $ = (selector, context = document) => context.querySelector(selector);
    const $$ = (selector, context = document) => Array.from(context.querySelectorAll(selector));

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // =============================================================================
    // Mobile Navigation
    // =============================================================================
    function initMobileNav() {
        const toggle = $('.nav-toggle');
        const menu = $('#nav-menu');
        if (!toggle || !menu) return;

        toggle.addEventListener('click', () => {
            const isOpen = menu.classList.toggle('is-open');
            toggle.setAttribute('aria-expanded', String(isOpen));
        });

        // Close on outside click
        document.addEventListener('click', (e) => {
            if (!menu.contains(e.target) && !toggle.contains(e.target)) {
                menu.classList.remove('is-open');
                toggle.setAttribute('aria-expanded', 'false');
            }
        });

        // Close on escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && menu.classList.contains('is-open')) {
                menu.classList.remove('is-open');
                toggle.setAttribute('aria-expanded', 'false');
                toggle.focus();
            }
        });
    }

    // =============================================================================
    // Toast Notifications
    // =============================================================================
    window.GPC = window.GPC || {};
    window.GPC.toast = function (message, type = 'info', duration = 4000) {
        const container = $('#toast-container');
        if (!container) return;

        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'polite');
        toast.innerHTML = `
            <span class="toast-message">${escapeHtml(message)}</span>
            <button class="toast-close" aria-label="Close notification">&times;</button>
        `;

        container.appendChild(toast);

        const closeToast = () => {
            toast.classList.add('is-hiding');
            toast.addEventListener('animationend', () => toast.remove());
        };

        toast.querySelector('.toast-close').addEventListener('click', closeToast);
        setTimeout(closeToast, duration);
    };

    // =============================================================================
    // Confirmation Dialog
    // =============================================================================
    window.GPC.confirm = function (title, message, onConfirm) {
        const dialog = $('#confirmation-dialog');
        if (!dialog) return;

        $('#confirm-title').textContent = title || 'Confirm Action';
        $('#confirm-message').textContent = message || 'Are you sure?';

        dialog.classList.add('is-open');
        dialog.setAttribute('aria-hidden', 'false');
        $('#confirm-action-btn').focus();

        const cleanup = () => {
            dialog.classList.remove('is-open');
            dialog.setAttribute('aria-hidden', 'true');
        };

        const confirmBtn = $('#confirm-action-btn');
        const newConfirm = confirmBtn.cloneNode(true);
        confirmBtn.parentNode.replaceChild(newConfirm, confirmBtn);

        newConfirm.addEventListener('click', () => {
            cleanup();
            if (typeof onConfirm === 'function') onConfirm();
        });

        $$('[data-close-modal]', dialog).forEach((btn) => {
            btn.addEventListener('click', cleanup);
        });

        dialog.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') cleanup();
        });
    };

    // =============================================================================
    // Lazy Loading Images
    // =============================================================================
    function initLazyLoading() {
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        if (img.dataset.src) {
                            img.src = img.dataset.src;
                            img.removeAttribute('data-src');
                        }
                        imageObserver.unobserve(img);
                    }
                });
            }, { rootMargin: '50px' });

            $$('img[data-src]').forEach((img) => imageObserver.observe(img));
        } else {
            // Fallback
            $$('img[data-src]').forEach((img) => {
                img.src = img.dataset.src;
            });
        }
    }

    // =============================================================================
    // Form Validation Helpers
    // =============================================================================
    function initFormValidation() {
        $$('form').forEach((form) => {
            form.addEventListener('submit', (e) => {
                let isValid = true;
                const requiredFields = form.querySelectorAll('[required]');

                requiredFields.forEach((field) => {
                    if (!field.value.trim()) {
                        isValid = false;
                        field.setAttribute('aria-invalid', 'true');
                        field.classList.add('is-invalid');
                    } else {
                        field.setAttribute('aria-invalid', 'false');
                        field.classList.remove('is-invalid');
                    }
                });

                if (!isValid) {
                    e.preventDefault();
                    window.GPC.toast('Please fill in all required fields.', 'error');
                }
            });
        });
    }

    // =============================================================================
    // API Helpers
    // =============================================================================
    window.GPC.api = {
        async request(url, options = {}) {
            const defaults = {
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                credentials: 'same-origin',
            };

            const config = { ...defaults, ...options };
            if (config.body && typeof config.body === 'object' && !(config.body instanceof FormData)) {
                config.body = JSON.stringify(config.body);
            }

            try {
                const response = await fetch(url, config);
                const data = await response.json();
                if (!response.ok) {
                    throw new Error(data.message || 'Request failed');
                }
                return data;
            } catch (error) {
                console.error('API Error:', error);
                window.GPC.toast(error.message || 'Network error. Please try again.', 'error');
                throw error;
            }
        },

        get(url) {
            return this.request(url, { method: 'GET' });
        },

        post(url, body) {
            return this.request(url, { method: 'POST', body });
        },

        patch(url, body) {
            return this.request(url, { method: 'PATCH', body });
        },

        delete(url) {
            return this.request(url, { method: 'DELETE' });
        },
    };

    // =============================================================================
    // Contact Form Handler
    // =============================================================================
    function initContactForm() {
        const form = $('#contact-form');
        if (!form) return;

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const submitBtn = form.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.disabled = true;
            submitBtn.textContent = 'Submitting...';

            try {
                const formData = new FormData(form);
                const payload = Object.fromEntries(formData.entries());
                await window.GPC.api.post('/api/v1/contact/enquiries/', payload);
                window.GPC.toast('Enquiry submitted successfully!', 'success');
                form.reset();
            } catch (error) {
                // Error handled by api helper
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = originalText;
            }
        });
    }

    // =============================================================================
    // Search & Filter Helpers
    // =============================================================================
    function initSearchFilters() {
        const searchInputs = [
            { id: 'dept-search', selector: '.dept-card' },
            { id: 'course-search', selector: '.course-card' },
            { id: 'faculty-search', selector: '.faculty-card' },
            { id: 'notice-search', selector: '.notice-item' },
            { id: 'event-search', selector: '.event-card' },
        ];

        searchInputs.forEach(({ id, selector }) => {
            const input = $(`#${id}`);
            if (!input) return;

            input.addEventListener('input', (e) => {
                const term = e.target.value.toLowerCase();
                $$(selector).forEach((item) => {
                    const text = item.textContent.toLowerCase();
                    item.style.display = text.includes(term) ? '' : 'none';
                });
            });
        });
    }

    // =============================================================================
    // Escape HTML
    // =============================================================================
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // =============================================================================
    // Initialize
    // =============================================================================
    function init() {
        initMobileNav();
        initLazyLoading();
        initFormValidation();
        initContactForm();
        initSearchFilters();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
