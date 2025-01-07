from flask import Blueprint, request, redirect, url_for, flash, render_template

from auth import guest_required
from form import RegisterForm
from services.user_service import UserService

register_page = Blueprint('register_page', __name__)

@register_page.route('/', methods=["GET", "POST"])
@guest_required
def page():
    form = RegisterForm()
    if request.method == "POST" and form.validate_on_submit():
        if form.password.data == form.password_again.data:
            input_data = form.data
            input_data.pop("password_again")
            input_data.pop("csrf_token")
            UserService.register(**input_data)
            flash("Successfully registered! Now please login!",category="success")
            return redirect(url_for("login_page.page"))
        flash("Passwords do not match",category="error")
    return render_template("register_page/page.jinja", form=form)