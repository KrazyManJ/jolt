from flask import Blueprint, render_template, redirect, url_for

from services.bike_service import BikeService

bike_details = Blueprint('bike_details', __name__)

@bike_details.route('/<bike_id>')
def page(bike_id: int):
    bike = BikeService.get_bike_by_id(bike_id)
    if not bike:
        return redirect(url_for("index.page"))
    return render_template("bike_details/page.jinja",bike=bike)