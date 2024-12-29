from flask import Blueprint, render_template

from auth import login_required, roles_required

bikes = Blueprint('bikes_management', __name__)

@bikes.route('/')
@login_required
@roles_required("employee")
def page():
    return render_template("bikes_management/page.jinja")