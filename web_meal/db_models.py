import peewee as pw

database = pw.SqliteDatabase("database.db")


class BaseModel(pw.Model):
    id = pw.AutoField()

    class Meta:
        database = database


class User(BaseModel):
    user_id = pw.TextField()


database.user = User

database.connect()
database.create_tables([User])
