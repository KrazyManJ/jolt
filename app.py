from flask import Flask, render_template

from database import database

app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_object('config')
database.init_app(app)


@app.route("/")
def index():
    return render_template("index.jinja")
