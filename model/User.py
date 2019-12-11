#  Copyright (c) 2019.  MIT license
#  Jipeng Qian.
#  This is a copyrighted source code under MIT license,
#  you should receive a copy of the copyright,
#  together with this source code.
#  Have fun with your favor!


import app

db = app.db


class User(db.Model):
    __tablename__ = 'tb_user'
    # NOTE: 字段名必须与数据库的字段名一致
    Id = db.Column(db.String(20), primary_key=True)
    Pwd = db.Column(db.String(20))
    Privilege = db.Column(db.Integer)

    def __repr__(self):
        return '<User %r>' % self.uid
