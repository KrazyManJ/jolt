from flask import Blueprint, render_template

from auth import login_required

user_profile = Blueprint('user_profile', __name__)

@user_profile.route('/')
@login_required
def page():
    return render_template("user_profile/page.jinja")