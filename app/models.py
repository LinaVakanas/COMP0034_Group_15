from app import db
## PUT CHARACTER LIMITS IN! ##


class Mentor(db.Model):
    __tablename__ = 'mentor'
    school_id = db.Column(db.Integer, db.ForeignKey('school.school_id'), nullable=False)
    school = db.relationship("School", foreign_keys=[school_id])
    user_type = db.Column(db.Integer, db.ForeignKey('user.user_type'), nullable=False)
    type = db.relation("User", foreign_keus=[user_type])
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    unique_id = db.relationship("User", foreign_keys=[user_id])
    email = db.Column(db.Text, db.ForeignKey('user.email'), nullable=False)
    user_email = db.relationship("User", foreign_keys=[email])


class School(db.Model):
    school_status = db.Column(db.Boolean, nullable=False)
    school_id = db.Column(db.Integer, nullable=False)
    school_name = db.Column(db.Text, nullable=False)
    school_email = db.Column(db.Text, db.ForeignKey('user.email'), nullable=False)
    email = db.relationship("User", foreign_keys=[school_email])
    ofsted_ranking = db.Column(db.Integer)
    ofsted_report = db.Column(db.BLOB) #not sure about how blob works


class User(db.Model):
    email = db.Column(db.Text, nullable=False, primary_key=True)
    user_type = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    password = db.Column(db.Text, nullable=False) #we can look at how Miss did that hash thing in her example
    bio = db.Column(db.String(300))
    active = db.Column(db.Boolean)
    profile_pic = db.Column(db.BLOB) #don't know if its acc blob
    creation_date = db.Column(db.String)


class Report(db.Model):
    report_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=)
    unique_id = db.relationship("User", foreign_keys=[user_id])
    content = db.Column(db.Text)
    type = db.Column(db.Boolean, nullable=False)
    creation_date = db.Column(db.String, nullable=False)


class Message(db.Model):
    message_id = db.Column(db.Integer, nullable=False, primary_key=True)
    time_sent = db.Column(db.String, nullable=False)
    content = db.Column(db.String(300), nullable=False)
    attachments = db.Column(db.BLOB)
    chatroom_id = db.Column(db.Integer, db.ForeignKey('chatroom.chatroom_id'), nullable=False)
    chatroom = db.relationship("Chatroom", foreign_keys=[chatroom_id])
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=)
    unique_id = db.relationship("User", foreign_keys=[user_id])


class Chatroom(db.Model):
    chatroom_id = db.Column(db.Integer, primary_key=True, nullable=False)
    creation_date = db.Column(db.String, nullable=False)
    pair_id = db.Column(db.Integer, db.ForeignKey('pair.pair_id'), nullable=False)
    pair = db.relationship("Pair", foreign_keus=[pair_id])


class Pair(db.Model):
    pair_id = db.Column(db.Integer, primary_key=True, nullable=False)
    mentor_id = db.Column(db.Integer, db.ForeignKey('mentor.user_id'), nullable=False)
    mentor = db.relationship("Mentor", foreign_keys=[mentor_id])
    mentee_id = db.Column(db.Integer, db.ForeignKey('mentee.user_id'), nullable=False)
    mentee = db.relationship("Mentee", foreign_keys=[mentee_id])


class PersonalInfo(db.Model):
    form_id = db.Column(db.Integer, primary_key=True, nullable=False)
    carer_email = db.Column(db.String, nullable=False)
    carer_name = db.Column(db.String, nullable=False)
    ## personality ##
    share_performance = db.Column(db.Boolean)
    status = db.Column(db.String(1))
    xperience = db.Column(db.String(3), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=)
    unique_id = db.relationship("User", foreign_keys=[user_id])


class PersonalIssues(db.Column):
    form_id = foreign key
    user_id = foreign key
    share_personal_issues = db.Column(db.Boolean, nullable=False)


class Hobbies(db.Column):
    form_id = foreign key
    user_id = foreign key



class MedicalCond(db.Model):
    share_med_cond = db.Column(db.Boolean, nullable=False)
    form_id = foreign key
    user_id = foreign key


class OccupationalField(db.Model):
    occupation_id = db.Column(db.Integer, primary_key=True, nullable=False)
    form_id = db.Column(db.Integer, db.ForeignKey('personalinfo.form_id'), nullable=False)
    form = db.relationship("PersonalInfo", foreign_keys=[form_id])
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    unique_id = db.relationship("User", foreign_keys=[user_id])
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


class StudentReview(db.Model):
    review_id = db.Column(db.Integer, nullable=False, primary_key=True)
    content = db.Column(db.String)
    attachment = db.Column(db.BLOB, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.teacher_id'), nullable=)
    teacher = db.relationship("Teacher", foreign_keys=[teacher_id])
    student_id = db.Column(db.Integer, db.ForeignKey('mentee.user_id'), nullable=)
    student = db.relationship("Mentee", foreign_keys=[student_id])
