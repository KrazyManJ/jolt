from database.database import get_db


class ServicingService:
    @staticmethod
    def get_all_services():
        db = get_db()
        sql = ("SELECT bike_service_id, b.bike_id AS id_bike, "
               "b.name AS bike_name, datetime_from, datetime_to,"
               " reason, price, s.name AS state FROM bike_services "
               "JOIN bikes AS b USING (bike_id) JOIN "
               "service_state_types AS s USING "
               "(service_state_type_id)")
        return db.execute(sql).fetchall()

    @staticmethod
    def get_state_choices():
        db = get_db()
        sql = "SELECT * FROM service_state_types"
        return db.execute(sql).fetchall()

    @staticmethod
    def get_state_by_id(state_id):
        db = get_db()
        sql = ("SELECT * FROM service_state_types WHERE service_state_types.service_state_type_id"
               " = ?")
        arguments = [state_id]
        return db.execute(sql, arguments).fetchone()

    @staticmethod
    def get_service_by_id(service_id):
        db = get_db()
        sql = "SELECT * FROM bike_services WHERE bike_service_id = ?"
        arguments = [service_id]
        return db.execute(sql, arguments).fetchone()

    @staticmethod
    def add_service(bike_id,service_state,datetime_from,datetime_to,reason,price):
        db = get_db()
        sql = ("INSERT INTO bike_services (bike_id, service_state_type_id, datetime_from, datetime_to, reason, price)"
               " VALUES (?, (SELECT service_state_type_id FROM"
               " service_state_types WHERE name = ?"
               "),?, ?, ?, ?)")
        arguments = [bike_id,service_state,datetime_from,datetime_to,reason,price]
        db.execute(sql, arguments)
        db.commit()

    @staticmethod
    def is_service_with_id(service_id):
        db = get_db()
        sql = "SELECT EXISTS(SELECT * FROM bike_services WHERE bike_service_id = ?) "
        arguments = [service_id]
        return bool(db.execute(sql,arguments).fetchone()[0])

    @staticmethod
    def edit_service(service_id,bike_id,service_state,
                     datetime_from,datetime_to,reason,price):
        db = get_db()
        sql = ("UPDATE bike_services SET bike_id = ?, service_state_type_id = "
               "(SELECT service_state_type_id FROM service_state_types "
               "WHERE name = ?), datetime_from = ?, datetime_to = ?, "
               "reason = ?, price = ? WHERE bike_service_id = ?")
        arguments = [bike_id,service_state,datetime_from,datetime_to,reason,price,service_id]
        db.execute(sql, arguments)
        db.commit()