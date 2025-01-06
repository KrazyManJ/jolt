from flask import Blueprint, render_template, request, flash, url_for, redirect

from auth import login_required, roles_required
from form import AddReturnReportForm, EditReturnReportForm
from services.borrow_service import BorrowService
from services.return_report_service import ReturnReportService

return_reports = Blueprint("return_reports", __name__)

@return_reports.route('/')
@login_required
@roles_required("employee")
def page():
    return render_template(
        "bikes_management/return_reports/page.jinja",
        return_reports=ReturnReportService.get_all()
    )

@return_reports.route('/add', methods=["GET", "POST"])
@login_required
@roles_required("employee")
def add_page():
    if len(BorrowService.get_choices_of_borrows_without_return_report()) == 0:
        flash("There are no borrows to be reported.",category="warning")
        return redirect(url_for("bikes_management.return_reports.page"))

    form = AddReturnReportForm()
    if request.method == "POST":
        if form.validate_on_submit():
            data = form.data
            data.pop("csrf_token")
            ReturnReportService.add_return_report(**data)
            flash(f"Return report was successfully added!",category="success")
            return redirect(url_for("bikes_management.return_reports.page"))
        else:
            flash(f"There was a problem while adding return report. Reason: {form.errors}",category="error")

    return render_template("bikes_management/return_reports/add_or_edit/page.jinja",form=form)

@return_reports.route('<return_report_id>/edit', methods=["GET", "POST"])
@login_required
@roles_required("employee")
def edit_page(return_report_id: int):
    report = ReturnReportService.get_report_by_id(return_report_id)

    if report is None:
        flash(f"Report with id '{return_report_id}' does not exists!",category="Error")
        return redirect(url_for("bikes_management.return_reports.page"))

    form = EditReturnReportForm()

    if request.method == "POST":
        if form.validate_on_submit():
            data = form.data
            data.pop("csrf_token")
            ReturnReportService.update_report_by_id(return_report_id,**data)
            flash(f"Return report with id '{return_report_id}' was successfully updated!",category="success")
            return redirect(url_for("bikes_management.return_reports.page"))
        else:
            flash(f"There was a problem while editing return report. Reason: {form.errors}",category="error")

    data = dict(report)
    data.pop("return_report_id")
    data.pop("borrow_id")
    data["bike_state_type_id"] = str(data.pop("bike_state_type_id"))
    for key in data.keys():
        form.__getattribute__(key).data = data[key]


    return render_template(
        "bikes_management/return_reports/add_or_edit/page.jinja",
        return_report_id=return_report_id,
        form=form
    )