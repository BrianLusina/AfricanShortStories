from flask import render_template, Flask
from config import config
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from datetime import datetime

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
mail = Mail()


def create_app(config_name):
    """
    Defines a new application WSGI
    :param config_name:
    :return: the WSGI Flask object
    """
    app = Flask(__name__, template_folder='templates', static_folder="static")

    # configurations
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # initialize the db and login manager
    db.init_app(app)
    login_manager.init_app(app)

    # initialize the app with flask mail
    mail.init_app(app)

    error_handlers(app)
    request_handlers(app, db)
    register_blueprints(app)
    return app


def error_handlers(app):
    """
    Error handlers for the app
    :param app: The app object
    """

    # Error handler for page not found
    @app.errorhandler(404)
    def not_found(error):
        return render_template('errorpages/404.html', user=current_user)

    @app.errorhandler(403)
    def error_403(error):
        return render_template("errorpages/403.html", user=current_user)

    @app.errorhandler(403)
    def error_500(error):
        return render_template("errorpages/500.html", user=current_user)

    @app.errorhandler(400)
    def not_found(error):
        return render_template('errorpages/400.html', user=current_user)


def request_handlers(app, db):
    """
    Handles requests sent by the application
    :param app: the current application
    :return:
    """

    @app.before_request
    def before_request():
        """
        Before submitting the request, change the currently logged in user 'last seen' status to now
        """
        if current_user.is_authenticated:
            current_user.last_seen = datetime.now()
            db.session.add(current_user)
            db.session.commit()

    # @app.after_request
    # def after_request(response):
    #     for query in get_debug_queries():
    #         if query.duration >= DATABASE_QUERY_TIMEOUT:
    #             app.logger.warning(
    #                 "SLOW QUERY: %s\nParameters: %s\nDuration: %fs\nContext: %s\n" %
    #                 (query.statement, query.parameters, query.duration,
    #                  query.context))
    #     return response


def register_blueprints(app):
    """
    Registers tall blueprints in the app
    :param app: The current flask application
    :return:
    """
    from app.mod_home import home_module
    from app.mod_story.views import story_module
    from app.mod_auth import auth
    from app.mod_dashboard import dashboard

    app.register_blueprint(home_module)
    app.register_blueprint(story_module)
    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
