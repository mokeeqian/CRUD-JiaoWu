#  Copyright (c) 2019.  MIT license
#  Jipeng Qian.
#  This is a copyrighted source code under MIT license,
#  you should receive a copy of the copyright,
#  together with this source code.
#  Have fun with your favor!


import app
import datetime
db = app.db


class Notice(db.Model):
    __tablename__ = 'tb_notice'
    NId = db.Column(db.String(20), primary_key=True)
    NTitle = db.Column(db.String(50))
    NContent = db.Column(db.String(200))
    NDate = db.Column(db.Date())
    NPublisherId = db.Column(db.String(20))
    # NPublisherName = db.Column(db.String(20))

    def __repr__(self):
        return '<Notice %r' %self.NId

    def to_list(self):
        notices = list()
        notices.append(self.NId)
        notices.append(self.NTitle)
        notices.append(self.NContent)
        notices.append(datetime.date.strftime(self.NDate, '%Y-%m-%d'))  # 注意这里是Date对象,需要转为str

        return notices
