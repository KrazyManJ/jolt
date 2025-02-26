import base64

from flask import Blueprint, render_template, flash, redirect, request, url_for

from auth import login_required, roles_required
from form import EditBikeForm, AddBikeForm
from services.bike_service import BikeService

bikes = Blueprint('bikes', __name__)

@bikes.route('/')
@login_required
@roles_required("employee")
def page():
    return render_template(
        'bikes_management/bikes/page.jinja',
        bikes=BikeService.get_all()
    )



@bikes.route('/add', methods=["GET", "POST"])
@login_required
@roles_required("employee")
def add_page():
    form = AddBikeForm()
    if request.method == "POST":
        if not form.validate_on_submit():
            flash("There was an error while adding bike!",category="error")
        else:
            file = form.image.data
            if file:
                input_data = form.data
                input_data["image"] = base64.b64encode(file.read()).decode('utf-8')
                input_data.pop('csrf_token')
                price = input_data.pop("price")
                bike_id = BikeService.add_bike(**input_data)
                BikeService.add_bike_price(bike_id, price)
                flash("Successfully added bike.",category="success")
                return redirect(url_for("bikes_management.bikes.page"))
    return render_template("bikes_management/bikes/add_or_edit/page.jinja", form=form, id=None)

@bikes.route('/<bike_id>/remove')
@login_required
@roles_required("employee")
def remove(bike_id: int):
    if not BikeService.is_bike_with_id(bike_id):
        flash(f"Bike with id '{bike_id}' does not exist.",category="error")
    elif BikeService.was_bike_borrowed_by_id(bike_id):
        flash(f"Bike with id '{bike_id}' was already borrowed and cannot be removed.",category="error")
    else:
        flash(f"Bike with id '{bike_id}' successfully deleted.",category="success")
        BikeService.delete_bike_with_id(bike_id)
    return redirect(url_for("bikes_management.bikes.page"))

@bikes.route('/<bike_id>/edit', methods=["GET", "POST"])
@login_required
@roles_required("employee")
def edit_page(bike_id: int):

    if not BikeService.is_bike_with_id(bike_id):
        flash(f"Bike with id '{bike_id}' does not exist.", category="error")
        return redirect(url_for("bikes_management.bikes.page"))

    form = EditBikeForm()
    data = dict(BikeService.get_bike_by_id(bike_id))

    if request.method == "POST":
        if not form.validate_on_submit():
            flash("There was an error while editing bike!", category="error")
        else:
            input_data = form.data
            file = form.image.data
            if file:
                input_data["image"] = base64.b64encode(file.read()).decode('utf-8')
            else:
                input_data["image"] = data.get("image")
            input_data.pop('csrf_token')
            price = input_data.pop('price')
            BikeService.edit_bike_by_id(bike_id,**input_data)
            if price != data["price"]:
                BikeService.add_bike_price(bike_id, price)
            flash(f"Successfully edited bike with id '{bike_id}'.", category="success")
            return redirect(url_for("bikes_management.bikes.page"))

    data.pop("bike_id")
    data.pop("image")
    data.pop("bike_price_id")
    data.pop("datetime")
    for key in data.keys():
        form.__getattribute__(key).data = data[key]
    return render_template("bikes_management/bikes/add_or_edit/page.jinja", form=form, id=bike_id)
