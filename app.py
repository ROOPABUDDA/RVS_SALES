"""import os
from flask import Flask, render_template

template_dir = os.path.abspath('SALES_CRM/templates')

app = Flask(__name__, template_folder=template_dir)

@app.route('/')
def welcome():
    return render_template('base.html')

if __name__ == '__main__':
    app.run(debug=True)
"""
from manage import application
if __name__ == "__main__":
    application.run(debug=True)
