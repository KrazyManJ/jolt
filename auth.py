from functools import wraps

from flask import flash, request
from flask import redirect
from flask import session
from flask import url_for


def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        print(session)
        if "authenticated" not in session:
            flash("You must be logged in")
            return redirect(url_for("login_page"))
        return func(*args, **kwargs)

    return decorated_function


def roles_required(*roles):
    def roles_decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if session['role'] not in roles:
                flash('You have no rights to do that', 'error')
                return redirect(request.referrer)
            return func(*args, **kwargs)

        return decorated_function

    return roles_decorator
