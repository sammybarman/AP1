from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import urllib.parse, os, subprocess, re, requests, sqlite3, csv, io, threading
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

@app.route("/index")
def renderPage():
    return render_template("index.html")

# @app.route("/about")
# def about():
#     return render_template("about.html")
#
# @app.route("/products")
# def products():
#     return render_template("products.html")
#
# @app.route("/why")
# def why():
#     return render_template("why.html")
#
# @app.route("/contact")
# def contact():
#     return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
