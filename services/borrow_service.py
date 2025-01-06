from datetime import datetime

from database.database import get_db


class BorrowService:
    @staticmethod
    def borrow(bike_id,user_id,datetime_to,payment_method):
        db = get_db()
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = ("INSERT INTO borrows (bike_id,user_id,datetime_from,datetime_to,payment_method) "
               "VALUES (?,?,?,?,?)")
        arguments = (bike_id,user_id,current_datetime,datetime_to,payment_method)
        db.execute(sql, arguments)
        db.commit()

    @staticmethod
    def get_borrows_of_user(user_id: int):
        db = get_db()
        return db.execute("""
            SELECT * 
            FROM borrows
            JOIN bikes USING(bike_id)
            WHERE user_id = ?
            ORDER BY datetime_from DESC
        """,(user_id,)).fetchall()
