document.addEventListener('DOMContentLoaded', function() {
    // Глобальный поиск
    const searchToggle = document.getElementById('header-search-toggle');
    const searchFullscreen = document.getElementById('search-fullscreen');
    const closeSearch = document.getElementById('close-search');
    const globalSearchInput = document.getElementById('global-search-input');
    const globalSearchButton = document.getElementById('global-search-button');
    
    if (searchToggle && searchFullscreen) {
        searchToggle.addEventListener('click', openSearch);
        closeSearch.addEventListener('click', closeSearchPanel);
        globalSearchButton.addEventListener('click', performGlobalSearch);
        
        globalSearchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performGlobalSearch();
            }
        });
    }
    
    // Добавление в корзину
    const addToCartButtons = document.querySelectorAll('.btn-primary');
    const cartCount = document.querySelector('.cart-count');
    let cartItems = 0;
    
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function() {
            cartItems++;
            if (cartCount) {
                cartCount.textContent = cartItems;
                // Анимация счетчика корзины
                cartCount.style.transform = 'scale(1.2)';
                setTimeout(() => {
                    cartCount.style.transform = 'scale(1)';
                }, 300);
            }
            
            // Анимация добавления в корзину
            const originalText = this.textContent;
            this.textContent = 'Добавлено!';
            this.style.backgroundColor = '#4CAF50';
            
            setTimeout(() => {
                this.textContent = originalText;
                this.style.backgroundColor = '';
            }, 1500);
        });
    });
    
    // Плавное появление элементов при загрузке
    const animateElements = document.querySelectorAll('.logo, nav ul li, .header-actions button');
    animateElements.forEach((element, index) => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(-10px)';
        
        setTimeout(() => {
            element.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, 100 + index * 100);
    });
    
    function openSearch() {
        searchFullscreen.style.display = 'flex';
        setTimeout(() => {
            searchFullscreen.classList.add('active');
            globalSearchInput.focus();
        }, 10);
    }
    
    function closeSearchPanel() {
        searchFullscreen.classList.remove('active');
        setTimeout(() => {
            searchFullscreen.style.display = 'none';
            globalSearchInput.value = '';
        }, 300);
    }
    
    function performGlobalSearch() {
        const query = globalSearchInput.value.trim();
        if (query) {
            window.location.href = '/search?type=vin&q=' + encodeURIComponent(query);
            closeSearchPanel();
        }
    }


    // Добавьте эти функции в script.js

    // Глобальная переменная для хранения состояния корзины
    let cartState = {
        items: [],
        total: 0,
        count: 0
    };

    // Функция добавления в корзину
    function addToCart(partId, button) {
        // Добавляем товар в состояние корзины
        const newItem = {
            id: partId,
            quantity: 1,
            // Здесь будут данные о товаре
        };
        
        cartState.items.push(newItem);
        cartState.count++;
        
        // Обновляем счетчик корзины в header
        updateCartCount();
        
        // Анимация добавления
        const originalText = button.innerHTML;
        button.innerHTML = '<i class="fas fa-check"></i> Добавлено';
        button.style.backgroundColor = '#4CAF50';
        
        setTimeout(() => {
            button.innerHTML = originalText;
            button.style.backgroundColor = '';
        }, 1500);
        
        // Отправляем данные на сервер (в реальном приложении)
        fetch('/api/cart/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ partId: partId })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Товар добавлен в корзину:', data);
        })
        .catch(error => {
            console.error('Ошибка:', error);
        });
    }

    // Обновление счетчика корзины
    function updateCartCount() {
        const cartCount = document.querySelector('.cart-count');
        if (cartCount) {
            cartCount.textContent = cartState.count;
            // Анимация
            cartCount.style.transform = 'scale(1.2)';
            setTimeout(() => {
                cartCount.style.transform = 'scale(1)';
            }, 300);
        }
    }

    // Инициализация корзины при загрузке
    function initCart() {
        // Загрузка состояния корзины из localStorage или сервера
        const savedCart = localStorage.getItem('cart');
        if (savedCart) {
            cartState = JSON.parse(savedCart);
            updateCartCount();
        }
    }

    // Сохранение состояния корзины
    function saveCart() {
        localStorage.setItem('cart', JSON.stringify(cartState));
    }

    // Вызов инициализации при загрузке
    document.addEventListener('DOMContentLoaded', function() {
        initCart();
        
        // Обработчики для кнопок добавления в корзину
        document.querySelectorAll('.add-to-cart').forEach(button => {
            button.addEventListener('click', function() {
                const partId = this.getAttribute('data-part-id');
                addToCart(partId, this);
            });
        });
    });





    
    // Загрузка данных для страниц
    if (typeof loadPageData === 'function') {
        loadPageData();
    }
});