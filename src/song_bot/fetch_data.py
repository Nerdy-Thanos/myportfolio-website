import tensorflow as tf

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Other imports for processing data
import string
import numpy as np
import pandas as pd

def tokenize_corpus(corpus, num_words=-1):
    # Fit a Tokenizer on the corpus
    if num_words > -1:
        tokenizer = Tokenizer(num_words=num_words)
    else:
        tokenizer = Tokenizer()
    tokenizer.fit_on_texts(corpus)
    return tokenizer

def create_lyrics_corpus(dataset, field):
    # Remove all other punctuation
    dataset[field] = dataset[field].str.replace('[{}]'.format(string.punctuation), '')
    # Make it lowercase
    dataset[field] = dataset[field].str.lower()
    # Make it one long string to split by line
    lyrics = dataset[field].str.cat()
    corpus = lyrics.split('\n')
    # Remove any trailing whitespace
    for l in range(len(corpus)):
        corpus[l] = corpus[l].rstrip()
    # Remove any empty lines
    corpus = [l for l in corpus if l != '']

    return corpus


def make_dataset():

    # Read the dataset from csv - just first 10 songs for now
    dataset = pd.read_csv('src/song_bot/archive/csv/Maroon5.csv', dtype=str).sample(20)
    # Create the corpus using the 'text' column containing lyrics
    corpus = create_lyrics_corpus(dataset, 'Lyric')
    # Tokenize the corpus
    tokenizer = tokenize_corpus(corpus)

    total_words = len(tokenizer.word_index) + 1

    input_sequences, max_sequence_len, one_hot_labels = preprocess_corpus(corpus, tokenizer, total_words)

    return max_sequence_len, total_words, input_sequences, one_hot_labels

def preprocess_corpus(corpus, tokenizer, total_words):
    sequences = []
    for line in corpus:
        token_list = tokenizer.texts_to_sequences([line])[0]
        for i in range(1, len(token_list)):
            n_gram_sequence = token_list[:i+1]
            sequences.append(n_gram_sequence)

    # Pad sequences for equal input length 
    max_sequence_len = max([len(seq) for seq in sequences])
    sequences = np.array(pad_sequences(sequences, maxlen=max_sequence_len, padding='pre'))

    # Split sequences between the "input" sequence and "output" predicted word
    input_sequences, labels = sequences[:,:-1], sequences[:,-1]
    # One-hot encode the labels
    one_hot_labels = tf.keras.utils.to_categorical(labels, num_classes=total_words)
    return input_sequences, max_sequence_len, one_hot_labels



