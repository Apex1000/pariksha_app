from flask import Flask, request, jsonify,render_template, redirect, url_for,session,message_flashed,send_file,send_from_directory
# from models import Exams
import simplejson
import json
import random
import string
import uuid
import os
import urllib.request
from config import Config
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
app.secret_key = 'worldsucks'
engine = create_engine('sqlite:///' + os.path.join(basedir, 'database.db'))
Session = sessionmaker(bind=engine)
ses = Session()

IMAGE_DIR = 'static/images'
app.config['IMAGE_DIR'] = IMAGE_DIR
# migrate = Migrate(app, db)
class Exams(db.Model):
    exam_id = db.Column(db.Integer, primary_key=True)
    teacher_name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    exam_name = db.Column(db.String(50))
    date = db.Column(db.String(50))
    time = db.Column(db.String(50))
    time_duration = db.Column(db.String(50))
    grade = db.Column(db.String(50))
    intro = db.Column(db.String(50))
    
class Questionss(db.Model):
    exam_id = db.Column(db.Integer)
    question_id = db.Column(db.Integer, primary_key=True)
    question_type = db.Column(db.String(50))
    question = db.Column(db.String(50))
    question_photo = db.Column(db.LargeBinary)
    opt1 = db.Column(db.String(50),default='NA')
    opt2 = db.Column(db.String(50),default='NA')
    opt3 = db.Column(db.String(50),default='NA')
    opt4 = db.Column(db.String(50),default='NA')
    mcqans = db.Column(db.String(50),default='NA')
    question_marks = db.Column(db.Integer)
    nagativemarks = db.Column(db.Float)
    imgfilename = db.Column(db.String())

class Students(db.Model):
    exam_id = db.Column(db.Integer)
    student_id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(50))
    rollno = db.Column(db.String(50))
    branch = db.Column(db.String(50))

class AnswerSheet(db.Model):
    exam_id = db.Column(db.Integer)
    answersheet_id = db.Column(db.Integer, primary_key=True)
    rollno = db.Column(db.String(50))
    answer = db.Column(db.String(5000))
    grade = db.Column(db.String(50))
class Feedback(db.Model):
    feedback_id = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String(50))
    msg = db.Column(db.String(5000))
def randstr():
    '''Creates a random string of alphanumeric characters.'''
    return ''.join(random.choice(string.ascii_uppercase + string.digits) \
                for _ in range(30))

def convertjson(data):
    l = []
    for i in data:
        data = {
            'exam_id':i.exam_id,
            'question_type':i.question_type,
            'question':i.question,
            # 'question_photo':str(i.question_photo),
            'opt1':i.opt1,
            'opt2':i.opt2,
            'opt3':i.opt3,
            'opt4':i.opt4,
            'mcqans':i.mcqans,
            'question_marks':i.question_marks,
            'imgfilename':i.imgfilename
        }
        l.append(data)
    return (simplejson.dumps(l))

@app.route('/receiver', methods=['POST','GET'])
def receiver():
     # POST request
    if request.method == 'POST':
        rollno = session['exam_id'] 
        examid = session['test_id']
        answer  = json.dumps(request.get_json())  # parse as JSON
        question = Questionss.query.filter_by(exam_id=examid).all()
        intro = Exams.query.filter_by(exam_id=examid).all()        
        ans = answer
        answer = answer.replace("[", "")
        answer = answer.replace("]", "")
        answer = answer.replace('"', '')
        answer = answer.replace(" ", "")
        answer = answer.split(',')
        json_string = json.dumps(answer)
        z=0
        crtans = 0.0
        totalq=0
        crtan = 0
        for i in question:
            print(i.mcqans ,answer[z] )
            if i.question_type=='MCQ':
                if (i.mcqans == answer[z]):
                    crtans = crtans+float(i.question_marks)
                else:
                    crtans = crtans-float(i.nagativemarks)
            z=z+1
        session['grade'] = crtans
        anns = AnswerSheet(exam_id=examid,rollno=rollno,answer=ans,grade = crtans)
        db.session.add(anns)
        db.session.commit()
        print (crtans)
        return 'OK', 200
    # GET request
    else:
        message = {'greeting':'Hello from Flask!'}
        print (jsonify(message))  # serialize and use JSON headers
    
