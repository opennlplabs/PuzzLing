import torch
from torch.utils.data import Dataset, DataLoader
import argparse
from transformers import AutoModel, AutoTokenizer
import requests
import json

import pandas as pd

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

language_path = {
					'Somali':       "./data/testing_set/demo.txt",
					'Xhosa':        "./data/testing_set/demo.txt",
					'Pashto':       "./data/testing_set/pashto/pashto.txt",
					'Twi':          "./data/testing_set/demo.txt",
					'Ukrainian':    "./data/testing_set/demo.txt"
				}

language_codes_ns = {'Somali':'so', 'Xhosa':'xh', 'Pashto':'ps', 'Twi':'tw', 'Ukrainian':'uk'}


url = 'https://platform.neuralspace.ai/api/translation/v1/annotated/translate'
headers = {}


def similarity(inputs_repre: torch.tensor, target_repre: torch.tensor):
	"""Cosine similarity between all the inputs and target pairs"""
	return inputs_repre.mm(target_repre.t())


def sentence_mapping(sentence: str):
	inputs = tokenizer(sentence, padding=True, truncation=True, return_tensors="pt").to(device)
	with torch.no_grad():
		embeddings = model(**inputs, output_hidden_states=True, return_dict=True).pooler_output

	return embeddings


def pre_question(question: str):
	question = question.strip().split(' ')
	# remove the Alphabet ID
	if question[0].isnumeric():
		question = ' '.join(question[1:])
	else:
		question = ' '.join(question)

	return question



def create_dataloader(language: str):
	file_name = language_path[language]
	dataset = []

	with open(file_name, 'r', encoding = "utf-8") as file:
		# randomly choose a sentence from the corpus set
		saved_file = file.readlines()

		# return the question on the frontend
		# do the pre_processing of the question and return

		for line in saved_file:
			sent1, sent2 = line.split('$')
			eng = pre_question(sent1)
			low = pre_question(sent2)
			dataset.append({'English': eng, 'LowLanguage': low})
	
	#dataset = pd.DataFrame(dataset)
	return DataLoader(dataset, batch_size=128, shuffle=False, num_workers=0)


def get_result(dataloader: dataset, languageToken: str, headers: dict):
	source = torch.tensor([]).to(device)
	target = torch.tensor([]).to(device)

	for i,data in enumerate(dataloader):
		englishtext = data['English']
		translatedtext = [translate(sentence, headers, languageToken) for sentence in data['LowLanguage']]

		englishembed = sentence_mapping(englishtext)
		translatedembed = sentence_mapping(translatedtext)

		source = torch.cat((source, englishembed), -1)
		target = torch.cat((target, translatedembed), -1)


	print("Source size: ", source.size())
	print("Target size: ", target.size())
	sim_matrix = similarity(source, target)
	print(sim_matrix)
	print("Matrix Size: ", sim_matrix.size())
	res = torch.softmax(sim_matrix, -1).diag().mean()

	return res





def translate(sentence: str, headers: dict, languageToken="zh-CN": str):
	"""Get the translations response from the Neural Space API"""
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

	translatedtext = response_dict["data"]["translatedText"]

	return translatedtext


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--auth_token', help='authorization token to NeuralSpace', default = '')
	parser.add_argument('--model_name', help='model name for sentence processing', default = 'princeton-nlp/sup-simcse-bert-base-uncased')
	parser.add_argument('--source_language', help='kind of low source language', default = 'Pashto')
	opt = parser.parse_args()

	auth_token = opt.auth_token

	tokenizer = AutoTokenizer.from_pretrained(opt.model_name)
	model = AutoModel.from_pretrained(opt.model_name).to(device)

	headers["Accept"] = "application/json, text/plain, */*"
	headers["authorization"] = auth_token
	headers["Content-Type"] = "application/json;charset=UTF-8"

	dataloader = create_dataloader(opt.source_language)
	res = get_result(dataloader,language_codes_ns[opt.source_language] ,headers)

	print(res)
