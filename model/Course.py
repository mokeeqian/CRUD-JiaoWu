#  Copyright (c) 2019.  MIT license
#  Jipeng Qian.
#  This is a copyrighted source code under MIT license,
#  you should receive a copy of the copyright,
#  together with this source code.
#  Have fun with your favor!

import app
db = app.db


class Course(db.Model):
    __tablename__ = 'tb_course'
    CId = db.Column(db.String(20), primary_key=True)
    CName = db.Column(db.String(20))
    CTeacherId = db.Column(db.String(20), db.ForeignKey('tb_teacher.TId'))
    CClassroom = db.Column(db.String(20))
    CTime = db.Column(db.String(20))
    CHours = db.Column(db.Integer)
    CVolum = db.Column(db.Integer)
    CRetake = db.Column(db.Integer)

    def __repr__(self):
        return '<Course %r>' % self.cname
