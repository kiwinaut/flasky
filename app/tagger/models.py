from peewee import *
# from enums import Mime
# import json
from config import CONFIG
from datetime import datetime
from . import clip

db = SqliteDatabase(CONFIG['1001.path'])



class BaseModel(Model):
    class Meta:
        database = db

class Files(BaseModel):
    filename = CharField()
    filepath = CharField()
    sha = CharField(unique=True)
    size = IntegerField()
    rating = IntegerField(default=0)
    visited = IntegerField(default=0)
    ctime = DateTimeField()
    mtime = DateTimeField()
    # thumb = BlobField(null=True)
    thumb_path = CharField(null=True)
    note = CharField(null=True)
        
    class Meta:
        indexes = (
            (('mtime',), False),
        )


class Libs(Files):
    pass

class Videos(Files):
    screen = BlobField(null=True)
    duration = IntegerField(null=True)


class Archives(Files):
    set = CharField(null=True)
    count = IntegerField(null=True)


    # @classmethod
    # def group_date_info(cls):
    #     '''SELECT strftime('%Y', mtime), strftime('%m', mtime), count(*) FROM Files
    #     GROUP BY strftime('%m %Y', mtime)
    #     order by mtime desc;
    #     WHERE timestamp >= strftime('%s', '2012-12-25 00:00:00') 
    #     year    month   count
    #     '''
    #     pass

    # @classmethod
    # def get_general(cls, where_, order, index):
    #     print(index)
    #     sq = Files.select(
    #         Files.id,
    #         Files.filename,
    #         Files.filepath,
    #         Files.mime,
    #         Files.count,
    #         Files.size,
    #         Files.mtime,
    #         Files.thumb,
    #         Files.note,
    #         Files.set,
    #         fn.GROUP_CONCAT(Names.name).alias('m_name'),
    #         fn.GROUP_CONCAT(Tags.tag).alias('m_tag'),
    #         Groups.group.alias('m_group')
    #     )
    #     sq = sq.join(Groups, JOIN.LEFT_OUTER)\
    #         .switch(Files)\
    #         .join(FileNames, JOIN.LEFT_OUTER)\
    #         .join(Names, JOIN.LEFT_OUTER)\
    #         .switch(Files)\
    #         .join(FileTags, JOIN.LEFT_OUTER)\
    #         .join(Tags, JOIN.LEFT_OUTER)
    #     if where_:
    #         sq = sq.where(where_)
    #     sq = sq.group_by(Files.id)\
    #         .order_by(order)\
    #         .paginate(index, PAGINATE_LIMIT)\
    #         .naive()
    #     return sq

    # @classmethod
    # def to_json(self):
    #     tagged_dict = {}
    #     sq = Files.select(
    #         Files.sha,
    #         Files.note,
    #         Files.set,
    #         Names.name.alias('m_name'),
    #         Tags.tag.alias('m_tag'),
    #         Groups.group.alias('m_group')
    #     )
    #     sq = sq.join(Groups, JOIN.LEFT_OUTER)\
    #         .switch(Files)\
    #         .join(FileNames, JOIN.LEFT_OUTER)\
    #         .join(Names, JOIN.LEFT_OUTER)\
    #         .switch(Files)\
    #         .join(FileTags, JOIN.LEFT_OUTER)\
    #         .join(Tags, JOIN.LEFT_OUTER)
    #     # if where_:
    #     #     sq = sq.where(where_)
    #     # sq = sq.group_by(Files.id)\
    #     sq = sq.order_by(Files.mtime)\
    #         .naive()
    #         # .paginate(index, PAGINATE_LIMIT)\

    #     for q in sq:
    #         tag_list = []
    #         tag_list.append(q.set)
    #         if q.m_name:
    #             tag_list.append(q.m_name)
    #         if q.m_tag:
    #             tag_list.append(q.m_tag)
    #         if q.m_group:
    #             tag_list.append(q.m_group)
    #         if len(tag_list) >= 2:

    #             tagged_dict[q.sha] = tag_list

    #     print(tagged_dict)
    #     with open('tagged.json', 'w') as fp:
    #         json.dump(tagged_dict, fp)

    # @classmethod
    # def get_general3(cls, expressions, index, order_exp, filter_=None, extra=None):
    #     sq = Files.select(
    #         Files.id,
    #         Files.filename,
    #         Files.filepath,
    #         Files.mime,
    #         Files.count,
    #         Files.size,
    #         Files.mtime,
    #         Files.thumb,
    #         Files.note,
    #         Files.set,
    #         fn.GROUP_CONCAT(Names.name).alias('m_name'),
    #         fn.GROUP_CONCAT(Tags.tag).alias('m_tag'),
    #         Groups.group.alias('m_group')
    #     )
    #     sq = sq.join(Groups, JOIN.LEFT_OUTER)\
    #         .switch(Files)\
    #         .join(FileNames, JOIN.LEFT_OUTER)\
    #         .join(Names, JOIN.LEFT_OUTER)\
    #         .switch(Files)\
    #         .join(FileTags, JOIN.LEFT_OUTER)\
    #         .join(Tags, JOIN.LEFT_OUTER)
    #     if len(expressions):
    #         sq = sq.where(*expressions)
    #     if filter_:
    #         sq = sq.where(filter_)
    #     if extra:
    #         sq = sq.where(extra)
    #     sq = sq.group_by(Files.id)\
    #         .order_by(order_exp)\
    #         .paginate(index, PAGINATE_LIMIT)\
    #         .naive()
    #     return sq

    # @classmethod
    # def get_general2(cls, expressions, index, order_exp, filter_=None, extra=None):
    #     sq = Files.select(
    #         Files.id,
    #         Files.filename,
    #         Files.filepath,
    #         Files.mime,
    #         Files.count,
    #         Files.size,
    #         Files.mtime,
    #         Files.thumb,
    #         Files.note,
    #         Files.set,
    #         Names.name.alias('m_name'),
    #         Tags.tag.alias('m_tag'),
    #         Groups.group.alias('m_group')
    #     )
    #     sq = sq.join(Groups, JOIN.LEFT_OUTER)\
    #         .switch(Files)\
    #         .join(FileNames, JOIN.LEFT_OUTER)\
    #         .join(Names, JOIN.LEFT_OUTER)\
    #         .switch(Files)\
    #         .join(FileTags, JOIN.LEFT_OUTER)\
    #         .join(Tags, JOIN.LEFT_OUTER)
    #     if len(expressions):
    #         sq = sq.where(*expressions)
    #     if filter_:
    #         sq = sq.where(filter_)
    #     if extra:
    #         sq = sq.where(extra)
    #     sq = sq.order_by(order_exp)\
    #         .paginate(index, PAGINATE_LIMIT)\
    #         .naive()
    #     return sq


    # @classmethod
    # def get_tags(cls, value):
    #     return (
    #         Files.select(
    #             fn.GROUP_CONCAT(Tags.tag).alias('m_tag'),
    #         )
    #         .join(FileTags)
    #         .join(Tags)
    #         .where(Files.id==value)
    #         .group_by(Files.id)
    #         .naive()
    #     )

    # @classmethod
    # def get_col(cls, select, group, expressions):
    #     return (
    #         Files.select(
    #             select
    #         )
    #         .join(Groups, JOIN.LEFT_OUTER)
    #         .switch(Files)
    #         .join(FileNames)
    #         .join(Names, JOIN.LEFT_OUTER)
    #         .where(*expressions)
    #         .group_by(group)
    #         .order_by(group)
    #         .naive()
    #     )

