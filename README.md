###Group 15 COMP0034###

The SQLite database, webapp_sqlite, has been provided along with the python file to create it, db_setup.py.
Within the __init__.py file, the initial_setup() function is used to create the admin and school 0 which is required
for full usage of the app.
When running the app normally, please uncomment db.create_all() and initial_setup().
If you would like to manually test the different features of the site, we recommend uncommenting db.drop_all() and 
populate_db() as well. populate_db() will fill the database with users at different stages of their applications.
Please see populate_db.py for more information on the users.

If you would like to run the unittests, please uncomment db.drop_all() and db.create_all(), 
and comment out populate_db() and initial_setup().

GitHub repository: https://github.com/LinaVakanas/COMP0034_Group_15.git

-------------------------------
References to images:
tick.png : https://loading.io/icon/7cz5z4 
search.png: https://loading.io/icon/s7te3x 
user_icon.ong: https://loading.io/icon/jrijl4 