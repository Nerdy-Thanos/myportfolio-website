from .fetch_data import make_dataset
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Bidirectional
from tensorflow.keras.callbacks import ModelCheckpoint
import os

def model_architecture(max_sequence_len, total_words):

    model = Sequential()
    model.add(Embedding(total_words, 64, input_length=max_sequence_len-1))
    model.add(Bidirectional(LSTM(20)))
    model.add(Dense(total_words, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

def train_model(model, input_sequences, one_hot_labels):

    checkpoint_path = "training_1/cp.ckpt"
    checkpoint_dir = os.path.dirname(checkpoint_path)
    cp_callback = ModelCheckpoint(filepath=checkpoint_path,
                                                    save_weights_only=True,
                                                    verbose=1)

    model.fit(input_sequences, one_hot_labels, batch_size=64 ,epochs=100, verbose=1, callbacks=[cp_callback],)
    model.save('maroon5.h5')

def load_latest_model_weights(model):
    checkpoint_path = "training_1/cp.ckpt"
    checkpoint_dir = os.path.dirname(checkpoint_path)
    latest_cpkt = tf.train.latest_checkpoint(checkpoint_dir)
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    latest_model = model.load_weights(checkpoint_path)
    return latest_model

    