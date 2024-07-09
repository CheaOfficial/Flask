from flask import Flask, request, redirect, url_for, render_template, flash, send_from_directory
# from models.person import Person
from datetime import date
import requests
import os
import sqlite3
import base64

from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = '123'


UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

product_list = [
    {
        'id': '1',
        'title': 'Day Break',
        'price': '20',
        'description': 'Stuff Description Lorem Ipsum',
        'image': 'product1.jpg',
    },
    {
        'id': '2',
        'title': "Night's Edge",
        'price': '20',
        'description': 'Stuff Description Lorem Ipsum',
        'image': 'product2.jpg',
    },
]

conn = sqlite3.connect('database.db', check_same_thread=False)


product_list = []
current_product = []
bot_token = "7304185845:AAGsw4p9dpfm9MFmfPmvohRUCnonaGcdwt8"
chat_id = "-1002190506945"
bot_username = "chey_product_bot"


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/blog')
def blog():
    return render_template('blog.html')


@app.route('/shop')
def shop():
    return render_template('shop.html')


@app.route('/help')
def help():
    return render_template('help.html')


# FROM THIS LINE TO BELOW WILL BE JUST TESTS/LESSONS
@app.route('/jinja')
def jinja():
    list = [
        {'name': 'Alice', 'age': 20, 'grade': 'A'},
        {'name': 'Bob', 'age': 22, 'grade': 'B'},
        {'name': 'Charlie', 'age': 23, 'grade': 'C'},
        {'name': 'David', 'age': 21, 'grade': 'B'},
        {'name': 'Eve', 'age': 22, 'grade': 'A'}
    ]
    time = 10
    # person = Person("Bro", 30)
    # user = request.args.get('username')
    user = "randomname"
    return render_template('jinja.html', time=time, list=list, user=user) #, person=person


@app.route('/submit', methods=['POST'])
def submit():
    username = request.form['username']  # Get the value of 'username' from the form data
    return render_template('index.html', user=username)


@app.route('/jinjalist')
def jinjastudentlist():
    list = [
        {'name': 'Alice', 'age': 20, 'grade': 'A'},
        {'name': 'Bob', 'age': 22, 'grade': 'B'},
        {'name': 'Charlie', 'age': 23, 'grade': 'C'},
        {'name': 'David', 'age': 21, 'grade': 'B'},
        {'name': 'Eve', 'age': 22, 'grade': 'A'}
    ]
    return render_template('jinjalist.html', list=list)


# product classwork
@app.route('/product')
def product():
    url = "https://fakestoreapi.com/products"
    response = requests.get(url)
    product = response.json()
    product_list = product
    return render_template('product.html', product_list=product_list)


@app.route('/product_detail')
def product_detail():
    product_id = request.args.get('id')
    url = "https://fakestoreapi.com/products/{}".format(product_id)
    response = requests.get(url)
    current_product = []
    current_product = response.json()
    return render_template('product_detail.html', current_product=current_product)


@app.route('/checkout')
def checkout():
    product_id = request.args.get('id')
    url = "https://fakestoreapi.com/products/{}".format(product_id)
    response = requests.get(url)
    current_product = []
    current_product = response.json()
    return render_template('checkout.html', current_product=current_product)


@app.route('/submit_order', methods=['GET'])
def submit_order():
    # Retrieve product ID from query parameter
    product_id = request.args.get('id')

    # Fetch product details from external API
    url = "https://fakestoreapi.com/products/{}".format(product_id)
    try:
        response = requests.get(url)
        current_product = response.json()

        # Retrieve customer information from query parameters
        fullname = request.args.get('fullname')
        phone = request.args.get('phone')
        email = request.args.get('email')

        # Construct HTML for the order summary
        html = (
            "<strong>🧾 {inv_no}</strong>\n"
            "<code>📆 {date}</code>\n"
            "<code>============================</code>\n"
            "<code>ID\t\tQuality\t\tPrice\t\tAmount</code>\n"
        ).format(
            inv_no='INV0001',  # Example invoice number
            date=date.today(),  # Current date
        )

        html += (
            f"<code>{current_product['id']}\t\t\t\t\t\t1\t\t\t\t\t{current_product['price']}\t\t\t\t{current_product['price']}</code>\n"
        )

        html += (
            "<code>-----------------------------</code>\n"
            "<code>Total: {total}$</code>\n"
            "<code>Grand Total: {grand_total}$</code>\n"
            # "<code>Discount: {discount}%</code>\n"
            # "<code>ប្រាក់ទទួល: {received_amount}$</code>\n"
            # "<code>💸ប្រាក់អាប់: {deposit_amount}$</code>\n"
        ).format(
            total=f'{current_product["price"]}',  # Example total
            grand_total=f'{current_product["price"]}',  # Example grand total
            # discount=f'{discount}',  # Example discount
            # received_amount=f'{received_amount}',  # Example received amount
            # deposit_amount=f'{deposit_amount}'  # Example deposit amount
        )

        html += (
            "<strong>🧾 Customer Information</strong>\n"
            f"<code> Customer Name   : {fullname}</code>\n"
            f"<code> Email           : {email}</code>\n"
            f"<code> Phone           : {phone}</code>\n"
            "<code>============================</code>\n"
        )

        # Get image URL for the product
        image_url = current_product['image']

        # Send the HTML as caption to Telegram
        response = requests.get(
            f"https://api.telegram.org/bot{bot_token}/sendPhoto",
            params={
                'chat_id': chat_id,
                'photo': image_url,
                'caption': html,
                'parse_mode': 'HTML'
            }
        )

        # Print the API response for debugging
        print(response.json())

        # Check if the request was successful
        if response.status_code != 200:
            return "Failed to send message to Telegram!", response.status_code

        # Render a template with the current product details
        return render_template("submit_order.html", current_product=current_product)

    except requests.exceptions.RequestException as e:
        return f"Error fetching product details: {e}"
    except ValueError as e:
        return f"Error decoding JSON: {e}"


