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

	translatedtext = response_dict["data"]["translated_text"]

	return translatedtext