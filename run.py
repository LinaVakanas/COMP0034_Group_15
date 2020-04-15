from flask import Flask
from app import create_app, db

app = create_app('config.TestConfig')
app.app_context().push()
app.secret_key='blahblahblahblah'

if __name__ == '__main__':
    app.run()
