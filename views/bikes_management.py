from flask import Blueprint

from views.bikes_management_views.bikes import bikes
from views.bikes_management_views.borrows import borrows
from views.bikes_management_views.servising import servising
from views.bikes_management_views.statistics import statistics

bikes_management = Blueprint('bikes_management', __name__)


bikes_management.register_blueprint(statistics, url_prefix='/statistics')
bikes_management.register_blueprint(bikes, url_prefix='/bikes')
bikes_management.register_blueprint(servising, url_prefix='/servising')
bikes_management.register_blueprint(borrows, url_prefix='/borrows')


