from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import re, sqlite3, json, datetime
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

conn_phones = sqlite3.connect('phones.db', check_same_thread=False)
cur_phones = conn_phones.cursor()
conn_purchase = sqlite3.connect('user_purchase_data.db', check_same_thread=False)
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

@app.before_request
def all_requests():
    referrer = request.headers.get("Referer")
    if referrer != None and 'login' in referrer and request.method == 'POST':
        session['login_context_processor'] = {'error': 'The password or email you entered was incorrect'}
    if request.method == 'GET':
        session['login_context_processor'] = {}

@app.before_first_request
def first_request():
    init_db()
    if User.query.filter_by(email='nikhil.narasimhan99@gmail.com').first() == None:
        new_user = user_datastore.create_user(email='nikhil.narasimhan99@gmail.com', password=hash_password('abcd1234'), name='Pravin Kate')
        role = basic_role = user_datastore.find_or_create_role(name='basic', description='Role for buyers')
        user_datastore.add_role_to_user(new_user, role)
        db_session.commit()

@app.route('/createuser', methods=['POST'])
def create_user():
    js = request.get_json()
    if User.query.filter_by(email=js['email']).first() != None:
        return jsonify({'status':'User already created'}), 400
    new_user = user_datastore.create_user(email=js['email'], password=hash_password(js['password']), name=js['name'])
    db_session.commit()
    return jsonify({'created_user': js['email']})

@security.login_context_processor
def login_context_processor():
    return session['login_context_processor']

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

@app.route("/cart")
@login_required
def cartpage():
    return render_template("cart.html")

@app.route("/account")
def account():
    return render_template("account.html")

@app.route("/getphones")
def get_phones():
    cur_phones.execute('SELECT PHONE_DATA.ID,PHONE.NAME, PRICE, IMG, RAM, STORAGE, PHONE_ID FROM PHONE_DATA, PHONE WHERE PHONE.ID == PHONE_ID ')
    res = dict()
    res['phones'] = list()
    for row in cur_phones.fetchall():
        element = dict()
        element['phone_data_id'] = row[0]
        element['name'] = row[1]
        element['price'] = row[2]
        element['img_link'] = row[3]
        element['ram'] = row[4]
        element['storage'] = row[5]
        element['phone_id'] = row[6]
        res['phones'].append(element)
    return jsonify(res)

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
@app.route("/cart_ops", methods=['GET', 'POST', 'DELETE'])
@login_required
def cart_func():
    if request.method == 'GET':
        cur_purchase.execute('SELECT ITEMS FROM CART WHERE USER_ID == ?', (session['user_id'],))
        items = list()
        try:
            products = json.loads(cur_purchase.fetchone()[0])
            for product in products:
                cur_phones.execute('SELECT PHONE_DATA.ID, PHONE.NAME, IMG, PRICE FROM PHONE_DATA, PHONE WHERE PHONE_ID == PHONE.ID')
                row = cur.fetchall()
                items.append({'phone_data_id': row[0], 'name': row[1], 'img_link': row[2], 'price': row[3]})
        except:
            items = list()
        return jsonify({'phones': items})
    elif request.method == 'POST':
        products = request.get_json()
        cur_purchase.execute('SELECT ITEMS FROM CART WHERE USER_ID == ?', (session['user_id'],))
        stored_products = []
        try:
            stored_products = json.loads(cur_purchase.fetchone()[0])
        except:
            stored_products = []
        stored_products = [] if stored_products == None else stored_products
        stored_products.append(int(products['product_id']))
        stored_products = list(set(stored_products))
        cur_purchase.execute('DELETE FROM CART WHERE USER_ID == ?', (session['user_id'],))
        cur_purchase.execute('INSERT INTO CART (USER_ID, ITEMS) VALUES (?,?)', (session['user_id'], json.dumps(stored_products, indent=2)))
        conn_purchase.commit()
        return jsonify({'status':'added to cart'})
    else:
        products = request.get_json()

# @params : phone_id
# @return : product details from db
@app.route("/getproduct")
def products():
    phone_id = request.args.get('phone_id')
    phone_data_id = request.args.get('phone_data_id')
    res = dict()
    res['other_variants'] = list()
    cur_phones.execute('SELECT PHONE_DATA.ID, PHONE.NAME, COMPANY.NAME, PRICE, IMG, COLOUR, OS.NAME, BATTERY, RAM, STORAGE, FEATURES FROM PHONE_DATA, PHONE, OS, COMPANY WHERE PHONE.ID == ? AND PHONE_ID == PHONE.ID AND OS_ID == OS.ID AND COMPANY_ID = COMPANY.ID AND PHONE_DATA.ID == ? ORDER BY PHONE_DATA.ID', (phone_id, phone_data_id))
    row = cur_phones.fetchone()
    res['phone_data_id'] = row[0]
    res['phone_name'] = row[1]
    res['company'] = row[2]
    res['price'] = row[3]
    res['img_link'] = row[4]
    res['colour'] = row[5]
    res['os'] = row[6]
    res['battery'] = row[7]
    res['ram'] = row[8]
    res['storage'] = row[9]
    res['features'] = json.loads(row[10])
    cur_phones.execute('SELECT PHONE_DATA.ID, COLOUR, RAM, STORAGE, PHONE_ID FROM PHONE_DATA, PHONE, OS, COMPANY WHERE PHONE.ID == ? AND PHONE_ID == PHONE.ID AND OS_ID == OS.ID AND COMPANY_ID = COMPANY.ID AND PHONE_DATA.ID != ? ORDER BY PHONE_DATA.ID', (phone_id, phone_data_id))
    for row in cur_phones.fetchall():
        res['other_variants'].append('<a href="/getproduct?phone_id={}&phone_data_id={}">{}</a>'.format(row[4], row[0], str(row[2])+' + '+str(row[3])+' + '+row[1]))
    return render_template('product.html', data=res)

@app.route("/checkout", methods=['POST'])
@login_required
def pay_for_cart():
    cur_purchase.execute('SELECT ITEMS FROM CART WHERE USER_ID == ?', (session['user_id'],))
    items = json.loads(cur_purchase.fetchone()[0])
    cur_purchase.execute('INSERT INTO HISTORY (USER_ID, ITEMS, DATE) VALUES (?,?,?)', (session['user_id'], json.dumps(items, indent=2), datetime.datetime.now().strftime('%d %b, %Y %H:%M:%S')))
    cur_purchase.execute('DELETE FROM CART WHERE USER_ID == ?', (session['user_id'],))
    cur_purchase.commit()
    return jsonify({'status': 'checkout complete'})

@app.route("/loggedin", methods=['GET'])
@login_required
def check_login():
    return jsonify({'status':1})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
