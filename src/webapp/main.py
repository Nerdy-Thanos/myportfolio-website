import random

from ..chatbot.viggy_bot import create_bot
from .helper_functions import clean_output
from ..companies_house.pdf_filings.fetch_pdf_filings import extract_filings_documents
from ..companies_house.pdf_filings.random import random_company_list
from . import create_app
from flask import render_template,request, send_from_directory

app = create_app()

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/ParseFilingsDocuments",methods=["GET","POST"])
def ParseFilingsDocuments():
    clean_output()
    if request.method=="POST":
        company_number=None
        if request.form["submit"]=="single":
            company_number = request.form.get("cn")
        if request.form["submit"]=="random":
            company_number=random.choice(random_company_list)
        filings_data = extract_filings_documents(company_number)
        return render_template('filings_table.html',  tables=[filings_data.to_html(classes='styled-table')], titles=filings_data.columns.values)
    return render_template("filings.html")

@app.route("/ViggyBotHome")
def ViggyBotHome():
    return render_template("chatbot.html")

@app.route("/ViggyBotResponse")
def ViggyBotResponse():
    bot = create_bot()
    user_text = request.args.get("msg")
    response = bot.get_response(user_text)
    return str(response)

@app.route("/DownloadFilingPDF", methods=["GET"])
def DownloadFilingPDF():
    return send_from_directory("static","output/temp.pdf", as_attachment=True,download_name="filing_doc.pdf")

@app.route("/DownloadResume", methods=["GET"])
def DownloadResume():
    return send_from_directory("static","resume/Vignesh_Resume.pdf", as_attachment=True, download_name="Vignesh_Resume.pdf")


if __name__=="__main__":
    app.run()