import os
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "development-secret-change-me")
ENABLE_CACHE = os.getenv("ENABLE_CACHE", "0") == "1"

PRODUCTS = [
    {"id": 1, "name": "Cloud Skin Foundation", "brand": "LUMIÈRE", "category": "Face", "price": 1299, "shade": "Warm Beige", "description": "A breathable, skin-like foundation with buildable medium coverage and a natural finish.", "tag": "BESTSELLER", "image": "https://images.unsplash.com/photo-1631730359585-38a4935cbec4?auto=format&fit=crop&w=900&q=85"},
    {"id": 2, "name": "Petal Pop Blush", "brand": "ROSE & RUE", "category": "Cheeks", "price": 749, "shade": "Peach Bloom", "description": "A soft, blendable powder blush that gives cheeks a fresh pop of colour.", "tag": "NEW", "image": "https://images.unsplash.com/photo-1599733589046-10c005739ef6?auto=format&fit=crop&w=900&q=85"},
    {"id": 3, "name": "Velvet Matte Lipstick", "brand": "LUMIÈRE", "category": "Lips", "price": 899, "shade": "Rosewood", "description": "Comfortable, richly pigmented colour with a smooth velvet-matte finish.", "tag": "POPULAR", "image": "https://images.unsplash.com/photo-1586495777744-4413f21062fa?auto=format&fit=crop&w=900&q=85"},
    {"id": 4, "name": "Dew Drop Highlighter", "brand": "GLOW THEORY", "category": "Face", "price": 999, "shade": "Champagne", "description": "A finely milled, light-catching glow for a soft-focus highlight.", "tag": "", "image": "https://images.unsplash.com/photo-1611930022073-b7a4ba5fcccd?auto=format&fit=crop&w=900&q=85"},
    {"id": 5, "name": "Everyday Eye Palette", "brand": "ROSE & RUE", "category": "Eyes", "price": 1499, "shade": "Soft Neutrals", "description": "Eight easy-to-wear matte and shimmer shades for everyday looks.", "tag": "EDITORS' PICK", "image": "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?auto=format&fit=crop&w=900&q=85"},
    {"id": 6, "name": "Lash Lift Mascara", "brand": "GLOW THEORY", "category": "Eyes", "price": 699, "shade": "Carbon Black", "description": "A defining mascara that separates and lifts for an eye-opening look.", "tag": "", "image": "https://images.unsplash.com/photo-1631214524020-7e18db9a8f92?auto=format&fit=crop&w=900&q=85"},
    {"id": 7, "name": "Silk Touch Primer", "brand": "LUMIÈRE", "category": "Face", "price": 1099, "shade": "Universal", "description": "A smoothing makeup primer designed to help makeup apply evenly.", "tag": "", "image": "https://images.unsplash.com/photo-1601049541289-9b1b7bbbfe19?auto=format&fit=crop&w=900&q=85"},
    {"id": 8, "name": "Gloss Glaze Lip Oil", "brand": "ROSE & RUE", "category": "Lips", "price": 599, "shade": "Berry Sheen", "description": "A glossy lip oil with a comfortable, non-sticky feel.", "tag": "NEW", "image": "https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?auto=format&fit=crop&w=900&q=85"},
]

def find_product(product_id):
    return next((p for p in PRODUCTS if p["id"] == product_id), None)

def cart_details():
    cart = session.get("cart", {})
    rows, total = [], 0
    for product_id, quantity in cart.items():
        product = find_product(int(product_id))
        if product:
            subtotal = product["price"] * quantity
            rows.append({"product": product, "quantity": quantity, "subtotal": subtotal})
            total += subtotal
    return rows, total

@app.context_processor
def inject_cart_count():
    return {"cart_count": sum(session.get("cart", {}).values())}

@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        if not name or not email or "@" not in email:
            flash("Please enter your name and a valid email address.", "error")
            return render_template("login.html")
        session["customer"] = name
        session.setdefault("cart", {})
        return redirect(url_for("home"))
    if session.get("customer"):
        return redirect(url_for("home"))
    return render_template("login.html")

@app.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.get("/home")
def home():
    query = request.args.get("q", "").strip()
    category = request.args.get("category", "All")
    products = PRODUCTS
    if category != "All":
        products = [p for p in products if p["category"] == category]
    if query:
        q = query.lower()
        products = [p for p in products if q in p["name"].lower() or q in p["brand"].lower() or q in p["category"].lower()]
    return render_template("home.html", products=products, query=query, category=category)

@app.get("/product/<int:product_id>")
def product_detail(product_id):
    product = find_product(product_id)
    if not product:
        return render_template("404.html"), 404
    return render_template("product.html", product=product)

@app.post("/cart/add/<int:product_id>")
def add_to_cart(product_id):
    product = find_product(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    cart = session.get("cart", {})
    key = str(product_id)
    cart[key] = min(cart.get(key, 0) + 1, 10)
    session["cart"] = cart
    flash(f"{product['name']} added to your bag.", "success")
    if request.form.get("buy_now") == "1":
        return redirect(url_for("cart"))
    return redirect(request.referrer or url_for("home"))

@app.get("/cart")
def cart():
    rows, total = cart_details()
    return render_template("cart.html", rows=rows, total=total)

@app.post("/cart/update")
def update_cart():
    product_id = request.form.get("product_id", "")
    action = request.form.get("action", "")
    cart = session.get("cart", {})
    if product_id in cart:
        if action == "increase":
            cart[product_id] = min(cart[product_id] + 1, 10)
        elif action == "decrease":
            cart[product_id] -= 1
            if cart[product_id] <= 0:
                cart.pop(product_id)
        elif action == "remove":
            cart.pop(product_id)
    session["cart"] = cart
    return redirect(url_for("cart"))

@app.get("/api/products")
def api_products():
    return jsonify({"count": len(PRODUCTS), "products": PRODUCTS})

@app.get("/api/search")
def api_search():
    q = request.args.get("q", "").lower()
    matches = [p for p in PRODUCTS if q in p["name"].lower() or q in p["category"].lower() or q in p["brand"].lower()]
    return jsonify({"count": len(matches), "products": matches})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False, threaded=True)
