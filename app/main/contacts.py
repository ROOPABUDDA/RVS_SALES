from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField, StringField

from wtforms import validators, ValidationError


class contactSearchForm(FlaskForm):
   #emp_name = TextField("Name")
   emp_name = StringField('emp_name', render_kw={"placeholder": "Name"})
   emp_organisation = StringField('emp_organisation', render_kw={"placeholder": "Organisation"})
   emp_designation = StringField('emp_designation', render_kw={"placeholder": "Designation"})
   emp_location = StringField('emp_location', render_kw={"placeholder": "Location"})
   emp_linkedin = StringField('emp_linkedin', render_kw={"placeholder": "Linkedin"})
   emp_decisionpower = StringField('emp_decisionpower', render_kw={"placeholder": "Decision Power"})

   submit_search = SubmitField("Search")


