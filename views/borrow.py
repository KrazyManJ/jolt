from flask import Blueprint, render_template, request, flash, redirect, url_for, session

from auth import login_required
from services.bike_service import BikeService
from services.borrow_service import BorrowService

borrow = Blueprint('borrow', __name__)

@borrow.route('/<bike_id>', methods=['GET', 'POST'])
@login_required
def page(bike_id):
    available = BikeService.is_bike_available(bike_id)
    if not available:
        return redirect(url_for('index.page'))
    if request.method == 'POST':
        flash("Borrow successful", category='success')
        BorrowService.borrow(bike_id,session['id'],request.form['to'],request.form['payment_method'])
        return redirect(url_for('index.page'))
    else:
        bike = BikeService.get_by_id_for_borrow(bike_id)
        return render_template("borrow/page.jinja", bike=bike)