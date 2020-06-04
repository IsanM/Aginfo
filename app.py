from flask import Flask, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:52377/Aginfo'
#db = SQLAlchemy(app)
