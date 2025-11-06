document.addEventListener('DOMContentLoaded', () => {
    // --- Configuration ---
    const API_HOST = 'http://127.0.0.1:5000';
    const API_ALL_PRODUCTS_URL = `${API_HOST}/api/products/all`;
    const PRODUCTS_PER_PAGE = 10;

    // --- DOM References ---
    const shortlistGrid = document.getElementById('shortlist-grid');
    const priceRange = document.getElementById('price-max');
    const priceValueSpan = document.getElementById('price-value');
    const filterSidebar = document.querySelector('.filter-sidebar');
    const productContent = document.querySelector('.product-content');
    const paginationContainer = document.createElement('div');
    paginationContainer.id = 'pagination-container';
    productContent.appendChild(paginationContainer);

    // --- State Management ---
    let allProducts = [];
    let filteredProducts = [];
    let currentPage = 1;

    // Initialize Price Display
    priceValueSpan.textContent = `$${priceRange.value}`;

    // ------------------------------------
    //  I. FILTER COLLECTION & APPLICATION
    // ------------------------------------
    function collectFilters() {
        const filters = {
            brands: [],
            categories: [],
            applications: [],
            sockets: [],
            cores: [],
            tdp: [],
            threads: [],
            cache: [],
            base_freq: [],
            tech: [],
            memory_type: [],
            max_memory_size: [],
            packaging: [],
            maxPrice: parseFloat(priceRange.value)
        };

        document.querySelectorAll('.filter-checkbox:checked').forEach(checkbox => {
            const groupName = checkbox.name;
            const value = checkbox.value;

            if (groupName === 'brand') filters.brands.push(value);
            else if (groupName === 'category') filters.categories.push(value);
            else if (groupName === 'application') filters.applications.push(value);
            else if (groupName === 'socket') filters.sockets.push(value);
            else if (groupName === 'tech') filters.tech.push(value);
            else if (groupName === 'packaging') filters.packaging.push(value);
            else if (groupName === 'memory_type') filters.memory_type.push(value);
            else if (groupName === 'cores') filters.cores.push(parseInt(value));
            else if (groupName === 'tdp') filters.tdp.push(parseInt(value));
            else if (groupName === 'threads') filters.threads.push(parseInt(value));
            else if (groupName === 'cache') filters.cache.push(parseInt(value));
            else if (groupName === 'max_memory_size') filters.max_memory_size.push(parseInt(value));
            else if (groupName === 'base_freq') filters.base_freq.push(parseFloat(value));
        });

        return filters;
    }

    function applyClientFilters() {
        const filters = collectFilters();

        filteredProducts = allProducts.filter(product => {
            if (product.price > filters.maxPrice) return false;
            if (filters.brands.length && !filters.brands.includes(product.brand)) return false;
            if (filters.categories.length && !filters.categories.some(cat => product.category.includes(cat))) return false;
            if (filters.applications.length && !filters.applications.includes(product.application)) return false;
            if (filters.sockets.length && !filters.sockets.includes(product.socket)) return false;
            if (filters.cores.length && !filters.cores.includes(product.cores)) return false;
            if (filters.tdp.length && !filters.tdp.includes(product.tdp)) return false;
            if (filters.threads.length && !filters.threads.includes(product.threads)) return false;
            if (filters.cache.length && !filters.cache.includes(product.cache)) return false;
            if (filters.base_freq.length && !filters.base_freq.includes(parseFloat(product.base_freq))) return false;
            if (filters.tech.length && !filters.tech.includes(product.tech)) return false;
            if (filters.memory_type.length && !filters.memory_type.includes(product.memory_type)) return false;
            if (filters.max_memory_size.length && !filters.max_memory_size.includes(product.max_memory_size)) return false;
            if (filters.packaging.length && !filters.packaging.includes(product.packaging)) return false;
            return true;
        });

        currentPage = 1;
        renderProducts(filteredProducts);
    }

    // ------------------------------------
    //  II. FETCH PRODUCTS FROM FLASK
    // ------------------------------------
    async function fetchAllProducts() {
        shortlistGrid.innerHTML = '<p class="loading-message">Loading products...</p>';
        filterSidebar.style.opacity = '0.5';

        try {
            const response = await fetch(API_ALL_PRODUCTS_URL);
            if (!response.ok) throw new Error('Could not connect to backend.');

            const data = await response.json();
            allProducts = (data.products || []).map(p => ({
                ...p,
                price: parseFloat(p.price),
                cores: parseInt(p.cores),
                tdp: parseInt(p.tdp),
                threads: parseInt(p.threads),
                cache: parseInt(p.cache),
                base_freq: parseFloat(p.base_freq),
                max_memory_size: parseInt(p.max_memory_size),
                description: p.description || 'No description available.'
            }));

            filteredProducts = allProducts;
            renderProducts(filteredProducts);
            filterSidebar.style.opacity = '1';
        } catch (error) {
            console.error("Fetch error:", error);
            shortlistGrid.innerHTML = `<p class="error-message">Error: ${error.message}</p>`;
        }
    }

    // ------------------------------------
    //  III. RENDER PRODUCTS + PAGINATION
    // ------------------------------------
    function renderProducts(productsToRender) {
        const startIndex = (currentPage - 1) * PRODUCTS_PER_PAGE;
        const endIndex = startIndex + PRODUCTS_PER_PAGE;
        const pageProducts = productsToRender.slice(startIndex, endIndex);

        shortlistGrid.innerHTML = '';

        if (pageProducts.length === 0) {
            shortlistGrid.innerHTML = `<p class="empty-message">No products match your criteria.</p>`;
            renderPagination(productsToRender.length);
            return;
        }

        pageProducts.forEach(product => {
            const specs = [
                `Brand: ${product.brand}`,
                `Socket: ${product.socket}`,
                `Cores/Threads: ${product.cores}/${product.threads}`,
                `Cache: ${product.cache} MB`,
                `TDP: ${product.tdp} W`,
                `Freq: ${product.base_freq} GHz`,
                `Tech: ${product.tech}`,
                `Memory: ${product.memory_type} (${product.max_memory_size} GB Max)`
            ].join(' | ');

            // ✅ UPDATED: Redirect based on product brand (Intel → intel.html, AMD → amd.html)
            const targetPage = `/productslist/${product.brand.toLowerCase()}.html`;

            const cardHtml = `
                <div class="product-card" data-product-id="${product.id}">
                    <div class="product-image-container" onclick="window.location.href='${targetPage}'">
                        <img src="${API_HOST}${product.image}" alt="${product.name}" 
                               onerror="this.src='https://placehold.co/150x150/d1d5db/374151?text=Image+NA'">
                    </div>
                    <div class="product-details">
                        <a href="${product.name.toLowerCase().replace(/\\s+/g, '-')}.html" class="product-link" style="text-decoration: none; color: inherit;">
                        <h4 class="product-title">${product.name}</h4></a>
                        <p class="product-spec-snippet">${product.description}</p>
                        <small class="product-meta">${specs}</small>
                    </div>
                    <div class="product-actions">
                        <div class="product-price-moq">
                            <p class="price-value">US <span class="price-large">$${product.price.toFixed(2)}</span>/pcs</p>
                            <p class="moq-info">20 pcs (MOQ) <span class="info-icon">ⓘ</span></p>
                        </div>
                        <button class="inquiry-btn" onclick="window.location.href='inquiry.html?product=${encodeURIComponent(product.name)}'">Inquiry</button>
                    </div>
                </div>
            `;
            shortlistGrid.insertAdjacentHTML('beforeend', cardHtml);
        });

        renderPagination(productsToRender.length);
    }

    // --- Pagination Renderer ---
    function renderPagination(totalProducts) {
        const totalPages = Math.ceil(totalProducts / PRODUCTS_PER_PAGE);
        paginationContainer.innerHTML = '';
        if (totalPages <= 1) return;

        const createPageButton = (text, pageNumber, isActive, isDisabled) => {
            const button = document.createElement('button');
            button.textContent = text;
            button.classList.add('pagination-btn');
            if (isActive) button.classList.add('active');
            if (isDisabled) {
                button.disabled = true;
                button.classList.add('disabled');
            } else {
                button.addEventListener('click', () => {
                    currentPage = pageNumber;
                    renderProducts(filteredProducts);
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                });
            }
            return button;
        };

        paginationContainer.appendChild(createPageButton('←', currentPage - 1, false, currentPage === 1));

        for (let i = 1; i <= totalPages; i++) {
            paginationContainer.appendChild(createPageButton(i.toString(), i, i === currentPage, false));
        }

        paginationContainer.appendChild(createPageButton('→', currentPage + 1, false, currentPage === totalPages));
    }

    // ------------------------------------
    //  IV. EVENT LISTENERS
    // ------------------------------------
    priceRange.addEventListener('input', () => {
        priceValueSpan.textContent = `$${priceRange.value}`;
        applyClientFilters();
    });

    document.querySelectorAll('.filter-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', applyClientFilters);
    });

    document.querySelectorAll('.filter-header').forEach(header => {
        header.addEventListener('click', () => {
            const group = header.parentElement;
            group.classList.toggle('active');
        });
    });

    // --- Initial Load ---
    fetchAllProducts();
});
