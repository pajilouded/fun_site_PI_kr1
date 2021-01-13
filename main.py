from flask import Flask, render_template, url_for, request
from werkzeug.utils import redirect

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
user_in = False

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

db = SQLAlchemy(app)


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    first_question = db.Column(db.String)
    second_question = db.Column(db.String)
    first_answer = db.Column(db.String)
    second_answer = db.Column(db.String)

    def __repr__(self):
        return "Ticket %r" % self.number


# отслеживание главной страницы
@app.route('/')
@app.route('/main')
def main():
    text_search = request.args.get('search')

    found_tickets = Ticket.query.all()
    if text_search:
        found_tickets = Ticket.query.filter(
            Ticket.first_question.contains(text_search.lower()) | Ticket.second_question.contains(text_search)).all()
    return render_template("main.html", found_tickets=found_tickets)


@app.route('/create_ticket', methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        number = request.form['number']
        first_q = request.form['first_q']
        first_ans = request.form['first_ans']
        second_q = request.form['second_q']
        second_ans = request.form['second_ans']
        try:
            ticket = Ticket(number=number, first_question=first_q, first_answer=first_ans, second_question=second_q,
                            second_answer=second_ans)
            db.session.add(ticket)
            db.session.commit()
            return redirect('/main')
        except:
            print('Ошибка создания')

    else:
        return render_template('create_ticket.html')


@app.route('/delete/<id>')
def delete(id):
    ticket_deteled = Ticket.query.get_or_404(id)
    try:
        db.session.delete(ticket_deteled)
        db.session.commit()
        return redirect('/main')
    except:
        return "При удалении произошла ошибка"

if __name__ == '__main__':
    app.run(debug=False)
