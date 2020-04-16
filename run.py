from app import create_app

app = create_app()
app.app_context().push()
# app.secret_key = 'bcd471dde8f8bb966fe9dd6c5d284b74'

if __name__ == '__main__':
    app.run()
