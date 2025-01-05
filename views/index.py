from flask import Blueprint, render_template, request, redirect

from services.bike_service import BikeService
from views.bikes_management import bikes

index = Blueprint('index', __name__)

@index.route('/', methods=['GET','POST'])
def page():
    if len(request.args) > 0:
        ready = request.args.getlist('ready')
        if len(ready) == 0:
            available, borrowed = 1, 0
        elif len(ready) == 1 and ready[0] == 'available':
            available, borrowed = 1, 1
        elif len(ready) == 1 and ready[0] == 'borrowed':
            available, borrowed = 0, 0
        elif len(ready) == 2:
            available, borrowed = 0, 1
        show = BikeService.get_all_to_show_by_filter(
            [available, borrowed],request.args.get("weight"),request.args["weight_lim"],
            request.args.getlist("size"),request.args.getlist("wsize"),request.args.getlist("material"),
            request.args.getlist("gear"),request.args.get('search'),request.args.get("bprice")
        )
    else:
        show = BikeService.get_all_to_show()
    filters = BikeService.get_filters()
    return render_template(
        'index/page.jinja', bikes=show, filters=filters, form=request.args)