import sqlite3

# Create a connection object that represents the database
conn = sqlite3.connect('webapp_sqlite.db')

# Step 2: Create a cursor object
c = conn.cursor()

# Step 3: Create the person and address tables


c.execute('''
          CREATE TABLE user
          (user_id INTEGER PRIMARY KEY,
          email TEXT UNIQUE NOT NULL,
          user_type TEXT NOT NULL,
          school_id INTEGER NOT NULL,
          password TEXT NOT NULL,
          is_active BOOLEAN,
          creation_date TEXT)
          ''')

c.execute('''
          CREATE TABLE admin
          (admin_id INTEGER PRIMARY KEY,
          user_id INTEGER,
          FOREIGN KEY (user_id) REFERENCES user(user_id))
          ''')

c.execute('''
          CREATE TABLE mentor
          (mentor_id INTEGER PRIMARY KEY,
          school_id INTEGER NOT NULL,
          first_name TEXT NOT NULL, 
          last_name TEXT NOT NULL,
          user_id INTEGER NOT NULL,
          paired BOOLEAN,
          is_approved BOOLEAN,
          FOREIGN KEY (user_id) REFERENCES user(user_id))
          ''')

c.execute('''
          CREATE TABLE mentee
          (mentee_id INTEGER PRIMARY KEY,
          school_id INTEGER NOT NULL,
          first_name TEXT NOT NULL, 
          last_name TEXT NOT NULL,
          user_id INTEGER NOT NULL,
          paired BOOLEAN,
          FOREIGN KEY (user_id) REFERENCES user(user_id),
          FOREIGN KEY (school_id) REFERENCES school(school_id))
          ''')


c.execute('''
          CREATE TABLE school
          (school_id INTEGER PRIMARY KEY,
          is_approved BOOLEAN NOT NULL ,
          school_name TEXT NOT NULL,
          school_email TEXT NOT NULL,
          ofsted_ranking INTEGER,
          ofsted_report BLOB)
          ''')


c.execute('''
          CREATE TABLE pair
          (id INTEGER PRIMARY KEY,
          creation_date TEXT NOT NULL,
          mentor_id INTEGER NOT NULL,
          mentee_id INTEGER NOT NULL,
          FOREIGN KEY (mentor_id) REFERENCES mentor(mentor_id),
          FOREIGN KEY (mentee_id) REFERENCES mentee(mentee_id)
          )
          ''')


c.execute('''
          CREATE TABLE personal_info
          (form_id INTEGER PRIMARY KEY,
          carer_email TEXT NOT NULL,
          carer_name TEXT NOT NULL,
          share_performance BOOLEAN,
          share_personal_issues BOOLEAN,
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
          CREATE TABLE location
          (form_id INTEGER PRIMARY KEY,
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

c.execute('''
          CREATE TABLE meeting
          (meeting_id INTEGER PRIMARY KEY,
          duration TEXT,
          date TEXT,
          time TEXT,
          address TEXT,
          postcode TEXT,
          type TEXT,
          mentee_approval INTEGER,
          teacher_approval INTEGER,
          user_id INTEGER NOT NULL,
          FOREIGN KEY (user_id) REFERENCES user(user_id))
          ''')


conn.commit()
conn.close()


