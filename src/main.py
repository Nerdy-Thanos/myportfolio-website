from .webapp import create_app

app = create_app()

@app.route("/")
def hello():
    return "Hello"

if __name__=="__main__":
    app.run()