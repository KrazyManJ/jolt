from flask import Blueprint, request, flash, redirect, session, url_for, render_template

from auth import guest_required
from form import LoginForm
from services.user_service import UserService

login_page = Blueprint('login_page', __name__)

@login_page.route('/', methods=["GET", "POST"])
@guest_required
def page():
    form = LoginForm()
    if request.method == "POST":

        user = UserService.verify(form.login.data,form.password.data)
        if not user:
            flash("Invalid username or password",category="error")
        else:
            session['authenticated'] = 1
            session['id'] = user['user_id']
            session['login_name'] = user['login_name']
            session['first_name'] = user['first_name']
            session['last_name'] = user['last_name']
            session['role'] = user['role_name']
            return redirect(url_for("index.page"))

    return render_template("login_page/page.jinja", form=form)