from database.database import get_db


class BikeService:
    @staticmethod
    def get_all_to_show():
        db = get_db()
        sql = ("SELECT bike_id,name,description,image,weight,body_size,"
               "wheel_size, body_material, gear_number, "
               "weight_limit, is_available FROM bikes "
               "WHERE is_shown = 1")
        return db.execute(sql).fetchall()

    @staticmethod
    def get_all_to_show_by_filter(availabilities, wmax, wlmax, bodies, wsizes, materials, gears):
        db = get_db()
        sql = ("SELECT bike_id,name,description,image,weight,body_size,wheel_size, body_material, gear_number,"
               "weight_limit, is_available FROM bikes WHERE is_shown = 1 AND (is_available = ? OR is_available = ?)"
               " AND weight <= ? AND weight_limit <= ?")
        arguments = availabilities+[wmax,wlmax]
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
        filters = [weights, weight_limits, body_sizes, wheel_sizes, body_materials, gear_numbers]
        return filters

