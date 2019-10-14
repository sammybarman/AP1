from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import re, sqlite3, json
from flask_security import Security, login_required, \
     SQLAlchemySessionUserDatastore, roles_accepted
from flask_security.utils import hash_password
from database import db_session, init_db
from models import User, Role

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'secret string'
app.config['SECURITY_PASSWORD_SALT'] = 'some arbitrary super secret string'
app.config['SECURITY_TRACKABLE'] = True

# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db_session,
                                                User, Role)
security = Security(app, user_datastore)

conn_purchase = sqlite3.connect('user_purchase_data.db')
cur_purchase = conn_purchase.cursor()
cur_purchase.executescript('''
CREATE TABLE IF NOT EXISTS CART (
ID INTEGER NOT NULL PRIMARY KEY,
USER_ID INTEGER NOT NULL UNIQUE,
ITEMS TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS HISTORY (
ID INTEGER NOT NULL PRIMARY KEY,
USER_ID INTEGER NOT NULL,
ITEMS TEXT NOT NULL,
DATE TEXT NOT NULL
);
''')

conn_purchase.commit()

@app.route('/')
def index():
    return redirect(url_for('home_page'), code=301)

# TODO:  need to add some random phones on homepage
@app.route("/home")
def home_page():
    return render_template("index.html")

@app.route("/product")
def product_page():
    return render_template("product.html")

# @params : every filter's key value pair, search term
# @return : list of phone_name, phone_img, phone_price
# TODO: Match search term with phone name, colour etc in db and return matched, atleast 10 results
# every phone should appear only once. need to embed phone_data id somewhere
# what to do in case of no match?
@app.route("/search")
def search_for_phones():
    os = request.args.get('OS')
    price_max = request.args.get('price_max')
    price_min = request.args.get('price_min')
    search_term = request.args.get('search_term')

@app.route("/contact")
def contact():
    return render_template("contact.html")

@login_required
@app.route("/cart", methods=['GET', 'POST'])
def cart_func():
    if request.method == 'GET':
        cur_purchase.execute('SELECT ITEMS FROM CART WHERE USER_ID == ?', (session['user_id'],))
        items = json.loads(cur_purchase.fetchone()[0])
        return render_template('upload.html', data=items)
    else:
        items = request.get_json()
        cur_purchase.execute('DELETE FROM CART WHERE USER_ID == ?', (session['user_id'],))
        cur_purchase.execute('INSERT INTO CART (USER_ID, ITEMS) VALUES (?,?)', (session['user_id'], json.dumps(items, indent=2)))
        conn_purchase.commit()
        return jsonify({'status':'added to cart'})

# @params : phone_id
# @return : product details from db
@app.route("/getproduct")
def products():
    phone_id = request.args.get('phone_id')
    phone_data_id = requests.args.get('phone_data_id')
    res = dict()
    res['others'] = list()
    cur_product.execute('SELECT PHONE_DATA.ID, IMG, COLOUR FROM PHONE_DATA, PHONE, OS, COMPANY WHERE PHONE.ID == ? AND PHONE_ID == PHONE.ID AND OS_ID == OS.ID AND COMPANY_ID = COMPANY.ID AND PHONE_DATA.ID != ? ORDER BY PHONE_DATA.ID', (phone_id, phone_data_id))
    for row in cur_product.fetchall():
        element = dict()
        element['phone_data_id'] = row[0]
        element['img_link'] = row[1]
        element['colour'] = row[2]
        res['others'].append(element)
    cur_product.execute('SELECT PHONE_DATA.ID, PHONE.NAME, COMPANY.NAME, PRICE, IMG, COLOUR, OS.NAME, BATTERY, RAM, STORAGE, FEATURES FROM PHONE_DATA, PHONE, OS, COMPANY WHERE PHONE.ID == ? AND PHONE_ID == PHONE.ID AND OS_ID == OS.ID AND COMPANY_ID = COMPANY.ID AND PHONE_DATA.ID == ? ORDER BY PHONE_DATA.ID', (phone_id, phone_data_id))
    res['current']['phone_data_id'] = row[0]
    res['current']['phone_name'] = row[1]
    res['current']['company'] = row[2]
    res['current']['price'] = row[3]
    res['current']['img_link'] = row[4]
    res['current']['colour'] = row[5]
    res['current']['os'] = row[6]
    res['current']['battery'] = row[7]
    res['current']['ram'] = row[8]
    res['current']['storage'] = row[9]
    res['current']['features'] = json.loads(row[10])
    return jsonify(res)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
