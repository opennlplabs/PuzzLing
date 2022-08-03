# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
Copyright (c) 2022 - Linguistics Justice League
"""

from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
import random
from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms import TextAreaField
from wtforms.widgets import TextArea
from getSemanticScore import calc_score
from getSpellingScore import spelling


# Creat a form class for user input text
class TextForm(FlaskForm):
    text = TextAreaField('Type Your Answer Here', widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField("Submit")


@blueprint.route('/index.html', methods=['GET', 'POST'])
@login_required
def index():
    # TODO
    """
    :return: score_value
    """
    score_value = "123"
    return render_template('home/index.html', segment='index',
                           score_value="{}".format(score_value))


@blueprint.route("/test.html", methods=['GET', 'POST'])
@login_required
def test():
    # read the testing corpus from the data/testing_set dir
    language = request.args.get('language', 'Somali')
    file_name = "data/testing_set/pashto/pashto.txt"
    with open(file_name, 'r', encoding="utf-8") as file:
        # randomly choose a sentence from the corpus set
        corpus_file = file.readlines()
        idx: int | str = request.args.get('index', random.randint(0, len(corpus_file) - 1))
        idx = int(idx)
        lines = corpus_file[idx]
        # this is the question set.
        question = lines.split("$")[1]
        # this is the reference answer part.
        ref_answer = lines.split("$")[0]

    text = None
    form = TextForm()

    # Validate Form
    if form.validate_on_submit():
        # text is the user input answer
        text = form.text.data
        form.text.data = ""

    return render_template(
        "home/test.html",
        question="{}".format(question),
        language="{}".format(language),
        index="{}".format(str(index)),
        text=text,
        form=form,
        spelling="{:.2f}".format(spelling(str(text))),
        # TODO there has some bugs in here.
        semantic="{:.2f}".format(calc_score(str(text), ref_answer))
    )


@blueprint.route("/score.html", methods=['GET', 'POST'])
@login_required
def score():
    sentence = request.form.get('inputText')
    target = request.args.get('question')
    return render_template(
        "home/score.html",
        target="{}".format(target),
        sentence="{}".format(sentence)
    )


@blueprint.route('/<template>')
@login_required
def route_template(template):
    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):
    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
