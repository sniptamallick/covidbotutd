from django.shortcuts import render
from django.urls import path
from django.http import HttpResponse
import json
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from .forms import NameForm
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import HttpResponseRedirect

chat = ChatBot(
    'CoronaBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.TimeLogicAdapter',
        'chatterbot.logic.BestMatch',
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand. I am still learning.',
            'maximum_similarity_threshold': 0.40
        }
    ],
    database_uri='sqlite:///database.sqlite3'
)

# Training With Own Questions 
from chatterbot.trainers import ListTrainer

trainer = ListTrainer(chat)

training_data_quesans = open('website/personal_ques.txt').read().splitlines()
training_data_personal = open('website/ques_ans.txt').read().splitlines()
training_data_utdans = open('website/utdcorona.txt').read().splitlines()


training_data = training_data_quesans + training_data_personal + training_data_utdans

trainer.train(training_data)

# Training With an english Corpus chatterbot
#from chatterbot.trainers import ChatterBotCorpusTrainer

#trainer_corpus = ChatterBotCorpusTrainer(chat)

#trainer_corpus.train(
    #'chatterbot.corpus.english')


# Create your views here.

def homepage(request):
    return render(request, 'website/index.html')

def chatbot(request):
	return render(request, 'website/chatbot.html')

@csrf_exempt
def get(request):
    message = request.GET['msg[text]']
    chat_response = chat.get_response(message)
    return HttpResponse(chat_response)


