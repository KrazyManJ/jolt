from database.database import get_db


class ReturnReportService:
    @staticmethod
    def get_bike_state_type_choices():
        db = get_db()
        return [tuple(v) for v in db.execute("SELECT * FROM bike_state_types").fetchall()]

    @staticmethod
    def add_return_report(borrow_id: int, bike_state_type_id: int, employee_note):
        db = get_db()
        db.execute(
            "INSERT INTO return_reports (borrow_id, bike_state_type_id, employee_note) VALUES (?,?,?)",
            (borrow_id,bike_state_type_id,employee_note)
        )
        db.commit()

    @staticmethod
    def get_all():
        db = get_db()
        return db.execute("""
            SELECT *
            FROM return_reports
            JOIN bike_state_types USING(bike_state_type_id)
            JOIN borrows USING(borrow_id)
            JOIN bikes USING(bike_id)
            JOIN users USING(user_id)
        """).fetchall()

    @staticmethod
    def get_report_by_id(return_report_id: int):
        db = get_db()
        return db.execute("""
            SELECT *
            FROM return_reports
            WHERE return_report_id = ?
        """,(return_report_id,)).fetchone()

    @staticmethod
    def update_report_by_id(return_report_id: int, bike_state_type_id, employee_note):
        db = get_db()
        db.execute("""
            UPDATE return_reports SET bike_state_type_id=?, employee_note=? WHERE return_report_id = ?
        """,(bike_state_type_id,employee_note,return_report_id))
        db.commit()