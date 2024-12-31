from database.database import get_db


class BikeService:
    @staticmethod
    def get_all_to_show():
        db = get_db()
        sql = ("SELECT name,description,weight,body_size,"
               "wheel_size, body_material, gear_number, "
               "weight_limit, is_available FROM bikes "
               "WHERE is_shown = 1")
        return db.execute(sql).fetchall()

    @staticmethod
    def get_filters():
        db = get_db()
        sql = ("WITH weights AS (SELECT DISTINCT weight FROM "
               "bikes SELECT * FROM weights;")