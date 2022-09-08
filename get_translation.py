import requests
import json

url = 'https://platform.neuralspace.ai/api/translation/v1/annotated/translate'

def translate(sentence, headers, languageToken="zh-CN"):
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

	print(response_dict["data"])
	translatedtext = response_dict["data"]["translatedText"]

	return translatedtext