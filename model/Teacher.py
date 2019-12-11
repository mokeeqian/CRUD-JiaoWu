#  Copyright (c) 2019.  MIT license
#  Jipeng Qian.
#  This is a copyrighted source code under MIT license,
#  you should receive a copy of the copyright,
#  together with this source code.
#  Have fun with your favor!

import app
db = app.db


class Teacher(db.Model):
    __tablename__ = 'tb_teacher'
    TId = db.Column(db.String(20), primary_key=True)
    TName = db.Column(db.String(20))
    TBirth = db.Column(db.String(20))
    TSex = db.Column(db.String(20))
    TDept = db.Column(db.String(20))

    def __repr__(self):
        return '<Teacher %r>' % self.TId