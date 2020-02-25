import task3
from flask import Flask, redirect, request, url_for,render_template

app = Flask(__name__)


def before_request():
    """
    Clears the cache so that it would be possible to use site multiple times.
    """
    app.jinja_env.cache = {}


app.before_request(before_request)


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Receive the user input and redirect to the /maps version of it.
    """
    if request.method == "GET":
        return render_template("main_page.html")

    if request.method == "POST":
        task3.main(request.form['contents'])
        return redirect(url_for('maps'))


@app.route("/map")
def maps():
    """
    Read the map and open it it the tab.
    """
    return render_template("map.html")