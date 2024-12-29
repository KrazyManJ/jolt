from flask import Blueprint, request, redirect, url_for, flash, render_template

from auth import guest_required
from form import RegisterForm
from services.user_service import UserService

register_page = Blueprint('register_page', __name__)

@register_page.route('/', methods=["GET", "POST"])
@guest_required
def page():
    form = RegisterForm()
    if request.method == "POST":
        user = request.form
        if user["password"] == user["passwordAgain"]:
            UserService.register(
                user["login"],
                user["firstname"],
                user["lastname"],
                user["email"],
                user["phone"],
                user["password"]
            )
            return redirect(url_for("login_page.page"))
        flash("Passwords do not match",category="error")
        form.fill_after_fail_attempt(user)
        return render_template("register_page/page.jinja", form=form)
    return render_template("register_page/page.jinja", form=form)