from flask import Blueprint, render_template

from auth import login_required, roles_required
from services.borrow_service import BorrowService

borrows = Blueprint("borrows",__name__)

@borrows.route('/')
@login_required
@roles_required("employee")
def page():
    return render_template(
        "bikes_management/borrows/page.jinja",
        borrows = BorrowService.get_all_borrows()
    )