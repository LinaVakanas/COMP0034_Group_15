# Authors: Mahdi Shah & Lina Vakanas

# # These are models which had initially been made but could not be implemented due to a lack of time. They would be
# # implemented as xtensions if further time was to be given.
#
# class Teacher(db.Model):
#     __tablename__ = 'teacher'
#     teacher_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     school_id = db.Column(db.Integer, nullable=False)
#     first_name = db.Column(db.String, nullable=False)
#     last_name = db.Column(db.String, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
#
#
# class Report(db.Model):
#     __tablename__ = 'report'
#     report_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
#     content = db.Column(db.Text)
#     type = db.Column(db.Boolean, nullable=False)
#     creation_date = db.Column(db.String, nullable=False)
#
#
# class Message(db.Model):
#     __tablename__ = 'message'
#     message_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     time_sent = db.Column(db.String, nullable=False)
#     content = db.Column(db.String(300), nullable=False)
#     attachments = db.Column(db.BLOB)
#     chatroom_id = db.Column(db.Integer, db.ForeignKey('chatroom.chatroom_id'), nullable=False)
#     chatroom = db.relationship("Chatroom", foreign_keys=[chatroom_id])
#     user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
#
#
# class Chatroom(db.Model):
#     __tablename__ = 'chatroom'
#     chatroom_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     creation_date = db.Column(db.String, nullable=False)
#     pair_id = db.Column(db.Integer, db.ForeignKey('pair.id'), nullable=False)
#
#
# class StudentReview(db.Model):
#     __tablename__ = 'student_review'
#     review_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     content = db.Column(db.String)
#     attachment = db.Column(db.BLOB, nullable=False)
#     teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.teacher_id'), nullable=False)
#     teacher = db.relationship("Teacher", foreign_keys=[teacher_id])
#     student_id = db.Column(db.Integer, db.ForeignKey('mentee.mentee_id'), nullable=False)
#     student = db.relationship("Mentee", foreign_keys=[student_id])
#
#
# # Same as current one, except for additional 'bio' and 'profile_picture'
# class User(UserMixin, db.Model):
#     __tablename__ = 'user'
#     email = db.Column(db.Text, nullable=False, unique=True)
#     user_type = db.Column(db.String, nullable=False)
#     user_id = db.Column(db.Integer,autoincrement=True, primary_key=True)
#     school_id = db.Column(db.Integer, nullable=False)
#     password = db.Column(db.String)
#     bio = db.Column(db.String(300))
#     is_active = db.Column(db.Boolean)
#     profile_pic = db.Column(db.BLOB)
#     creation_date = db.Column(db.String)