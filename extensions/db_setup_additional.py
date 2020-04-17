# Authors: Mahdi Shah & Lina Vakanas

# # These are SQLite tables which had initially been made but could not be implemented due to a lack of time. They would
# # be implemented as extensions if further time was to be given.
#
# c.execute('''
#           CREATE TABLE user
#           (user_id INTEGER PRIMARY KEY,
#           email TEXT UNIQUE NOT NULL,
#           user_type TEXT NOT NULL,
#           school_id INTEGER NOT NULL,
#           password TEXT NOT NULL,
#           bio VARCHAR(300),
#           is_active BOOLEAN,
#           profile_pic BLOB,
#           creation_date TEXT)
#           ''')
#
#
# c.execute('''
#           CREATE TABLE teacher
#           (teacher_id INTEGER PRIMARY KEY,
#           school_id INTEGER NOT NULL,
#           first_name TEXT NOT NULL,
#           last_name TEXT NOT NULL,
#           user_id INTEGER NOT NULL,
#           email TEXT NOT NULL,
#           FOREIGN KEY (user_id) REFERENCES user(user_id))
#           ''')
#
#
# c.execute('''
#           CREATE TABLE report
#           (report_id INTEGER PRIMARY KEY,
#           content TEXT,
#           type BOOLEAN NOT NULL ,
#           creation_date TEXT NOT NULL,
#           user_id INTEGER NOT NULL )
#           ''')
#
#
# c.execute('''
#           CREATE TABLE chatroom
#           (chatroom_id INTEGER PRIMARY KEY,
#           pair_id INTEGER NOT NULL,
#           creation_date TEXT NOT NULL,
#           user_id INTEGER NOT NULL,
#            FOREIGN KEY (pair_id) REFERENCES pair(id) )
#           ''')
#
#
# c.execute('''
#           CREATE TABLE message
#           (message_id INTEGER PRIMARY KEY,
#           time_sent TEXT NOT NULL,
#           content VARCHAR(300) NOT NULL,
#           attachments BLOB,
#           chatroom_id INTEGER NOT NULL,
#           user_id INTEGER NOT NULL,
#           FOREIGN KEY (chatroom_id) REFERENCES chatroom(chatroom_id))
#           ''')
#
#
# c.execute('''
#           CREATE TABLE student_review
#           (review_id INTEGER PRIMARY KEY,
#           content TEXT,
#           attachment BLOB NOT NULL,
#           teacher_id INTEGER NOT NULL REFERENCES teacher(teacher_id),
#           student_id INTEGER NOT NULL REFERENCES mentee(mentee_id),
#           user_id INTEGER NOT NULL,
#           FOREIGN KEY (user_id) REFERENCES user(user_id))
#           ''')