import os
from flask import Flask, render_template
from flask_nav import Nav
from flask_nav.elements import Subgroup, Link, View, Text, Navbar, Separator, Navbar

template_dir = os.path.abspath('app/templates')

app = Flask(__name__, template_folder=template_dir)
nav = Nav(app)

nav.register_element('my_navbar', Navbar(
	'thenav',
	View('Home', 'index'),
	View('Organisation', 'organisation'),
    View('Contacts', 'contacts'),
    View('Analytics', 'analytics')))

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/organisation')
def organisation():
	return render_template('organisation.html')

@app.route('/contacts')
def contacts():
	return render_template('contacts.html')

@app.route('/analytics')
def analytics():
	return render_template('analytics.html')

if __name__ == '__main__':
	app.run(debug=True)