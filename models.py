from flask.ext.sqlalchemy import SQLAlchemy
from manage import db
from sqlalchemy.orm import defer, undefer
from sqlalchemy import func,text,and_	
import csv
from flask import Flask, make_response  


class org(db.Model):
	"""docstring forxcrg"""
	org_id = db.Column(db.Integer, primary_key=True)
	org_name = db.Column(db.VARCHAR(500), nullable=True)
	org_website = db.Column(db.VARCHAR(500),nullable=True)
	org_description = db.Column(db.VARCHAR(500),nullable=True)
	org_primaryindustry = db.Column(db.VARCHAR(500),nullable=True)
	org_secondaryindustry = db.Column(db.VARCHAR(500),nullable=True)
	org_revenue = db.Column(db.Integer,nullable=True)
	itbudget = db.Column(db.Integer,nullable=True)
	hq_address = db.Column(db.VARCHAR(500),nullable=True)
	hq_city = db.Column(db.VARCHAR(250),nullable=True)
	hq_state = db.Column(db.VARCHAR(250),nullable=True)
	hq_zipcode = db.Column(db.VARCHAR(250),nullable=True)
	hq_county = db.Column(db.VARCHAR(250),nullable=True)
	hq_country = db.Column(db.VARCHAR(250),nullable=True)
	year_founded = db.Column(db.Integer,nullable=True)
	org_technologies = db.Column(db.VARCHAR(500),nullable=True)
	related_case_study = db.Column(db.VARCHAR(500),nullable=True)
	org_tag = db.Column(db.VARCHAR(500),nullable=True)

	def __init__(self, org_name,org_website,org_description,org_primaryindustry,org_secondaryindustry,org_revenue,itbudget,hq_address,hq_city,hq_state,hq_zipcode,hq_county,hq_country,year_founded,org_technologies,related_case_study,org_tag):
				# def __init__(self,args):
		# super(ClassName, self).__init__()
		# self.arg = arg
		self.org_name = org_name
		self.org_website =org_website
		self.org_description = org_description
		self.org_primaryindustry = org_primaryindustry
		self.org_secondaryindustry = org_secondaryindustry
		self.org_revenue = org_revenue
		self.itbudget = itbudget
		self.hq_address = hq_address
		self.hq_city = hq_city
		self.hq_state = hq_state
		self.hq_zipcode = hq_zipcode
		self.hq_county =hq_county
		self.hq_country = hq_country
		self.year_founded = year_founded
		self.org_technologies =org_technologies
		self.related_case_study =related_case_study
		self.org_tag = org_tag


class employeecontact(db.Model):

	"""docstring for employeecontact"""
	emp_id = db.Column(db.Integer, primary_key=True)
	emp_org_id = db.Column(db.Integer, db.ForeignKey('org.org_id'),
        nullable=False)
	first_name = db.Column(db.VARCHAR(250),nullable=True)
	last_name = db.Column(db.VARCHAR(250),nullable=True)
	emp_designation = db.Column(db.VARCHAR(250),nullable=True)
	emp_mailid = db.Column(db.VARCHAR(250),nullable=True)
	emp_linkedin = db.Column(db.VARCHAR(250),nullable=True)
	emp_phonnumber = db.Column(db.VARCHAR(250),nullable=True)
	emp_directphone = db.Column(db.VARCHAR(250),nullable=True)

	def __init__(self,emp_org_id, first_name,last_name,emp_designation,emp_mailid,emp_linkedin,emp_phonnumber,emp_directphone):
		# super(employeecontact, self).__init__()
		# self.arg = arg
		
		self.emp_org_id = emp_org_id
		self.first_name = first_name
		self.last_name = last_name
		self.emp_designation = emp_designation
		self.emp_mailid = emp_mailid
		self.emp_linkedin = emp_linkedin
		self.emp_phonnumber = emp_phonnumber
		self.emp_directphone = emp_directphone


		


def create_sqlalchemy():
	db.create_all()



def insert_into_db(orgname,orgwebsite,orgdescription,orgprimaryindustry,orgsecondaryindustry,orgrevenue,itbudget,hqaddress,hqcity,hqstate,hqzipcode,hqcounty,hqcountry,yearfounded,technologies,relatedcasestudy,orgtag,fistname,lastname,designation,emailid,linkedinid,phonenumber,diretphonenumer):
	
	# exists = db.session.query(org.org_id).filter_by(org_name=orgname).scalar() is not None
	# import pdb; pdb.set_trace()
	empPerOrgCount = 0
	org_exist = org.query.filter_by(org_name=orgname).count()
	print(org_exist)
	if org_exist ==0:
		org_import = org(orgname,orgwebsite,orgdescription,orgprimaryindustry,orgsecondaryindustry,orgrevenue,itbudget,hqaddress,hqcity,hqstate,hqzipcode,hqcounty,hqcountry,yearfounded,technologies,relatedcasestudy,orgtag)
		db.session.add(org_import)
		
	employee_org_id = db.session.query(org.org_id).filter_by(org_name=orgname).first()
	print(employee_org_id)
	emp_exist = employeecontact.query.filter_by(emp_mailid=emailid).count()
	print(emp_exist)
	if emp_exist == 0:
		print("inside emp count")
		emp_contact = employeecontact(employee_org_id,fistname,lastname,designation,emailid,linkedinid,phonenumber,diretphonenumer)
		db.session.add(emp_contact)
	db.session.commit()
	return True

