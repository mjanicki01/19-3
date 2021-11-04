from flask import Flask, request, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey, Question

app = Flask(__name__)

app.config['SECRET_KEY'] = "chickens"
debug = DebugToolbarExtension(app)

responses = []
questions = []

@app.route('/')
def show_form():
    survey_q = satisfaction_survey.get_questions()
    for q in survey_q:
        qq = q.get_questions()
        questions.append(qq)
    return render_template('home.html', questions = questions)


