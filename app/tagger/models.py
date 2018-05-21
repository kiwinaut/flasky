from peewee import *
# from enums import Mime
# import json
from config import CONFIG
from datetime import datetime
from . import clip

db = SqliteDatabase(CONFIG['1001.path'])



__version__ = '1.1.0'



class BaseModel(Model):
    class Meta:
        database = db

class Files(BaseModel):
    filename = CharField()
    filepath = CharField(unique=True)
    sha = CharField(unique=True)
    size = IntegerField()
    rating = IntegerField(default=0)
    visited = IntegerField(default=0)
    ctime = DateTimeField()
    mtime = DateTimeField()
    note = CharField(null=True)
        
    class Meta:
        indexes = (
            (('mtime',), False),
        )


class Videos(Files):
    duration = IntegerField(null=True)


class Archives(Files):
    set = CharField(null=True)
    count = IntegerField(null=True)


class Tags(BaseModel):
    tag = CharField()
    lastupdated = DateTimeField(default=datetime.now())


class Collections(BaseModel):
    collection = CharField()


class ColTags(BaseModel):
    tag = ForeignKeyField(Tags)
    collection = ForeignKeyField(Collections)

    class Meta:
        primary_key = CompositeKey('tag', 'collection')


class Models(BaseModel):
    model = CharField()


class ModelTags(BaseModel):
    tag = ForeignKeyField(Tags)
    model = ForeignKeyField(Models)

    class Meta:
        primary_key = CompositeKey('tag', 'model')

class VideoTags(BaseModel):
    tag = ForeignKeyField(Tags)
    file = ForeignKeyField(Videos)

    class Meta:
        primary_key = CompositeKey('tag', 'file')


class ArchiveTags(BaseModel):
    tag = ForeignKeyField(Tags)
    file = ForeignKeyField(Archives)

    class Meta:
        primary_key = CompositeKey('tag', 'file')


def stringvalidator(f):
    def wrapper(*args):
        nargs = [i.strip().lower() for i in args]
        return f(*nargs)
    return wrapper



