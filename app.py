from flask import Flask, request, jsonify, send_from_directory, render_template, abort
from flask_cors import CORS
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import psycopg2
from dotenv import load_dotenv

# ======================================================
# ✅ LOAD ENVIRONMENT VARIABLES
# ======================================================
load_dotenv()


# ======================================================
# ✅ FRONTEND PATH SETUP (Environment-Independent)
# ======================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'jubilant_ui'))
TEMPLATES_DIR = os.path.join(FRONTEND_DIR, 'templates')
STATIC_DIR = os.path.join(FRONTEND_DIR, 'static')

# Debug print (optional)
print(f"🧩 Using templates from: {TEMPLATES_DIR}")
print(f"🧩 Using static files from: {STATIC_DIR}")

# ======================================================
# ✅ Initialize Flask
# ======================================================
app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)
CORS(app)

# ======================================================
# ✅ SMTP CONFIGURATION
# ======================================================
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
TO_EMAIL = "goguldev28@gmail.com"

# ======================================================
# ✅ POSTGRESQL CONFIGURATION
# ======================================================
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

print(f"🔍 Connecting to PostgreSQL: host={DB_HOST}, dbname={DB_NAME}, user={DB_USER}")

conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASS
)
cur = conn.cursor()

# ======================================================
# ✅ STATIC & TEMPLATE ROUTES
# ======================================================
@app.route("/")
def home():
    return render_template("index.html")

@app.route('/images/<path:filename>')
def serve_images(filename):
    image_folder = os.path.join(STATIC_DIR, 'images')
    return send_from_directory(image_folder, filename)

@app.route('/productslist/<slug>.html')
def product_page(slug):
    slug = slug.lower().strip()
    file_path = f'productslist/{slug}.html'
    full_path = os.path.join(TEMPLATES_DIR, file_path)
    if os.path.exists(full_path):
        return render_template(file_path)
    else:
        return f"<h2>Product page for '{slug}' not found.</h2>", 404

# ======================================================
# ✅ MOCK PRODUCT DATA & SHORTLIST API
# ======================================================
# (Your existing product, HDD, and shortlist logic stays the same)
# — I’ve kept it all here
# (No changes made to your product data, filtering, or DB logic)

