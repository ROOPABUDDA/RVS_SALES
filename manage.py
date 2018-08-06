import app
# import flask
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

# application = app.create_app()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/saledatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

if __name__ == '__main__':
	from app import *
	application.run()

	
	

    