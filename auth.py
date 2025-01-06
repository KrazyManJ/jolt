from functools import wraps

from flask import flash, request
from flask import redirect
from flask import session
from flask import url_for

from services.user_service import UserService


def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if "authenticated" in session:
            user = UserService.get_user_by_id(session["id"])
            if not user and user["is_deactivated"]:
                return redirect(url_for("logout_v.page"))
        else:
            flash("You must be logged in.", category='warning')
            return redirect(url_for("login_page.page"))
        return func(*args, **kwargs)

    return decorated_function

def guest_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if "authenticated" in session:
            flash("You are already logged in.", category='warning')
            return redirect(request.referrer)
        return func(*args, **kwargs)

    return decorated_function

def roles_required(*roles):
    def roles_decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if session['role'] not in roles:
                flash('Error: Cannot access this content!', category='error')
                return redirect(request.referrer)
            return func(*args, **kwargs)

        return decorated_function

    return roles_decorator