# A welcome message to test our server
@app.route('/answersheet', methods=['POST','GET'])
def answer():
    if request.method == 'POST':
        examid = request.form['test']
        session['exam_id']=examid
        data = Students.query.filter_by(exam_id=examid).all()
        # student = ses.query(AnswerSheet,Students).outerjoin(AnswerSheet, Students.rollno==AnswerSheet.rollno).all()
        # intro = AnswerSheet.query.filter_by(exam_id=examid).all()
        # print (student)
        return render_template('sheet.html',answersheet = data)
    else:
        if (session):
            examid = session['exam_id']
            data = Students.query.filter_by(exam_id=examid).all()
        # student = Students.query.filter_by(exam_id=examid).all()
        # intro = AnswerSheet.query.filter_by(exam_id=examid).all()
        # print (data)
            # student = db.session.query(AnswerSheet,Students).outerjoin(AnswerSheet, Students.rollno==AnswerSheet.rollno).all()
            # # intro = AnswerSheet.query.filter_by(exam_id=examid).all()
            # print (student)
            
            return render_template('sheet.html',answersheet = data)
        else:
            return render_template('answersheet.html')
@app.route('/answersheet/<id>', methods=['POST','GET'])
def answers(id):
    examid = session['exam_id']
    question = Questionss.query.filter_by(exam_id=examid).all()
    questions = convertjson(question)
    # print(question)
    intro = AnswerSheet.query.filter_by(exam_id=examid,rollno=id).all()
    if(intro):
        return render_template('answer.html', answer=intro,question=questions)
    else:
        
        return render_template('late.html')    
@app.route('/')
def index():
    if (session):
        session.clear()    
    return render_template('index.html')
@app.route('/exam', methods=['POST','GET'])
def exam():
    if request.method == 'POST':
        x = uuid.uuid1()
        y = str(x.int)
        z = int(y[:10])
        exam_id = z
        name = request.form['name']
        email = request.form['email']
        re_email = request.form['reemail']
        exam_name = request.form['exam_name']
        instructions = request.form['instructions']
        date = request.form['date']
        time = request.form['time']
        duration = request.form['timeduration']
        grade = request.form['showgrade']
        session['exam_id'] = exam_id
        exam = Exams(exam_id=exam_id,teacher_name=name,email=email,exam_name=exam_name,date=date,time=time,time_duration=duration,grade=grade,intro = instructions)
        
        db.session.add(exam)
        db.session.commit()
        if email!= re_email:

            return redirect(url_for('exam'))
        else:
            return redirect(url_for('addquestion'))

    return render_template('hosttest.html')

@app.route('/addquestion',methods=['POST','GET'])
def addquestion():
    if request.method == 'POST':
        exam_id = session['exam_id']
        question_type = request.form['question_type']
        question = request.form['question']
        file = request.files['file']
        opt1 = request.form['opt1']
        opt2 = request.form['opt2']
        opt3 = request.form['opt3']
        opt4 = request.form['opt4']
        mcqans = request.form['mcqans']
        marks = request.form['marks']
        nagativemarks = request.form['negativemarks']
        filename = secure_filename(file.filename)
        
        safefilename = secure_filename(randstr() + '-' + file.filename)
        file.save(os.path.join(IMAGE_DIR,safefilename))
        if question_type == 'Descriptive':
            question = Questionss(exam_id=exam_id,question_type=question_type,
                                    question=question,question_photo=file.read(),question_marks=marks,imgfilename=safefilename,nagativemarks=nagativemarks)
        else:
            question = Questionss(exam_id=exam_id,question_type=question_type,question=question,
                                    question_photo=file.read(),opt1=opt1,opt2=opt2,opt3=opt3,
                                    opt4=opt4,mcqans=mcqans,question_marks=marks,imgfilename=safefilename,nagativemarks=nagativemarks)
        # file.save(os.path.join(IMAGE_DIR,safefilename))
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('addquestion'))
    examid = int(session['exam_id'])
    data = Questionss.query.filter_by(exam_id=examid).all()
    return render_template('addquestion.html',form = data)

