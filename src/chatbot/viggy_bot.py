from src.chatbot.chatterbot.trainers import ChatterBotCorpusTrainer
from .chatterbot.chatterbot import ChatBot

def create_bot():
    viggy_bot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")
    trainer = ChatterBotCorpusTrainer(viggy_bot)
    trainer.train("chatterbot.corpus.english")
    return viggy_bot
