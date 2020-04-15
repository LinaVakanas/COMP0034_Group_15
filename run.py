from app import create_app

app = create_app('config.TestConfig')
app.app_context().push()
app.secret_key = '5630f31ff36f2368'

if __name__ == '__main__':
    app.run()