MOCK_PRODUCTS = [
    {
        "id": "cpu-101",
        "name": "Intel",
        "price": 189.00,
        "brand": "Intel",
        "category": "Intel CPU Processors Whole CPU Processors",
        "application": "Gaming",
        "socket": "LGA1700",
        "cores": 24,
        "threads": 32,
        "base_freq": 3.0,
        "cache": 32,
        "tdp": 125,
        "tech": "7nm",
        "memory_type": "DDR5",
        "max_memory_size": 128,
        "packaging": "Boxed",
        "image": "/static/images/amdepyc.jpg",
    },
    {
        "id": "cpu-112",
        "name": "Intel Core i9-13900K",
        "price": 189.00,
        "brand": "Intel",
        "category": "CPU Processors - Desktops Whole CPU Processors",
        "application": "Gaming",
        "socket": "LGA1700",
        "cores": 24,
        "threads": 32,
        "base_freq": 3.0,
        "cache": 36,
        "tdp": 125,
        "tech": "7nm",
        "memory_type": "DDR5",
        "max_memory_size": 128,
        "packaging": "Boxed",
        "image": "/static/images/amdepyc.jpg",
        "description": "abcdeoid e;ifnh,iFBYERJKH,GFB,wmg",
    },
    {
        "id": "cpu-102",
        "name": "AMD Ryzen 9 7950X",
        "price": 699.00,
        "brand": "AMD",
        "category": "AMD CPU Processors Whole CPU Processors",
        "application": "Desktop",
        "socket": "AM5",
        "cores": 16,
        "threads": 32,
        "base_freq": 4.5,
        "cache": 64,
        "tdp": 170,
        "tech": "5nm",
        "memory_type": "DDR5",
        "max_memory_size": 128,
        "packaging": "Boxed",
        "image": "/static/images/amdepyc.jpg",
    },
    {
        "id": "cpu-103",
        "name": "Intel Xeon Silver 4314",
        "price": 550.00,
        "brand": "Intel",
        "category": "Processors - Servers Whole CPU Processors",
        "application": "Server",
        "socket": "LGA4677",
        "cores": 16,
        "threads": 32,
        "base_freq": 2.4,
        "cache": 30,
        "tdp": 105,
        "tech": "10nm",
        "memory_type": "DDR5",
        "max_memory_size": 512,
        "packaging": "Tray",
        "image": "/static/images/amdepyc.jpg",
    },
    {
        "id": "cpu-104",
        "name": "AMD EPYC 9654",
        "price": 399.00,
        "brand": "AMD",
        "category": "Processors - Servers Whole CPU Processors",
        "application": "Server",
        "socket": "SP5",
        "cores": 96,
        "threads": 192,
        "base_freq": 2.7,
        "cache": 384,
        "tdp": 360,
        "tech": "5nm",
        "memory_type": "DDR5",
        "max_memory_size": 2048,
        "packaging": "Tray",
        "image": "/static/images/amdepyc.jpg",
    },
    {
        "id": "cpu-105",
        "name": "Intel Core i5-12400",
        "price": 179.00,
        "brand": "Intel",
        "category": "CPU Processors - Desktops",
        "application": "Desktop",
        "socket": "LGA1700",
        "cores": 6,
        "threads": 12,
        "base_freq": 2.5,
        "cache": 18,
        "tdp": 65,
        "tech": "10nm",
        "memory_type": "DDR4",
        "max_memory_size": 128,
        "packaging": "Boxed",
        "image": "/static/images/amdepyc.jpg",
    },
    {
        "id": "cpu-106",
        "name": "AMD Ryzen 5 7600",
        "price": 229.00,
        "brand": "AMD",
        "category": "AMD CPU Processors",
        "application": "Personal",
        "socket": "AM5",
        "cores": 6,
        "threads": 12,
        "base_freq": 3.8,
        "cache": 32,
        "tdp": 65,
        "tech": "5nm",
        "memory_type": "DDR5",
        "max_memory_size": 128,
        "packaging": "Boxed",
        "image": "/static/images/amdepyc.jpg",
    },
    {
        "id": "cpu-107",
        "name": "Intel Core i7-12700K",
        "price": 409.00,
        "brand": "Intel",
        "category": "CPU Processors - Desktops",
        "application": "Gaming",
        "socket": "LGA1700",
        "cores": 12,
        "threads": 20,
        "base_freq": 3.6,
        "cache": 25,
        "tdp": 125,
        "tech": "10nm",
        "memory_type": "DDR5",
        "max_memory_size": 128,
        "packaging": "Boxed",
        "image": "/static/images/amdepyc.jpg",
    },
    {
        "id": "cpu-108",
        "name": "AMD Ryzen Threadripper Pro 3995WX",
        "price": 299.00,
        "brand": "AMD",
        "category": "Processors - Servers",
        "application": "Server",
        "socket": "sTRX4",
        "cores": 64,
        "threads": 128,
        "base_freq": 2.7,
        "cache": 256,
        "tdp": 280,
        "tech": "7nm",
        "memory_type": "DDR4",
        "max_memory_size": 2048,
        "packaging": "Tray",
        "image": "/static/images/amdepyc.jpg",
    },
    {
        "id": "cpu-109",
        "name": "Intel Core i3-12100",
        "price": 109.00,
        "brand": "Intel",
        "category": "CPU Processors - Desktops",
        "application": "Personal",
        "socket": "LGA1700",
        "cores": 4,
        "threads": 8,
        "base_freq": 3.3,
        "cache": 12,
        "tdp": 60,
        "tech": "10nm",
        "memory_type": "DDR4",
        "max_memory_size": 64,
        "packaging": "Boxed",
        "image": "/static/images/amdepyc.jpg",
    },
    {
        "id": "cpu-110",
        "name": "AMD Ryzen 7 7700X",
        "price": 329.00,
        "brand": "AMD",
        "category": "AMD CPU Processors",
        "application": "Gaming",
        "socket": "AM5",
        "cores": 8,
        "threads": 16,
        "base_freq": 4.5,
        "cache": 32,
        "tdp": 105,
        "tech": "5nm",
        "memory_type": "DDR5",
        "max_memory_size": 128,
        "packaging": "Boxed",
        "image": "/static/images/amdepyc.jpg",
    }
] # keep your full data here
HDD_PRODUCTS = [
    {
        "id": "hdd001",
        "name": "Seagate Barracuda 1TB",
        "brand": "Seagate",
        "category": "Internal HDD",
        "application": "Desktop",
        "capacity": 1000,
        "rpm": 7200,
        "form_factor": "3.5",
        "interface": "SATA",
        "speed": 200,
        "cache": 64,
        "price": 39.99,
        "image": "/static/images/seagate_1tb.jpg",
        "description": "Reliable 1TB HDD for desktop PCs."
    },
    {
        "id": "hdd002",
        "name": "Western Digital Blue 2TB",
        "brand": "Western Digital",
        "category": "Internal HDD",
        "application": "Desktop",
        "capacity": 2000,
        "rpm": 7200,
        "form_factor": "3.5",
        "interface": "SATA",
        "speed": 200,
        "cache": 64,
        "price": 54.99,
        "image": "/static/images/wd_blue_2tb.jpg",
        "description": "WD Blue 2TB HDD ideal for storage upgrades."
    },
    {
        "id": "hdd003",
        "name": "Toshiba X300 4TB",
        "brand": "Toshiba",
        "category": "Enterprise HDD",
        "application": "Server",
        "capacity": 4000,
        "rpm": 7200,
        "form_factor": "3.5",
        "interface": "SATA",
        "speed": 240,
        "cache": 128,
        "price": 109.99,
        "image": "/static/images/toshiba_x300_4tb.jpg",
        "description": "High-performance enterprise-grade HDD."
    },
    {
        "id": "hdd004",
        "name": "Seagate IronWolf 8TB NAS",
        "brand": "Seagate",
        "category": "NAS",
        "application": "NAS",
        "capacity": 8000,
        "rpm": 7200,
        "form_factor": "3.5",
        "interface": "SATA",
        "speed": 210,
        "cache": 256,
        "price": 179.99,
        "image": "/static/images/ironwolf_8tb.jpg",
        "description": "Designed for NAS systems with continuous operation."
    },
    {
        "id": "hdd005",
        "name": "Samsung T7 Portable SSD 1TB",
        "brand": "Samsung",
        "category": "SSD",
        "application": "External",
        "capacity": 1000,
        "rpm": None,
        "form_factor": "M.2",
        "interface": "USB 3.0",
        "speed": 3500,
        "cache": 0,
        "price": 139.99,
        "image": "/static/images/samsung_t7.jpg",
        "description": "Ultra-fast portable SSD for professionals."
    }
]  # keep your full HDD data here
shortlist_db = {'user-123': ['cpu-101', 'cpu-106', 'cpu-109']}

