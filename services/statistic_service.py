from database.database import get_db


class StatisticService:
    @staticmethod
    def get_cashflow():
        db = get_db()
        sql = """
            WITH data AS (
                SELECT
                    (SELECT SUM(price)
                        FROM borrows br
                        JOIN bike_prices bp ON br.bike_id = bp.bike_id
                        WHERE price = (
                            SELECT price
                            FROM bike_prices
                            WHERE bike_id = br.bike_id
                            AND datetime <= br.datetime_from
                            ORDER BY datetime DESC
                            LIMIT 1
                        )
                    ) AS incomes,
                    (SELECT SUM(price) FROM bike_services) AS costs
            )
            SELECT incomes, costs, incomes - costs AS balance FROM data;
        """
        return db.execute(sql).fetchone()

    @staticmethod
    def get_cashflow_by_datetimes(datetime_from, datetime_to):
        db = get_db()
        sql = """
                WITH data AS (
                    SELECT
                        (SELECT SUM(price)
                            FROM borrows br
                            JOIN bike_prices bp ON br.bike_id = bp.bike_id
                            WHERE price = (
                                SELECT price
                                FROM bike_prices
                                WHERE bike_id = br.bike_id
                                AND datetime <= br.datetime_from
                                ORDER BY datetime DESC
                                LIMIT 1
                            ) AND datetime_from >= ?
                            AND datetime_to <= ?
                        ) AS incomes,
                        (SELECT SUM(price) FROM bike_services WHERE datetime_from >= ?
                        AND datetime_to <= ?) AS costs
                )
                SELECT incomes, costs, incomes - costs AS balance FROM data;
            """
        arguments = [datetime_from, datetime_to,datetime_from, datetime_to]
        return db.execute(sql,arguments).fetchone()

    @staticmethod
    def get_amount():
        db = get_db()
        sql = "SELECT COUNT(*) AS amount FROM borrows"
        return db.execute(sql).fetchone()

    @staticmethod
    def get_amount_by_datetimes(datetime_from, datetime_to):
        db = get_db()
        sql = """SELECT COUNT(*) AS amount FROM borrows WHERE datetime_from >= ?
                 AND datetime_to <= ?"""
        arguments = [datetime_from,datetime_to]
        return db.execute(sql,arguments).fetchone()

    @staticmethod
    def get_bikes():
        db = get_db()
        sql = """SELECT image, name, (SELECT COUNT(*) AS borrowed FROM borrows WHERE 
                 bike_id=b.bike_id) AS count
                 FROM bikes AS b ORDER BY count DESC"""
        return db.execute(sql).fetchall()