#get all details from database
def getOrgAndEmpCount():
	orgAndEmpCount = {}
	orgCount = db.session.query(org).count()
	empCount = db.session.query(employeecontact).count()
	orgAndEmpCount['orgCount'] = orgCount
	orgAndEmpCount['empCount'] = empCount

	orgIds  =  db.session.query(org.org_id).all()
	
	org_dict = []
	for orgId in orgIds:
		# print('================',orgId[0])
		empPerOrgCount = employeecontact.query.filter_by(emp_org_id = orgId).count()

		org_dict.append( {'empPerOrgCount':empPerOrgCount,
							'orgDetails':org.query.get(orgId)
							}
							)
		
	return org_dict, orgCount, empCount




def getOrgEmpDetails(orgname):
	orgEmpDetails = {}
	employee_org_id = db.session.query(org.org_id).filter_by(org_name=orgname).first()
	orgDetails = org.query.get(employee_org_id)
	empDetails = employeecontact.query.filter_by(emp_org_id = orgDetails.org_id).all()
	totalEmpCount = employeecontact.query.filter_by(emp_org_id = orgDetails.org_id).count()
	orgEmpDetails['orgDetails'] = orgDetails
	orgEmpDetails['empDetails'] = empDetails
	orgEmpDetails['totalEmpCount'] = totalEmpCount
	return orgEmpDetails

def getOrgDetails(orgIds):
	orgDetails = [];
	for orgId in orgIds:
		orgDetail = org.query.get(orgId)
		orgDetails.append(orgDetail)
	return orgDetails

def writeToCSV(orgDetails):
	orgData = []
	myFields = ['#', 'Company Name', 'Wesite','Description', 'Primary Industry' , 'Secondary Industry', 'Revenue(mn)', 'IT Budget' , 'HQ Address', 'HQ City', 'HQ State', 'HQ Zipcode' , 'HQ County','HQ Country','Tag']
	for orgDetail in orgDetails:
		orgData.append({ 'Company Name': orgDetail.org_name, 'Wesite': orgDetail.org_website,
			'Description': orgDetail.org_description, 'Primary Industry': orgDetail.org_primaryindustry ,
			 'Secondary Industry': orgDetail.org_secondaryindustry, 'Revenue(mn)': orgDetail.org_revenue, 
			 'IT Budget': orgDetail.itbudget , 'HQ Address': orgDetail.hq_address, 'HQ City': orgDetail.hq_city,
			  'HQ State': orgDetail.hq_state, 'HQ Zipcode': orgDetail.hq_zipcode , 'HQ County': orgDetail.hq_county,
			  'HQ Country': orgDetail.hq_country,'Year (Founded)':orgDetail.year_founded,'Technologies':orgDetail.org_technologies ,
			  'Related Case Study':orgDetail.related_case_study,
			  'Tag': orgDetail.org_tag})
	# print(orgData)
	return orgData

def orgData():
	# res = org.query.filter(org.org_name.like(keyword + '%')).all()
	res = org.query.all()
	return res

def empData(orgName):
	orgData =org.query.filter_by(org_name=orgName).first()
	orgId = orgData.org_id
	res = employeecontact.query.filter_by(emp_org_id = orgId).all()
	return res

def getMaxAndMinRevenue():
	maxMinReveue = {}
	maxRevenue = db.session.query(db.func.max(org.org_revenue)).scalar()
	minRevenue = db.session.query(db.func.min(org.org_revenue)).scalar()
	maxMinReveue['maxRevenue'] = maxRevenue
	maxMinReveue['minRevenue'] = minRevenue
	return maxMinReveue

def searchData(formData):
	orgName = formData['filterOrg']
	industryList = formData.getlist('filterIndustry')
	regionList = formData.getlist('filterRegion')
	minRevenue = formData['filterMinVal']
	maxRevenue = formData['filterMaxVal']
	tags = formData['tags']
	conditions = []
	if orgName:
		conditions.append(org.org_name.like("%" + orgName + "%") )
	if industryList:
		conditions.append(org.org_primaryindustry.in_(industryList))
	if regionList:
		conditions.append(org.hq_country.in_(industryList))
	if minRevenue:
		conditions.append(org.org_revenue>=minRevenue)
	if maxRevenue:
		conditions.append(org.org_revenue<=maxRevenue)
	if tags:
		conditions.append(org.org_tag.like("%" + tags + "%") )
	orgData = org.query.filter(and_(*conditions)).all()
	orgIds = []
	for orgID in orgData:
		print('dataaaaaaaaaaaa',orgID.org_id)
		orgIds.append(orgID.org_id)
	# orgData = org.query.filter(and_(org.org_name.like("%" + orgName + "%") , org.org_primaryindustry.in_(industryList))).all()
	org_dict = []
	for orgId in orgIds:
		empPerOrgCount = employeecontact.query.filter_by(emp_org_id = orgId).count()

		org_dict.append( {'empPerOrgCount':empPerOrgCount,
							'orgDetails':org.query.get(orgId)
							}
							)
	print('xxxxxxxxxxxxxxxxxx',org_dict)
	return org_dict
		
    	

    	

    
	

	  
    
