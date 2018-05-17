from flask import Blueprint, render_template, abort, request, redirect, url_for
# from jinja2 import TemplateNotFound
# from tinydb import TinyDB
# from .models import Todo, fn, SQL
from werkzeug.datastructures import MultiDict
import urllib
from .models import Query
import subprocess as sp
from config import CONFIG
from .info import get_info
# from werkzeug.wrappers import Response

class Args:
    defaults = {
        'sort': 'mtime',
        'order': 'desc',
        'view': 'list',
        'page': 1,
        'per_page': 40,
        'set': '',
        'table': '',
        'tag': '',
        'filename': ''
    }
    def __init__(self, imd):
        self.imd = MultiDict(imd)

    def __getitem__(self, key):
        return self.imd.get(key, self.defaults[key])

    def getlist(self, key, *args, **kw):
        return self.imd.getlist(key, *args, **kw)

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


tagger = Blueprint('tagger', __name__, static_folder='%s/persistent/1001/thumbs'%CONFIG['mount'], static_url_path='/s')



@tagger.route("", methods=["GET"])
def main():
    return redirect(url_for('.get_tags'), code=302)

@tagger.route("/tags", methods=["GET"])
def get_tags():
    q = Query.get_tags()
    return render_template(
        '1001/tags.html',
        q=q
        )

@tagger.route("/tags/<tag>", methods=["GET"])
def get_tag(tag):
    item = Query.get_tag(tag)
    relateds = Query.get_related_tags(tag)
    return render_template(
        '1001/tag.html',
        item=item,
        relateds=relateds
        )

@tagger.route("/tags/<tag>", methods=["PUT"])
def set_tag(tag):
    new_tag = request.form['tag']
    collection = request.form['collection']
    aliasof = request.form['aliasof']
    r = Query.update_tag(tag, new_tag, collection, aliasof)
    return str(r)

@tagger.route("/tags/<tag>", methods=["DELETE"])
def delete_tag(tag):
    r = Query.delete_tag(tag)
    return str(r)

@tagger.route("/<media>", methods=["GET"])
def get_files(media):
    q = Query.get_files( request.args, media)
    if request.args.get('view','list') == 'list':
        temp = '1001/files-list.html'
    else:
        temp = '1001/files-grid.html'
    return render_template(
        temp,
        list=q,
        media=media,
        args=Args(request.args)
        )


@tagger.route("/<media>", methods=["POST"])
def add_tags(media):
    try:
        tag = request.form['tag']
        ids = request.form.getlist('id', type=int)
        Query.add_tag_links(media, ids, tag)
        return ""
    except Exception as e:
        print(e)
        abort(500)

@tagger.route("/<media>", methods=["DELETE"])
def remove_tags(media):
    try:
        # print(request.form)
        # print(request.args)
        tag = request.args['tag']
        ids = request.args.getlist('id', type=int)
        Query.delete_tag_links(media, ids, tag)
        return ""
    except Exception as e:
        print(e)
        abort(500)



@tagger.route("/<media>/multiedit", methods=["GET"])
def groupedit(media):
    q = Query.get_files( request.args, media)
    return render_template(
        '1001/files-edit.html',
        list=q,
        media=media,
        args=Args(request.args),
        last = Query.last_tags()
        )

@tagger.route("/<media>/<int:index>", methods=["GET"])
def item(media, index):
    try:
        q = Query.get_item(media, index)
        return render_template(
            '1001/file.html',
            item=q,
            media=media,
            index=index,
            last = Query.last_tags()
            )
    except:
        abort(500)

@tagger.route("/archives/<int:index>/infolist", methods=["GET"])
def archive_infolist(index):
    # try:
        q = Query.get_item('archives', index)
        # fpath = CONFIG['mount']+'/'+q.filepath
        # import zipfile
        # z = zipfile.ZipFile(fpath)
        # return str(z.namelist())
        return render_template('1001/info.html', info=get_info(q.filepath))
    # except:
    #     abort(500)

@tagger.route("/<media>/<int:index>", methods=["PUT"])
def item_update(media, index):
    # try:
        note = request.form['note']
        set = request.form.get('set')
        screen = request.form.get('screen')
        thumb = request.form['thumb']
        res = Query.update2(media,index,set,note,thumb,screen)
        return str(res)
    # except:
    #     abort(500)

@tagger.route("/<media>/<int:index>", methods=["DELETE"])
def item_delete(media, index):
    # try:
        scope = request.args['scope']
        if scope == "entry":
            fpath = Query.delete_item2(media,index)
        elif scope == "all":
            fpath = Query.delete_item2(media,index)
            r = sp.call(["gio", "trash", CONFIG['mount']+'/'+fpath])
        else:
            abort(400)
        return str(index)
    # except:
    #     abort(500)

@tagger.route("/<media>/<int:index>/open", methods=["POST"])
def item_open(media, index):
    # try:
        path = request.form['path']
        app = request.form['app']
        print(path)
        if app == 'default':
            r = sp.call(["gio", "open", CONFIG['mount']+'/'+path])
        elif app =='mcomix':
            r = sp.call(["mcomix", CONFIG['mount']+'/'+path])
        elif app =='folder':
            r = sp.call(['nautilus', '-s', CONFIG['mount']+'/'+path])
        else:
            abort(400)
        return ''
    # except:
    #     abort(500)

@tagger.route("/<media>/<int:index>/next", methods=["GET"])
def item_next(media, index):
    try:
        return str(index)
    except:
        abort(500)

@tagger.route("/<media>/<int:index>/prev", methods=["GET"])
def item_prev(media, index):
    try:
        return str(index)
    except:
        abort(500)

# @tagger.route("/<int:index>", methods=["DELETE"])
# def item_delete(index):

#     return render_template(
#         'tagger-item.html'        
#         )

@tagger.route("/<media>/<int:index>/tags", methods=["GET"])
def get_item_tags(media, index):
    try:
        q = Query.get_item_tags(media, index)
        return render_template(
        '1001/ajax-file-tags.html',
        files=q,
        media=media,
        index=index,
        )
    except Exception as e:
        print(e)
        abort(500)

@tagger.route("/<media>/<int:index>/tags", methods=["POST"])
def add_tag(media, index):
    try:
        tag = request.form['tag']
        update_number, is_tag_created = Query.add_tag_link(media, index, tag)
        q = Query.get_item_tags(media, index)
        return render_template(
        '1001/ajax-file-tags.html',
        files=q,
        media=media,
        index=index,
        )
    except Exception as e:
        print(e)
        abort(500)

@tagger.route("/<media>/<int:index>/tags/<string:tag>", methods=["DELETE"])
def remove_tag(media, index, tag):
    try:
        update_number = Query.delete_tag_link(media, index, tag)
        print(update_number)
        q = Query.get_item_tags(media, index)
        return render_template(
        '1001/ajax-file-tags.html',
        files=q,
        media=media,
        index=index,
        )
    except Exception as e:
        print(e)
        abort(500)

