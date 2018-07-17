from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField, StringField

from wtforms import validators, ValidationError


class contactSearchForm(FlaskForm):
   #emp_name = TextField("Name")
   emp_name = StringField('emp_name', render_kw={"placeholder": "Full Name"})
   emp_job_title = StringField('emp_job_title', render_kw={"placeholder": "Job Title"})
   emp_company_name = StringField('emp_company_name', render_kw={"placeholder": "Company Name"})
   emp_job_function = StringField('emp_job_function', render_kw={"placeholder": "Job Function"})
   emp_mgmt_level = StringField('emp_mgmt_level', render_kw={"placeholder": "Management Level"})
   emp_industry = StringField('emp_industry', render_kw={"placeholder": "Industry"})
   emp_geography = StringField('emp_geography', render_kw={"placeholder": "Geography"})


   submit_emp_search = SubmitField("Search")
   submit_emp_download = SubmitField("Import")


