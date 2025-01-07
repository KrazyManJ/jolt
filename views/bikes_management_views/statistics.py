from datetime import datetime

from flask import Blueprint, render_template, request, flash

from auth import login_required, roles_required
from services.statistic_service import StatisticService

statistics = Blueprint('statistics', __name__)

@statistics.route('/')
@login_required
@roles_required("employee")
def page():
    cashflow_data = []
    amount_data = None
    if request.args:
        if not (request.args.get('cashflow_from') or request.args.get('cashflow_to')):
            cashflow_data = StatisticService.get_cashflow()
        else:
            datetime_from = datetime.fromisoformat(request.args['cashflow_from']).strftime('%Y-%m-%d %H:%M:%S')
            datetime_to = datetime.fromisoformat(request.args['cashflow_to']).strftime('%Y-%m-%d %H:%M:%S')
            if datetime_from < datetime_to:
                cashflow_data = StatisticService.get_cashflow_by_datetimes(datetime_from, datetime_to)
            else:
                flash("Invalid period.",category="error")
        if not (request.args.get('amount_from') or request.args.get('amount_to')):
            amount_data = StatisticService.get_amount()
        else:
            datetime_from = datetime.fromisoformat(request.args.get('amount_from')).strftime('%Y-%m-%d %H:%M:%S')
            datetime_to = datetime.fromisoformat(request.args['amount_to']).strftime('%Y-%m-%d %H:%M:%S')
            if datetime_from < datetime_to:
                amount_data = StatisticService.get_amount_by_datetimes(datetime_from, datetime_to)
            else:
                flash("Invalid period.", category="error")
    else:
        if not (request.args.get('cashflow_from') or request.args.get('cashflow_to')):
            cashflow_data = StatisticService.get_cashflow()
        if not (request.args.get('amount_from') or request.args.get('amount_to')):
            amount_data = StatisticService.get_amount()
    bikes = StatisticService.get_bikes()
    return render_template('bikes_management/statistics/page.jinja',cashflow=cashflow_data,
                           amount=amount_data, bikes=bikes)