from flask import Blueprint, render_template

from auth import login_required
from services.bike_service import BikeService

borrow = Blueprint('borrow', __name__)

@borrow.route('/<id>', methods=['GET', 'POST'])
@login_required
def page(id):
    bike = BikeService.get_by_id_for_borrow(id)
    return render_template("borrow/page.jinja", bike=bike)