import os
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import datetime, timezone
from werkzeug.utils import secure_filename
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

# Initialize Flask extensions globally
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'login'

# Constants
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "default-secret-key"),
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL", "sqlite:///inventory.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        UPLOAD_FOLDER=UPLOAD_FOLDER
    )

    # Ensure upload folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Context processor for global variables
    @app.context_processor
    def inject_business_name():
        return {'business_name': "DOMAGLAM BEAUTY AFFAIRS"}

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Define custom escapejs filter
    @app.template_filter('escapejs')
    def escapejs_filter(s):
        if s is None:
            return ''
        # Convert to string if it's not already
        s = str(s)
        # Basic JS escaping: escape backslashes, quotes, and newlines.
        return s.replace('\\', '\\\\').replace("'", "\\'").replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r')

    # Routes
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                return redirect(url_for('dashboard'))
            
            return render_template("login.html", error="Invalid credentials")
        return render_template("login.html")

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @app.route('/')
    @login_required
    def dashboard():
        total_products = Inventory.query.count()
        total_sales = db.session.query(db.func.sum(Sale.quantity)).scalar() or 0
        return render_template("dashboard.html",
                               user=current_user.username,
                               total_products=total_products,
                               total_sales=total_sales)

    @app.route('/inventory')
    @login_required
    def inventory():
        items = Inventory.query.all()
        return render_template("inventory.html", inventory=items)

    @app.route('/add-product', methods=['GET', 'POST'])
    @login_required
    def add_product():
        categories = {
            "cream": ["body cream", "face cream", "children's cream", "other"],
            "soap": ["laundry soap", "bathing soap", "liquid soap", "powder soap/detergent", "other"],
            "fragrances": ["Perfume", "deodorant (body spray, roll-on)", "others"],
            "jewelry": ["earrings", "necklace", "bracelet", "others"],
            "hair/accessories": [
                "Shampoo", "Conditioner", "Hair oil", "Hair gel", "Hair mousse", "Hair spray", "Hair serum",
                "Hair dye", "Hair masks", "Hair extensions", "Hair clippers", "Wigs", "Hairbands",
                "Scrunchies", "Hair clips", "Barrettes", "Headbands", "Hairpins", "Bows", "Combs",
                "Brushes", "Hair ties", "Hair claws", "Tiara", "Hair sticks", "other"
            ],
            "other": ["Custom"]  # Added "Other" as a main category
        }

        if request.method == 'POST':
            product_name = request.form.get('name')
            category = request.form.get('category')
            if category == "other":
                category = request.form.get('custom_category')  # Get the custom category input
            subcategory = request.form.get('subcategory')
            price = request.form.get('unit_price')
            total_stock = request.form.get('total_stock')
            product_code = request.form.get('product_code', '').strip()

            # Check if the product already exists
            existing_product = Inventory.query.filter_by(item_name=product_name).first()
            if existing_product:
                flash("Product already exists! Consider restocking.", "warning")
                return redirect(url_for('add_product'))

            # Handle custom subcategory if "other" is selected
            if subcategory == "other":
                subcategory = request.form.get('custom_subcategory')

            # Generate a unique product code if not provided
            if not product_code:
                product_code = generate_unique_product_code()

            # Ensure the generated product code is unique
            while Inventory.query.filter_by(product_code=product_code).first():
                product_code = generate_unique_product_code()

            # Save product to database
            new_product = Inventory(
                item_name=product_name,
                category=category,
                subcategory=subcategory,
                unit_price=float(price),
                total_stock=int(total_stock),
                product_code=product_code
            )
            db.session.add(new_product)
            db.session.commit()

            flash("Product added successfully!", "success")  # Show success message
            return redirect(url_for('add_product'))  # Redirect to the same page

        return render_template("add_product.html", categories=categories)

    def generate_unique_product_code():
        """Generate a unique 8-character product code."""
        while True:
            code = str(uuid.uuid4())[:8].upper()
            if not Inventory.query.filter_by(product_code=code).first():
                return code

    @app.route('/api/inventory', methods=['GET', 'POST'])
    @login_required
    def manage_inventory():
        if request.method == 'GET':
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)

            pagination = Inventory.query.paginate(page=page, per_page=per_page, error_out=False)

            data = [{
                "id": item.id,
                "item_name": item.item_name,
                "total_stock": item.total_stock,
                "unit_price": item.unit_price,
                "image_path": item.image_path,
                "category": item.category,
                "subcategory": item.subcategory
            } for item in pagination.items]

            return jsonify({
                "products": data,
                "page": pagination.page,
                "total_pages": pagination.pages
            }), 200

        elif request.method == 'POST':
            data = request.get_json()
            if not data or "name" not in data:
                return jsonify({"error": "Invalid input"}), 400
            new_item = Inventory(
                item_name=data.get('name'),
                total_stock=data.get('total_stock', 0),
                unit_price=data.get('price_per_unit')
            )
            db.session.add(new_item)
            db.session.commit()
            return jsonify({"message": "Item added successfully"}), 201

    @app.route('/api/inventory/<int:product_id>', methods=['DELETE'])
    @login_required
    def delete_product(product_id):
        product = db.session.get(Inventory, product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"}), 200

    @app.route('/api/sales', methods=['POST'])
    @login_required
    def process_sale():
        data = request.get_json()
        product_id = data.get("product_id")
        quantity = data.get("quantity")
        payment_method = data.get("payment_method")

        if not product_id or not quantity or not payment_method:
            return jsonify({"error": "Missing sale data"}), 400

        product = db.session.get(Inventory, product_id)
        if not product or product.total_stock < int(quantity):
            return jsonify({"error": "Insufficient stock"}), 400

        try:
            product.total_stock -= int(quantity)
            sale = Sale(product_id=product.id, quantity=int(quantity), payment_method=payment_method)
            
            db.session.add(sale)
            db.session.commit()
            
            return jsonify({"message": "Sale recorded successfully"}), 200
        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "Database error occurred"}), 500

    @app.route('/sales', methods=['GET', 'POST'])
    @login_required
    def sales_page():
        if request.method == 'POST':
            # Process sale form submission (placeholder)
            sale_data = request.form.to_dict()
            print("Sale Data:", sale_data)
            return redirect(url_for('dashboard'))
        # For GET requests, pass the current time to the template
        current_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        return render_template("sales.html", current_time=current_time)

    @app.route("/get-subcategories")
    @login_required
    def get_subcategories():
        category = request.args.get("category", "").strip()

        categories = {
            "cream": ["body cream", "face cream", "children's cream", "other"],
            "soap": ["laundry soap", "bathing soap", "liquid soap", "powder soap/detergent", "other"],
            "fragrances": ["Perfume", "deodorant (body spray, roll-on)", "others"],
            "jewelry": ["earrings", "necklace", "bracelet", "others"],
            "hair/accessories": [
                "Shampoo", "Conditioner", "Hair oil", "Hair gel", "Hair mousse", "Hair spray", "Hair serum",
                "Hair dye", "Hair masks", "Hair extensions", "Hair clippers", "Wigs", "Hairbands",
                "Scrunchies", "Hair clips", "Barrettes", "Headbands", "Hairpins", "Bows", "Combs",
                "Brushes", "Hair ties", "Hair claws", "Tiara", "Hair sticks", "other"
            ]
        }

        return jsonify(categories.get(category, []))  # Return subcategories as JSON

    @app.route('/get-product-by-code')
    @login_required
    def get_product_by_code():
        code = request.args.get("code", "").strip()
        product = Inventory.query.filter_by(product_code=code).first()

        if product:
            return jsonify({
                "success": True,
                "name": product.item_name,
                "price": product.unit_price,
                "stock": product.total_stock
            })
        
        return jsonify({"success": False, "message": "Product not found."})

    return app

# Database Models
class Inventory(db.Model):
    __tablename__ = 'inventory'
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    total_stock = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    image_path = db.Column(db.String(255), nullable=True)
    category = db.Column(db.String(100), nullable=False)
    subcategory = db.Column(db.String(100), nullable=True)
    product_code = db.Column(db.String(50), unique=True, nullable=True)  # Ensure this field exists

    def __repr__(self):
        return f"<Inventory {self.item_name} - {self.product_code}>"

class Sale(db.Model):
    __tablename__ = 'sale'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('inventory.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(password)

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
