from flask import Flask
# from flask_bootstrap import Bootstrap
# from flask_mail import Mail
# from flask_moment import Moment

# from flask_sqlalchemy import SQLAlchemy
# from config import config

# bootstrap = Bootstrap()
# mail = Mail()
# moment = Moment()
# db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    # app.config.from_object(config[config_name])
    # config[config_name].init_app(app)

    # bootstrap.init_app(app)
    # mail.init_app(app)
    # moment.init_app(app)
    # db.init_app(app)

    # attach routes and custom error pages here

    from .heidy.views import heidy
    from .bf.views import bf
    from .onlyall.models import Todo
    from .onlyall.views import onlyall
    from .tagger.views import tagger

    Todo.create_table(fail_silently=True)

    app.register_blueprint(heidy, url_prefix='/heidy')
    app.register_blueprint(bf, url_prefix='/bf')
    app.register_blueprint(onlyall, url_prefix='/onlyall')
    app.register_blueprint(tagger, url_prefix='/tagger')

    return app

