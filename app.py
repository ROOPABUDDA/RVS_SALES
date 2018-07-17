import os
from flask import Flask, render_template, flash, request, session, abort, redirect, send_from_directory
from werkzeug.utils import secure_filename
import pandas as pd
import glob
from flaskext.mysql import MySQL
from pandas.io import sql
from app.main.organisationform import OrganisationSearchForm
from app.main.contacts import contactSearchForm


template_dir = os.path.abspath('app/templates')
static_path = os.path.abspath('app/static')
UPLOAD_FOLDER = '/home/roopa/others/RVS/internals/RVS_SALES/uploads'
DOWNLOAD_FOLDER = '/home/roopa/others/RVS/internals/RVS_SALES/downloads'
ALLOWED_EXTENSIONS = set(['csv', 'xlsx', 'xls'])

app = Flask(__name__, template_folder=template_dir, static_folder=static_path)
app.secret_key = 'development key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MYSQL_DATABASE_USER'] = 'roopa'
app.config['MYSQL_DATABASE_PASSWORD'] = 'sathROO@315'
app.config['MYSQL_DATABASE_DB'] = 'dbtest2'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

database = MySQL()

database.init_app(app)

file_type = "/home/roopa/others/RVS/internals/RVS_SALES/uploads/*.xls"
test_file = "/home/roopa/others/RVS/internals/RVS_SALES/app/templates/test.html"
file_list = []
col_name = []
file_name = ""

# Code to read data from excel file into pandas:

#file_name = file_name.split("/")[-1].split(".")[0]

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

@app.route('/')
def login():
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

@app.route("/upload_file",methods=['POST'])
def upload_file():
    global dataframe1
    global file_name
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("store to database")
            #check this part if the below function is called
            getfile(filename)
            result = create_table(filename)
            print("inserting into db tabel now")

            # ............work her
            # parameters are filename and the global dataframe
            table_result = insert_into_table(file_name)
            #print(dataframe1)
            # insert_db(dataframe1)
            conn = database.connect()
            cursor = conn.cursor()
            # print(col_name)
            # for index, row in dataframe1.iterrows():
            #     print(index)
            #     print(row)
            # print(result)
            #dftest = dataframe1.iloc[:, 0:10]
            #print(dftest)
            #print(dataframe1.iloc[:, :])
            # redirect(url_for('create_table', filename=filename))
            # with open(test_file, 'w') as f:
            #     print("creating file here")
            #     f.write(dftest.to_html(classes='df'))

            return render_template('home.html')
            #"File uploaded successfully"
            # redirect(url_for('uploaded_file', filename=filename))

    return render_template('home.html')

@app.route('/organisation')
def organisation():
    form = OrganisationSearchForm()
    return render_template('organisation.html', form=form)

@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    global dataframe1
    global dftest

    form = contactSearchForm(request.form)
    if request.method == 'POST':
        # global dataframe1
        # global dftest
        contact_name = request.form['emp_name']
        contact_job_title = request.form['emp_job_title']
        contact_company_name = request.form['emp_company_name']
        contact_job_function = request.form['emp_job_function']
        contact_mgmt_level =request.form['emp_mgmt_level']
        contact_industry = request.form['emp_industry']
        contact_geography = request.form['emp_geography']
        print(contact_name)
        print(contact_job_title)
        # add code her to searc for specific column in the given dataframe
        #print(dataframe1.loc[dataframe1['HQ Country'] == contact_geography])
        #dataframe_search = dataframe1.loc[dataframe1['HQ Country'] == contact_geography]
        dataframe_search = dataframe1
        if(contact_name != ""):
            dataframe_search = dataframe1.loc[dataframe1['First Name'] == contact_name]

        if(contact_job_title != ""):
            dataframe_search = dataframe_search.loc[dataframe_search['Job Title'] == contact_job_title]

        if(contact_company_name != ""):
            dataframe_search = dataframe_search.loc[dataframe_search['Company Name'] == contact_company_name]

        if(contact_job_function != ""):
            dataframe_search = dataframe_search.loc[dataframe_search['Job Title'] == contact_job_title]

        if(contact_mgmt_level != ""):
            dataframe_search = dataframe_search.loc[dataframe_search['Job Title'] == contact_job_title]

        if(contact_industry != ""):
            dataframe_search = dataframe_search.loc[dataframe_search['Primary Industry'] == contact_industry]

        if(contact_geography != ""):
            dataframe_search = dataframe_search.loc[dataframe_search['HQ Country'] == contact_geography]

        dftest = dataframe_search.iloc[:, 0:10]
        print(dftest)

        with open(test_file, 'w') as f:
                print("creating file here")
                f.write(dftest.to_html(classes='df'))
    if request.method == 'PATCH':
        # global dataframe1
        # global dftest
        #download file here
        #with open(download_file,'w') as f:dataframe
        writer = pd.ExcelWriter(DOWNLOAD_FOLDER+'/output.xlsx')
        print("writer her is ")
        print(writer)
        dftest.to_excel(writer,'Sheet1')
        #return render_template('contacts.html', form=form)

    return render_template('contacts.html', form=form)


@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

@app.route('/companyname')
def companyname():
    return render_template('companyname.html')

@app.route('/home')
def home():
    return render_template('home.html')


"""
@app.route('/submit_organisation')
def submit_organisation():
    if request.method == 'POST':
      upload = request.form['nm']
      return redirect(url_for('success',name = user))
    print("sample text print")
    r = request.get_json() or {}
    print(r)

    forward_message = "Moving Forward..."
    return render_template('index.html', message=forward_message)
"""

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)
    # app.run(debug=True)
