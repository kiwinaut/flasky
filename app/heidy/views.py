from flask import Blueprint, render_template, request
# from jinja2 import TemplateNotFound
from tinydb import TinyDB
from config import CONFIG

# def show(page):
#     try:
#         # return render_template('pages/%s.html' % page)
#         return main.root_path
#     except TemplateNotFound:
#         abort(404)



heidy = Blueprint('heidy', __name__, static_folder='%s/persistent/heidy'%CONFIG['mount'], static_url_path='/imgs')
DBPATH ='%s/persistent/heidy/heidy_check.json'%CONFIG['mount']


@heidy.route("", methods=["GET"])
def list():
    print(DBPATH)
    db = TinyDB(DBPATH)
    # all = db.all()
    table = db.table('sets')
    all=table.all()
    # c = table.all()
    def chunks(l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]

    db.close()
    return render_template('heidy_check.html', all=chunks(all,40), folder='sets')

@heidy.route("/<int:index>", methods=["PUT"])
def update(index):
    s = str(request.form.get('status'))
    db = TinyDB(DBPATH)
    table = db.table('sets')
    res = table.update({'status': s}, doc_ids=[index])
    return(str(res))



@heidy.route("/vids", methods=["GET"])
def listvids():
    db = TinyDB(DBPATH)
    # all = db.all()
    table = db.table('vids')
    all=table.all()
    # c = table.all()
    def chunks(l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]

    db.close()
    return render_template('heidy_check.html', all=chunks(all,40), folder='vids')

@heidy.route("/vids/<int:index>", methods=["PUT"])
def updatevids(index):
    s = str(request.form.get('status'))
    db = TinyDB(DBPATH)
    table = db.table('vids')
    res = table.update({'status': s}, doc_ids=[index])
    return(str(res))

