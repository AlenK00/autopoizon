from flask import Flask, render_template, request, jsonify
import json
import os
import random

app = Flask(__name__)

# Загрузка данных
def load_data(filename):
    try:
        with open(f'data/{filename}', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Главная страница
@app.route('/')
def index():
    brands = load_data('brands.json')
    return render_template('index.html', brands=brands)

# Страница каталога
"""@app.route('/catalog')
def catalog():
    return render_template('catalog.html')"""

# Добавьте этот маршрут в app.py
@app.route('/catalog')
def catalog():
    parts = load_data('parts.json')
    
    # Добавим больше демо-данных для каталога
    if not parts or len(parts) < 10:
        parts = generate_demo_parts()
    
    return render_template('catalog.html', parts=parts)

# Добавьте эту функцию для генерации демо-данных
def generate_demo_parts():
    categories = [
        "Двигатель", "Трансмиссия", "Тормозная система", 
        "Подвеска", "Электрика", "Кузовные детали", "Салон"
    ]
    
    brands = ["chery", "geely", "haval", "changan", "byd", "jac", "dfsk", "faw", "baic"]
    models = ["tiggo", "coolray", "h6", "cs75", "song", "s7", "x70", "f7", "beijing"]
    
    demo_parts = []
    
    for i in range(1, 31):  # 30 демо-товаров
        category = random.choice(categories)
        brand = random.choice(brands)
        model = random.choice(models)
        
        part = {
            "id": f"part_{i:03d}",
            "name": f"{category} {random.choice(['комплект', 'деталь', 'модуль'])} {brand.upper()}",
            "part_number": f"{brand.upper()}-{model.upper()}-{i:03d}",
            "brand_id": brand,
            "model_id": model,
            "category": category,
            "price": random.randint(500, 30000),
            "image": f"part_{random.randint(1, 10)}.jpg",
            "vin_compatibility": [f"LVVDB11B8BD{random.randint(100000, 999999)}" for _ in range(3)]
        }
        
        demo_parts.append(part)
    
    return demo_parts

# Страница марок
@app.route('/brands')
def brands():
    brands = load_data('brands.json')
    return render_template('brands.html', brands=brands)

# Страница моделей марки
@app.route('/brand/<brand_id>')
def brand_models(brand_id):
    brands = load_data('brands.json')
    models = load_data('models.json')
    
    brand = next((b for b in brands if b['id'] == brand_id), None)
    brand_models = [m for m in models if m['brand_id'] == brand_id]
    
    if not brand:
        return "Марка не найдена", 404
        
    return render_template('brand_models.html', brand=brand, models=brand_models)

# Страница годов выпуска модели
@app.route('/model/<model_id>')
def model_years(model_id):
    models = load_data('models.json')
    model = next((m for m in models if m['id'] == model_id), None)
    
    if not model:
        return "Модель не найдена", 404
        
    # Годы выпуска (в реальном приложении брались бы из базы данных)
    years = list(range(2015, 2023))
        
    return render_template('model_years.html', model=model, years=years)

# Поиск по VIN
@app.route('/search')
def search():
    query = request.args.get('q', '')
    search_type = request.args.get('type', 'vin')
    model_id = request.args.get('model', '')
    year = request.args.get('year', '')
    
    # Здесь будет логика поиска по VIN или номеру детали
    results = []
    
    if search_type == 'vin':
        # Поиск по VIN
        results = search_by_vin(query, model_id, year)
    else:
        # Поиск по номеру детали
        results = search_by_part_number(query)
    
    return render_template('search_results.html', query=query, results=results, search_type=search_type)


# API для поиска по VIN
@app.route('/api/search/vin')
def api_search_vin():
    vin = request.args.get('q', '')
    results = search_by_vin(vin)
    return jsonify(results)

# API для поиска по номеру детали
@app.route('/api/search/part')
def api_search_part():
    part_number = request.args.get('q', '')
    results = search_by_part_number(part_number)
    return jsonify(results)



#-------------
# Добавьте эти маршруты в app.py после существующих

# Страница профиля
@app.route('/profile')
def profile():
    # Данные пользователя (в реальном приложении из базы данных)
    user_data = {
        "full_name": "Иванова Анна Сергеевна",
        "email": "anna.ivanova@email.com",
        "phone": "+7 (999) 123-45-67",
        "company": "ООО 'АвтоСервис'",
        "inn": "1234567890",
        "address": {
            "city": "Москва",
            "street": "ул. Ленина, д. 123",
            "postal_code": "123456"
        },
        "delivery_preferences": {
            "courier": True,
            "pickup": False,
            "express_delivery": True
        }
    }
    return render_template('profile.html', user=user_data)

# Страница корзины
@app.route('/cart')
def cart():
    cart_items = [
        {
            "id": "part_001",
            "name": "Тормозные колодки передние",
            "part_number": "CH-TG-001",
            "price": 4500,
            "quantity": 2,
            "image": "part_1.jpg",
            "brand": "Chery",
            "model": "Tiggo"
        },
        {
            "id": "part_003",
            "name": "Свечи зажигания",
            "part_number": "GL-CR-001",
            "price": 2800,
            "quantity": 1,
            "image": "part_3.jpg",
            "brand": "Geely",
            "model": "Coolray"
        }
    ]
    
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

# Страница оформления заказа
@app.route('/checkout')
def checkout():
    # Данные для страницы оформления
    order_data = {
        "items": [
            {
                "id": "part_001",
                "name": "Тормозные колодки передние",
                "price": 4500,
                "quantity": 2,
                "total": 9000
            },
            {
                "id": "part_003", 
                "name": "Свечи зажигания",
                "price": 2800,
                "quantity": 1,
                "total": 2800
            }
        ],
        "subtotal": 11800,
        "shipping": 0,
        "discount": 590,
        "total": 11210,
        "address": {
            "city": "Москва",
            "street": "ул. Ленина, д. 123",
            "postal_code": "123456"
        }
    }
    
    return render_template('checkout.html', order=order_data)

# API для работы с корзиной
@app.route('/api/cart/add', methods=['POST'])
def api_cart_add():
    data = request.json
    # Логика добавления в корзину
    return jsonify({"success": True, "message": "Товар добавлен в корзину"})

@app.route('/api/cart/update', methods=['POST'])
def api_cart_update():
    data = request.json
    # Логика обновления корзины
    return jsonify({"success": True, "message": "Корзина обновлена"})

@app.route('/api/cart/remove', methods=['POST'])
def api_cart_remove():
    data = request.json
    # Логика удаления из корзины
    return jsonify({"success": True, "message": "Товар удален из корзины"})

@app.route('/api/order/create', methods=['POST'])
def api_order_create():
    data = request.json
    # Логика создания заказа
    return jsonify({"success": True, "order_id": "ORD-123456", "message": "Заказ создан"})
#---------




# Заглушки функций поиска
"""def search_by_vin(vin):
    # В реальном приложении здесь был бы поиск в базе данных
    parts = load_data('parts.json')
    return [p for p in parts if vin.lower() in p.get('vin_compatibility', [])]"""

def search_by_vin(vin, model_id='', year=''):
    # В реальном приложении здесь был бы поиск в базе данных
    parts = load_data('parts.json')
    filtered_parts = parts
    
    # Фильтрация по VIN
    if vin:
        filtered_parts = [p for p in filtered_parts if vin.lower() in [v.lower() for v in p.get('vin_compatibility', [])]]
    
    # Фильтрация по модели
    if model_id:
        filtered_parts = [p for p in filtered_parts if p.get('model_id') == model_id]
    
    # Фильтрация по году
    if year:
        try:
            year_int = int(year)
            filtered_parts = [p for p in filtered_parts if year_int in p.get('years', [])]
        except ValueError:
            pass
    
    return filtered_parts







def search_by_part_number(part_number):
    # В реальном приложении здесь был бы поиск в базе данных
    parts = load_data('parts.json')
    return [p for p in parts if part_number.lower() in p.get('part_number', '').lower()]

if __name__ == '__main__':
    # Создаем папки, если их нет
    os.makedirs('data', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('static/images/brands', exist_ok=True)
    
    # Запускаем приложение
    app.run(debug=True, port=5001)