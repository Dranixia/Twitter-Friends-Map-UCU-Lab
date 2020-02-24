import task3
from flask import Flask, redirect, request, url_for,render_template

app = Flask(__name__)


def before_request():
    app.jinja_env.cache = {}


app.before_request(before_request)


@app.route("/", methods=["GET", "POST"])
def index():
    print('ind')
    if request.method == "GET":
        return render_template("main_page.html")

    if request.method == "POST":
        task3.main(request.form['contents'])
        return redirect(url_for('map'))


@app.route("/map", methods=["GET"])
def map():
    return render_template("map.html")