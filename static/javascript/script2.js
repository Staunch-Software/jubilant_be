document.addEventListener('DOMContentLoaded', () => {

  // ------------------------------------
  // CONFIGURATION
  // ------------------------------------
  const API_HOST = 'http://127.0.0.1:5000';
  const API_ALL_PRODUCTS_URL = `${API_HOST}/api/products/hdd`;
  const PRODUCTS_PER_PAGE = 10;

  // ------------------------------------
  // DOM REFERENCES
  // ------------------------------------
  const productGrid = document.getElementById('product-grid');
  const filterSidebar = document.querySelector('.filter-sidebar');
  const paginationContainer = document.getElementById('pagination-container');

  // Price filter (optional – skip if not in HTML)
  const priceRange = document.getElementById('price-max');
  const priceValueSpan = document.getElementById('price-value');

  // ------------------------------------
  // STATE
  // ------------------------------------
  let allProducts = [];
  let filteredProducts = [];
  let currentPage = 1;

  // ------------------------------------
  // FILTER COLLECTION
  // ------------------------------------
  function collectFilters() {
    const filters = {
      category: [],
      brand: [],
      application: [],
      capacity: [],
      form_factor: [],
      rpm: [],
      interface: [],
      speed: [],
      cache: [],
      maxPrice: priceRange ? parseFloat(priceRange.value) : Infinity
    };

    document.querySelectorAll('.filter-checkbox:checked').forEach(checkbox => {
      const group = checkbox.name;
      const value = checkbox.value;

      if (group in filters) {
        if (['capacity', 'rpm', 'speed', 'cache'].includes(group)) {
          filters[group].push(parseFloat(value));
        } else {
          filters[group].push(value);
        }
      }
    });

    return filters;
  }

  // ------------------------------------
  // CLIENT-SIDE FILTERING
  // ------------------------------------
  function applyClientFilters() {
    const filters = collectFilters();

    filteredProducts = allProducts.filter(product => {
      if (product.price > filters.maxPrice) return false;

      if (filters.category.length && !filters.category.includes(product.category)) return false;
      if (filters.brand.length && !filters.brand.includes(product.brand)) return false;
      if (filters.application.length && !filters.application.includes(product.application)) return false;
      if (filters.capacity.length && !filters.capacity.includes(product.capacity)) return false;
      if (filters.form_factor.length && !filters.form_factor.includes(product.form_factor)) return false;
      if (filters.rpm.length && !filters.rpm.includes(product.rpm)) return false;
      if (filters.interface.length && !filters.interface.includes(product.interface)) return false;
      if (filters.speed.length && !filters.speed.includes(product.speed)) return false;
      if (filters.cache.length && !filters.cache.includes(product.cache)) return false;

      return true;
    });

    currentPage = 1;
    renderProducts(filteredProducts);
  }

  // ------------------------------------
  // FETCH PRODUCTS FROM BACKEND
  // ------------------------------------
  async function fetchAllProducts() {
    productGrid.innerHTML = '<p class="loading-message">Loading hard drive products...</p>';
    filterSidebar.style.opacity = '0.5';

    try {
      const response = await fetch(API_ALL_PRODUCTS_URL);
      if (!response.ok) throw new Error('Failed to fetch products.');

      const data = await response.json();
      allProducts = (data.products || [])
        .filter(p => p.category && p.category.toLowerCase().includes('hdd')) // show only HDDs/SSDs
        .map(p => ({
          ...p,
          price: parseFloat(p.price),
          capacity: parseFloat(p.capacity),
          rpm: parseFloat(p.rpm),
          cache: parseFloat(p.cache),
          speed: parseFloat(p.speed),
          description: p.description || 'No description available.'
        }));

      filteredProducts = allProducts;
      renderProducts(filteredProducts);
      filterSidebar.style.opacity = '1';
    } catch (err) {
      console.error('Error loading products:', err);
      productGrid.innerHTML = `<p class="error-message">Error: ${err.message}</p>`;
    }
  }

  // ------------------------------------
  // PRODUCT RENDERING + PAGINATION
  // ------------------------------------
  function renderProducts(productsToRender) {
    const startIndex = (currentPage - 1) * PRODUCTS_PER_PAGE;
    const endIndex = startIndex + PRODUCTS_PER_PAGE;
    const pageProducts = productsToRender.slice(startIndex, endIndex);

    productGrid.innerHTML = '';

    if (pageProducts.length === 0) {
      productGrid.innerHTML = '<p class="empty-message">No products match your filters.</p>';
      renderPagination(productsToRender.length);
      return;
    }

    pageProducts.forEach(product => {
      const specs = [
        `Brand: ${product.brand || 'N/A'}`,
        `Capacity: ${product.capacity || 'N/A'} GB`,
        `RPM: ${product.rpm || 'N/A'}`,
        `Form Factor: ${product.form_factor || 'N/A'}`,
        `Interface: ${product.interface || 'N/A'}`,
        `Cache: ${product.cache || 'N/A'} MB`,
        `Speed: ${product.speed || 'N/A'} MB/s`
      ].join(' | ');

      const card = `
        <div class="product-card">
          <div class="product-image-container">
            <img src="${API_HOST}${product.image}" alt="${product.name}" 
                 onerror="this.src='https://placehold.co/150x150/d1d5db/374151?text=No+Image'">
          </div>
          <div class="product-details">
            <h4>${product.name}</h4>
            <p class="product-spec-snippet">${product.description}</p>
            <small>${specs}</small>
          </div>
          <div class="product-actions">
            <p class="price-value">US <span class="price-large">$${product.price.toFixed(2)}</span>/pcs</p>
            <p class="moq-info">MOQ: 20 pcs</p>
            <button class="inquiry-btn" onclick="window.location.href='/inquiry.html?product=${encodeURIComponent(product.name)}'">Inquiry</button>
          </div>
        </div>
      `;
      productGrid.insertAdjacentHTML('beforeend', card);
    });

    renderPagination(productsToRender.length);
  }

  // ------------------------------------
  // PAGINATION RENDERER
  // ------------------------------------
  function renderPagination(totalProducts) {
    const totalPages = Math.ceil(totalProducts / PRODUCTS_PER_PAGE);
    paginationContainer.innerHTML = '';
    if (totalPages <= 1) return;

    const createButton = (text, pageNum, disabled = false, active = false) => {
      const btn = document.createElement('button');
      btn.textContent = text;
      btn.classList.add('pagination-btn');
      if (active) btn.classList.add('active');
      if (disabled) {
        btn.disabled = true;
        btn.classList.add('disabled');
      } else {
        btn.addEventListener('click', () => {
          currentPage = pageNum;
          renderProducts(filteredProducts);
          window.scrollTo({ top: 0, behavior: 'smooth' });
        });
      }
      return btn;
    };

    paginationContainer.appendChild(createButton('←', currentPage - 1, currentPage === 1));

    for (let i = 1; i <= totalPages; i++) {
      paginationContainer.appendChild(createButton(i, i, false, i === currentPage));
    }

    paginationContainer.appendChild(createButton('→', currentPage + 1, currentPage === totalPages));
  }

  // ------------------------------------
  // EVENT LISTENERS
  // ------------------------------------
  document.querySelectorAll('.filter-checkbox').forEach(checkbox => {
    checkbox.addEventListener('change', applyClientFilters);
  });

  document.querySelectorAll('.filter-header').forEach(header => {
    header.addEventListener('click', () => {
      header.parentElement.classList.toggle('active');
    });
  });

  if (priceRange && priceValueSpan) {
    priceValueSpan.textContent = `$${priceRange.value}`;
    priceRange.addEventListener('input', () => {
      priceValueSpan.textContent = `$${priceRange.value}`;
      applyClientFilters();
    });
  }

  // ------------------------------------
  // INITIAL LOAD
  // ------------------------------------
  fetchAllProducts();

});
