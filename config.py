# flaskでログイン機能を実装するためのクラスを追加 モデルに継承させることでログイン状態の管理などができる
# モデル＝テーブルを操作するためのクラス
from flask_login import UserMixin
from peewee import SqliteDatabase, Model, IntegerField, CharField, TextField

db = SqliteDatabase("db.sqlite")


# UserMixinクラスを継承
class User(Model, UserMixin):
    id = IntegerField(primary_key=True)
    name = CharField(unique=True)
    email = CharField(unique=True)
    password = TextField()

    class Meta:
        database = db
        table_name = "users"


db.create_tables([User])
