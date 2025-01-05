from flask import Blueprint, render_template, flash, redirect, url_for, request, session

from auth import login_required, roles_required
from form import EditUserForm
from services.user_service import UserService

users_management = Blueprint('users_management', __name__)

@users_management.route('/')
@login_required
@roles_required("admin")
def page():
    return render_template("users_management/page.jinja",users=UserService.get_all_users())

@users_management.route('/<user_id>/edit', methods=["GET","POST"])
@login_required
@roles_required("admin")
def edit_page(user_id: int):
    user = UserService.get_user_by_id(user_id)
    if not user:
        flash(f"User with id '{user_id}' does not exist!",category="error")
        return redirect(url_for("users_management.page"))
    if user["user_id"] == session["id"]:
        flash(f"Cannot edit yourself!",category="error")
        return redirect(url_for("users_management.page"))

    form = EditUserForm()


    if request.method == "POST":
        if form.validate_on_submit():
            form_data = form.data
            form_data.pop("csrf_token")
            form_data["role_id"] = form_data.pop("role")
            UserService.update_user_by_id(user_id,**form_data)
            flash(f"User with id '{user_id}' was updaated!",category="success")
        else:
            flash(f"There was problem while updating '{user_id}'! Reason: {form.errors}",category="error")
        return redirect(url_for("users_management.page"))

    data = dict(user)
    data.pop("password_hash")
    data.pop("user_id")
    data.pop("name")
    data["role"] = str(data.pop("role_id"))
    for key in data.keys():
        try:
            form.__getattribute__(key).data = data[key]
        except:
            pass
    return render_template("users_management/edit/page.jinja",form=form)