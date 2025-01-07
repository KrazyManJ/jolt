from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, request, flash

from auth import login_required, roles_required
from form import ServiceForm
from services.bike_service import BikeService
from services.servicing_service import ServicingService

servising = Blueprint('servising', __name__)

@servising.route('/')
@login_required
@roles_required("employee")
def page():
    return render_template(
        'bikes_management/servising/page.jinja',
        services=ServicingService.get_all_services()
    )


@servising.route('/add-service', methods=["GET", "POST"])
@login_required
@roles_required("employee")
def add_page():
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
            return redirect(url_for("bikes_management.servising.page"))
    return render_template("bikes_management/servising/add_or_edit/page.jinja", form=form)

@servising.route('/edit-service/<service_id>', methods=["GET", "POST"])
@login_required
@roles_required("employee")
def edit_page(service_id):
    if not ServicingService.is_service_with_id(service_id):
        return redirect(url_for("bikes_management.servising.page"))

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
            return redirect(url_for("bikes_management.servising.page"))

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
    return render_template("bikes_management/servising/add_or_edit/page.jinja", form=form, service_id=service_id)

@servising.route('/delete-service/<service_id>')
@login_required
@roles_required("employee")
def remove(service_id):
    if not ServicingService.is_service_with_id(service_id):
        return redirect(url_for("bikes_management.servising.page"))
    ServicingService.delete_service(service_id)
    flash(f"Successfully deleted service record with id '{service_id}'",category="success")
    return render_template(
        'bikes_management/servising/page.jinja',
        services=ServicingService.get_all_services()
    )