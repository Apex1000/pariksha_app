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
from ..models import Questionss,AnswerSheet,Feedback,Exams,Students
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

@admin.route('/newstudent')
def newstudent():
    return render_template('admin/newstudent.html',title='Pariksha-Admin')

@admin.route('/teachers')
def teachers():
    return render_template('admin/teachers.html',title='Pariksha-Admin')

@admin.route('/newteacher')
def newteacher():
    return render_template('admin/newteacher.html',title='Pariksha-Admin')