def get_user_id():
    return 'user-123'

@app.route('/api/products/all', methods=['GET'])
def get_all_products():
    user_id = get_user_id()
    user_shortlist_ids = shortlist_db.get(user_id, [])
    all_products_with_status = []
    for product in MOCK_PRODUCTS:
        product_copy = product.copy()
        product_copy['isShortlisted'] = product_copy['id'] in user_shortlist_ids
        all_products_with_status.append(product_copy)
    return jsonify({"success": True, "products": all_products_with_status})

@app.route('/api/shortlist/filter', methods=['POST'])
def filter_shortlist():
    user_id = get_user_id()
    filters = request.json or {}
    user_shortlist_ids = shortlist_db.get(user_id, [])
    shortlisted_products = [p.copy() for p in MOCK_PRODUCTS if p['id'] in user_shortlist_ids]

    def to_int_list(v):
        if not v:
            return []
        return [int(x) for x in v]

    filter_brands = filters.get('brands', [])
    filter_categories = filters.get('categories', [])
    filter_applications = filters.get('applications', [])
    filter_sockets = filters.get('sockets', [])
    filter_cores = to_int_list(filters.get('cores', []))
    filter_threads = to_int_list(filters.get('threads', []))
    filter_cache = to_int_list(filters.get('cache', []))
    filter_tech = filters.get('tech', [])
    max_price = float(filters.get('maxPrice', float('inf')))
    max_freq = float(filters.get('maxFreq', float('inf')))
    max_cache = float(filters.get('maxCache', float('inf')))
    max_tdp = float(filters.get('maxTdp', float('inf')))

    final_products = []
    for product in shortlisted_products:
        try:
            if filter_brands and product.get('brand') not in filter_brands:
                continue
            if filter_categories and not any(cat in (product.get('category') or '') for cat in filter_categories):
                continue
            if filter_applications and product.get('application') not in filter_applications:
                continue
            if filter_sockets and product.get('socket') not in filter_sockets:
                continue
            if filter_cores and int(product.get('cores', 0)) not in filter_cores:
                continue
            if filter_threads and int(product.get('threads', 0)) not in filter_threads:
                continue
            if filter_cache and int(product.get('cache', 0)) not in filter_cache:
                continue
            if filter_tech and product.get('tech') not in filter_tech:
                continue
            if float(product.get('price', 0)) > max_price:
                continue
            if float(product.get('base_freq', 0)) > max_freq:
                continue
            if float(product.get('cache', 0)) > max_cache:
                continue
            if float(product.get('tdp', 0)) > max_tdp:
                continue
            product['isShortlisted'] = True
            final_products.append(product)
        except Exception:
            continue

    return jsonify({"success": True, "products": final_products})


