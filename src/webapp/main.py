import random
from ..song_bot.fetch_data import make_dataset
from ..song_bot.load_and_predict import load_saved_model, predict_next_words
from sys import stdout
from ..song_bot.train import model_architecture, train_model
from logging import StreamHandler
from .helper_functions import clean_output
from ..companies_house.pdf_filings.fetch_pdf_filings import extract_filings_documents
from ..companies_house.pdf_filings.random import random_company_list
from . import create_app
from flask import render_template,request, send_from_directory, redirect, url_for
from flask_socketio import SocketIO
from engineio.payload import Payload

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
	
if __name__=="__main__":
	socketio.run(processes=8)