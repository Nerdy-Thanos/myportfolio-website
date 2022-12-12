import base64
from io import StringIO
import io
import random
from PIL import Image
from ..face_mask.camera import Camera
from ..face_mask.camera_flip import Flip
from numpy import array
from ..face_mask.test import load_models, recognise_mask
from ..song_bot.fetch_data import make_dataset
from ..song_bot.load_and_predict import load_saved_model, predict_next_words
from sys import stdout
from ..song_bot.train import model_architecture, train_model
import logging
from .helper_functions import clean_output
from ..companies_house.pdf_filings.fetch_pdf_filings import extract_filings_documents
from ..companies_house.pdf_filings.random import random_company_list
from . import create_app
from flask import render_template,request, send_from_directory, redirect, url_for, Response
import cv2
import time
from imutils.video import VideoStream
from flask_socketio import SocketIO, emit

app = create_app()

app.logger.addHandler(logging.StreamHandler(stdout))
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
socketio = SocketIO(app)
camera = Camera(Flip())

@socketio.on('connect', namespace='/test')
def test_connect():
	app.logger.info("client connected")

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

@app.route("/DownloadFilingPDF", methods=["GET"])
def DownloadFilingPDF():
	return send_from_directory("static","output/temp.pdf", as_attachment=True,download_name="filing_doc.pdf")

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

@app.route("/FaceMasks")
def FaceMasks():
	return render_template("mask.html")

@socketio.on('image')
def image(data_image):
	sbuf = StringIO()
	sbuf.write(data_image)

	# decode and convert into image
	b = io.BytesIO(base64.b64decode(data_image))
	pimg = Image.open(b)

	## converting RGB to BGR, as opencv standards
	frame = cv2.cvtColor(array(pimg), cv2.COLOR_RGB2BGR)
	## converting RGB to BGR, as opencv standards
	face_detection_model, mask_detection_model = load_models()

	output_frame = recognise_mask(frame, face_detection_model, mask_detection_model)

	# base64 encode
	stringData = base64.b64encode(output_frame).decode('utf-8')
	b64_src = 'data:image/jpg;base64,'
	stringData = b64_src + stringData

	# emit the frame back
	emit('response_back', stringData)

if __name__=="__main__":
	socketio.run()