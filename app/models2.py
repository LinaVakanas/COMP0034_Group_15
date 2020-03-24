from app import db


class User(db.Model):
    __tablename__ = "user"
    email = db.Column(db.Text, nullable=False, unique=True)
    user_type = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    school_id = db.Column(db.Integer, nullable=False)
    password = db.Column(db.Text, nullable=False) #we can look at how Miss did that hash thing in her example
    bio = db.Column(db.String(300))
    active = db.Column(db.Boolean)
    profile_pic = db.Column(db.BLOB) #don't know if its acc blob
    creation_date = db.Column(db.String)

    # defining relationships
    reports = db.relationship('Report', backref='user')
    personal_info = db.relationship('PersonalInfo', backref='user')
    personal_issues = db.relationship('PersonalIssues', backref='user')
    hobbies = db.relationship('Hobbies', backref='user')
    medical_conds = db.relationship('MedicalCond', backref='user')
    occupation = db.relationship('OccupationalField', backref='user')
    location = db.relationship('Location', backref='user')

    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": user_type
    }


class Mentor(User):
    __tablename__ = 'mentor'
    mentor_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    paired_status = db.Column(db.Boolean, nullable=False)
    # unique_id = db.relationship("User", foreign_keys=[user_id])

    __mapper_args__ = {
        "polymorphic_identity": "mentor"
    }


class Mentee(User):
    __tablename__ = 'mentee'
    mentee_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    user_id = db.Column(None, db.ForeignKey('user.user_id'))
    paired_status = db.Column(db.Boolean, nullable=False)
    # unique_id = db.relationship("User", foreign_keys=[user_id])

    __mapper_args__ = {
        "polymorphic_identity": "mentee"
    }


class Teacher(User):
    __tablename__ = 'teacher'
    teacher_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    # unique_id = db.relationship("User", foreign_keys=[user_id])
    # relationships
    student_reviews = db.relationship('StudentReview', backref='teachers')


class School(db.Model):
    __tablename__ = 'school'
    school_status = db.Column(db.Boolean, nullable=False)
    school_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    school_name = db.Column(db.Text, nullable=False)
    school_email = db.Column(db.Text, db.ForeignKey('user.email'), nullable=False)
    email = db.relationship("User", foreign_keys=[school_email])
    ofsted_ranking = db.Column(db.Integer)
    ofsted_report = db.Column(db.BLOB) #not sure about how blob works


class Report(db.Model):
    __tablename__ = 'report'
    report_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id), nullable=False)
    # unique_id = db.relationship("User", foreign_keys=[user_id])
    content = db.Column(db.Text)
    type = db.Column(db.Boolean, nullable=False)
    creation_date = db.Column(db.String, nullable=False)


class Message(db.Model):
    __tablename__ = 'message'
    message_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    time_sent = db.Column(db.String, nullable=False)
    content = db.Column(db.String(300), nullable=False)
    attachments = db.Column(db.BLOB)
    chatroom_id = db.Column(db.Integer, db.ForeignKey('chatroom.chatroom_id'), nullable=False)
    chatroom = db.relationship("Chatroom", foreign_keys=[chatroom_id])
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    # unique_id = db.relationship("User", foreign_keys=[user_id])


class Chatroom(db.Model):
    __tablename__ = 'chatroom'
    chatroom_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    creation_date = db.Column(db.String, nullable=False)
    pair_id = db.Column(db.Integer, db.ForeignKey('pair.pair_id'), nullable=False)
    # pair = db.relationship("Pair", foreign_keys=[pair_id])


class Pair(db.Model):
    pair_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    mentor_id = db.Column(db.Integer, db.ForeignKey('mentor.mentor_id'), nullable=False)
    # mentor = db.relationship("Mentor", foreign_keys=[mentor_id])
    mentee_id = db.Column(db.Integer, db.ForeignKey('mentee.mentee_id'), nullable=False)
    # mentee = db.relationship("Mentee", foreign_keys=[mentee_id])

    # relationships
    mentor = db.relationship("Mentor", backref="pair")
    mentee = db.relationship("Mentee", backref="pair")


class PersonalInfo(db.Model):
    __tablename__ = 'personal_info'
    form_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    carer_email = db.Column(db.String, nullable=False)
    carer_name = db.Column(db.String, nullable=False)
    ## personality ##
    share_performance = db.Column(db.Boolean)
    status = db.Column(db.String(1))
    xperience = db.Column(db.String(3), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id), nullable=False)
    # unique_id = db.relationship("User", foreign_keys=[user_id])


class PersonalIssues(db.Model):
    __tablename__ = 'personal_issues'
    form_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    # unique_id = db.relationship("User", foreign_keys=[user_id])
    depression = db.Column(db.Boolean)
    self_harm = db.Column(db.Boolean)
    family = db.Column(db.Boolean)
    drugs = db.Column(db.Boolean)
    ed = db.Column(db.Boolean)
    share_personal_issues = db.Column(db.Boolean, nullable=True)


class Hobbies(db.Model):
    __tablename__ = 'hobbies'
    form_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    # unique_id = db.relationship("User", foreign_keys=[user_id])
    football = db.Column(db.Boolean)
    drawing = db.Column(db.Boolean)


class MedicalCond(db.Model):
    __tablename__ = 'medical_condition'
    form_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    cond1 = db.Column(db.Boolean)
    share_med_cond = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    # unique_id = db.relationship("User", foreign_keys=[user_id])


class OccupationalField(db.Model):
    __tablename__ = 'occupational_field'
    occupation_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # form_id = db.Column(db.Integer, db.ForeignKey('personalinfo.form_id'), nullable=False)
    # form = db.relationship("PersonalInfo", foreign_keys=[form_id])
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    # unique_id = db.relationship("User", foreign_keys=[user_id])
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


class StudentReview(db.Model):
    __tablename__ = 'student_review'
    review_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    content = db.Column(db.String)
    attachment = db.Column(db.BLOB, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey(Teacher.teacher_id), nullable=False)
    student = db.relationship("Mentee", backref="student_review")
    student_id = db.Column(db.Integer, db.ForeignKey(Mentee.mentee_id), nullable=False)


class Location(db.Model):
    __tablename__ = 'location'
    form_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id), nullable=False)
    address = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    postcode = db.Column(db.String, nullable=False)
    avoid_area = db.Column(db.String)
    user_type = db.Column(db.String)
