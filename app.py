from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:mechaaq@localhost/sbdaslab'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class idlist(db.Model):
    id_list = db.Column(db.Integer, primary_key=True)

    def __init__(self, id_list):
        self.id_list = id_list


class Attendee(db.Model):
    inv_id = db.Column(db.Integer)
    name = db.Column(db.String(50))
    phoneno = db.Column(db.String(15), primary_key=True)
    menuid = db.Column(db.String(15))

    def __init__(self, inv_id, name, phoneno, menuid):
        self.inv_id = inv_id
        self.name = name
        self.phoneno = phoneno
        self.menuid = menuid

#db.create_all()


@app.route('/')
def start():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        inv_id_login = request.form['inv_id_login']
        if db.session.query(idlist).filter(idlist.id_list == inv_id_login).count() == 1:
            return render_template('index.html')
        else:
            return render_template('login.html', message='Invite ID does not exist')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        inv_id = request.form['inv_id']
        name = request.form['invitee']
        phoneno = request.form['phone']
        menuid = request.form['menu']
        #print(inv_id, name, phoneno, menu)
        if inv_id == '' or name == '' or phoneno == '' or menuid == '':
            return render_template('index.html', message='Please fill all fields')
        if db.session.query(Attendee).filter(Attendee.phoneno == phoneno).count() == 1:
            return render_template('index.html', message='Phone number already exist')
        if db.session.query(idlist).filter(idlist.id_list == inv_id).count() != 1:
            return render_template('index.html', message='Invite ID does not exist')
        if db.session.query(Attendee).filter(Attendee.inv_id == inv_id).count() <= 3:
            data = Attendee(inv_id, name, phoneno, menuid)
            db.session.add(data)
            db.session.commit()
            return render_template('success.html')
        return render_template('index.html', message='You have reached maximum of 4 people per invitation')


if __name__ == '__main__':
    app.run()
