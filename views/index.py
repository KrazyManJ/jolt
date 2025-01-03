from flask import Blueprint, render_template, request

from services.bike_service import BikeService
from views.bikes_management import bikes

index = Blueprint('index', __name__)

@index.route('/', methods=['GET','POST'])
def page():
    if request.method == 'POST':
        print(request.form.getlist('ready'))
        ready = request.form.getlist('ready')
        if len(ready) == 0:
            available, borrowed = 1, 0
        elif len(ready) == 1 and ready[0] == 'available':
            available, borrowed = 1, 1
        elif len(ready) == 1 and ready[0] == 'borrowed':
            available, borrowed = 0, 0
        elif len(ready) == 2:
            available, borrowed = 0, 1
        show = BikeService.get_all_to_show_by_filter(
            [available, borrowed],request.form["weight"],request.form["weight_lim"],
            request.form.getlist("size"),request.form.getlist("wsize"),request.form.get("material"),
            request.form.get("gear")
        )
    else:
        show = BikeService.get_all_to_show()
    filters = BikeService.get_filters()
    return render_template(
        'index/page.jinja', bikes=show, filters=filters)