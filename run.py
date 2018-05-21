# import os
from app import create_app
from flask import render_template
from datetime import datetime
from humanfriendly import format_size
from config import CONFIG

CONFIG.parse()
# from app.models import User, Role
# from flask_migrate import Migrate

# app = create_app(os.getenv('FLASK_CONFIG') or 'default')
# migrate = Migrate(app, db)

# @app.shell_context_processor
# def make_shell_context():
#     return dict(db=db, User=User, Role=Role)
app = create_app(None)

@app.template_filter('strf')
def strf(date):
    if date:
        return datetime.strftime(date, "%Y %b %d")
    else:
        return ""

@app.template_filter('strf2')
def strf2(date):
    if date:
        return datetime.strftime(date, "%y %b %d %H:%M")
    else:
        return ""

@app.template_filter('humanfriendly')
def humanfriendly(size):
    return format_size(size)

@app.route("/")
def main():
    return render_template('main.html')


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

print(CONFIG['debug'])
app.run(debug=CONFIG['debug'])
# app.run()
