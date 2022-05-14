import os
from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

from bs4 import BeautifulSoup
import requests

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    image = db.column(db.Text)

    def __repr__(self):
        return f"<Product {self.title}>"

source = requests.get("https://handmade-egypt.com/product-category/chairs/").text

soup = BeautifulSoup(source, "lxml")

products = soup.find_all("div", class_="product")

for product in products:
    title = product.h3.text
    
    try:
        price = float(product.find("span", class_="price").bdi.text[3:].replace(',', ''))
    except:
        price = 0
    
    image = product.find("a", class_="product-image-link").img["src"]

    product_entry = Product(
        title=title,
        price=price,
        image=image,
        category="Chairs"
    )
    
    db.session.add(product_entry)

db.session.commit()

@app.route("/")
def index():
    return 'None'
