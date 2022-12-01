from . import create_app
from flask import render_template

app = create_app()

@app.route("/")
def hello():
    return render_template("index.html")

if __name__=="__main__":
    app.run()