class Query:

    def get_tags():
        q = Tags.select().order_by(Tags.tag)
        return q

    def get_tags_bycount(media):
        if media == 'archives':
            j = ArchiveTags
        elif media == 'videos':
            j = VideoTags

        q = Tags.select(Tags.tag,fn.COUNT(j.file).alias('m_count')).join(j).group_by(Tags.tag).order_by(SQL('m_count desc'))
        return q

    def last_tags():
        # q = Tags.select().order_by(Tags.lastupdated.desc()).limit(20)
        # q = Tags.select().where(Tags.id << SQL('(SELECT "t2"."pindex" FROM "todo" as "t2" WHERE "t2"."group" == "{}" GROUP BY "t2"."pindex" HAVING count("t2"."pindex") > 1)'.format(gp)))
        q = db.execute_sql('SELECT * FROM(SELECT * FROM Tags ORDER BY Tags.lastupdated DESC LIMIT 0,20) ORDER BY tag ASC')
        return q

    def get_related_tags(tag):
        jstring = 'archivetags'
        #TODO
        qu = '''
            select tags.tag from tags
            inner join {j} on tags.id == {j}.tag_id 
            where {j}.file_id in
            (
            select {j}.file_id from tags 
            inner join {j} on tags.id == {j}.tag_id 
            where tag == ?
            )
            group by tags.id order by tags.tag
        '''.format(j=jstring)
        q = db.execute_sql(qu, (tag,))
        return q

    def get_tag(tag):
        q = Tags.get(tag=tag)
        return q

    @stringvalidator
    def update_tag(old_tag_value, new_tag_value, collection, aliasof):
        oldtag = Tags.get(tag=old_tag_value)

        if new_tag_value and new_tag_value != oldtag.tag:
            newtag, is_tag_created = Tags.get_or_create(tag=new_tag_value)
            for j in (ArchiveTags, VideoTags,):
                j.update(tag=newtag).where(j.tag==oldtag).execute()

            oldtag.delete_instance()
            active_tag = newtag
        else:
            active_tag = Tags.get(tag=old_tag_value)

        if collection != oldtag.collection:
            active_tag.collection = collection
            active_tag.save()

        if aliasof != oldtag.aliasof:
            if aliasof:
                parent = Tags.get(tag=aliasof)
                active_tag.aliasof = parent.tag
            else:
                active_tag.aliasof = ''
            active_tag.save()


    def delete_tag(tags):
        tag = Tags.get(tag=tags)
        for j in (ArchiveTags, VideoTags,):
            r = j.delete().where(j.tag==tag).execute()
        r = tag.delete_instance()
        return r


    def tables(media):
        if media == 'archives':
            Table = Archives
            j = ArchiveTags
        elif media == 'videos':
            Table = Videos
            j = VideoTags
        return Table, j

    def update2(media, index, set, note, thumb, screen):
        if media == 'archives':
            Table = Archives
            # j = ArchiveTags
            r = Table.update(set=set, note=note).where(Table.id==index).execute()
        elif media == 'videos':
            Table = Videos
            # j = VideoTags
            r = Table.update(note=note).where(Table.id==index).execute()
            if screen == 'true':
                item=Table.get(id=index)
                clip.new_screenshot(item)
        #TODO thumb
        if thumb:
            item=Table.get(id=index)
            clip.rethumb(item, media, thumb)
        return r
        
        
    def get_item_tags(media, index):
        Table, j = Query.tables(media)
        sq = Table.select(
                Tags.tag.alias('m_tag'),
            ).join(j, JOIN.LEFT_OUTER)\
            .join(Tags, JOIN.LEFT_OUTER)\
            .where(Table.id==index)\
            .objects()
        return sq

    def rethumb(media, ids):
        Table, j = Query.tables(media)
        sq = Table.select(Table.filepath, Table.sha).where(Table.id << ids)
        for q in sq:
            clip.rethumb(q, media)

    def rescreen(media, ids):
        sq = Videos.select(Videos.filepath, Videos.sha).where(Videos.id << ids)
        for q in sq:
            clip.new_screenshot(q)

        

    def add_tag_links(media, ids, tag):
        tag, is_tag_created = Tags.get_or_create(tag=tag.strip().lower())
        Table, j = Query.tables(media)
        with db.atomic():
            for id in ids:
                j.create(tag=tag, file=id)
        tag.lastupdated = datetime.now()
        tag.save()
        return None
        
    def delete_tag_links(media, ids, tag):
        tagrow = Tags.get(tag=tag.strip().lower())
        Table, j = Query.tables(media)
        r = j.delete().where(j.tag==tagrow, j.file<<ids).execute()
        return r
        
        
    def add_tag_link(media, index, tag):
        tag, is_tag_created = Tags.get_or_create(tag=tag.strip().lower())
        Table, j = Query.tables(media)
        r = j.insert(tag=tag, file=index).execute()
        tag.lastupdated = datetime.now()
        tag.save()
        return r, is_tag_created
        
    def delete_tag_link(media, index, tag):
        tagrow = Tags.get(tag=tag.strip().lower())
        Table, j = Query.tables(media)
        r = j.delete().where(j.tag==tagrow, j.file==index).execute()
        return r
        

    def get_item(media, id):
        Table, j = Query.tables(media)
        if media == 'archives':
            sq = Table.select(
                Table.id,
                Table.filename,
                Table.filepath,
                Table.sha,
                # Files.mime,
                Table.count,
                Table.size,
                Table.mtime,
                Table.note,
                Table.set,
                fn.GROUP_CONCAT(Tags.tag).alias('m_tag'),
            )
        elif media == 'videos':
            sq = Table.select(
                Table.id,
                Table.filename,
                Table.filepath,
                Table.sha,
                # Files.mime,
                # Files.count,
                Table.size,
                Table.mtime,
                Table.note,
                Table.duration,
                fn.GROUP_CONCAT(Tags.tag).alias('m_tag'),
            )

        sq= sq.join(j, JOIN.LEFT_OUTER)\
            .join(Tags, JOIN.LEFT_OUTER)\
            .where(Table.id==id)\
            .group_by(Table.id).objects()
        return sq.get()

    def delete_item(media, id, tag=None):
        Table, j = tables(media)
        if tag:
            res = j.delete().join(Table, JOIN.LEFT_OUTER).switch(j)\
                .join(Tags, JOIN.LEFT_OUTER)\
                .where(Tags.tag==tag)#.execute()
        else:
            res = Table.delete().where(Table.id==int(id))#.execute()
        return res


    def delete_item2(media, id):
        #erro protection
        Table, j = Query.tables(media)
        item = Table.get(id=id)
        res = j.delete().where(j.file_id==item.id).execute()
        fpath = item.filepath
        item.delete_instance()
        return fpath

    def get_files(
            args,
            media='archive',
            # tag=None,
            # filename=None,
            # order='01',
            # page='1',
            # limit='50',
            # tagisnone=False,
            # yearmonth=None,
            # **kwrags
        ):
            Table, j = Query.tables(media)
            if media == 'archives':
                sq = Table.select(
                    Table.id,
                    Table.filename,
                    Table.filepath,
                    Table.sha,
                    # Files.mime,
                    # Files.count,
                    Table.size,
                    Table.mtime,
                    Table.note,
                    Table.set,
                    # fn.GROUP_CONCAT(Tags.tag).alias('m_tag'),
                )
            elif media == 'videos':
                sq = Table.select(
                    Table.id,
                    Table.filename,
                    Table.filepath,
                    Table.sha,
                    # Files.mime,
                    # Files.count,
                    Table.size,
                    Table.mtime,
                    Table.note,
                    Table.duration,
                    # fn.GROUP_CONCAT(Tags.tag).alias('m_tag'),
                )

            if 'tag' in args and args['tag'] != '':
                sq = sq.join(j, JOIN.LEFT_OUTER)\
                    .join(Tags, JOIN.LEFT_OUTER)
                    
                # tag_list = args['tag'].strip().split(',')
                tag_list = args.getlist('tag')
                # if 'onetag' in args:
                #     sq = sq.where(Tags.tag==tag_list[0].strip().lower())\
                #     .group_by(Table.id).having(fn.COUNT(Table.id) >= len(tag_list))
                    
                if len(tag_list) == 1:
                    sq = sq.where(Tags.tag==tag_list[0].strip().lower())
                else:
                    sq = sq.where(Tags.tag << tag_list)\
                    .group_by(Table.id).having(fn.COUNT(Table.id) >= len(tag_list))
                # exp = []
                # for t in tag_list:
                #     exp.append(Tags.tag==t.strip().lower())

                # sq = sq.where(*exp)\
            elif 'notag' in args:
                sq = sq.join(j, JOIN.LEFT_OUTER)\
                .where(j.file_id >> None)

            if 'set' in args and args['set'] != '' and media == 'archives':
                sq = sq.where(Table.set** '%{}%'.format(args['set']))

            if 'filename' in args and args['filename'] != '' and media == 'archives':
                sq = sq.where(Table.filename** '%{}%'.format(args['filename']))


            # if yearmonth:
            #     sq = sq.where(fn.strftime('%Y%m', Table.mtime)==yearmonth)

            sort_string = args.get('sort', default='mtime')
            order_string = args.get('order', default='desc')
            sort = getattr(Table, sort_string)
            order = getattr(sort, order_string)
            sq = sq.order_by(order(), Table.mtime.asc())

                        

            sq = sq.paginate(int(args.get('page', default='1')), int(args.get('per_page', default='40'))).objects()
            # print(sq.sql())
            return sq

