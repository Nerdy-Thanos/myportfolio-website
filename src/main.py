from ..webapp import create_app

app = create_app()

@app.route("/")
def home():
    print("Hello World!")
    
if __name__== "__main__":
    app.run(port=5000)