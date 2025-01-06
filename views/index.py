from flask import Blueprint, render_template, request, redirect

from services.bike_service import BikeService
from views.bikes_management import bikes

index = Blueprint('index', __name__)

@index.route('/', methods=['GET','POST'])
def page():
    if len(request.args) > 0:
        show = BikeService.get_all_to_show_by_filter(
            bool(request.args.get("available")),
            bool(request.args.get("not-available")),
            request.args.get("weight"),
            request.args.get("weight_lim"),
            request.args.getlist("size"),
            request.args.getlist("wsize"),
            request.args.getlist("material"),
            request.args.getlist("gear"),
            request.args.get('search'),
            request.args.get("bprice")
        )
    else:
        show = BikeService.get_all_to_show()
        print(show)
    filters = BikeService.get_filters()
    return render_template(
        'index/page.jinja', bikes=show, filters=filters, form=request.args)