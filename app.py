from flask import Flask, render_template, request, url_for, redirect, session, flash
from livereload import Server

from auth import login_required, roles_required
from database import database
from form import LoginForm, RegisterForm
from services.user_service import UserService

app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_object('config')
database.init_app(app)


@app.route("/")
def index():
    return render_template("index.jinja")

@app.route('/bikes-management')
@login_required
@roles_required("employee")
def bikes_management_page():
    return render_template("bikes_management.jinja")

@app.route('/user-profile')
@login_required
def user_profile_page():
    return render_template("user_profile.jinja")

@app.route('/login', methods=["GET", "POST"])
def login_page():
    if request.method == "POST":

        user = UserService.verify(
            request.form["login"],
            request.form["password"]
        )
        if not user:
            flash("Invalid username or password",category="error")
            return redirect(request.path)
        else:
            session['authenticated'] = 1
            session['id'] = user['user_id']
            session['login_name'] = user['login_name']
            session['first_name'] = user['first_name']
            session['last_name'] = user['last_name']
            session['role'] = user['role_name']


        return redirect(url_for("index"))

    return render_template("login_page.jinja",form=LoginForm())

@app.route('/register', methods=["GET", "POST"])
def register_page():
    if request.method == "POST":
        UserService.register(
            request.form["login"],
            request.form["firstname"],
            request.form["lastname"],
            request.form["email"],
            request.form["phone"],
            request.form["password"]
        )
        return redirect(url_for("login_page"))
    return render_template("register_page.jinja",form=RegisterForm())

@app.route('/logout')
@login_required
def logout():
    for val in [
        'authenticated',
        'id',
        'login_name',
        'first_name',
        'last_name',
        'role'
    ]:
        session.pop(val)
    return redirect(url_for('index'))



if __name__ == '__main__':
    server = Server(app.wsgi_app)
    server.serve(host='0.0.0.0',port=5001,debug=True)
    # app.run('0.0.0.0', port=5001, debug=True)