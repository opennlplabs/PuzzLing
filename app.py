from flask import Flask

flask_app = Flask(__name__)

flask_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
flask_app.secret_key = 'any random string'
#run_with_ngrok(flask_app)


@flask_app.route("/", methods=['GET', 'POST'])
def Home():
	# read the testing corpus from the data/testing_set dir
	language = request.args.get('language', 'Somali')
	file_name = language_path[language]

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
		# question = pre_question(lines)

	#session['question'] = question
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

	target = escape(target)#translate(escape(target),headers,languageToken=language_codes_ns[language])
	prediction_score = calc_score(sentence, target)
	spelling_score = spelling(sentence)

	# ouput the correlation function
	return render_template(
		"score.html", 
		prediction_text = "{}".format(prediction_score), 
		spelling_score = "{}".format(spelling_score),
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
