#  Copyright (c) 2019.  MIT license
#  Jipeng Qian.
#  This is a copyrighted source code under MIT license,
#  you should receive a copy of the copyright,
#  together with this source code.
#  Have fun with your favor!
import app
db = app.db


class Student(db.Model):
    __tablename__ = 'tb_student'
    SId = db.Column(db.String(20), primary_key=True)
    SName = db.Column(db.String(20))
    SSex = db.Column(db.String(20))
    SBirth = db.Column(db.String(20))
    SMajor = db.Column(db.String(20))
    SDept = db.Column(db.String(20))

    def __repr__(self):
        return '<Student %r>' % self.sname
