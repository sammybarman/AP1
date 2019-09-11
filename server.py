from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
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
