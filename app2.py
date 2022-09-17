from flask import (
	Flask,
	request,
	jsonify,
	send_file,
	send_from_directory,
	render_template,
	escape,
	session,
	redirect,
	url_for,
)
import struct
import sqlite3
import base64
from functools import lru_cache
from werkzeug.utils import secure_filename
import time
import requests
import json
import argparse
import random
import os

from calc_score import calc_score
from get_translation import translate
from pre_question import pre_question
from spelling import spelling
from grammar import grammar

language_path = "./data/testing_set/demo.txt"
# {
# 				'Somali':	"./data/testing_set/demo.txt",
# 				'Xhosa':	"./data/testing_set/demo.txt",
# 				'Pashto':	"./data/testing_set/demo.txt",
# 				'Twi':		"./data/testing_set/demo.txt",
# 				'Ukrainian':"./data/testing_set/demo.txt",
# 				'Amharic':"./data/testing_set/demo.txt"
# 				}#"./data/testing_set/pashto/pashto.txt",

language_codes_ns = {
	'Assamese':	'as',
	'Bengali':	'bn',	'Gujarati':	'gu',
'Hindi':	'hi',	'Kannada':	'kn',	'Malayalam':	'ml',
'Marathi':	'mr',	'Nepali':	'ne',	'Odia (Oriya)':	'or',
'Punjabi':	'pa',	'Sindhi':	'sd',	'Sinhala (Sinhalese)':	'si',
'Tamil':	'ta',	'Telugu':	'te',	'Urdu': 'ur',
'Burmese (Myanmar)':	'my',	'Cebuano':	'ceb',	'Dhivehi':	'dv',
'Hmong':	'hmn',	'Indonesian':	'id',	'Javanese':	'jv',
'Khmer':	'km',	'Malay':	'ms',	'Loa':	'lo',
'Sundanese':	'su',	'Tagalog (Filipino)':	'tl',	'Thai':	'th',
'Urdu':	'ur',	'Vietnamese':	'vi',
'Arabic':	'ar',	'Hebrew':	'he',	'Pashto':	'ps',
'Persian':	'fa',	'Uighur':	'ug',	'Turkmen':	'tk',
'Armenian':	'hy',	'Azerbaijani':	'az',	'Chinese (Simplified)':	'zh-CN',
'Chinese (Traditional)':	'zh-TW',	'Georgian':	'ka',	'Japanese':	'ja',
'Kazakh':	'kk',	'Kirghiz':	'ky',	'Korean':	'ko',
'Kurdish':	'ku',	'Kyrgyz':	'ky',	'Mongolian':	'mn',
'Russian':	'ru',	'Tagalog':	'tl',	'Tajik':	'tg',
'Tatar':	'tt',	'Uzbek':	'uz',
'Afrikaans':	'af',	'Amharic': 'am',	'Bambara':	'bm',
'English':	'en',	'French':	'fr',	'Hausa':	'ha',
'Igbo':	'ig',	'Kinyarwanda':	'rw',	'Lingala':	'ln',
'Malagasy':	'mg',	'Nyanja (Chichewa)':	'ny',	'Oromo':	'om',
'Sesotho':	'st',	'Shona':	'sh',	'Somali':	'so',
'Swahili':	'sw',	'Tigrinya':	'ti',	'Tsonga':	'ts',
'Twi':	'tw',	'Xhosa':	'xh',	'Yoruba':	'yo',
'Zulu':	'zu',
'Albanian':	'sq',	'Aragonese':	'an',	'Bashkir':	'ba',
'Basque':	'eu',	'Belarusian':	'be',	'Bosnian':	'bs',
'Breton':	'br',	'Bulgarian':	'bg',	'Catalan':	'ca',
'Chechen':	'ce',	'Chuvash':	'cv',	'Corsican':	'co',
'Croatian':	'hr',	'Czech':	'cs',	'Danish':	'da',
'Dutch':	'nl',	'English':	'en',	'Esperanto':	'eo',
'Estonian':	'et',	'Finnish':	'fi',	'French':	'fr',
'Frisian':	'fy',	'Galician':	'gl',	'German':	'de',
'Greek':	'el',	'Hungarian':	'hu',	'Icelandic':	'is',
'Irish':	'ga',	'Italian':	'it',	'Latin':	'la',
'Latvian':	'lv', 'Lithuanian':	'lt',	'Luxembourgish':	'lb',
'Macedonian':	'mk',	'Maltese':	'mt',	'Norwegian Bokmål':	'nb',
'Occitan':	'oc',	'Polish':	'pl',	'Portuguese':	'pt',
'Romanian':	'ro',	'Scots Gaelic':	'gd',	'Serbian':	'sr',
'Slovak':	'sk',	'Slovenian':	'sl',	'Spanish':	'es',
'Swedish':	'sv',	'Turkish':	'tr',	'Ukrainian':	'uk',
'Welsh':	'cy',	'Yiddish':	'yi',
'Aymara':	'ay',	'Dutch':	'nl',	'English':	'en',
'French':	'fr',	'Guarani':	'gn',	'Haitian':	'ht',
'Hawaiian':	'haw',	'Portuguese':	'pt',	'Quechua':	'qu',
'Samoan':	'sm',	'Spanish':	'es',	'Yiddish':	'yi',
'Maori':	'mi'
					}

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['pdf'])

