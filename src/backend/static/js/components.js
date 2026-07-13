/**
 * GPC ERP - Reusable Components
 * Pagination, Dynamic Lists, Skeleton Loaders
 */

(function () {
    'use strict';

    window.GPC = window.GPC || {};

    // =============================================================================
    // Pagination Component
    // =============================================================================
    window.GPC.Pagination = class {
        constructor(container, options = {}) {
            this.container = container;
            this.currentPage = options.currentPage || 1;
            this.totalPages = options.totalPages || 1;
            this.onPageChange = options.onPageChange || (() => {});
            this.render();
        }

        render() {
            if (!this.container || this.totalPages <= 1) return;

            const nav = document.createElement('nav');
            nav.setAttribute('aria-label', 'Pagination');
            const ul = document.createElement('ul');
            ul.className = 'pagination';

            // Previous
            ul.appendChild(this._createPageItem(this.currentPage - 1, 'Previous', this.currentPage === 1, true));

            // Page numbers
            const range = this._getPageRange();
            for (let i = range.start; i <= range.end; i++) {
                ul.appendChild(this._createPageItem(i, String(i), false, false, i === this.currentPage));
            }

            // Next
            ul.appendChild(this._createPageItem(this.currentPage + 1, 'Next', this.currentPage === this.totalPages, true));

            nav.appendChild(ul);
            this.container.innerHTML = '';
            this.container.appendChild(nav);
        }

        _createPageItem(page, label, disabled, isNav, isCurrent = false) {
            const li = document.createElement('li');
            if (isCurrent) {
                li.innerHTML = `<span class="current" aria-current="page">${label}</span>`;
            } else if (disabled) {
                li.innerHTML = `<span class="disabled">${label}</span>`;
            } else {
                const a = document.createElement('a');
                a.href = '#';
                a.textContent = label;
                a.addEventListener('click', (e) => {
                    e.preventDefault();
                    this.currentPage = page;
                    this.render();
                    this.onPageChange(page);
                });
                li.appendChild(a);
            }
            return li;
        }

        _getPageRange() {
            const delta = 2;
            let start = Math.max(1, this.currentPage - delta);
            let end = Math.min(this.totalPages, this.currentPage + delta);
            if (end - start < delta * 2) {
                if (start === 1) {
                    end = Math.min(this.totalPages, start + delta * 2);
                } else {
                    start = Math.max(1, end - delta * 2);
                }
            }
            return { start, end };
        }
    };

    // =============================================================================
    // Skeleton Loader Helper
    // =============================================================================
    window.GPC.Skeleton = {
        show(container, count = 3) {
            if (!container) return;
            const template = document.getElementById('skeleton-template');
            if (!template) return;

            container.innerHTML = '';
            for (let i = 0; i < count; i++) {
                const clone = template.content.cloneNode(true);
                container.appendChild(clone);
            }
        },

        hide(container) {
            if (!container) return;
            container.innerHTML = '';
        },
    };

    // =============================================================================
    // Dynamic List Loader
    // =============================================================================
    window.GPC.DynamicList = class {
        constructor(container, options = {}) {
            this.container = container;
            this.apiUrl = options.apiUrl;
            this.renderItem = options.renderItem;
            this.emptyMessage = options.emptyMessage || 'No items found.';
            this.skeletonCount = options.skeletonCount || 3;
        }

        async load(params = {}) {
            if (!this.container) return;
            window.GPC.Skeleton.show(this.container, this.skeletonCount);

            try {
                const query = new URLSearchParams(params).toString();
                const url = `${this.apiUrl}?${query}`;
                const response = await window.GPC.api.get(url);
                window.GPC.Skeleton.hide(this.container);

                const items = response.data?.results || response.data || [];
                if (items.length === 0) {
                    this.container.innerHTML = `<div class="empty-state"><p>${this.emptyMessage}</p></div>`;
                    return;
                }

                const wrapper = document.createElement('div');
                wrapper.className = 'card-grid';
                items.forEach((item) => {
                    wrapper.innerHTML += this.renderItem(item);
                });
                this.container.innerHTML = '';
                this.container.appendChild(wrapper);
            } catch (error) {
                window.GPC.Skeleton.hide(this.container);
                this.container.innerHTML = `<div class="empty-state"><p>Failed to load items. Please try again.</p></div>`;
            }
        }
    };
})();
