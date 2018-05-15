from peewee import *



db = SqliteDatabase('/home/soni/.cache/onlyall.db')


class BaseModel(Model):
    class Meta:
        database = db


class Todo(BaseModel):
    model = CharField()
    group = CharField()
    date = DateTimeField(null=True)
    count = IntegerField(null=True)
    video = CharField(null=True)
    pindex = IntegerField(null=True)
    thumb = CharField()
    blob = BlobField(null=True)
    status = CharField(null=True)


# if not Todo.table_exists():
#     # db.connect()
#     db.create_tables([Todo])
#     db.close()