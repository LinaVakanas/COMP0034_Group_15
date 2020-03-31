import sqlite3

# Step 1: Create a connection object that represents the database
conn = sqlite3.connect('webapp_sqlite.db')

# Step 2: Create a cursor object
c = conn.cursor()

# Step 3: Create the person and address tables

c.execute('''
          CREATE TABLE user
          (user_id INTEGER PRIMARY KEY,
          email TEXT NOT NULL,
          user_type TEXT NOT NULL,
          school_id INTEGER NOT NULL,
          password TEXT NOT NULL,
          bio VARCHAR(300),
          active BOOLEAN,
          profile_pic BLOB,
          creation_date TEXT)
          ''')

c.execute('''
          CREATE TABLE mentor
          (mentor_id INTEGER PRIMARY KEY,
          school_id INTEGER NOT NULL,
          first_name TEXT NOT NULL, 
          last_name TEXT NOT NULL,
          user_id INTEGER NOT NULL,
          paired BOOLEAN,
          FOREIGN KEY (user_id) REFERENCES user(user_id))
          ''')

c.execute('''
          CREATE TABLE mentee
          (mentee_id INTEGER PRIMARY KEY,
          school_id INTEGER NOT NULL,
          first_name TEXT NOT NULL, 
          last_name TEXT NOT NULL,
          user_id INTEGER NOT NULL,
          paired BOOL,
          FOREIGN KEY (user_id) REFERENCES user(user_id))
          ''')

c.execute('''
          CREATE TABLE teacher
          (teacher_id INTEGER PRIMARY KEY,
          school_id INTEGER NOT NULL,
          first_name TEXT NOT NULL, 
          last_name TEXT NOT NULL,
          user_id INTEGER NOT NULL,
          email TEXT NOT NULL,
          FOREIGN KEY (user_id) REFERENCES user(user_id))
          ''')

c.execute('''
          CREATE TABLE school
          (school_id INTEGER PRIMARY KEY,
          school_status BOOLEAN NOT NULL ,
          school_name TEXT NOT NULL,
          school_email TEXT NOT NULL,
          email TEXT NOT NULL,
          ofsted_ranking INTEGER,
          ofsted_report BLOB,
          FOREIGN KEY (school_email) REFERENCES user(email))
          ''')

c.execute('''
          CREATE TABLE report
          (report_id INTEGER PRIMARY KEY,
          content TEXT,
          type BOOLEAN NOT NULL ,
          creation_date TEXT NOT NULL,
          user_id INTEGER NOT NULL )
          ''')

c.execute('''
          CREATE TABLE pair
          (pair_id INTEGER PRIMARY KEY,
          creation_date TEXT NOT NULL,
          mentor_id INTEGER NOT NULL,
          mentee_id INTEGER NOT NULL,
          FOREIGN KEY (mentor_id) REFERENCES mentor(mentor_id),
          FOREIGN KEY (mentee_id) REFERENCES mentee(mentee_id)
          )
          ''')

c.execute('''
          CREATE TABLE chatroom
          (chatroom_id INTEGER PRIMARY KEY,
          pair_id INTEGER NOT NULL,
          creation_date TEXT NOT NULL,
          user_id INTEGER NOT NULL,
           FOREIGN KEY (pair_id) REFERENCES pair(pair_id) )
          ''')

c.execute('''
          CREATE TABLE message
          (message_id INTEGER PRIMARY KEY,
          time_sent TEXT NOT NULL,
          content VARCHAR(300) NOT NULL,
          attachments BLOB,
          chatroom_id INTEGER NOT NULL,
          user_id INTEGER NOT NULL,
          FOREIGN KEY (chatroom_id) REFERENCES chatroom(chatroom_id))
          ''')

c.execute('''
          CREATE TABLE personal_info
          (form_id INTEGER PRIMARY KEY,
          carer_email TEXT NOT NULL,
          carer_name TEXT NOT NULL,
          share_performance BOOLEAN,
          status VARCHAR(1),
          xperience VARCHAR(3),
          user_id INTEGER NOT NULL,
          FOREIGN KEY (user_id) REFERENCES user(user_id))
          ''')

c.execute('''
          CREATE TABLE personal_issues
          (form_id INTEGER PRIMARY KEY,
          depression BOOLEAN,
          self_harm BOOLEAN,
          family BOOLEAN,
          drugs BOOLEAN,
          ed BOOLEAN,
          share_personal_issues BOOLEAN,
          user_id INTEGER NOT NULL,
          FOREIGN KEY (user_id) REFERENCES user(user_id))
          ''')

c.execute('''
          CREATE TABLE medical_cond
          (form_id INTEGER PRIMARY KEY,
          cond1 BOOLEAN,
          share_med_cond BOOLEAN,
          user_id INTEGER NOT NULL,
          FOREIGN KEY (user_id) REFERENCES user(user_id))
          ''')

c.execute('''
          CREATE TABLE occupational_field
          (occupation_id INTEGER PRIMARY KEY,
          eng BOOLEAN,
          maths BOOLEAN,
          med BOOLEAN,
          pharm BOOLEAN,
          chem BOOLEAN,
          phys BOOLEAN,
          bio BOOLEAN,
          law BOOLEAN,
          finance BOOLEAN,
          hist BOOLEAN,
          geo BOOLEAN,
          engl BOOLEAN,
          user_id INTEGER NOT NULL,
          FOREIGN KEY (user_id) REFERENCES user(user_id))
          ''')

c.execute('''
          CREATE TABLE student_review
          (review_id INTEGER PRIMARY KEY,
          content TEXT,
          attachment BLOB NOT NULL,
          teacher_id INTEGER NOT NULL REFERENCES teacher(teacher_id),
          student_id INTEGER NOT NULL REFERENCES mentee(mentee_id),
          user_id INTEGER NOT NULL,
          FOREIGN KEY (user_id) REFERENCES user(user_id))
          ''')

c.execute('''
          CREATE TABLE location
          (occupation_id INTEGER PRIMARY KEY,
          address TEXT NOT NULL,
          city TEXT NOT NULL,
          postcode TEXT NOT NULL,
          avoid_area TEXT,
          user_id INTEGER NOT NULL,
          FOREIGN KEY (user_id) REFERENCES user(user_id))
          ''')

c.execute('''
          CREATE TABLE hobbies
          (form_id INTEGER PRIMARY KEY,
          football BOOLEAN,
          drawing BOOLEAN,
          user_id INTEGER NOT NULL,
          FOREIGN KEY (user_id) REFERENCES user(user_id))
          ''')