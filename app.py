import os
from flask import Flask, render_template, flash, request, session, abort, redirect,url_for, send_from_directory,make_response,Response 
from werkzeug.utils import secure_filename
import pandas as pd
import glob
from flaskext.mysql import MySQL
from pandas.io import sql
from app.main.organisationform import OrganisationSearchForm
from app.main.contacts import contactSearchForm
import xlrd
from flask_jsglue import JSGlue
from pandas import ExcelWriter
from pandas import ExcelFile
from flask.ext.sqlalchemy import SQLAlchemy
from models import create_sqlalchemy
from models import insert_into_db,getOrgAndEmpCount,getOrgEmpDetails,getOrgDetails,writeToCSV,orgData,empData,getMaxAndMinRevenue,searchData
from flask import Flask, make_response 
import csv
import json
# import StringIO 
# from app.main.company import getOrgEmpDetails

from flask.ext.login import LoginManager, login_required, login_user, \
    logout_user, current_user, UserMixin
from requests_oauthlib import OAuth2Session
from requests.exceptions import HTTPError


template_dir = os.path.abspath('app/templates')
static_path = os.path.abspath('app/static')
UPLOAD_FOLDER = 'D:/Python/Projects/RVS_Sales_CRM/uploads'
ALLOWED_EXTENSIONS = set(['csv', 'xlsx', 'xls'])

app = Flask(__name__, template_folder=template_dir, static_folder=static_path)
app.secret_key = 'development key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'saledatabase'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

database = MySQL()

