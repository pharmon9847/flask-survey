from passwords import FLASK_SECRET_KEY
from flask import Flask, request, render_template, redirect, flash, session, make_response
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

RESPONSES_KEY = 'responses'
CURRENT_SURVEY_KEY = 'current_survey'

app = Flask(__name__)
app.config['SECRET_KEY'] = FLASK_SECRET_KEY
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route('/')
def home_page_choose_survey():
    """The home page of the survey app
    """
    return render_template('choose-survey.html', surveys=surveys)

@app.route('/', methods=["POST"])
def choose_survey():
    """Choose a survey
    """
    
    survey_id = request.form['survey_code']
    
    # can't re-take survey until cookie times out
    if request.cookies.get(f'completed_{survey_id}'):
        return render_template('already_completed.html')
    
    survey = surveys[survey_id]
    session[CURRENT_SURVEY_KEY] = survey_id
    
    return render_template('home.html', survey=survey)

@app.route('/begin', methods=['POST'])
def begin_survey():
    """clear session of responses.
    """
    
    session[RESPONSES_KEY] = []
    
    return redirect('/questions/0')

@app.route('/answer', methods=['POST'])
def handle_question():
    """Save response. Redirect to next question."""
    
    # get the response choice
    choice = request.form['answer']
    text = request.form.get('text', '')
    
    # add response to session
    responses = session[RESPONSES_KEY]
    responses.append({'choice': choice, 'text': text})

    # add response to session
    session[RESPONSES_KEY] = responses
    survey_code = session[CURRENT_SURVEY_KEY]
    survey = surveys[survey_code]
    
     
    if (len(responses) == len(survey.questions)):
        # All questions answered
        return redirect('/complete')
    
    else:
        return redirect(f'/questions/{len(responses)}')

@app.route('/questions/<int:qid>')
def show_question(qid):
    """Display current question"""
    responses = session.get(RESPONSES_KEY)
    survey_code = session[CURRENT_SURVEY_KEY]
    survey = surveys[survey_code]
    
    if (responses is None):
        # trying to access question page too early
        # send them home
        return redirect('/')
    
    if (len(responses) == len(survey.questions)):
        # all questions answered
        # send them to thank you page
        return redirect('/complete')
    
    if (len(responses) != qid):
        # trying to answer out of order
        flash(f'Invalid question id: {qid}.')
        return redirect(f'/questions/{len(responses)}')
    
    question = survey.questions[qid]
    
    return render_template('question.html', question_num=qid, question=question)

@app.route('/complete')
def complete():
    """survey completed. Show completion page.
    """
    
    survey_id = session[CURRENT_SURVEY_KEY]
    survey = surveys[survey_id]
    responses = session[RESPONSES_KEY]
    
    html = render_template('completion.html', survey=survey, responses=responses)
    
    # set cookie noting survey is done to prevent retaking it
    response = make_response(html)
    response.set_cookie(f'completed_{survey_id}', 'yes', max_age=60)
    return response