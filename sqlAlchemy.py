from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1728@localhost:5432/postgres'
app.config['SECRET_KEY'] = "random string"
import requests

db = SQLAlchemy(app)


class students(db.Model):
    id = db.Column('student_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    addr = db.Column(db.String(200))
    pin = db.Column(db.String(10))

    def __init__(self, name, city, addr, pin):
        self.name = name
        self.city = city
        self.addr = addr
        self.pin = pin


def obtenerCampeones():
    campeones = []

    respuesta = requests.get('http://ddragon.leagueoflegends.com/cdn/11.1.1/data/es_MX/champion.json').json()

    for i in respuesta['data']:
        campeones.append(respuesta['data'][i]['name'])
    return campeones


@app.route('/')
def show_all():
    return render_template('show_all.html', students=students.query.all())


@app.route('/campeones')
def campeones():
    return render_template('campeones.html', campeones=obtenerCampeones())


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['city'] or not request.form['addr']:
            flash('Please enter all the fields', 'error')
        else:
            student = students(request.form['name'], request.form['city'],
                               request.form['addr'], request.form['pin'])

            db.session.add(student)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('show_all'))
    return render_template('new.html')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
