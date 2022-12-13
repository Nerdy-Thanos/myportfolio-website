import base64
import random
import time
from ..mask_detection.test import load_models, recognise_mask
from ..song_bot.fetch_data import make_dataset
from ..song_bot.load_and_predict import load_saved_model, predict_next_words
from sys import stdout
from ..song_bot.train import model_architecture, train_model
import logging
from .helper_functions import clean_output, readb64
from ..companies_house.pdf_filings.fetch_pdf_filings import extract_filings_documents
from ..companies_house.pdf_filings.random import random_company_list
from . import create_app
from flask import render_template,request, send_from_directory, redirect, url_for
import cv2
from flask_socketio import SocketIO, emit
from engineio.payload import Payload
from threading import Thread
import cmake

app = create_app()

app.logger.addHandler(logging.StreamHandler(stdout))
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

@socketio.on('catch-frame')
def catch_frame(data):

	emit('response_back', data)  

@socketio.on('image')
def image(data_image):
	time.sleep(0.5)
	read_thread = Thread(target=readb64, args=(data_image,))
	load_thread = Thread(target=load_models, args=())

	read_thread.start()
	load_thread.start()

	frame = (readb64(data_image))
	
	face_detection_model, mask_detection_model = load_models()

	predict_thread = Thread(target=recognise_mask, args=(frame, face_detection_model, mask_detection_model, ))
	predict_thread.start()
	predict_thread.join()

	output_frame = recognise_mask(frame, face_detection_model, mask_detection_model)
	imgencode = cv2.imencode('.jpeg', output_frame,[cv2.IMWRITE_JPEG_QUALITY,40])[1]

	# base64 encode
	stringData = base64.b64encode(imgencode).decode('utf-8')
	b64_src = 'data:image/jpeg;base64,'
	stringData = b64_src + stringData

	# emit the frame back
	emit('response_back', stringData)
	
if __name__=="__main__":
	socketio.run(processes=8)