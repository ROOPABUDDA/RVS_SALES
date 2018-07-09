from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField

from wtforms import validators, ValidationError

class OrganisationSearchForm(FlaskForm):
   org = TextField("Organisation",[validators.Required("Please enter organisation name.")])
   revenue = TextField("Revenue")
   employee = TextField("Employee")
   region = TextField("Region")
   exist_customer = TextField("Existing Customer")
   industry = SelectField("Industry",choices = [('Sel','Select'),
      ('IT', 'Information Technology'),
      ('insurance', 'Insurance'),
      ('agriculture','Agriculture')])
