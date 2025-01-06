from datetime import datetime

from database.database import get_db


class BikeService:
    @staticmethod
    def get_all():
        db = get_db()
        return db.execute("""
            SELECT *
            FROM bikes b
            JOIN bike_prices USING (bike_id)
            WHERE datetime = (SELECT datetime FROM bike_prices WHERE bike_id = b.bike_id ORDER BY datetime DESC LIMIT 1)
        """).fetchall()

    @staticmethod
    def get_all_to_show():
        db = get_db()
        return db.execute("""
            SELECT b.bike_id, b.name, b.description, b.image, b.weight, b.body_size, b.wheel_size, b.body_material, b.gear_number, b.weight_limit, b.is_shown, bp.*, CASE
                WHEN DATETIME(CURRENT_TIMESTAMP, 'localtime') BETWEEN br.datetime_from AND br.datetime_to AND br.datetime_from IS NOT NULL THEN 0
                WHEN DATETIME(CURRENT_TIMESTAMP, 'localtime') BETWEEN bs.datetime_from AND bs.datetime_to AND bs.datetime_from IS NOT NULL THEN 0
                ELSE b.is_available
            END AS is_available
            FROM bikes b
            LEFT JOIN borrows br USING(bike_id)
            LEFT JOIN bike_services bs USING(bike_id)
            JOIN bike_prices bp USING(bike_id)
            WHERE (
                br.datetime_from = (SELECT datetime_from FROM borrows WHERE bike_id = b.bike_id ORDER BY datetime_from DESC LIMIT 1)
                OR
                br.datetime_from IS NULL
            )
            AND (
                bs.datetime_from = (SELECT datetime_from FROM bike_services WHERE bike_id = b.bike_id ORDER BY datetime_from DESC LIMIT 1)
                OR
                bs.datetime_from IS NULL
            )
            AND bp.datetime = (SELECT datetime FROM bike_prices WHERE bike_id = b.bike_id ORDER BY datetime DESC LIMIT 1)
            AND b.is_shown = 1
        """).fetchall()

    @staticmethod
    def get_all_to_show_by_filter(is_available,is_not_available, wmax, wlmax, bodies, wsizes, materials, gears,
                                  search_data, bprice):
        db = get_db()
        sql = ("""
            WITH all_bikes AS (
                SELECT b.bike_id, b.name, b.description, b.image, b.weight, b.body_size, b.wheel_size, b.body_material, b.gear_number, b.weight_limit, b.is_shown, bp.*, CASE
                    WHEN DATETIME(CURRENT_TIMESTAMP, 'localtime') BETWEEN br.datetime_from AND br.datetime_to AND br.datetime_from IS NOT NULL THEN 0
                    WHEN DATETIME(CURRENT_TIMESTAMP, 'localtime') BETWEEN bs.datetime_from AND bs.datetime_to AND bs.datetime_from IS NOT NULL THEN 0
                    ELSE b.is_available
                END AS is_available
                FROM bikes b
                LEFT JOIN borrows br USING(bike_id)
                LEFT JOIN bike_services bs USING(bike_id)
                JOIN bike_prices bp USING(bike_id)
                WHERE (
                    br.datetime_from = (SELECT datetime_from FROM borrows WHERE bike_id = b.bike_id ORDER BY datetime_from DESC LIMIT 1)
                    OR
                    br.datetime_from IS NULL
                )
                AND (
                    bs.datetime_from = (SELECT datetime_from FROM bike_services WHERE bike_id = b.bike_id ORDER BY datetime_from DESC LIMIT 1)
                    OR
                    bs.datetime_from IS NULL
                )
                AND bp.datetime = (SELECT datetime FROM bike_prices WHERE bike_id = b.bike_id ORDER BY datetime DESC LIMIT 1)
                AND b.is_shown = 1
            )
            SELECT *
            FROM all_bikes
            WHERE 
                price <= ? 
                AND (is_available = ? OR is_available != ?)
                AND weight <= ?
                AND weight_limit <= ? 
        """)
        arguments = [bprice,is_available,is_not_available,wmax,wlmax]
        if bodies:
            sql+=" AND body_size IN ({})".format( ', '.join(['?'] * len(bodies)))
            arguments += bodies
        if wsizes:
            sql+= " AND wheel_size IN ({})".format( ', '.join(['?'] * len(wsizes)))
            arguments += wsizes
        if materials:
            sql+= " AND body_material IN ({})".format( ', '.join(['?'] * len(materials)))
            arguments += materials
        if gears:
            sql += " AND gear_number IN ({})".format( ', '.join(['?'] * len(gears)))
            arguments += gears
        if search_data:
            sql +=" AND (name LIKE ? OR description LIKE ?)"
            arguments += ['%'+search_data+'%','%'+search_data+'%']
        return db.execute(sql,arguments).fetchall()

    @staticmethod
    def get_filters():
        db = get_db()
        sql = ("SELECT MIN(weight) AS wmin, MAX(weight) AS wmax FROM "
               "bikes")
        weights = db.execute(sql).fetchone()
        sql = "SELECT MIN(weight_limit) AS wlmin, MAX(weight_limit) AS wlmax FROM bikes"
        weight_limits = db.execute(sql).fetchone()
        sql = "SELECT DISTINCT body_size FROM bikes"
        body_sizes = db.execute(sql).fetchall()
        sql = "SELECT DISTINCT wheel_size FROM bikes"
        wheel_sizes = db.execute(sql).fetchall()
        sql = "SELECT DISTINCT body_material FROM bikes"
        body_materials = db.execute(sql).fetchall()
        sql = "SELECT DISTINCT gear_number FROM bikes"
        gear_numbers = db.execute(sql).fetchall()
        sql = "SELECT MIN(price) AS pmin, MAX(price) AS pmax FROM bike_prices"
        prices = db.execute(sql).fetchone()
        filters = [weights, weight_limits, body_sizes, wheel_sizes, body_materials, gear_numbers, prices]
        return filters

    @staticmethod
    def add_bike(name,description,image ,weight, body_size, wheel_size, body_material, gear_number, weight_limit):
        db = get_db()
        sql = f"INSERT INTO bikes (name, description, image, weight, body_size, wheel_size, body_material, gear_number, weight_limit) VALUES ({','.join(['?']*9)})"
        bike_id = db.execute(sql,(name,description,image ,weight, body_size, wheel_size, body_material, gear_number, weight_limit)).lastrowid
        db.commit()
        return bike_id

    @staticmethod
    def is_bike_with_id(bike_id: int):
        db = get_db()
        return bool(db.execute(f"SELECT EXISTS(SELECT bike_id FROM bikes WHERE bike_id = ?)",(bike_id,)).fetchone()[0])

    @staticmethod
    def is_bike_available(bike_id: int):
        db = get_db()
        sql = """
            WITH all_bikes AS (
                SELECT b.bike_id, b.name, b.description, b.image, b.weight, b.body_size, b.wheel_size, b.body_material, b.gear_number, b.weight_limit, b.is_shown, bp.*, CASE
                    WHEN DATETIME(CURRENT_TIMESTAMP, 'localtime') BETWEEN br.datetime_from AND br.datetime_to AND br.datetime_from IS NOT NULL THEN 0
                    WHEN DATETIME(CURRENT_TIMESTAMP, 'localtime') BETWEEN bs.datetime_from AND bs.datetime_to AND bs.datetime_from IS NOT NULL THEN 0
                    ELSE b.is_available
                END AS is_available
                FROM bikes b
                LEFT JOIN borrows br USING(bike_id)
                LEFT JOIN bike_services bs USING(bike_id)
                JOIN bike_prices bp USING(bike_id)
                WHERE (
                    br.datetime_from = (SELECT datetime_from FROM borrows WHERE bike_id = b.bike_id ORDER BY datetime_from DESC LIMIT 1)
                    OR
                    br.datetime_from IS NULL
                )
                AND (
                    bs.datetime_from = (SELECT datetime_from FROM bike_services WHERE bike_id = b.bike_id ORDER BY datetime_from DESC LIMIT 1)
                    OR
                    bs.datetime_from IS NULL
                )
                AND bp.datetime = (SELECT datetime FROM bike_prices WHERE bike_id = b.bike_id ORDER BY datetime DESC LIMIT 1)
                AND b.is_shown = 1
            )
            SELECT EXISTS(SELECT bike_id FROM all_bikes WHERE bike_id = ? AND is_available = 1)
        """
        arguments = [bike_id]
        return bool(db.execute(sql,arguments).fetchone()[0])

    @staticmethod
    def delete_bike_with_id(bike_id: int):
        db = get_db()
        db.execute("DELETE FROM bikes WHERE bike_id = ?",(bike_id,))
        db.commit()

    @staticmethod
    def get_bike_by_id(bike_id: int):
        db = get_db()
        return db.execute("SELECT * FROM bikes JOIN bike_prices USING(bike_id) WHERE bike_id = ? ORDER BY datetime DESC LIMIT 1",(bike_id,)).fetchone()

    @staticmethod
    def edit_bike_by_id(bike_id: int, name,description,image ,weight, body_size, wheel_size, body_material, gear_number, weight_limit, is_available, is_shown):
        db = get_db()
        sql = "UPDATE bikes SET name=?,description=?,image=?,weight=?,body_size=?,wheel_size=?,body_material=?,gear_number=?,weight_limit=?,is_available=?,is_shown=? WHERE bike_id = ?"
        params = [name,description,image,weight,body_size,wheel_size,body_material,gear_number,weight_limit,is_available,is_shown,bike_id]
        db.execute(sql,params)
        db.commit()

    @staticmethod
    def add_bike_price(bike_id: int, price: int):
        db = get_db()
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.execute("INSERT INTO bike_prices (bike_id, price, datetime) VALUES (?,?,?)",(bike_id, price, current_datetime))
        db.commit()

    @staticmethod
    def was_bike_borrowed_by_id(bike_id):
        db = get_db()
        return bool(db.execute("SELECT EXISTS(SELECT * FROM bikes JOIN borrows USING(bike_id) WHERE bike_id = ?)",(bike_id,)).fetchone()[0])