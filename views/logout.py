from flask import Blueprint, session, redirect, url_for

from Jolt.auth import login_required

logout_v = Blueprint('logout_v', __name__)

@logout_v.route('/')
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
    return redirect(url_for('index.page'))