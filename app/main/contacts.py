from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField

from wtforms import validators, ValidationError


class contactSearchForm(FlaskForm):
   emp_name = TextField("Name")
   emp_organisation = TextField("Organisation")
   emp_designation = TextField("Designation")
   emp_location = TextField("Location")
   emp_linkedin = TextField("Linkedin")
   emp_decisionpower = TextField("Decision Power")

   submit_search = SubmitField("Search")


