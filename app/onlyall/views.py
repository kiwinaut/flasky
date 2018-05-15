from flask import Blueprint, render_template, abort, request
# from jinja2 import TemplateNotFound
# from tinydb import TinyDB
from .models import Todo, fn, SQL
import urllib
from werkzeug.datastructures import MultiDict
from config import CONFIG
# def show(page):
#     try:
#         # return render_template('pages/%s.html' % page)
#         return main.root_path
#     except TemplateNotFound:
#         abort(404)

class Args:
    defaults = {
        'sort' : 'model',
        'order' : 'desc',
        'view' : 1
    }
    def __init__(self, imd):
        self.imd = MultiDict(imd)

    def __getitem__(self, key):
        return self.imd.get(key, self.defaults[key])

    def norder(self):
        if self['order'] == 'asc':
            return 'desc'
        else:
            return 'asc'

    def encode(self, **kwargs):
        copy = self.imd.copy()
        for i in kwargs:
            copy[i] = kwargs[i]
        return urllib.parse.urlencode(copy)
        

onlyall = Blueprint('onlyall', __name__, static_folder='%s/persistent/onlyall'%CONFIG['mount'], static_url_path='/i')

# @onlyall.context_processor
# def utility_processor():
#     def encode2(pargs, *args):
#         d = pargs.to_dict()
#         for i in args:
#             d.update(i)
#         return urllib.parse.urlencode(d)
#     def inverse(i):
#         if i == 'asc':
#             return 'desc'
#         else:
#             return 'asc'
#     return dict(encode2=encode2, inverse=inverse)


@onlyall.route("", methods=["GET"])
def list():
    print(request.args)

    q = Todo.select(
    Todo.id,
    Todo.model,
    Todo.group,
    Todo.date,
    Todo.count,
    Todo.pindex,
    Todo.thumb,
    Todo.status
    )

    if 'model' in request.args and request.args['model'] != '':
        q = q.where(Todo.model==request.args['model'])
    if 'group' in request.args and request.args['group'] != '':
        q = q.where(Todo.group==request.args['group'])
    if 'year' in request.args and request.args['year'] != '':
        if 'month' in request.args and request.args['month'] != '':
            co ='%s %02d' % (request.args.get('year',type=int), request.args.get('month', type=int))
            q = q.where(SQL('strftime(\'%Y %m\',\'t1\'.\'date\') = ?', co ))
        else:
            q = q.where(SQL('strftime(\'%Y\',\'t1\'.\'date\') = ?', request.args['year']))

    sort_string = request.args.get('sort', default='model')
    order_string = request.args.get('order', default='desc')
    sort = getattr(Todo, sort_string)
    order = getattr(sort, order_string)
    q = q.order_by(order(), Todo.group.asc())
    set_select = Todo.select(Todo.group, fn.Count(Todo.group).alias('count')).group_by(Todo.group)
    model_select = Todo.select(Todo.model, fn.Count(Todo.model).alias('count')).group_by(Todo.model)

    return render_template(
        'onlyall.html',
        q=q, set_select=set_select,
        model_select=model_select,
        args=Args(request.args)
        )

@onlyall.route("/dups", methods=["GET"])
def dups():
    # print(type(request.args['kk']))
    # sql ='''
    # SELECT "t1"."id", "t1"."model", "t1"."group", "t1"."date", "t1"."count", "t1"."pindex", "t1"."thumb", "t1"."status" FROM "todo" AS t1 
    # WHERE "t1"."pindex" IN (SELECT "t2"."pindex" FROM "todo" as t2 GROUP BY "t2"."pindex" HAVING count("t2"."pindex") > 1) 
    # ORDER BY "t1"."pindex" DESC, "t1"."group" ASC
    # '''
    q = Todo.select(
    Todo.id,
    Todo.model,
    Todo.group,
    Todo.date,
    Todo.count,
    Todo.pindex,
    Todo.thumb,
    Todo.status
    )
    gp = request.args.get('group', 'OnlyTease')

    q = q.where(Todo.pindex << SQL('(SELECT "t2"."pindex" FROM "todo" as "t2" WHERE "t2"."group" == "{}" GROUP BY "t2"."pindex" HAVING count("t2"."pindex") > 1)'.format(gp)))


    sort_string = request.args.get('sort', default='pindex')
    order_string = request.args.get('order', default='desc')
    sort = getattr(Todo, sort_string)
    order = getattr(sort, order_string)

    q = q.order_by(order(), Todo.group.asc())
    set_select = Todo.select(Todo.group, fn.Count(Todo.group).alias('count')).group_by(Todo.group)
    model_select = Todo.select(Todo.model, fn.Count(Todo.model).alias('count')).group_by(Todo.model)

    return render_template(
        'onlyall.html',
        q=q, set_select=set_select,
        model_select=model_select,
        sort_args=(sort_string, order_string,),
        args=request.args
        )

@onlyall.route("/<int:index>", methods=["PUT"])
def update(index):
    s = str(request.form.get('status'))
    res = Todo.update(status=s).where(Todo.id==index).execute()
    return(str(res))



# @onlyall.route("/vids", methods=["GET"])
# def listvids():
#     db = TinyDB('/home/soni/Downloads/p/heidy/heidy_check.json')
#     # all = db.all()
#     table = db.table('vids')
#     all=table.all()
#     # c = table.all()
#     def chunks(l, n):
#         """Yield successive n-sized chunks from l."""
#         for i in range(0, len(l), n):
#             yield l[i:i + n]

#     db.close()
#     return render_template('heidy_check.html', all=chunks(all,40), folder='vids')

# @onlyall.route("/vids/<int:index>", methods=["PUT"])
# def updatevids(index):
#     s = str(request.form.get('status'))
#     db = TinyDB('/home/soni/Downloads/p/heidy/heidy_check.json')
#     table = db.table('vids')
#     res = table.update({'status': s}, doc_ids=[index])
#     return(str(res))


@onlyall.after_request
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