@app.get('/add_product')
def add_product():
    row = conn.execute("""select * from tbl_product""")
    product = []
    for item in row:
        product.append(
            {
                'id': item[0],
                'title': item[1],
                'cost': item[2],
                'price': item[3],
                'category': item[4],
                'description': item[5],
                'image': item[6]
            }
        )
    # print(product)
    return render_template('add_product.html', product=product)
    # return product


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.post('/submit_add_product')
def submit_add_product():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    title = request.form.get('title')
    price = request.form.get('price')
    category = request.form.get('category')
    description = request.form.get('description')

    row = conn.execute("""
        INSERT INTO 
        tbl_product (ptitle, pprice, pcategory, pdescription, pimage)
        VALUES (?, ?, ?, ?, ?)
    """, (title, price, category, description, filename))
    product = []

    # file = request.files['file']
    # file.save(os.path.join(app.config['UPLOAD_FOLDER'] + '/products',file.filename))

    conn.commit()
    return redirect(url_for('add_product'))
    # return  f'Testing Submit Product'


@app.post('/edit_product')
def edit_product():
    edit_picture = request.files.get('edit_picture')
    image_url = None

    if edit_picture and edit_picture.filename != '' and allowed_file(edit_picture.filename):
        filename = secure_filename(edit_picture.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        edit_picture.save(filepath)
        image_url = filename  # Store the relative filename

    pid = request.form.get('edit_product_id')
    title = request.form.get('edit_title')
    price = request.form.get('edit_price')
    category = request.form.get('edit_category')
    description = request.form.get('edit_description')

    cur = conn.cursor()

    if image_url:
        cur.execute("""
            UPDATE tbl_product 
            SET ptitle = ?, pprice = ?, pcategory = ?, pdescription = ?, pimage = ?
            WHERE pid = ?
        """, (title, price, category, description, image_url, pid))
    else:
        cur.execute("""
            UPDATE tbl_product 
            SET ptitle = ?, pprice = ?, pcategory = ?, pdescription = ?
            WHERE pid = ?
        """, (title, price, category, description, pid))

    conn.commit()

    return redirect(url_for('add_product'))


@app.post('/delete_product')
def delete_product():
    pid = request.form.get('delete_product_id')

    # Ensure pid is passed as a tuple
    conn.execute("""
        DELETE FROM tbl_product 
        WHERE pid = ?
    """, (pid,))

    conn.commit()  # Ensure the changes are committed to the database
    return redirect(url_for('add_product'))


@app.route('/crop_image', methods=['GET', 'POST'])
def crop_image():
    if request.method == 'POST':
        cropped_image_data = request.form['cropped_image']
        original_filename = request.form['original_filename']

        try:
            # Decode the base64 image data
            header, data = cropped_image_data.split(',', 1)
            image_data = base64.b64decode(data)

            # Save the image to a file
            with open(f'static/uploads/{original_filename}', 'wb') as f:
                f.write(image_data)

            return redirect(url_for('add_product'))
        except Exception as e:
            return f"An error occurred: {str(e)}"

    image_data = request.args.get('image')
    return render_template('cropper/crop_image.html', image_data=image_data)


# TEST TEST TEST
@app.route('/input')
def input():
    return render_template('tests/input.html')

@app.route('/debug', methods=['POST', 'GET'])
def process():
    if request.method == 'POST':
        username = request.form['username']
        # Perform any processing with the input data if needed
        return render_template('tests/output.html', username=username)
    elif request.method == 'GET':
        username = request.args.get('username')



# RUN APP
if __name__ == '__main__':
    app.run(debug=True)
