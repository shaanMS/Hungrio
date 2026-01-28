/**
 * Product Management Module
 * Handles product listing, filtering, sorting, and pagination
 */

class ProductManager {
    constructor() {
        this.products = [];
        this.filteredProducts = [];
        this.categories = new Set();
        this.currentPage = 1;
        this.totalPages = 1;
        this.pageSize = 12;
        this.filters = {
            category: 'all',
            foodType: 'all',
            priceRange: 1000,
            searchQuery: '',
            sortBy: 'name_asc'
        };
        
        this.init();
    }
    
    /**
     * Initialize product manager
     */
    init() {
        this.bindEvents();
        this.loadProducts();
        this.loadCategories();
    }
    
    /**
     * Bind DOM events
     */
    bindEvents() {
        // Search input
        const searchInput = document.getElementById('searchInput');
        searchInput.addEventListener('input', debounce((e) => {
            this.filters.searchQuery = e.target.value;
            this.filterProducts();
        }, 300));
        
        // Category filters
        document.querySelectorAll('input[name="category"]').forEach(input => {
            input.addEventListener('change', (e) => {
                this.filters.category = e.target.value;
                this.filterProducts();
            });
        });
        
        // Food type filters
        document.querySelectorAll('input[name="foodType"]').forEach(input => {
            input.addEventListener('change', (e) => {
                this.filters.foodType = e.target.value;
                this.filterProducts();
            });
        });
        
        // Price range slider
        const priceSlider = document.getElementById('priceSlider');
        const priceValue = document.getElementById('priceValue');
        priceSlider.addEventListener('input', (e) => {
            const value = parseInt(e.target.value);
            priceValue.textContent = value === 1000 ? '₹1000+' : `₹${value}`;
            this.filters.priceRange = value;
            this.filterProducts();
        });
        
        // Sort select
        const sortSelect = document.getElementById('sortSelect');
        sortSelect.addEventListener('change', (e) => {
            this.filters.sortBy = e.target.value;
            this.sortProducts();
            this.displayProducts();
        });
        
        // Clear filters button
        const clearFiltersBtn = document.getElementById('clearFilters');
        clearFiltersBtn.addEventListener('click', () => this.clearFilters());
        
        // Load more button
        const loadMoreBtn = document.getElementById('loadMore');
        loadMoreBtn.addEventListener('click', () => this.loadMore());
        
        // Pagination (will be handled dynamically)
    }
    
    /**
     * Load products from API
     */
    async loadProducts() {
      //  prompt('123454')
        try {
            showLoading(true);
          //  prompt('123454')
            const response = await apiCall(`${API_CONFIG.BASE_URL}${API_CONFIG.PRODUCTS}?page=${this.currentPage}`);
            
            if (response && response.results) {
                this.products = response.results;
                this.totalPages = Math.ceil(response.count / this.pageSize);
                this.filteredProducts = [...this.products];
                
                this.displayProducts();
                this.updatePagination();
                this.updateProductStats();
            }
        } catch (error) {
            console.error('Error loading products:', error);
            showNotification('Failed to load products. Please try again.', 'error');
        } finally {
            showLoading(false);
        }
    }
    
    /**
     * Load categories from products
     */
    loadCategories() {
        this.products.forEach(product => {
            if (product.category_name) {
                this.categories.add(product.category_name);
            }
        });
        
        this.displayCategories();
    }
    
    /**
     * Display categories in filter section
     */
    displayCategories() {
        const categoryContainer = document.querySelector('.filter-options');
        const firstOption = categoryContainer.querySelector('.filter-option');
        categoryContainer.innerHTML = '';
        categoryContainer.appendChild(firstOption);
        
        this.categories.forEach(category => {
            const label = createElement('label', {
                className: 'filter-option'
            });
            
            const input = createElement('input', {
                type: 'checkbox',
                name: 'category',
                value: category
            });
            
            const span = createElement('span', {}, category);
            
            label.appendChild(input);
            label.appendChild(span);
            categoryContainer.appendChild(label);
            
            // Add event listener
            input.addEventListener('change', (e) => {
                this.filters.category = e.target.value;
                this.filterProducts();
            });
        });
    }
    
