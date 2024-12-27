from flask import Blueprint, render_template

from Jolt.auth import login_required, roles_required

bikes_management = Blueprint('bikes_management', __name__)

@bikes_management.route('/bikes-management')
@login_required
@roles_required("employee")
def page():
    return render_template("bikes_management/page.jinja")