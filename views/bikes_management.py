import base64
from datetime import datetime

from flask import Blueprint, render_template, request, flash, redirect, url_for

from auth import login_required, roles_required
from form import AddBikeForm, EditBikeForm, ServiceForm
from services.bike_service import BikeService
from services.servicing_service import ServicingService

bikes = Blueprint('bikes_management', __name__)

@bikes.route('/')
@login_required
@roles_required("employee")
def page():
    return render_template("bikes_management/page.jinja",bikes=BikeService.get_all(),services=ServicingService.get_all_services())

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
                return redirect(url_for("bikes_management.page"))
    return render_template("bikes_management/add_or_edit/page.jinja", form=form, id=None)

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
    return redirect(url_for("bikes_management.page"))

@bikes.route('/<bike_id>/edit',methods=["GET","POST"])
@login_required
@roles_required("employee")
def edit_page(bike_id: int):

    if not BikeService.is_bike_with_id(bike_id):
        flash(f"Bike with id '{bike_id}' does not exist.", category="error")
        return redirect(url_for("bikes_management.page"))

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
            return redirect(url_for("bikes_management.page"))

    data.pop("bike_id")
    data.pop("image")
    data.pop("bike_price_id")
    data.pop("datetime")
    for key in data.keys():
        form.__getattribute__(key).data = data[key]
    return render_template("bikes_management/add_or_edit/page.jinja", form=form, id=bike_id)

@bikes.route('/add-service', methods=["GET", "POST"])
@login_required
@roles_required("employee")
def add_service_page():
    form = ServiceForm()
    if request.method == "POST":
        if not form.validate_on_submit():
            flash("There was an error while adding service!", category="error")
        else:
            form_data = form.data
            form_data.pop('csrf_token')
            bike_data = form_data.pop("name_id")
            bike_id = bike_data.split(" - ")[0]
            service_state_data = form_data.pop("state")
            service_state_name = service_state_data.split(" - ")[0]
            ServicingService.add_service(bike_id,service_state_name,**form_data)
            flash("Successfully added service record!",category="success")
            return redirect(url_for("bikes_management.page"))
    return render_template("bikes_management/add_or_edit_service/page.jinja", form=form)

@bikes.route('/edit-service/<service_id>', methods=["GET","POST"])
@login_required
@roles_required("employee")
def edit_service_page(service_id):
    if not ServicingService.is_service_with_id(service_id):
        return redirect(url_for("bikes_management.page"))

    form = ServiceForm()

    if request.method == "POST":
        if not form.validate_on_submit():
            flash("There was an error while editing service!", category="error")
        else:
            form_data = form.data
            form_data.pop('csrf_token')
            bike_data = form_data.pop("name_id")
            bike_id = bike_data.split(" - ")[0]
            service_state_data = form_data.pop("state")
            service_state_name = service_state_data.split(" - ")[0]
            ServicingService.edit_service(service_id,bike_id,service_state_name,**form_data)
            flash(f"Successfully edited service record with id '{service_id}'.",category="success")
            return redirect(url_for("bikes_management.page"))

    data = dict(ServicingService.get_service_by_id(service_id))
    data.pop("bike_service_id")
    bike_id = data.pop("bike_id")
    bike = BikeService.get_bike_by_id(bike_id)
    data["name_id"] = str(bike["bike_id"]) + " - " + bike["name"]
    service_state_id = data.pop("service_state_type_id")
    service_state = ServicingService.get_state_by_id(service_state_id)
    data["state"] = service_state["name"]
    data["datetime_from"] = datetime.strptime(data["datetime_from"], "%Y-%m-%d %H:%M:%S")
    data["datetime_to"] = datetime.strptime(data["datetime_to"], "%Y-%m-%d %H:%M:%S")
    for key in data.keys():
        form.__getattribute__(key).data = data[key]
    return render_template("bikes_management/add_or_edit_service/page.jinja", form=form, service_id=service_id)