    /**
     * Filter products based on current filters
     */
    filterProducts() {
        this.filteredProducts = this.products.filter(product => {
            // Category filter
            if (this.filters.category !== 'all' && product.category_name !== this.filters.category) {
                return false;
            }
            
            // Food type filter
            if (this.filters.foodType === 'veg' && !product.is_veg) {
                return false;
            }
            if (this.filters.foodType === 'nonveg' && product.is_veg) {
                return false;
            }
            
            // Price filter
            if (parseFloat(product.final_price) > this.filters.priceRange) {
                return false;
            }
            
            // Search filter
            if (this.filters.searchQuery) {
                const searchLower = this.filters.searchQuery.toLowerCase();
                return product.name.toLowerCase().includes(searchLower) ||
                       product.description.toLowerCase().includes(searchLower) ||
                       product.category_name.toLowerCase().includes(searchLower);
            }
            
            return true;
        });
        
        this.sortProducts();
        this.displayProducts();
        this.updateProductStats();
    }
    
    /**
     * Sort products based on current sort option
     */
    sortProducts() {
        switch (this.filters.sortBy) {
            case 'name_asc':
                this.filteredProducts.sort((a, b) => a.name.localeCompare(b.name));
                break;
            case 'name_desc':
                this.filteredProducts.sort((a, b) => b.name.localeCompare(a.name));
                break;
            case 'price_asc':
                this.filteredProducts.sort((a, b) => parseFloat(a.final_price) - parseFloat(b.final_price));
                break;
            case 'price_desc':
                this.filteredProducts.sort((a, b) => parseFloat(b.final_price) - parseFloat(a.final_price));
                break;
            case 'newest':
                this.filteredProducts.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
                break;
        }
    }
    
    /**
     * Display products in grid
     */
    displayProducts() {
        const productsGrid = document.getElementById('productsGrid');
        productsGrid.innerHTML = '';
        
        if (this.filteredProducts.length === 0) {
            productsGrid.innerHTML = `
                <div class="no-products">
                    <i class="fas fa-search"></i>
                    <h3>No products found</h3>
                    <p>Try adjusting your filters or search term</p>
                    <button class="btn-clear-filters" onclick="productManager.clearFilters()">
                        Clear All Filters
                    </button>
                </div>
            `;
            return;
        }
        
        this.filteredProducts.forEach(product => {
            const productCard = this.createProductCard(product);
            productsGrid.appendChild(productCard);
        });
    }
    
    /**
     * Create product card element
     * @param {object} product - Product data
     * @returns {HTMLElement} Product card element
     */
    createProductCard(product) {
        const card = createElement('div', { className: 'product-card' });
        
        const discount = calculateDiscount(
            parseFloat(product.base_price),
            parseFloat(product.final_price)
        );
        
        const imageSection = createElement('div', { className: 'product-image' }, [
            createElement('i', { className: 'fas fa-utensils' }),
            createElement('div', {
                className: `veg-indicator ${product.is_veg ? 'veg' : 'nonveg'}`
            })
        ]);
        
        const infoSection = createElement('div', { className: 'product-info' }, [
            createElement('h3', { className: 'product-title' }, product.name),
            createElement('p', { className: 'product-description' }, product.description || 'No description available'),
            createElement('div', { className: 'product-meta' }, [
                createElement('span', { className: 'product-category' }, product.category_name),
                createElement('span', { className: 'product-subcategory' }, product.subcategory_name)
            ]),
            createElement('div', { className: 'product-price' }, [
                discount > 0 ? createElement('span', { className: 'original-price' }, formatPrice(product.base_price)) : null,
                createElement('span', { className: 'final-price' }, formatPrice(product.final_price)),
                discount > 0 ? createElement('span', { className: 'discount-badge' }, `${discount}% OFF`) : null
            ])
        ]);
        
        const actionsSection = createElement('div', { className: 'product-actions' }, [
            createElement('button', {
                className: 'btn-add-to-cart',
                onclick: () => addToCart(product.id, 1)
            }, [
                createElement('i', { className: 'fas fa-cart-plus' }),
                'Add to Cart'
            ]),
            createElement('button', {
                className: 'btn-view-details',
                onclick: () => this.viewProductDetails(product.id)
            }, [
                createElement('i', { className: 'fas fa-eye' }),
                'View Details'
            ])
        ]);
        
        infoSection.appendChild(actionsSection);
        card.appendChild(imageSection);
        card.appendChild(infoSection);
        
        return card;
    }
    