@app.route('/api/shortlist/toggle', methods=['POST'])
def toggle_shortlist():
    user_id = get_user_id()
    data = request.json or {}
    product_id = data.get('productId')
    action = data.get('action')

    if not product_id or action not in ['add', 'remove']:
        return jsonify({"success": False, "message": "Invalid product or action."}), 400

    if user_id not in shortlist_db:
        shortlist_db[user_id] = []

    user_shortlist = shortlist_db[user_id]

    if action == 'add':
        if product_id not in user_shortlist:
            user_shortlist.append(product_id)
            return jsonify({"success": True, "message": "Product added to shortlist."}), 201
        else:
            return jsonify({"success": True, "message": "Already shortlisted."}), 200
    else:
        shortlist_db[user_id] = [id for id in user_shortlist if id != product_id]
        return jsonify({"success": True, "message": "Product removed from shortlist."}), 200


# ======================================================
# ✅ CONTACT, CONSULTATION, INQUIRY ROUTES (unchanged)
# ======================================================
@app.route("/send-contact", methods=["POST"])
def send_contact():
    try:
        product_name = request.form.get("product_name") or request.form.get("product-name")
        quantity = request.form.get("quantity")
        company_name = request.form.get("company_name") or request.form.get("company-name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        inquiry_details = request.form.get("inquiry_details") or request.form.get("inquiry-details")
        get_notified = request.form.get("get_notified") == "on"

        cur.execute("""
            INSERT INTO contact_form (product_name, quantity, company_name, email, phone, inquiry_details, get_notified)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (product_name, quantity, company_name, email, phone, inquiry_details, get_notified))
        conn.commit()

        msg = MIMEMultipart()
        msg["From"] = SMTP_USER
        msg["To"] = TO_EMAIL
        msg["Subject"] = f"New Contact Form Submission from {company_name or 'Unknown Company'}"
        msg.attach(MIMEText(f"""
        A new contact form submission was received:

        Product Name: {product_name}
        Quantity: {quantity}
        Company Name: {company_name}
        Email: {email}
        Phone: {phone}
        Inquiry Details: {inquiry_details}
        Wants Notification: {'Yes' if get_notified else 'No'}
        """, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)

        return jsonify({"success": True, "message": "✅ Your message has been sent successfully!"})
    except Exception as e:
        print("❌ Error handling contact form:", e)
        return jsonify({"success": False, "message": "❌ Something went wrong. Please try again."}), 500


@app.route("/send-consultation", methods=["POST"])
def send_consultation():
    try:
        product_name = request.form.get("product_name")
        quantity = request.form.get("quantity")
        company_name = request.form.get("company_name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        inquiry_details = request.form.get("inquiry_details")
        notify_price = request.form.get("notify_price") == "on"

        cur.execute("""
            INSERT INTO consultations (product_name, quantity, company_name, email, phone, inquiry_details, notify_price)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (product_name, quantity, company_name, email, phone, inquiry_details, notify_price))
        conn.commit()

        msg = MIMEMultipart()
        msg["From"] = SMTP_USER
        msg["To"] = TO_EMAIL
        msg["Subject"] = f"New Consultation Request from {company_name or 'Unknown Company'}"
        body = f"""
        New Consultation Request Received:

        Product Name: {product_name}
        Quantity: {quantity}
        Company Name: {company_name}
        Email: {email}
        Phone: {phone}
        Inquiry Details: {inquiry_details}
        Notify for Price: {'Yes' if notify_price else 'No'}
        """
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)

        return jsonify({"success": True, "message": "✅ Your consultation has been submitted successfully!"})
    except Exception as e:
        print("❌ Error in /send-consultation:", e)
        return jsonify({"success": False, "message": "❌ Something went wrong while submitting your request."}), 500