database.init_app(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/saledatabase'
# db = SQLAlchemy(app)

# jsglue = JSGlue(app)

file_type = "D:/Python/Projects/RVS_Sales_CRM/uploads/*.xls"

file_list = []
col_name = []
file_name = ""

# Code to read data from excel file into pandas:

#file_name = file_name.split("/")[-1].split(".")[0]

def import_data_to_db(filename):
    # import pdb; pdb.set_trace()
    df = pd.read_excel(filename)
    df = df.astype(object).where(pd.notnull(df), None)
    for index, row in df.iterrows():

        insert_into_db(row['Company Name'],row['Company Website'],row['Company Description'],row['Primary Industry'],row['Secondary Industry'],row['Revenue (mn)'],row['IT Budget (mn)'],
            row['HQ Address'],row['HQ City'],row['HQ State'],row['HQ ZipCode'],row['HQ County'],row['HQ Country'], row['Year (Founded)'],row['Technologies'],row['Related Case Study'],row['Tags'], 
            row['First Name'], row['Last Name'], row['Job Title'], row['Email Address'], row['LinkedIn Profile '],
            row['Phone Number'],row['Direct Phone'])
        #     insert_into_org = "INSERT INTO org(org_name,org_website,org_description,org_primaryindustry,org_secondaryindustry,org_revenue,itbudget,hq_address,hq_city,hq_state,hq_zipcode,hq_country,year_founded) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"


def getfile(filename):
    global file_name
    global dataframe1
    for each in glob.glob(file_type):
        file_list.append(each)
    print("printing filelist in get file")
    print(file_list)
    for each in file_list:
        file_name = each.split("/")[-1].split(".")[0]
        dataframe1 = pd.read_excel(each)
        col_name.append(dataframe1.columns.values)
        print(col_name)
        print(col_name)

def db_colname(pandas_colname):
    """Convert pandas column name to a DBMS column name.
        TODO: deal with name length restrictions, esp for Oracle
    """
    colname = pandas_colname.replace(' ', '_').strip()
    return colname


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_table(filename):
    global file_name
    print(filename)
    try:
        print("testing")
        print(file_name)
        table_name = file_name
        field_name_list = col_name[0]
        field_list = []
        for field in field_name_list:
            field_list.append(field + " VARCHAR(50) DEFAULT NULL")
        field_query = " ( " + ", ".join(field_list) + " ) "
        create_table_query = 'CREATE TABLE `' + table_name + '`' + 'IF NOT EXISTS' + field_query
        conn = database.connect()
        cursor = conn.cursor()
        cursor.execute(create_table_query)
        cursor.close()
        return "Table: " + table_name + " created successfully"
    except Exception as e:
        return str(e)
def insert_into_table(filename):
    global dataframe1
    print("filename")
    print(filename)
    print(dataframe1)
    return True



@app.route('/uploadtodb', methods=['POST'])
def importFileToDb():

    # import pdb; pdb.set_trace()
    print("inside")
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            create_sqlalchemy()
            
            import_data_to_db(file)
        return redirect(url_for('dash'))

    return render_template('dashboard.html')


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('dashboard.html')


@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
        return redirect(url_for('dash'))
    else:
        flash('wrong password!')
    return home()


@app.route("/dashboard",methods = ['GET', 'POST'])
def dash():
    
    OrgDetails, orgCount, empCount = getOrgAndEmpCount()
    print(OrgDetails)
    orgDetails = orgData()
    IndustryList = []
    for industry in orgDetails:
        IndustryList.append(industry.org_primaryindustry)
    uniqueIndustryList = list(set(IndustryList))
    geographyList = []
    for geography in orgDetails:
        geographyList.append(geography.hq_country)
    uniqueCountryList = list(set(geographyList))
    revenue = getMaxAndMinRevenue()
    if request.method == 'POST':
        formData = request.form
        searchRes = searchData(formData)
        print(type(searchRes))
        if len(searchRes) == 0:
            print("No result found!!")
            OrgDetails = searchRes
        else:
            print('ppppppp',searchRes)
            OrgDetails = searchRes
    return render_template("dashboard.html", recCount  = OrgDetails,
        orgCount = orgCount,empCount =empCount,
        industryList=uniqueIndustryList ,geographyList = uniqueCountryList, 
        revenue = revenue
     )

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()



@app.route('/organisation',methods = ['GET', 'POST'])
def organisation():
    OrgDetails, orgCount, empCount = getOrgAndEmpCount()
    orgDetails = orgData()
    IndustryList = []
    for industry in orgDetails:
        IndustryList.append(industry.org_primaryindustry)
    uniqueIndustryList = list(set(IndustryList))
    geographyList = []
    for geography in orgDetails:
        geographyList.append(geography.hq_country)
    uniqueCountryList = list(set(geographyList))
    revenue = getMaxAndMinRevenue()
    if request.method == 'POST':
        formData = request.form
        print('org form---------------',formData)
        searchRes = searchData(formData)
        print(type(searchRes))
        if len(searchRes) == 0:
            print("No result found!!")
            OrgDetails = searchRes
        else:
            print('ppppppp',searchRes)
            OrgDetails = searchRes

    return render_template('organisation.html', recCount  = OrgDetails,orgCount = orgCount,empCount =empCount,
        industryList=uniqueIndustryList,geographyList = uniqueCountryList)


@app.route('/download' , methods=['POST'])
def download():
    orgIdStr = request.form['org_id']
    orgId = orgIdStr.split(",")
    orgDetails = getOrgDetails(orgId)
    orgList = []
    dataList = writeToCSV(orgDetails)
    df = pd.DataFrame(dataList)
    resp = make_response(df.to_csv())
    resp.headers["Content-Disposition"] = "attachment; filename=organization.csv"
    resp.headers["Content-Type"] = "text/csv"
    return resp
    return  redirect(url_for('organisation'))



@app.route('/contacts')
def contacts():
	form = contactSearchForm() 
	return render_template('contacts.html', form=form)


@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

@app.route('/companyname/?name:<orgname>')
def companyname(orgname):
    orgEmpDetails = getOrgEmpDetails(orgname)
    jobFunctions = empData(orgname)
    jobFunctionList = []
    for jobFunction in jobFunctions:
        jobFunctionList.append(jobFunction.emp_designation)
    uniqueJobFunctionList = list(set(jobFunctionList))
    return render_template('companyname.html' , orgEmpDetails = orgEmpDetails, jobFunctions = jobFunctionList)

@app.route('/getCompanyList')
def getCompanyList():
    # import pdb; pdb.set_trace()
    keyword = request.form.get('companyname')
    orgDetails = orgData()
    companyNames = []
    for company in orgDetails:
        companyNames.append(company.org_name)
    return Response(json.dumps(companyNames), mimetype='application/json')
    # return redirect(url_for('organisation'))

@app.route('/getIndustryList')
def getIndustryList():
    orgDetails = orgData()
    IndustryList = []
    for industry in orgDetails:
        IndustryList.append(industry.org_primaryindustry)
    print(IndustryList)
    return IndustryList

@app.route('/getGeographyList')
def getGeographyList():
    orgDetails = orgData()
    geographyList = []
    for geography in orgDetails:
        geographyList.append(geography.hq_country)
    return Response(json.dumps(geographyList), mimetype='application/json')

@app.route('/getEmployeeNames/<companyname>')
def getEmployeeNames(companyname):
    print(companyname)
    empDetails = empData(companyname)
    empNames = []
    for name in empDetails:
        empNames.append(name.first_name)
        empNames.append(name.last_name)
    return Response(json.dumps(empNames), mimetype='application/json')

@app.route('/getEmpDesignation/<companyname>')
def getEmpDesignation(companyname):
    empDetails = empData(companyname)
    empDes = []
    for designation in empDetails:
        empDes.append(designation.emp_designation)
    return Response(json.dumps(empDes), mimetype='application/json')


# @app.route('/getTags')
# def getGeographyList():
#     orgDetails = orgData()
#     tags = []
#     for tag in orgDetails:
#         tags.append(tag.org_tag)
#     return Response(json.dumps(tags), mimetype='application/json')




if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)
    # app.run(debug=True)