    /**
     * View product details
     * @param {number} productId - Product ID
     */
    viewProductDetails(productId) {
        // This would navigate to a product detail page
        // For now, show a notification
        showNotification('Product details feature coming soon!', 'info');
    }
    
    /**
     * Load more products (for infinite scroll/pagination)
     */
    loadMore() {
        if (this.currentPage < this.totalPages) {
            this.currentPage++;
            this.loadProducts();
        } else {
            showNotification('No more products to load!', 'info');
        }
    }
    
    /**
     * Update pagination controls
     */
    updatePagination() {
        const pagination = document.getElementById('pagination');
        pagination.innerHTML = '';
        
        if (this.totalPages <= 1) return;
        
        // Previous button
        const prevButton = createElement('button', {
            onclick: () => this.goToPage(this.currentPage - 1),
            disabled: this.currentPage === 1
        }, [
            createElement('i', { className: 'fas fa-chevron-left' }),
            ' Previous'
        ]);
        pagination.appendChild(prevButton);
        
        // Page numbers
        const startPage = Math.max(1, this.currentPage - 2);
        const endPage = Math.min(this.totalPages, this.currentPage + 2);
        
        for (let i = startPage; i <= endPage; i++) {
            const pageButton = createElement('button', {
                className: i === this.currentPage ? 'active' : '',
                onclick: () => this.goToPage(i)
            }, i.toString());
            pagination.appendChild(pageButton);
        }
        
        // Next button
        const nextButton = createElement('button', {
            onclick: () => this.goToPage(this.currentPage + 1),
            disabled: this.currentPage === this.totalPages
        }, [
            'Next ',
            createElement('i', { className: 'fas fa-chevron-right' })
        ]);
        pagination.appendChild(nextButton);
    }
    
    /**
     * Go to specific page
     * @param {number} page - Page number
     */
    goToPage(page) {
        if (page < 1 || page > this.totalPages || page === this.currentPage) return;
        
        this.currentPage = page;
        this.loadProducts();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    
    /**
     * Update product statistics display
     */
    updateProductStats() {
        const productCount = document.getElementById('productCount');
        const selectedCategory = document.getElementById('selectedCategory');
        
        productCount.textContent = `${this.filteredProducts.length} products`;
        selectedCategory.textContent = this.filters.category === 'all' 
            ? 'All Categories' 
            : this.filters.category;
    }
    
    /**
     * Clear all filters
     */
    clearFilters() {
        // Reset filter inputs
        document.getElementById('searchInput').value = '';
        document.querySelector('input[name="category"][value="all"]').checked = true;
        document.querySelector('input[name="foodType"][value="all"]').checked = true;
        document.getElementById('priceSlider').value = 1000;
        document.getElementById('priceValue').textContent = '₹1000+';
        document.getElementById('sortSelect').value = 'name_asc';
        
        // Reset filter state
        this.filters = {
            category: 'all',
            foodType: 'all',
            priceRange: 1000,
            searchQuery: '',
            sortBy: 'name_asc'
        };
        
        // Reset to first page
        this.currentPage = 1;
        
        // Reload products
        this.loadProducts();
        
        showNotification('All filters cleared', 'success');
    }
}

/**
 * Show/hide loading state
 * @param {boolean} isLoading - Whether to show loading
 */
function showLoading(isLoading) {
    const productsGrid = document.getElementById('productsGrid');
    const loadMoreBtn = document.getElementById('loadMore');
    
    if (isLoading) {
        productsGrid.innerHTML = `
            <div class="loading-spinner">
                <i class="fas fa-spinner fa-spin"></i>
                <p>Loading delicious dishes...</p>
            </div>
        `;
        loadMoreBtn.disabled = true;
    } else {
        loadMoreBtn.disabled = false;
    }
}

// Initialize product manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.productManager = new ProductManager();
});

// Export for use in other modules
window.ProductManager = ProductManager;