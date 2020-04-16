from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    email = db.Column(db.Text, nullable=False, unique=True)
    user_type = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer,autoincrement=True, primary_key=True)
    school_id = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String)
    bio = db.Column(db.String(300))
    is_active = db.Column(db.Boolean)
    profile_pic = db.Column(db.BLOB)
    creation_date = db.Column(db.String)

    def get_id(self):
        return self.user_id

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    user = db.relationship("User", backref='admin')


class Mentor(db.Model):
    __tablename__ = 'mentor'
    mentor_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    school_id = db.Column(db.Integer, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    user = db.relationship("User", backref='mentor')
    paired = db.Column(db.Boolean)
    is_approved = db.Column(db.Boolean)


class Mentee(db.Model):
    __tablename__ = 'mentee'
    mentee_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school.school_id'), nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    user = db.relationship("User", backref='mentee')
    paired = db.Column(db.Boolean)


class School(db.Model):
    __tablename__ = 'school'
    is_approved = db.Column(db.Boolean, nullable=False)
    school_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    school_name = db.Column(db.Text, nullable=False)
    school_email = db.Column(db.Text, nullable=False)
    ofsted_ranking = db.Column(db.Integer)
    ofsted_report = db.Column(db.BLOB) #not sure about how blob works


class Pair(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    mentor_id = db.Column(db.Integer, db.ForeignKey('mentor.mentor_id'), nullable=False)
    mentor = db.relationship("Mentor", backref='pair')
    mentee_id = db.Column(db.Integer, db.ForeignKey('mentee.mentee_id'), nullable=False)
    mentee = db.relationship("Mentee", backref='pair')
    meetings = db.relationship('Meeting', backref='pair')
    creation_date = db.Column(db.String)


class PersonalInfo(db.Model):
    __tablename__ = 'personal_info'
    form_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    carer_email = db.Column(db.String, nullable=False)
    carer_name = db.Column(db.String, nullable=False)
    ## personality ##
    share_performance = db.Column(db.Boolean)
    status = db.Column(db.String(1))
    xperience = db.Column(db.String(3), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    user = db.relationship("User", backref='personal_info')
    share_personal_issues = db.Column(db.Boolean, nullable=True)


class PersonalIssues(db.Model):
    __tablename__ = 'personal_issues'
    form_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    user = db.relationship("User", backref='personal_issues')
    depression = db.Column(db.Boolean)
    self_harm = db.Column(db.Boolean)
    family = db.Column(db.Boolean)
    drugs = db.Column(db.Boolean)
    ed = db.Column(db.Boolean)


class Hobbies(db.Model):
    __tablename__ = 'hobbies'
    form_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    user = db.relationship("User", backref='hobbies')
    football = db.Column(db.Boolean)
    drawing = db.Column(db.Boolean)


class OccupationalField(db.Model):
    __tablename__ = 'occupational_field'
    occupation_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    user = db.relationship("User", backref='occupational_field')
    eng = db.Column(db.Boolean)
    maths = db.Column(db.Boolean)
    med = db.Column(db.Boolean)
    pharm = db.Column(db.Boolean)
    chem = db.Column(db.Boolean)
    phys = db.Column(db.Boolean)
    bio = db.Column(db.Boolean)
    law = db.Column(db.Boolean)
    finance = db.Column(db.Boolean)
    hist = db.Column(db.Boolean)
    geo = db.Column(db.Boolean)
    engl = db.Column(db.Boolean)


class Location(db.Model):
    __tablename__ = 'location'
    form_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    user = db.relationship("User", backref='location')
    address = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    postcode = db.Column(db.String, nullable=False)
    avoid_area = db.Column(db.String)


class Meeting(db.Model):
    __tablename__ = 'meeting'
    meeting_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    pair_id = db.Column(db.Integer, db.ForeignKey('pair.id'))
    # time-related
    date = db.Column(db.String(10), unique=True)
    time = db.Column(db.String(5))
    duration = db.Column(db.String(3), nullable=False)
    # location-related
    address = db.Column(db.String, nullable=True)
    postcode = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    # approvals
    school_approval = db.Column(db.Boolean)
    mentee_approval = db.Column(db.Integer)



