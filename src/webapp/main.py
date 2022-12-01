from src.companies_house.pdf_filings.fetch_pdf_filings import extract_filings_documents

from . import create_app
from flask import render_template

app = create_app()

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/ParseFilingsDocuments",methods=["GET","POST"])
def ParseFilingsDocuments():
    company_number = None
    filings_data = extract_filings_documents(company_number)
    return render_template("filings.html")

if __name__=="__main__":
    app.run()