from flask import Flask, render_template
from livereload import Server

from database import database
from form import LoginForm

app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_object('config')
database.init_app(app)


@app.route("/")
def index():
    return render_template("index.jinja")

@app.route('/bikes-management')
def bikes_management_page():
    return render_template("bikes_management.jinja", page_title="Bikes management")

@app.route('/user-profile')
def user_profile_page():
    return render_template("user_profile.jinja", page_title="My profile")

@app.route('/login')
def login_page():
    return render_template("login_page.jinja",form=LoginForm())

if __name__ == '__main__':
    server = Server(app.wsgi_app)
    server.serve(host='0.0.0.0',port=5001,debug=True)
    # app.run('0.0.0.0', port=5001, debug=True)