headers = {}

flask_app = Flask(__name__)
flask_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
flask_app.secret_key = 'any random string'


@flask_app.route("/", methods=['GET', 'POST'])
def Home():
	# read the testing corpus from the data/testing_set dir
	language = request.args.get('language', 'Somali')
	file_name = language_path

	with open(file_name, 'r', encoding = "utf-8") as file:
		# randomly choose a sentence from the corpus set
		saved_file = file.readlines()
		index = request.args.get('index', random.randint(0,len(saved_file)-1))
		index = int(index)
		lines = saved_file[index]

		#lines = random.sample(file.readlines(), 1)
		# convert the list output into string
		#lines = " ".join(lines)
		# return the question on the frontend
		question = lines
		# do the pre_processing of the question and return
		question = pre_question(lines)
		question = translate(question,headers,languageToken='en', targetLanguage=language_codes_ns[language]) 
	# render the question into the index web
	return render_template(
		"index.html", 
		question = "{}".format(question),
		language = "{}".format(language),
		index = "{}".format(str(index)),
	)


@flask_app.route("/predict", methods=['GET', 'POST'])
def predict():
	# retrieve the answer input from the user text-ins
	sentence = request.form.get('inputText')
	target = request.args.get('question')#request.args.get('question')
	language = request.args.get('language', None)
	index = request.args.get('index', -1)
	index = int(index)

	if sentence is None:
		raise ValueError('No inputs')

	if index <= 0:
		raise ValueError('Index should be larger than 0')

	if language == None:
		raise ValueError('Invalid Language')

	target = translate(escape(target),headers,languageToken=language_codes_ns[language]) 
	#escape(target)
	prediction_score = calc_score(sentence, target)
	spelling_score = spelling(sentence)
	grammar_score = grammar(sentence)

	# ouput the correlation function
	return render_template(
		"score.html", 
		prediction_text = "{}".format(prediction_score), 
		spelling_score = "{}".format(spelling_score),
		grammar_score = "{}".format(grammar_score),
		sentence = "{}".format(sentence), 
		target = "{}".format(target),
		language = "{}".format(language),
		index = "{}".format(str(index))
		)


def allowed_file(filename):
	return '.' in filename and \
	filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@flask_app.route('/upload_files/', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			# Make sure the filename is valid
			filename = secure_filename(file.filename)
			# Should we save the uploaded file
			#file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			
			#Process files
			#filename = func(filename)
			return redirect(url_for('uploaded_file',filename=filename))


@flask_app.route("/files/")
def render_the_files_page():
	return render_template("files.html")


@flask_app.errorhandler(404)
def page_not_found(e):
	# note that we set the 404 status explicitly
    return render_template('404.html'), 404

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--auth_token', help='authorization token to NeuralSpace', default = '')
	parser.add_argument('--test', help='testing mode', action='store_true')
	opt = parser.parse_args()

	auth_token = opt.auth_token

	headers["Accept"] = "application/json, text/plain, */*"
	headers["authorization"] = auth_token
	headers["Content-Type"] = "application/json;charset=UTF-8"

	if opt.test:
		from flask_ngrok import run_with_ngrok
		run_with_ngrok(flask_app)
		flask_app.run()
		
	else:
		flask_app.run(debug=True)























