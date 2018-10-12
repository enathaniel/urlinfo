import os
from flask import Flask, jsonify, request
from . import config

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    config.configure_app(app)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # initialize database
    from database import db
    db.initialize(app)

    from endpoint import resource_urlinfo
    app.register_blueprint(resource_urlinfo.bp)

    return app