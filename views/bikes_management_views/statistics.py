from flask import Blueprint, render_template

from auth import login_required, roles_required

statistics = Blueprint('statistics', __name__)

@statistics.route('/')
@login_required
@roles_required("employee")
def page():
    return render_template('bikes_management/statistics/page.jinja')