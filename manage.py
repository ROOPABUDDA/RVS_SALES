import app
import flask

application = app.create_app()


if __name__ == '__main__':
    application.run()