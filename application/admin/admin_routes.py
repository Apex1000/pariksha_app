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
from ..models import Teachers
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template

# Blueprint Configuration
admin = Blueprint('admin',__name__,
                    template_folder='templates',
                    static_folder='static/admin',
                    url_prefix='/admin'
                    )

@admin.route('/')
def dashboard():
    return render_template('admin/admin.html',title='Pariksha-Admin')

@admin.route('/students')
def students():
    return render_template('admin/students.html',title='Pariksha-Admin')

@admin.route('/newstudent',methods=['POST','GET'])
def newstudent():    
    return render_template('admin/newstudent.html',title='Pariksha-Admin')

@admin.route('/teachers')
def teachers():
    teachers = Teachers.query.all()
    count = Teachers.query.count()
    return render_template('admin/teachers.html',title='Pariksha-Admin',data=teachers,count=count)

@admin.route('/newteacher',methods=['POST','GET'])
def newteacher():
    if request.method == "POST":
        username = request.form['username']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        mobile = request.form['mobile']
        skill = request.form['skillinfo']
        address =request.form['address']
        city = request.form['city']
        state = request.form['state']
        pin_code = request.form['postalcode']
        aboutme = request.form['aboutme']
        newteacher = Teachers(username=username,firstname=firstname,lastname=lastname,email=email,mobile=mobile,
                            skill=skill,address=address,city=city,state=state,pin_code=pin_code,aboutme=aboutme)
        db.session.add(newteacher)
        db.session.commit()
        return redirect(url_for('admin.newteacher'))
    teachers = Teachers.query.all()
    return render_template('admin/newteacher.html',title='Pariksha-Admin',data=teachers)