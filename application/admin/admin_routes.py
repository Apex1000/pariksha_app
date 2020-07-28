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
admins = Blueprint('admins',__name__,
                    template_folder='templates',
                    static_folder='static/admin',
                    url_prefix='/admin'
                    )

@admins.route('/')
def admin():
    return render_template('admin/admin.html')