@app.route('/result')
def result():
    examid = session['exam_id']
    grade = session['grade'] 
    session.clear()
    return render_template('result.html',ExamID=examid,grade = grade)

@app.route('/submit')
def submit():
    examid = session['exam_id']
    session.clear()
    return render_template('submit.html',ExamID=examid)

@app.route('/taketest',methods=['POST','GET'])
def taketest():
    if request.method == 'POST':
        examid = int(request.form['examid'])
        name = request.form['name']
        rollno = request.form['rollno']
        branch = request.form['branch']
        student = Students(exam_id=examid,student_name=name,rollno=rollno,branch=branch)
        db.session.add(student)
        db.session.commit()
        session['exam_id']= rollno
        session['test_id']= examid
        return redirect(url_for('instructions'))
    return render_template('taketest.html')

@app.route('/instructions',methods=['POST','GET'])
def instructions():
    if session:
        examid = int(session['test_id'])
        intro = Exams.query.filter_by(exam_id=examid).all()        
        sysdate = str(datetime.date(datetime.now()))
        systime = str(datetime.time(datetime.now()))
        systime = systime.split(':')
        time = intro[0].time
        time = time.split(':')
        count = int(time[0])-int(systime[0])
        count = count*60
        count = (count - int(systime[1]))+int(time[1])
        sysdate = sysdate.split('-')
        date =intro[0].date
        date =date.split('-')
        days = ((int(date[0])-int(sysdate[0]))*364)-((int(date[1])-int(sysdate[1]))*30)-(int(date[2])-int(sysdate[2]))
        hours = days*24
        print(hours)
        print(count)
        return render_template('instructions.html',intro = intro,count=count+hours)



@app.route('/questions',methods=['POST','GET'])
def questions():
    # print(datetime.date(datetime.now()))
    # print(datetime.time(datetime.now()))
    if session:
        examid = int(session['test_id'])
        question = Questionss.query.filter_by(exam_id=examid).all()
        intro = Exams.query.filter_by(exam_id=examid).all()        
        jsondata = convertjson(question)
        tt = json.dumps(jsondata)
        z = len(question)
        id=0
        date = str(datetime.date(datetime.now()))
        time = str(datetime.time(datetime.now()))
        time1 = time.split(':')
        # t = time1[0]+':'+time1[1]
        tt1 = intro[0].time
        tt1 = tt1.split(':')
        th = int(tt1[0])
        tm = int(tt1[1])
        print(tm,time1[1])
        session['id'] = id
        # if(date == intro[0].date) and (th==int(time1[0]) and tm==int(time1[1])):
        return render_template('question.html',questions = jsondata,intro = intro,z=z,t = question)
        # else:
        #     return redirect(url_for('instructions'))
    else:
        return redirect(url_for('taketest'))
@app.route('/endtest')
def endtest():
    session.clear()
    return redirect(url_for('index'))

@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='images/' + filename), code=301)
@app.route('/feedback',methods=['POST','GET'])
def feedback():
    if request.method == 'POST':
        name = request.form['name']
        msg = request.form['message']
        feedback = Feedback(name = name, msg = msg)
        db.session.add(feedback)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('feedback.html')

@app.route('/showfeedback',methods=['POST','GET'])
def showfeedback():
    feedback = Feedback.query.all()
    return render_template('showfeedback.html',feedback=feedback)


          
if __name__ == '__main__':
    db.create_all()
    app.run(threaded=True, port=8000)
