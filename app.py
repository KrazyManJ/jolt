from flask import Flask
# from livereload import Server

from views.bikes_management import bikes
from views.index import index
from views.login_page import login_page
from views.logout import logout_v
from views.register_page import register_page
from views.user_profile import user_profile
from database import database

app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_object('config')
database.init_app(app)
app.register_blueprint(index, url_prefix='/')
app.register_blueprint(bikes, url_prefix='/bikes-management')
app.register_blueprint(user_profile, url_prefix='/user-profile')
app.register_blueprint(login_page, url_prefix='/login')
app.register_blueprint(register_page, url_prefix='/register')
app.register_blueprint(logout_v, url_prefix='/logout')


if __name__ == '__main__':
    # server = Server(app.wsgi_app)
    # server.serve(host='0.0.0.0',port=5001,debug=True)
    app.run('0.0.0.0', port=5001, debug=True)