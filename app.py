import os
from flask import Flask, render_template
from app.main.organisationform import OrganisationSearchForm

template_dir = os.path.abspath('app/templates')

app = Flask(__name__, template_folder=template_dir)
app.secret_key = 'development key'


@app.route('/')
def index():
	# keep login here
	return render_template('login.html')


@app.route('/organisation')
def organisation():
    form = OrganisationSearchForm()
    return render_template('organisation.html', form=form)


@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


@app.route('/analytics')
def analytics():
    return render_template('analytics.html')


if __name__ == '__main__':
    app.run(debug=True)