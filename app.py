from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mkcs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Mkcs(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    studentname = db.Column(db.String(200), nullable=False)
    classwork = db.Column(db.String(500), nullable=False)
    course = db.Column(db.String(500), nullable=False)
    date_started = db.Column(db.String(200), nullable=False)
    fees = db.Column(db.Integer, nullable=False)
    feespaid = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.studentname}"


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == "POST":
        studentname = request.form['studentname']
        classwork = request.form['classwork']
        course = request.form['course']
        datestarted = request.form['datestarted']
        fees = request.form['fees']
        feespaid = request.form['feespaid']
        mkcs = Mkcs(studentname=studentname, classwork=classwork, course=course, fees=fees, feespaid=feespaid, date_started=datestarted)
        db.session.add(mkcs)
        db.session.commit()
    alldata = Mkcs.query.all()
    print(alldata)
    return render_template('index.html', alldata=alldata)

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == "POST":
        studentname = request.form['studentname']
        classwork = request.form['classwork']
        course = request.form['course']
        datestarted = request.form['datestarted']
        fees = request.form['fees']
        feespaid = request.form['feespaid']
        mkcs = Mkcs.query.filter_by(sno=sno).first()
        mkcs.studentname = studentname
        mkcs.classwork = classwork
        mkcs.course = course
        mkcs.date_started = datestarted
        mkcs.fees = fees
        mkcs.feespaid = feespaid
        db.session.add(mkcs)
        db.session.commit()
        return redirect('/')
    data = Mkcs.query.filter_by(sno=sno).first()
    return render_template('update.html', data=data)


@app.route('/delete/<int:sno>')
def delete(sno):
    mkcs = Mkcs.query.filter_by(sno=sno).first()
    db.session.delete(mkcs)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':

    app.run(debug=False, port=8000)
