from flask import Flask
from flask_bootstrap import Bootstrap

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')

    with app.app_context():

        from app.main import bp as bp_main
        app.register_blueprint(bp_main)

        return app