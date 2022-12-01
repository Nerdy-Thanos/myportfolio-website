import random
from ..companies_house.pdf_filings.fetch_pdf_filings import extract_filings_documents
from ..companies_house.pdf_filings.random import random_company_list
from . import create_app
from flask import render_template,request

app = create_app()

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/ParseFilingsDocuments",methods=["GET","POST"])
def ParseFilingsDocuments():
    if request.method=="POST":
        company_number=None
        if request.form["submit"]=="single":
            company_number = request.form.get("cn")
        if request.form["submit"]=="random":
            company_number=random.choice(random_company_list)
        filings_data = extract_filings_documents(company_number)
        return render_template('filings_table.html',  tables=[filings_data.to_html(classes='data')], titles=filings_data.columns.values)
    return render_template("filings.html")

@app.route("/DownloadFilingPDF")
def DownloadFilingPDF():
    return None

if __name__=="__main__":
    app.run()