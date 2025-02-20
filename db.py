from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
import random
import hashlib

# app = Flask(__name__)
"""""
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\liyun\\Downloads\\fivebluepetal-main\\capstone-project-3900-h11b-five-blue-petals\\BFP.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + '/Users/jiataoli/Desktop/3900/first.db'
"""""
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BFP.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    U_id = db.Column(db.Integer, nullable=False)
    token = db.Column(db.String(200), nullable=False)
    nickname = db.Column(db.String(50))
    is_online = db.Column(db.Boolean)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100))
    mobile = db.Column(db.String(20))

    def __init__(self, id_number, token, nickname, online, em, passw, addre, mobile):
        self.U_id = id_number
        self.token = token
        self.nickname = nickname
        self.is_online = online
        self.email = em
        self.password = passw
        self.address = addre
        self.mobile = mobile


class Search_history(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    U_id = db.Column(db.Integer, nullable=False)
    history = db.Column(db.String(50), nullable=False)

    def __init__(self, U_id, history):
        self.U_id = U_id
        self.history = history


class Shopping_cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    U_id = db.Column(db.Integer, nullable=False)
    P_id = db.Column(db.Integer, nullable=False)

    def __init__(self, U_id, P_id):
        self.U_id = U_id
        self.P_id = P_id


class Click_history(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    U_id = db.Column(db.Integer, nullable=False)
    P_id = db.Column(db.Integer, nullable=False)

    def __init__(self, U_id, P_id):
        self.U_id = U_id
        self.P_id = P_id


class Purchase_history(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    U_id = db.Column(db.Integer, nullable=False)
    O_id = db.Column(db.Integer, nullable=False)

    def __init__(self, pic_link, pro_id):
        self.U_id = U_id
        self.O_id = O_id


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pro_id = db.Column(db.Integer)
    name = db.Column(db.String(50))
    if_shown = db.Column(db.Boolean)
    price = db.Column(db.Float)
    stock = db.Column(db.Integer)
    sold = db.Column(db.Integer)
    discount = db.Column(db.Float)
    tags = db.Column(db.String(100))
    description = db.Column(db.String(1000))

    def __init__(self, pro_id, name, if_shown, price, stock, sold, discount, tags, description):
        self.pro_id = pro_id
        self.name = name
        self.if_shown = if_shown
        self.price = price
        self.stock = stock
        self.sold = sold
        self.discount = discount
        self.tags = tags
        self.description = description


class Product_picture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pic_link = db.Column(db.String(50))
    pro_id = db.Column(db.Integer)

    def __init__(self, pic_link, pro_id):
        self.pic_link = pic_link
        self.pro_id = pro_id


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    U_id = db.Column(db.Integer)
    status = db.Column(db.Integer)
    time = db.Column(db.String(10))
    address = db.Column(db.String(100))
    comment = db.Column(db.String(200))
    track_number = db.Column(db.String(100))

    def __init__(self, U_id, status, time, address, comment, track_number):
        self.U_id = U_id
        self.status = status
        self.time = time
        self.address = address
        self.comment = comment
        self.track_number = track_number


class Order_products(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    o_id = db.Column(db.Integer)
    p_id = db.Column(db.Integer)

    def __init__(self, o_id, p_id):
        self.o_id = o_id
        self.p_id = p_id
        print(o_id, p_id)


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password


db.create_all()


def load_data():
    print("^^^^^^^^^^^^&&&&&&&&&&&&&&*($%*)#*$%")
    with open('static/data.json') as json_file:
        data = json.load(json_file)
        for pro in data['products']:
            tags = ",".join(pro["usage"])
            create_product(pro["id"], pro["title"], True, pro["price"], round(random.uniform(2, 4) * random.uniform(1, 2) * 100), round(random.uniform(2, 4) * random.uniform(1, 2) * 100), 0, tags, pro["description"])
            for image in pro["image"]:
                create_product_picture(image, int(pro["id"]))
    create_user(0, "13421234123412341234", "frank", False, "Phranqueli@gmail.com", hashlib.sha256("123456".encode()).hexdigest(), "Street Address111%%%Suburb111%%%Zip111%%%State111", "1339121234")
    create_user(1, "1342123412341234123412341234", "david", False, "Phranqueli123@gmail.com", hashlib.sha256("123456".encode()).hexdigest(), "Street Address222%%%Suburb222%%%Zip222%%%State222", "0455555666")
    create_user(2, "13421234123412341234123412341234", "tony", False, "Phranqueli14123@gmail.com", hashlib.sha256("123456".encode()).hexdigest(), "Street Address333%%%Suburb333%%%Zip333%%%State333", "0468987654")


def add_item(item):
    db.session.add(item)
    db.session.commit()


# addre can be NULL at the beginning
def create_user(id_number, token, nickname, online, em, passw, addre, mobile):
    new_user = User(id_number, token, nickname, online, em, passw, addre, mobile)
    add_item(new_user)


# can be NULL at the beginning
def create_order(id_number, status, time, address, comment, track_number):
    new_order = Order(id_number, status, time, address, comment, track_number)
    add_item(new_order)


def create_product(id_number, name, if_shown, price, stock, sold, discount, tags, desciprtion):
    new_product = Product(id_number, name, if_shown, price, stock, sold, discount, tags, desciprtion)
    add_item(new_product)


def create_product_picture(pic_link, pro_id):
    new_pic_pro = Product_picture(pic_link, pro_id)
    add_item(new_pic_pro)


def create_op(o_id, p_id):
    new_op = Order_products(o_id, p_id)
    add_item(new_op)


def creatte_admin(em, passs):
    new_adm = Admin(em, passs)
    add_item(new_adm)


def find_pics(pr_id):
    l_of_link = []
    pics = Product_picture.query.filter_by(pro_id=pr_id).all()
    for p in pics:
        l_of_link.append(p.pic_link)
    return l_of_link


def find_usages(id):
    product = Product.query.filter_by(pro_id=id).first()
    return product.tags.split(",")


def product_to_dict(product):
    pics = find_pics(product.pro_id)
    usages = find_usages(product.pro_id)
    return {
        "title": product.name,
        "price": product.price,
        "product_ID": product.pro_id,
        "image": pics,
        "stock":product.stock,
        "discount":product.discount,
        "usage": usages,
        "description": product.description
    }


def order_to_dict(order):
    user = User.query.filter_by(U_id=order.U_id).first()
    ops = Order_products.query.filter_by(o_id=order.id).all()
    products = []
    prods = []
    for op in ops:
        pro = Product.query.filter_by(pro_id=op.p_id).first()
        products.append(pro)
    for p in products:
        prods.append(product_to_dict(p))
    return {"order_ID": order.id,
            "customer": {'nickname': user.nickname, 'address': user.address, 'email': user.email,
                         'mobile': user.mobile},
            "product": prods,
            "status": order.status,
            "track_number": order.track_number}


def user_to_dict(user):
    orders = Order.query.filter_by(U_id = user.U_id).all()
    o_ids = []
    for order in orders:
        o_ids.append(order.id)
    o_ids.sort(reverse=True)
    return {"id":user.U_id, "address":user.address, "orders":o_ids, "name": user.nickname, 
    "email": user.email, "phone": user.mobile}


def getProductById(id):
    return Product.query.filter_by(pro_id=int(id)).first()
