from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField, StringField

from wtforms import validators, ValidationError


class contactSearchForm(FlaskForm):
   #emp_name = TextField("Name")
   emp_name = StringField('emp_name', render_kw={"placeholder": "Full Name"})
   emp_job_title = StringField('emp_organisation', render_kw={"placeholder": "Job Title"})
   emp_company_name = StringField('emp_designation', render_kw={"placeholder": "Company Name"})
   emp_job_function = StringField('emp_location', render_kw={"placeholder": "Job Functio"})
   emp_mgmt_level = StringField('emp_linkedin', render_kw={"placeholder": "Management Level"})
   emp_industry = StringField('emp_decisionpower', render_kw={"placeholder": "Industry"})
   emp_geography = StringField('emp_decisionpower', render_kw={"placeholder": "Geography"})


   submit_search = SubmitField("Search")


