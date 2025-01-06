from flask import Blueprint, render_template, session

from auth import login_required
from services.borrow_service import BorrowService

user_profile = Blueprint('user_profile', __name__)

@user_profile.route('/')
@login_required
def page():
    for a in BorrowService.get_borrows_of_user(session["id"]):
        dfrom = a["datetime_from"]
        dto = a["datetime_to"]
        print("from", dfrom, type(dfrom))
        print("to", dto, type(dto))
    return render_template(
        "user_profile/page.jinja",
        borrows=BorrowService.get_borrows_of_user(session["id"])
    )