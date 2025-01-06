from datetime import datetime

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
        flash("Borrow was successful. By the time of beginning of borrow, please visit our store.", category='success')
        BorrowService.borrow(bike_id,session['id'],datetime.fromisoformat(request.form['to']).strftime('%Y-%m-%d %H:%M:%S'),request.form['payment_method'])
        return redirect(url_for('index.page'))
    else:
        bike = BikeService.get_bike_by_id(bike_id)
        return render_template("borrow/page.jinja", bike=bike)