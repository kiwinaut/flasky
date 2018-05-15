from flask import Blueprint, render_template, abort, request
# from jinja2 import TemplateNotFound
from tinydb import TinyDB, where
from operator import itemgetter
import subprocess as sp

bf = Blueprint('bf', __name__)

CO = None

# @bf.route("/")
# def main():
#     return render_template('main.html')

@bf.route("/", methods=["GET"])
def bf_list():
    db = TinyDB('/media/soni/1001/bfdb.json')
    all = db.all()
    table = db.table('codes')
    c = table.all()
    c = sorted(c, key=itemgetter('code'))

    db.close()
    return render_template('bf.html', all=all, counter=c)

# @bf.route("/bf/<int:index>", methods=["GET"])
# def bf_item_get(index):
#     db = TinyDB('/media/soni/1001/bfdb.json')
#     res = db.get(doc_id=index)
#     # print(res)
#     db.close()
#     # res = sorted(res, key=itemgetter('filename'))
#     return render_template('bf.html', all=[res], counter=CO)

# page = request.args.get('page', default = 1, type = int)
# filter = request.args.get('filter', default = '*', type = str)
@bf.route("/<int:index>", methods=["DELETE"])
def bf_item_delete(index):
    return 'item {} deleted'.format(index)

@bf.route("/open/<int:index>", methods=["POST"])
def open(index):
    db = TinyDB('/media/soni/1001/bfdb.json')
    res = db.get(doc_id=index)
    db.close()
    sp.call(["mcomix",res['filepath']])
    return ''

@bf.route("/star/<int:index>", methods=["POST"])
def star(index):
    print(dir(request.form))
    print(request.form)
    update = {}
    for k,v in request.form.items():
        print(k,v)
        if k == 'star':
            update['star'] = v
    # star = bool(int(request.args.get('star', 0)))
    # db = TinyDB('/media/soni/1001/bfdb.json')
    # res = db.update({'star': star}, doc_ids=[index])
    # db.close()
    # return str(res[0])
    return '0'


@bf.route("/filter/<string:code>", methods=["GET"])
def bf_get(code):
    db = TinyDB('/media/soni/1001/bfdb.json')
    order = bool(int(request.args.get('o', 0)))
    res = db.search(where('code') == code)
    table = db.table('codes')
    c = table.all()
    c = sorted(c, key=itemgetter('code'))
    # print(res)
    db.close()
    res = sorted(res, key=itemgetter('filename'), reverse=order)
    return render_template('bf.html', all=res, counter=c, order=order)