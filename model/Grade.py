#  Copyright (c) 2019.  MIT license
#  Jipeng Qian.
#  This is a copyrighted source code under MIT license,
#  you should receive a copy of the copyright,
#  together with this source code.
#  Have fun with your favor!

import app
db = app.db

import model.Course as Course
import model.Teacher as Teacher


class Grade(db.Model):
    __tablename__ = 'tb_grade'
    SId = db.Column(db.String(20), db.ForeignKey('tb_student.SId'), primary_key=True)
    CId = db.Column(db.String(20), db.ForeignKey('tb_course.CId'), primary_key=True)
    Grade = db.Column(db.Integer)

    # 重写这个方法，用orm查询得到的query对象结果就是这个方法的返回值，很方便
    # 可惜的是，返回值只能是str类型，我需要List类型，所以只能强制转换一下
    # emmmmmmmmmmmmm 这样强制转换貌似后面很麻烦。。。。
    def __repr__(self):
        return '<Grade %r' %self.Grade

    def to_list(self):
        grades = list()
        grades.append(self.CId)
        # grades.append(self.SId)
        cname = Course.query.filter_by(CId=self.CId).one().CName

        print("======== " + cname + " ========")

        cteacher_id = Course.query.filter_by(CId=self.CId).one().CTeacherId
        cteacher_name = Teacher.query.filter_by(TId=cteacher_id).one().TName
        grades.append(cname)
        grades.append(cteacher_name)

        grades.append(self.Grade)   #FIXME: 修改变量名，和类名重复了
        return grades
