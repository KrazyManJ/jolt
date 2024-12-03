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
        SELECT u.user_id, u.login_name, u.first_name, u.last_name, r.name as role_name
        FROM users u
        JOIN roles r ON u.role_id = r.role_id
        WHERE u.login_name = ? AND u.password_hash = ?
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
        INSERT INTO users (login_name,first_name,last_name,email,phone_number,password_hash)
        VALUES (?,?,?,?,?,?)
        """

        arguments = [login,first_name,last_name,email,phone_number,UserService.__hash_password(password)]

        db.execute(sql, arguments)
        db.commit()
