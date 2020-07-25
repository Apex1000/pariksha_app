from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Exams(db.Model):
    __tablename__ = 'exams'
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
    __tablename__ = 'questions'
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
    __tablename__ = 'students'
    exam_id = db.Column(db.Integer)
    student_id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(50))
    rollno = db.Column(db.String(50))
    branch = db.Column(db.String(50))

class AnswerSheet(db.Model):
    __tablename__ = 'answersheet'
    exam_id = db.Column(db.Integer)
    answersheet_id = db.Column(db.Integer, primary_key=True)
    rollno = db.Column(db.String(50))
    answer = db.Column(db.String(5000))
    grade = db.Column(db.String(50))
class Feedback(db.Model):
    __tablename__ = 'feedback'
    feedback_id = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String(50))
    msg = db.Column(db.String(5000))

class User(UserMixin, db.Model):
    """User account model."""
    __tablename__ = 'login-users'
    
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(100),
        nullable=False,
        unique=False
    )
    email = db.Column(
        db.String(40),
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.String(200),
        primary_key=False,
        unique=False,
        nullable=False
	)
    

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(
            password,
            method='sha256'
        )

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)    