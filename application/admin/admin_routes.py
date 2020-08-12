from flask import current_app as app,request, jsonify,render_template, redirect, url_for,session,message_flashed,send_file,send_from_directory
from flask import render_template,jsonify
from ..models import db
from ..auth import auth_routes
import simplejson
import json
import simplejson
import json
import random
import string
import uuid
import os
import urllib.request
from datetime import datetime
from ..models import Teachers,Studentdata,Exams,AnswerSheet,Studentdata,Workers
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template

# Blueprint Configuration
admin = Blueprint('admin',__name__,
                    template_folder='templates',
                    static_folder='static',
                    url_prefix='/admin'
                    )

IMAGE_DIR = 'application/static/images'
def randstr():
    '''Creates a random string of alphanumeric characters.'''
    return ''.join(random.choice(string.ascii_uppercase + string.digits) \
                for _ in range(30))


@admin.route('/')
def dashboard():
    count = Teachers.query.count()
    studentdata = Studentdata.query.all()
    studentcount = Studentdata.query.count()
    data = Exams.query.all()
    eanswersheet = AnswerSheet.query.count()
    return render_template('main/admin.html',
                            title='Pariksha-Admin',
                            countteacher=count,
                            data = data,
                            count = eanswersheet,
                            studentdata = studentdata,
                            studentcount = studentcount)

@admin.route('/students')
def students():
    return render_template('students/students.html',title='Pariksha-Admin')

@admin.route('/newstudent',methods=['POST','GET'])
def newstudent():
    if request.method == "POST":
        admisson_no = request.form['admisson_no']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        std = request.form['std']
        dob = request.form['dob']
        photo = request.files['photo']
        mobile = request.form['mobile']
        father_name = request.form['father_name']
        mother_name = request.form['mother_name']
        address =request.form['address']
        city = request.form['city']
        state = request.form['state']
        pin_code = request.form['postalcode']
        filename = secure_filename(photo.filename)
        safefilename = secure_filename(randstr() + '-' + photo.filename)
        photo.save(os.path.join(IMAGE_DIR,safefilename))
        newstudent = Studentdata(admission_no=admisson_no,firstname=firstname,lastname=lastname,standard=std,mobile=mobile,
                            dob=dob,photo=safefilename,father_name=father_name,mother_name=mother_name,address=address,city=city,state=state,pin_code=pin_code)
        db.session.add(newstudent)
        db.session.commit()
        return redirect(url_for('admin.newstudent'))
    students = Studentdata.query.all()
    return render_template('students/newstudent.html',title='Pariksha-Admin',data = students)

@admin.route('/students/profile/<id>')
def studentprofile(id):
    data = Studentdata.query.filter_by(admission_no=id).first()
    return render_template('students/profile.html',title='Pariksha-Admin',
                            data = data)

@admin.route('/class_student/<id>',methods=['GET'])
def class_student(id):
    data = Studentdata.query.filter_by(standard=id).all()
    return render_template('students/class_students.html',title='Pariksha-Admin',data=data,std=id)

@admin.route('/teachers')
def teachers():
    teachers = Teachers.query.all()
    count = Teachers.query.count()
    return render_template('teachers/teachers.html',title='Pariksha-Admin',data=teachers,count=count)

@admin.route('/newteacher',methods=['POST','GET'])
def newteacher():
    if request.method == "POST":
        username = request.form['username']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        photo = request.files['photo']
        dob = request.form['dob']
        email = request.form['email']
        mobile = request.form['mobile']
        skill = request.form['skillinfo']
        address =request.form['address']
        city = request.form['city']
        state = request.form['state']
        pin_code = request.form['postalcode']
        aboutme = request.form['aboutme']
        filename = secure_filename(photo.filename)
        safefilename = secure_filename(randstr() + '-' + photo.filename)
        photo.save(os.path.join(IMAGE_DIR,safefilename))
        newteacher = Teachers(username=username,firstname=firstname,lastname=lastname,email=email,mobile=mobile,
                            photo=safefilename,dob=dob,skill=skill,address=address,city=city,state=state,pin_code=pin_code,aboutme=aboutme)
        db.session.add(newteacher)
        db.session.commit()
        return redirect(url_for('admin.newteacher'))
    teachers = Teachers.query.all()
    return render_template('teachers/newteacher.html',title='Pariksha-Admin',data=teachers)

@admin.route('teachers/profile/<id>')
def teachersprofile(id):
    data = Teachers.query.filter_by(id=id).first()
    return render_template('teachers/profile.html',title='Pariksha-Admin',
                            data = data)

@admin.route('/workers')
def workers():
    workers = Workers.query.all()
    return render_template('workers/workers.html',title='Pariksha-Admin',data = workers)

@admin.route('workers/add', methods=['POST','GET'])
def newworker():
    if request.method == "POST":
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        mobile = request.form['mobile']
        photo = request.files['photo']
        category = request.form['category']
        dob= request.form['date']
        address =request.form['address']
        city = request.form['city']
        state = request.form['state']
        pin_code = request.form['postalcode']
        filename = secure_filename(photo.filename)
        safefilename = secure_filename(randstr() + '-' + photo.filename)
        photo.save(os.path.join(IMAGE_DIR,safefilename))
        newworker = Workers(firstname=firstname,lastname=lastname,mobile=mobile,category=category,photo=safefilename,
                            dob=dob,address=address,city=city,state=state,pin_code=pin_code)
        db.session.add(newworker)
        db.session.commit()
        return redirect(url_for('admin.newworker'))
    
    workers = Workers.query.all()
    return render_template('workers/newworker.html',title='Pariksha-Admin',data=workers)

@admin.route('/worker/profile/<id>')
def workerprofile(id):
    data = Workers.query.filter_by(id=id).first()
    return render_template('workers/profile.html',title='Pariksha-Admin',data=data)
