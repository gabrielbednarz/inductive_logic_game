from flask import Flask, render_template, url_for, redirect, request, session, flash, get_flashed_messages
from calculations import questions, DATA
from flask_sqlalchemy import SQLAlchemy
import random
import os


app = Flask(__name__)
app.secret_key = 'random_string'

instance_path = os.path.join(os.getcwd(), 'instance')
os.makedirs(instance_path, exist_ok=True)  # Creates only if not exists.
db_path = os.path.join(instance_path, 'game_results.db')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


class Data(db.Model):
    __tablename__ = 'game_results'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    round_number = db.Column(db.Integer)
    question_number = db.Column(db.Integer)
    correct_answer = db.Column(db.Float)
    your_answer = db.Column(db.Float)
    total_score = db.Column(db.Integer)

    def __init__(self, round_number, question_number, correct_answer, your_answer, total_score):
        self.round_number = round_number
        self.question_number = question_number
        self.correct_answer = correct_answer
        self.your_answer = your_answer
        self.total_score = total_score


counter = []


@app.route('/')
def start():
    return render_template('game_main.html')


@app.route('/initialize_session', methods=['POST'])
def initialize_session():
    session['score'] = 0
    session['how_many_rounds'] = int(request.form.get('number_of_rounds'))
    session['copy_r'] = int(request.form.get('number_of_rounds'))
    return redirect(url_for('play'))


@app.route('/results')
def results():
    rows = Data.query.all()  # A table/model row is a list of Data objects.
    return render_template('results.html', rows=rows)


# Dodać do każdej render_template, gdzie jest round.html, current_round_number=current_round_number i wyżłobić miejsce
# w dokumencie HTML na coś w rodzaju "Round {{current_round_number}}".

@app.route('/round', methods=['POST', 'GET'])
def play():

    current_round_number = session['copy_r'] + 1 - session['how_many_rounds']
    c = current_round_number  # For simplicity.

    if session['how_many_rounds'] < 1:
        return redirect(url_for('results'))
        # return render_template('results.html', score=session['score'])

    elif request.method == 'GET' and len(counter) == 0:
        counter.append(1)
        flash(f'Score: {session["score"]}.')
        return render_template('round.html', exercise=DATA[session['how_many_rounds']][0], question=questions[0], c=c)

    elif request.method == 'POST':

        user_answer = float(request.form.get('user_answer'))
        for i in range(1, len(questions)):
            if len(counter) == i:
                counter.append(1)
                if user_answer == DATA[session['how_many_rounds']][i]:
                    flash(f'Correct. The answer to the previous task is {DATA[session["how_many_rounds"]][i]}.')
                    session['score'] += 1 if i < 5 else 3
                else:
                    flash(f'Incorrect. The answer to the previous task is {DATA[session["how_many_rounds"]][i]}.')
                flash(f'Score: {session["score"]}.')

                new_row = Data(round_number=current_round_number, question_number=i,
                               correct_answer=DATA[session['how_many_rounds']][i], your_answer=user_answer,
                               total_score=session['score'])
                db.session.add(new_row)
                db.session.commit()

                return render_template('round.html', exercise=DATA[session['how_many_rounds']][0],
                                       question=questions[i], user_answer=user_answer, c=c)

        if len(counter) == len(questions):

            counter.clear()

            if user_answer == DATA[session['how_many_rounds']][len(questions)]:
                flash(f'Correct. The answer to the previous task is {DATA[session["how_many_rounds"]][8]}.')
                session['score'] += 3
            else:
                flash(f'Incorrect. The answer to the previous task is {DATA[session["how_many_rounds"]][8]}.')

            new_row = Data(round_number=current_round_number, question_number=len(questions),
                           correct_answer=DATA[session['how_many_rounds']][len(questions)], your_answer=user_answer,
                           total_score=session['score'])
            db.session.add(new_row)
            db.session.commit()

            session['how_many_rounds'] -= 1

            return redirect(url_for('play'))


if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
    app.run(debug=True)
