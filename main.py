from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request, render_template
from flask import redirect, url_for

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////home/sardor/deepen.soft/task1/flask/product.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7Cffdffggfg0sKR6b'

db = SQLAlchemy(app)


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return f"Category(id={self.id}, title={self.title})"


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtext = db.Column(db.String(200))
    price = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('products', lazy=True))

    def __init__(self, title, subtext, price, category_id):
        self.title = title
        self.subtext = subtext
        self.price = price
        self.category_id = category_id

    def __repr__(self):
        return f"Product(id={self.id}, title={self.title}, subtext={self.subtext}, price={self.price}, category_id={self.category_id})"


@app.route("/")
def index():
    # product = Product(title='banana', price=3, subtext="banabanana", category_id=1)
    # db.session.add(product)
    # new_product = Product(title='New banana', price=8, subtext="new banana", category_id=2)
    # db.session.add(new_product)
    # db.session.commit()
    products = Product.query.all()
    categories = Category.query.all()
    print(categories)
    for c in products:
        print(c.id)

    return render_template('index.html',
                           products=products,
                           categories=categories
                           )

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    categories = Category.query.all()

    if request.method == 'POST':
        title = request.form['title']
        subtext = request.form['subtext']
        price = request.form['price']
        category_id = request.form['category']

        category = Category.query.get(category_id)
        product = Product(title=title, subtext=subtext, price=price, category_id=category)

        db.session.add(product)
        db.session.commit()

        return redirect(url_for('display_products'))
    return render_template('add_product.html', categories=categories)


@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST', "PATCH"])
def edit_product(product_id):
    product = Product.query.get(product_id)
    categories = Category.query.all()

    if request.method == 'POST':
        product.title = request.form['title']
        product.subtext = request.form['subtext']
        product.price = request.form['price']

        category_id = request.form['category']
        category = Category.query.get(category_id)
        product.category = category

        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_product.html', product=product, categories=categories)


@app.route('/delete_product/<int:product_id>', methods=['GET', 'POST'])
def delete_product(product_id):
    product = Product.query.get(product_id)

    db.session.delete(product)
    db.session.commit()

    return redirect('/')


@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        title = request.form['title']

        category = Category(title=title)
        db.session.add(category)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('add_category.html')


@app.route('/edit_category/<int:category_id>', methods=['GET', 'POST', "PATCH"])
def edit_category(category_id):
    category = Category.query.get(category_id)
    if request.method == 'POST':
        category.title = request.form['title']
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit_category.html', category=category)


@app.route('/delete_category/<int:category_id>', methods=['GET', 'POST'])
def delete_category(category_id):
    category = Category.query.get(category_id)

    db.session.delete(category)
    db.session.commit()

    return redirect('/')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