# class Screenshots(BaseModel):
#     screenshot = BlobField()
#     file = ForeignKeyField(Files)


# class Category(BaseModel):
#     category = CharField()
#     path = CharField(null=True)
    

class Tags(BaseModel):
    tag = CharField()
    collection = CharField(default='')
    # category = ForeignKeyField(Category)
    lastupdated = DateTimeField(default=datetime.now())
    aliasof = CharField(default='')


class LibTags(BaseModel):
    tag = ForeignKeyField(Tags)
    file = ForeignKeyField(Libs)

    class Meta:
        primary_key = CompositeKey('tag', 'file')


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


# class FileNames(BaseModel):
#     file = ForeignKeyField(Files)
#     name = ForeignKeyField(Names)

#     class Meta:
#         indexes = (
#         #     # create a unique on file/tag
#         #     (('file', 'tag'), True),

#             # create a unique on tag/file
#             (('name', 'file'), True),
#         )


if not ArchiveTags.table_exists():
    db.create_tables([
        Libs,
        Videos,
        Archives,
        Tags, 
        LibTags, 
        VideoTags, 
        ArchiveTags, 
    ])

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
                # Files.mime,
                # Files.count,
                Table.size,
                Table.mtime,
                Table.thumb_path,
                Table.note,
                Table.set,
                fn.GROUP_CONCAT(Tags.tag).alias('m_tag'),
            )
        elif media == 'videos':
            sq = Table.select(
                Table.id,
                Table.filename,
                Table.filepath,
                # Files.mime,
                # Files.count,
                Table.size,
                Table.mtime,
                Table.thumb_path,
                Table.note,
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
                    # Files.mime,
                    # Files.count,
                    Table.size,
                    Table.mtime,
                    Table.thumb_path,
                    Table.note,
                    Table.set,
                    # fn.GROUP_CONCAT(Tags.tag).alias('m_tag'),
                )
            elif media == 'videos':
                sq = Table.select(
                    Table.id,
                    Table.filename,
                    Table.filepath,
                    # Files.mime,
                    # Files.count,
                    Table.size,
                    Table.mtime,
                    Table.thumb_path,
                    Table.note,
                    # Table.set,
                    # fn.GROUP_CONCAT(Tags.tag).alias('m_tag'),
                )

            if 'tag' in args and args['tag'] != '':
                sq = sq.join(j, JOIN.LEFT_OUTER)\
                    .join(Tags, JOIN.LEFT_OUTER)
                    
                # tag_list = args['tag'].strip().split(',')
                tag_list = args.getlist('tag')
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
            print(sq.sql())
            return sq

