from database.database import get_db


class BorrowService:
    @staticmethod
    def borrow(bike_id,user_id,datetime_to,payment_method):
        db = get_db()
        sql = ("INSERT INTO borrows (bike_id,user_id,datetime_to,payment_method) "
               "VALUES (?,?,?,?)")
        arguments = (bike_id,user_id,datetime_to,payment_method)
        print(sql,arguments)
        db.execute(sql, arguments)
        db.commit()