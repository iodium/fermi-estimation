from flask import Flask, render_template, request, flash, redirect, url_for, session
import sqlite3
from questions import QUESTIONS as QU, get_score
import datetime
import pandas as pd

app = Flask(__name__)
app.secret_key = "key"


def get_daily_questions():
    """
    Gets questions for the quiz based on date
        

    Returns:
        List of three questions sourced from questions.py
    """
    global day_index
    epoch = datetime.date(2026, 1, 1) # Creates group of 3 based off of the current day using mod
    day_index = (datetime.date.today() - epoch).days
    num_groups = len(QU) // 3
    group = day_index % num_groups
    start = group * 3
    return QU[start:start + 3]

@app.route('/')
def home():
    """
        Displays the home/quiz page
    
        Arguments:
            accessed_results_but_not_completed
            -> if user tries to access the results page without finishing the quiz first
               this helps display an alert message to tell the user they need to finish first
            - This is only passed in through redirects, so it's not included as a standard parameter 
        
        Returns:
            Renders quiz.html template with the daily questions
            If a cookie is found showing that the user has already done today's quiz, they are redirected to results page
    """
    today_questions = get_daily_questions() # get questions for today from question bank

    if session.get('date') == day_index and session.get('responses'):  # checks cookies to see if someone already did today's quiz
        return redirect(url_for('results', completed_but_tried_to_access_again=True)) # if yes, redirect to show their results 

    # if they haven't taken it yet, just send them to quiz normally 
    return render_template('quiz.html',
                           questions=today_questions,
                           accessed_results_but_not_completed=request.args.get('accessed_results_but_not_completed', default=False, type=bool)) # Renders template for quiz, sources questions from get_daily_questions()

@app.route('/stats')
def statistics():
    """
    Displays the statistics page for aggregate data about all users

    Returns:
        Renders statistics.html template with current statistics
    """
    return render_template('stats.html', **get_stats()) # Rendeers template for statistics, statistics sourced from get_stats()

@app.route('/submit', methods=['POST'])
def submit():
    """
    Runs when quiz is submited, handles errors and puts submission into stats.db (aggregate database)

    Returns:
        Redirects to results page to show user's results 
    """
    questions = get_daily_questions() # Get today's questions
    errors = []
    responses = {} # Create empty list and dict for storage
    for q in questions: # Loop through to see if there are errors in the submission
        print(f'min_ + {q["id"]}') # Debug print
        try:
            min_answer = float(request.form.get(f'min_{q["id"]}'))
            max_answer = float(request.form.get(f'max_{q["id"]}')) # Store min and max for question

            if min_answer > max_answer:
                errors.append('Upper bound must be greater than or equal to lower bound.')
            if min_answer <= 0:
                errors.append('Lower bound must be positive.') # Error messages, invalid numbers
            else:
                responses[q['id']] = (min_answer, max_answer) # No error, add submission to response list
        except (ValueError, TypeError):
            errors.append('You may not leave answer fields open and you must enter only numbers.')  # Error message, invalid input type
    if errors: # Display errors for viewer, restart quiz
        print(set(errors))
        for error in set(errors):
            flash(error, 'error')
        return redirect(url_for('home'))
    
    results = []
    for q in questions: # Loop through questions to add to stats.db
        min_answer, max_answer = responses[q['id']]
        scores = get_score(q, min_answer, max_answer, 0.2) # Get hit, width, and score from get_score()

        results.append(scores)
        new_row = pd.DataFrame([{ # Create temp dataframe with submission data
            "question_id": q["id"],
            "min": min_answer,
            "max": max_answer,
            "hit": scores[1],
            "width": scores[2],
            "score": scores[0],
        }])

        session['date'] = day_index # make cookie, saving the date that the user did the quiz on
        session['responses'] = responses # save the user's responses (used when displaying their results )
        session.permanent = True # makes it so that the cookie doesn't get trashed when the browser closes 

        conn = sqlite3.connect("stats.db") # Append submission data to stats.db
        new_row.to_sql("submissions", conn, if_exists="append", index=False)
        conn.close()
    return redirect(url_for('results'))

@app.route('/results')
def results():
    """
        Opens the results page

        Arguments:
        completed_but_tried_to_access_again - means user completed the quiz and tried to go back to the quiz page
            -> Will help display the alert message for this situation
            - this argument is only for redirects and is not a standard paramter in the function 

        Returns:
            1. If quiz hasn't been completed, redirects to quiz page
            2. If quiz has been completed, redirects to results page
        """
    questions = get_daily_questions()

    if not session.get('responses') or session.get('date') != day_index: # Reroutes to home if quiz not completed, or if the session is stale (e.g. day rolled over since submitting)
        return redirect(url_for('home', accessed_results_but_not_completed=True))

    responses = session.get('responses') # Gets responses from cookie, stores in dict
    answer_data = [] # new list to store data to dislay user's results that were taken from the cookie 
    for i in range(3):
        # recalculate user's score for each question based on their responses that were saved in the cookie 
        scores = get_score(questions[i], responses[questions[i]['id']][0], responses[questions[i]['id']][1], 0.2)
        print(scores)

        answer_data.append({ # make dictionary with data to show to the user
            "question": questions[i]["question"],
            "display": questions[i]["display"],
            "category": questions[i]["category"],
            "user_answer": responses[questions[i]["id"]],
            "score": scores[0],
            "hit": scores[1]
        })
    return render_template('results.html', answers=answer_data, completed_but_tried_to_access_again=request.args.get('completed_but_tried_to_access_again', default=False, type=bool))

def get_stats():
    """
    Gathers all the data used in the statistics screen from stats.db

    Returns:
        Dictionary of all statistics used by the statistics screen
    """
    with sqlite3.connect('stats.db') as conn: # Opens stats.db as df, easier to read as a panda dataframe
        df = pd.read_sql('SELECT * FROM submissions', con=conn)

    total_subs = len(df)
    if total_subs == 0: # Returns empty if no data
        return {
            'total_subs': 0,
            'average_hit': None,
            'average_weight': None,
            'average_score': None,
            'easyQ': None,
            'hardQ': None,
            'easyC': None,
            'hardC': None,
        }

    average_hit = round(df['hit'].mean() * 100, 1) # Store score values
    average_weight = round(df['width'].mean(), 2)
    average_score = round(df['score'].mean(), 1)

    question_by_id = {q['id']: q for q in QU}
    by_question = df.groupby('question_id')['score'].mean() # Groups submissions in question_by_id into mean score values for questions
    hardest_question_id = by_question.idxmin() # Gets easiest and hardest questioniD via average score
    easiest_question_id = by_question.idxmax()
    hardQ = question_by_id[hardest_question_id]['question'] # Gets the actual question wording for easiest and wardest
    easyQ = question_by_id[easiest_question_id]['question']

    category_by_id = {q['id']: q['category'] for q in QU} # Same stuff as before but for categories instead of questions
    df['category'] = df['question_id'].map(category_by_id)
    by_category = df.groupby('category')['score'].mean()
    hardC = by_category.idxmin()
    easyC = by_category.idxmax()

    return { # returns statistics df
        'total_subs': total_subs,
        'average_hit': average_hit,
        'average_weight': average_weight,
        'average_score': average_score,
        'easyQ': easyQ,
        'hardQ': hardQ,
        'easyC': easyC,
        'hardC': hardC,
    }


if __name__ == '__main__':
    app.run(debug=True)