@app.route("/send-inquiry", methods=["POST"])
def send_inquiry():
    try:
        name = request.form.get("name")
        sender_email = request.form.get("email")
        phone = request.form.get("phone")
        product = request.form.get("product")
        quantity = request.form.get("quantity") or 0

        cur.execute("""
            INSERT INTO inquiries (name, email, phone, product, quantity)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, sender_email, phone, product, quantity))
        conn.commit()

        msg = MIMEMultipart()
        msg["From"] = SMTP_USER
        msg["To"] = TO_EMAIL
        msg["Subject"] = f"New Inquiry from {name}"
        msg.add_header('Reply-To', sender_email)

        body = f"""
        New Inquiry received:

        Name: {name}
        Email: {sender_email}
        Phone: {phone}
        Product: {product}
        Quantity: {quantity}
        """
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)

        return jsonify({"success": True, "message": "✅ Inquiry saved and email sent successfully!"})
    except Exception as e:
        print("❌ Error in /send-inquiry:", e)
        return jsonify({"success": False, "message": "❌ Failed to process inquiry."}), 500

@app.route("/send-submit", methods=["POST"])
def send_submit():
    try:
        product_name = request.form.get("product-name")
        quantity = request.form.get("quantity")
        company_name = request.form.get("company-name")
        email = request.form.get("email-address")
        phone = request.form.get("phone")
        inquiry_details = request.form.get("inquiry-details")
        notify_prices = request.form.get("notify-prices") == "on"

        cur.execute("""
            INSERT INTO inquiry_submissions (product_name, quantity, company_name, email, phone, inquiry_details, notify_prices)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (product_name, quantity, company_name, email, phone, inquiry_details, notify_prices))
        conn.commit()

        msg = MIMEMultipart()
        msg["From"] = SMTP_USER
        msg["To"] = TO_EMAIL
        msg["Subject"] = f"New Inquiry Form Submission - {company_name or 'No Company'}"
        body = f"""
        A new inquiry has been received.

        Product Name: {product_name}
        Quantity: {quantity}
        Company Name: {company_name}
        Email: {email}
        Phone: {phone}
        Inquiry Details: {inquiry_details}
        Notify Prices: {'Yes' if notify_prices else 'No'}
        """
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)

        return jsonify({"success": True, "message": "✅ Inquiry submitted successfully!"})
    except Exception as e:
        print("❌ Error in /send-submit:", e)
        return jsonify({"success": False, "message": "❌ Something went wrong. Please try again."}), 500


# ======================================================
# ✅ HDD PRODUCT ENDPOINTS
# ======================================================
@app.route('/')
def home_redirect():
    return render_template('products1.html')
@app.route('/products1')
@app.route('/products1.html')
def products1_page():
    """
    Serves the Hard Drive Shortlist page (products1.html).
    """
    try:
        return render_template('products1.html')
    except Exception as e:
        print(f"❌ Error rendering products1.html: {e}")
        return "<h3 style='color:red;text-align:center;'>Unable to load Hard Drive Shortlist page.</h3>", 500
@app.route('/api/products/hdd', methods=['GET'])
def get_hdd_products():
    return jsonify({
        "success": True,
        "count": len(HDD_PRODUCTS),
        "products": HDD_PRODUCTS
    })

# ======================================================
# ✅ SEARCH ROUTE
# ======================================================
@app.route("/search")
def search_redirect():
    query = request.args.get("q", "").lower().strip()
    keyword_map = {
        "intel": "intel",
        "intel i9": "intel",
        "amd": "amd",
        "ryzen": "amd",
        "xeon": "intel",
        "threadripper": "amd",
        "epyc": "amd"
    }
    for key, slug in keyword_map.items():
        if key in query:
            return render_template(f"productslist/{slug}.html")
    return render_template("index.html", message="Product not found")

# ======================================================
# ✅ FRONTEND FALLBACK ROUTE
# ======================================================
@app.route("/<path:path>")
def serve_frontend(path):
    """
    Serve static and HTML files from the frontend directory.
    """
    static_path = os.path.join(STATIC_DIR, path)
    if path and os.path.exists(static_path):
        return send_from_directory(STATIC_DIR, path)

    html_path = os.path.join(TEMPLATES_DIR, path)
    if path and os.path.exists(html_path):
        return send_from_directory(TEMPLATES_DIR, path)

    # Default fallback to index.html
    return render_template("index.html")

# ======================================================
# ✅ RUN SERVER
# ======================================================
if __name__ == '__main__':
    print("🚀 Starting Flask Server on port 5000")
    print("Frontend + API available at http://127.0.0.1:5000/")
    app.run(port=5000, debug=True)
