from flask import Blueprint, render_template

from services.bike_service import BikeService

index = Blueprint('index', __name__)

@index.route('/')
def page():
    bikes = BikeService.get_all_to_show()
    return render_template(
        'index/page.jinja', bikes=bikes)