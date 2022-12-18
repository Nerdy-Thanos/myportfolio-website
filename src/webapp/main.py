
from src.stock.pred import clean_static_dir, daily_change, fetch_data, multi_variate_analysis, plot_all_stocks, plot_volume
from ..gan.gen import generate_image
from ..song_bot.fetch_data import make_dataset
from ..song_bot.load_and_predict import load_saved_model, predict_next_words
from sys import stdout
from ..song_bot.train import model_architecture, train_model
from logging import StreamHandler
from . import create_app
from flask import render_template,request, send_from_directory, redirect, url_for
from flask_socketio import SocketIO
from engineio.payload import Payload
from base64 import b64encode
from io import BytesIO



app = create_app()

app.logger.addHandler(StreamHandler(stdout))
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
Payload.max_decode_packets = 2048
socketio = SocketIO(app)


@socketio.on('connect', namespace='/test')
def test_connect():
	app.logger.info("client connected")

@app.route("/")
def hello():
	return render_template("index.html")

@app.route("/DownloadResume", methods=["GET"])
def DownloadResume():
	return send_from_directory("static","resume/Vignesh_Resume.pdf", as_attachment=True, download_name="Vignesh_Resume.pdf")

@app.route("/TrainSongBot")
def TrainSongBot():
	max_sequence_len, total_words, input_sequences, one_hot_labels = make_dataset()
	model = model_architecture(max_sequence_len=max_sequence_len, total_words=total_words) 
	train_model(model, input_sequences=input_sequences, one_hot_labels=one_hot_labels)
	return "Model Trained"

@app.route("/GenerateImages", methods=["GET","POST"])
def GenerateImages():
	image=None
	if request.method=="POST":
		image = generate_image()
		image = image.resize((640,480))
		image_io = BytesIO()
		image.save(image_io, 'PNG')
		dataurl = 'data:image/png;base64,' + b64encode(image_io.getvalue()).decode('ascii')
		return render_template("image.html", image=dataurl)
	return render_template("gan.html")

@app.route("/SongBot", methods=["GET", "POST"])
def SongBot():
	artist=None
	if request.method=="POST":
		artist = request.form["artist"]
		num_words = request.form["word"]
		msg = request.form["msg"]
		return redirect(url_for("SongBotPredict", artist=artist, msg=msg, num_words=num_words))
	return render_template("chatbot.html", artist=artist)

@app.route("/<artist>/SongBotPredict", methods=["GET","POST"])
def SongBotPredict(artist):
	userText = request.args.get('msg')
	num_words = request.args.get('num_words')
	loaded_model = load_saved_model(artist)
	lyrics = predict_next_words(loaded_model, artist, userText, int(num_words))
	return render_template("chatbot_predict.html",lyrics=lyrics, artist=artist)

@app.route("/StockEDA", methods=["GET","POST"])
def StockEDA():
	if request.method=="POST":
		clean_static_dir()
		stock = request.form["stock"]
		start = request.form.get("start")
		end = request.form.get("end")
		data = fetch_data(stock, start, end)
		plot_all_stocks(data, stock)
		plot_volume(data, stock)
		multi_variate_analysis(data)
		daily_change(data)
		return redirect(url_for("StockEDAResults"))
	return render_template("stock.html")

@app.route("/StockEDAResults", methods=["GET","POST"])
def StockEDAResults():
	return render_template("stock_results.html")
	

if __name__=="__main__":
	socketio.run(processes=8)