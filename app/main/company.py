from flask.ext.sqlalchemy import SQLAlchemy
from manage import db
from sqlalchemy.orm import defer, undefer
from sqlalchemy import func
from models import employeecontact,org

def getOrgEmpDetails(orgname):
	orgEmpDetails = {}
	employee_org_id = db.session.query(org.org_id).filter_by(org_name=orgname).first()
	orgDetails = org.query.get(employee_org_id)
	empDetails = employeecontact.query.filter_by(emp_org_id = orgDetails.org_id).all()
	totalEmpCount = employeecontact.query.filter_by(emp_org_id = orgDetails.org_id).count()
	orgEmpDetails['orgDetails'] = orgDetails
	orgEmpDetails['empDetails'] = empDetails
	orgEmpDetails['totalEmpCount'] = totalEmpCount
	print("inside company.py")
	return orgEmpDetails