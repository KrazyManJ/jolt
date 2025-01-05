from flask import Blueprint, render_template

from services.bike_service import BikeService

bike_details = Blueprint('bike_details', __name__)

@bike_details.route('/<bike_id>')
def page(bike_id: int):
    return render_template("bike_details/page.jinja",bike=BikeService.get_bike_by_id(bike_id))