from bs4 import BeautifulSoup
import os, requests, sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

c.execute("""
    CREATE TABLE products (
        id INTEGER PRIMARY_KEY,
        title TEXT,
        price REAL,
        category TEXT,
        img_path TEXT
    )
    """)

source = requests.get("https://handmade-egypt.com/store/").text

soup = BeautifulSoup(source, "lxml")

categories_list = soup.find("ul", id="menu-categories")

categories = categories_list.find_all("li")

categories_to_urls = {}

for category in categories:
    category_formatted = category.text.lower().replace(", ", "-").replace(" & ", "-")
    
    # Skip the 'clothes' category
    if category_formatted == "clothes":
        continue
    
    category_url = f"https://handmade-egypt.com/product-category/{category_formatted}/"
    categories_to_urls[category_formatted] = category_url

# Escape FileExistsError (In case or re-running the script, this exception may arise)
try:
    os.mkdir("static/images/")
except FileExistsError:
    pass

for category, category_url in categories_to_urls.items():
    category_source = requests.get(category_url).text
    category_soup = BeautifulSoup(category_source, "lxml")
    products = category_soup.find_all("div", class_="product")

    # Escape FileExistsError (In case or re-running the script, this exception may arise)
    try:
        os.mkdir(f"images/{category}")
    except FileExistsError:
        pass

    product_id = 1
    for product in products:
        title = product.h3.text
        
        # Image file details
        img_url = product.find("a", class_="product-image-link").img["src"]
        img_title = title.replace(" ", "-")
        img_path = f"images/{category}/{img_title}{img_url[-4:]}"
        img_bytes = requests.get(img_url).content
        
        # Save new image file
        with open(img_path, "wb") as handler:
            handler.write(img_bytes)

        try:
            price = float(product.find("span", class_="price").bdi.text[3:].replace(',', ''))
        except:
            price = 0

        c.execute("INSERT INTO products VALUES (:id, :title, :price, :category, :img_path)",
                {"id": product_id, "title": title, "price": price, "category": category, "img_path": img_path}
            )
        conn.commit()

        product_id += 1

products = conn.execute("SELECT * FROM products").fetchall()
for product in products:
    print(product)

conn.close()
