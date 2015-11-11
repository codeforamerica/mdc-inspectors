# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import os
import sys
import logging

from flask import Flask, render_template
from werkzeug.utils import import_string

from inspectors.settings import ProdConfig
from inspectors.assets import assets
from inspectors.extensions import (
    bcrypt,
    cache,
    db,
    ma,
    login_manager,
    migrate,
    debug_toolbar,
    mail
)
from inspectors import (registration, inspections, surveys)


def create_app():
    """An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/
    """
    config_string = os.environ.get('CONFIG', 'inspectors.settings.ProdConfig')
    config = import_string(config_string)
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_logging(app)
    return app


def register_extensions(app):
    assets.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    return None


def register_blueprints(app):
    app.register_blueprint(registration.views.blueprint)
    app.register_blueprint(surveys.views.blueprint)
    return None


def register_errorhandlers(app):
    def render_error(error):
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template("{0}.html".format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None

def register_logging(app):
    app.logger.removeHandler(app.logger.handlers[0])
    app.logger.setLevel(logging.DEBUG)
    stdout = logging.StreamHandler(sys.stdout)
    stdout.setFormatter(logging.Formatter(
    '''-------------------------------
%(asctime)s | %(name)s | %(levelname)s in %(module)s: %(message)s'''))
    app.logger.addHandler(stdout)
    return None
