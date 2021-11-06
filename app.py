from flask import Flask, request, render_template, redirect, flash, jsonify
from flask.helpers import url_for
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey, Question, Survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "chickens"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []
questions = []


survey_q = satisfaction_survey.get_questions()
for q in survey_q:
    qq = q.get_questions()
    qc = q.get_choices()
    questions.append({'question': qq, 'choices': qc})


@app.route('/')
def show_form():
    title = satisfaction_survey.title
    instr = satisfaction_survey.instructions
    return render_template('home.html', questions = questions, title = title, instructions = instr)


@app.route('/responses/new/<int:index>', methods=["POST"])
def add_responses(index):
        response = int(request.form["question"])
        responses.append({"index": index, "question": questions[index]['question'], "choice": questions[index]['choices'][response]})
        return redirect('/questions/' + str(index + 1))


@app.route('/questions/<int:index>', methods=["GET", "POST"])
def load_question(index):
    title = satisfaction_survey.title
    instr = satisfaction_survey.instructions #Should these be global instead of repeating in multiple functions?
    if index < len(questions):
        return render_template('question.html', index = index, question = questions[index], title = title)
    elif index == len(questions):
        return render_template('thankyou.html', title=title, responses = responses)
    else:
        return render_template('error.html', title=title)