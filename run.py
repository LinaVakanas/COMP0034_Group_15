# Authors: Mahdi Shah & Lina Vakanas

from switchapp import create_app

app = create_app()
app.app_context().push()

if __name__ == '__main__':
    app.run()
