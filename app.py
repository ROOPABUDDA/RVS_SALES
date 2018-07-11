import os
from flask import Flask, render_template, flash, request, session, abort
from app.main.organisationform import OrganisationSearchForm
from app.main.contacts import contactSearchForm


template_dir = os.path.abspath('app/templates')
static_path = os.path.abspath('app/static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_path)
app.secret_key = 'development key'

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('home.html')


@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()


@app.route("/dashboard")
def dash():
    return render_template("dashboard.html")

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()


@app.route('/organisation')
def organisation():
    form = OrganisationSearchForm()
    return render_template('organisation.html', form=form)


@app.route('/contacts')
def contacts():
	form = contactSearchForm()
	return render_template('contacts.html', form=form)


@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

@app.route('/companyname')
def companyname():
    return render_template('companyname.html')

@app.route('/submit_organisation')
def submit_organisation():
	print("sample text print")
	forward_message = "Moving Forward..."
	return render_template('index.html', message=forward_message)


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
     app.run(debug=True,host='0.0.0.0', port=4000)
    # app.run(debug=True) 