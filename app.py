from flask import (
    Flask,
    request,
    jsonify,
    send_file,
    send_from_directory,
    render_template,
    escape,
    session,
)
import struct
import sqlite3
import base64
from functools import lru_cache
from flask_ngrok import run_with_ngrok
import time
import requests
import json
import argparse
import random

import torch
from transformers import AutoModel, AutoTokenizer


tokenizer = AutoTokenizer.from_pretrained("princeton-nlp/sup-simcse-bert-base-uncased")
model = AutoModel.from_pretrained("princeton-nlp/sup-simcse-bert-base-uncased")

def sentence_mapping(sentence):
    inputs = tokenizer(sentence, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        embeddings = model(**inputs, output_hidden_states=True, return_dict=True).pooler_output

    return embeddings

flask_app = Flask(__name__)
flask_app.secret_key = 'any random string'
#run_with_ngrok(flask_app)

def l2norm(x, dim=-1):
    return x / x.norm(2, dim=dim, keepdim=True).clamp(min=1e-6)

@flask_app.route("/")
def Home():
    # read the testing corpus from the data/testing_set dir
    file_name = "./data/testing_set/demo.txt"
    with open(file_name, 'r', encoding = "utf-8") as file:
        # randomly choose a sentence from the corpus set
        lines = random.sample(file.readlines(), 1)
        # convert the list output into string
        question = " "
        question = question.join(lines)

    question = question.strip().split(' ')
    if question[0].isnumeric():
        question = ' '.join(question[1:])
    else:
        question = ' '.join(question)

    #if question.endswith('\n'):
    #    question = question.replace('\n', '')

    session['question'] = question
    # render the question into the index web
    return render_template("index.html", question="{}".format(question))


@flask_app.route("/predict", methods=['GET', 'POST'])
def predict():
    # retrieve the answer input from the user text-ins
    sentence = request.form.get('inputText')
    target = request.args.get('question')#request.args.get('question')
    target = escape(target)#translate(escape(target))
    prediction_score = calc_score(sentence, target)
    # ouput the correlation function
    return render_template("score.html", prediction_text = "{}".format(prediction_score), sentence= "{}".format(sentence), target = "{}".format(target))


def calc_score(inputs, target):
    if isinstance(target, str):
        target = [target]
        inputs = [inputs]

    assert len(target) == 1
    assert len(inputs) == 1
    inputs_repre = sentence_mapping(inputs)
    target_repre = sentence_mapping(target)

    score = similarity(l2norm(inputs_repre), l2norm(target_repre))

    #score = random.random()

    return score


def similarity(inputs_repre, target_repre):
    """Cosine similarity between all the inputs and target pairs"""
    return inputs_repre.mm(target_repre.t()).item()


url = 'https://platform.neuralspace.ai/api/translation/v1/annotated/translate'
#auth_token = 
headers = {}


def translate(sentence, languageToken="zh-CN"): 
    passedValue = sentence.encode('utf-8').decode('latin1')
    data = f"""
    {{
        "text": "{passedValue}",
        "sourceLanguage":"{languageToken}",
        "targetLanguage": "en"
    }}
    """
    resp = requests.post(url, headers=headers, data=data)

    response_dict = json.loads(resp.text)
    translatedtext = response_dict["data"]["translated_text"]

    return translatedtext


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--auth_token', help='authorization token to NeuralSpace', default = '')
    opt = parser.parse_args()

    auth_token = opt.auth_token

    headers["Accept"] = "application/json, text/plain, */*"
    headers["authorization"] = auth_token
    headers["Content-Type"] = "application/json;charset=UTF-8"

    flask_app.run(debug=True)























