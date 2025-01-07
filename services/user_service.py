import hashlib

from database.database import get_db
import config

class UserService:

    @staticmethod
    def __hash_password(password: str):
        return hashlib.sha256(f'{password}{config.PASSWORD_SALT}'.encode()).hexdigest()

    @staticmethod
    def verify(login: str, password: str):
        db = get_db()

        sql = '''
        SELECT u.user_id, u.login, u.first_name, u.last_name, r.name as role_name
        FROM users u
        JOIN roles r ON u.role_id = r.role_id
        WHERE u.login = ? AND u.password_hash = ? AND NOT u.is_deactivated = 1
        '''
        arguments = [login, UserService.__hash_password(password)]

        user = db.execute(sql, arguments).fetchone()

        return user if user else None

    @staticmethod
    def register(
        login,
        first_name,
        last_name,
        email,
        phone_number,
        password
    ):
        db = get_db()

        sql = """
        INSERT INTO users (login,first_name,last_name,email,phone_number,password_hash)
        VALUES (?,?,?,?,?,?)
        """

        arguments = [login, first_name, last_name, email, phone_number, UserService.__hash_password(password)]

        db.execute(sql, arguments)
        db.commit()

    @staticmethod
    def get_all_users():
        db = get_db()
        return db.execute("SELECT * FROM users JOIN roles USING(role_id)").fetchall()

    @staticmethod
    def get_role_choices():
        db = get_db()
        return [tuple(v) for v in db.execute("SELECT * FROM roles").fetchall()]

    @staticmethod
    def get_user_by_id(user_id: int):
        db = get_db()
        return db.execute("SELECT * FROM users JOIN roles USING(role_id) WHERE user_id = ?",(user_id,)).fetchone()

    @staticmethod
    def update_user_by_id(user_id: int, login, first_name, last_name, email, phone_number, is_deactivated, role_id):
        db = get_db()
        sql = "UPDATE users SET login=?,first_name=?,last_name=?,email=?,phone_number=?,is_deactivated=?,role_id=? WHERE user_id = ?"
        params = [login,first_name,last_name,email,phone_number,is_deactivated,role_id,user_id]
        db.execute(sql,params)
        db.commit()