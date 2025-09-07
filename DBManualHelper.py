import peewee as pw

database = pw.SqliteDatabase('users.db')
class BaseModel(pw.Model):
    class Meta:
        database = database

class User(BaseModel):
    user_id = pw.IntegerField(unique=True)
    faculty_id = pw.CharField()
    group_id = pw.IntegerField()

database.connect()
database.create_tables([User])