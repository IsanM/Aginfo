from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail



app = Flask(__name__)
app.config.from_pyfile('config.cfg')
app.config[
    'SECRET_KEY'] = '-\x03\xb5\xf6\x86\xee81\x0c\xbb\xe8\xfb\x1e\x08I\x065vyS\xd2\x1a\xff\xae\x10M\xb7k\x0c\xa1\xacY'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# migrations
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'
############ MAIL Configuration ####################
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'ishanmadhawa440@gmail.com'
app.config['MAIL_PASSWORD'] = 'bscsd1809'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LeGCK0ZAAAAAGfjov9hTnafxfxR0Zgk-qdZ9r6o'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LeGCK0ZAAAAAPxJwDZ-dIiNll1rXBpl_FAblWxe'



# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:52377/Aginfo'
# db = SQLAlchemy(app)


from flasksystem import routes

