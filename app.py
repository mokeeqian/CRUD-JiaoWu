#!/bin/env python3
# encoding = utf-8

#  Copyright (c) 2019.  MIT license
#  Jipeng Qian.
#  This is a copyrighted source code under MIT license,
#  you should receive a copy of the copyright,
#  together with this source code.
#  Have fun with your favor!

import json
from flask import Flask, request, render_template, flash, session
from flask import redirect
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
# 在实际的开发中，经常需要修改数据库结构。
# 通常我们不需要直接动手去修改数据库，而是先修改ORM对应的模型，然后再把模型映射到数据库中。
# flask-migrate就是做这个事情的。
from flask_migrate import Migrate, MigrateCommand
# 可以通过命令行的形式来操作flask。例如通过命令跑一个开发版本的服务器、设置数据库、定时任务等。
from flask_script import Manager
# 下面两行代码，仅当报错ImportError: No module named 'MySQLdb'时需要运行。
# 具体可以参考：http://blog.51cto.com/huangmanyao/2091761 这是我在debug时遇到的问题。
import pymysql

"""
配置
"""
# pymysql.install_as_MySQLdb()
app = Flask(__name__)
manager = Manager(app)
# 配置与数据库的连接
app.secret_key = 'sdfghjk'
app.config['WTF_CSRF_ENABLED'] = False
# 显示原始sql语句
app.config['SQLALCHEMY_ECHO'] = True
# 设置session生命周期
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)

# 注意：虽然mysql中的建立的数据库可以不包含任何表，但是student数据库必须事先建立好，否则将无法创建连接。
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:990505@127.0.0.1:3306/jiaowu'
# 设置这一项为True后，每次请求结束后都会自动提交数据库中的变动。
# 设置为False后，每次使用commit来提交对数据库的最终修改是一种比较安全的做法。
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 增加db命令到命令行
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

"""
工具
"""


# 获取指定表的全部数据
def get_table_data(table, conditions=None):
    conn = pymysql.connect(
        host='127.0.0.1', port=3306,
        user='root', passwd='990505',
        db='jiaowu', charset='utf8',
    )
    # 游标对象
    cur = conn.cursor()

    if conditions is not None:
        sql = "select * from " + table + conditions
    else:
        sql = "select * from " + table
    # 结果集
    res = cur.execute(sql)
    # 查询多条记录s
    res = cur.fetchmany(res)
    cur.close()
    conn.commit()
    # 记得释放资源
    conn.close()
    return res


# 登录验证
def find_user(Id: str, Pwd: str):
    conn = pymysql.connect(
        host='127.0.0.1', port=3306,
        user='root', passwd='990505',
        db='jiaowu', charset='utf8',
    )
    # 游标对象
    cur = conn.cursor()

    sql = "SELECT Privilege FROM tb_user WHERE Id=%s and Pwd=%s"
    # 结果集
    cur.execute(sql, [Id, Pwd])  # 貌似不支持格式化字符串，要把参数放在这个函数
    # 查询多条记录
    res = cur.fetchone()
    cur.close()
    conn.commit()
    # 记得释放资源
    conn.close()

    if res:
        return res
    return None


# 注册验证
def is_id_exist(Id: str):
    conn = pymysql.connect(
        host='127.0.0.1', port=3306,
        user='root', passwd='990505',
        db='jiaowu', charset='utf8',
    )
    # 游标对象
    cur = conn.cursor()

    sql = "SELECT Privilege FROM tb_user WHERE Id=%s"
    # 结果集
    res = cur.execute(sql, [Id])  # 貌似不支持格式化字符串，要把参数放在这个函数
    # 查询多条记录
    res = cur.fetchmany(res)
    cur.close()
    conn.commit()
    # 记得释放资源
    conn.close()

    if res:
        return res
    return False


def db_wraper(sql: str):
    conn = pymysql.connect(
        host='127.0.0.1', port=3306,
        user='root', passwd='990505',
        db='jiaowu', charset='utf8',
    )

    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()

# 将查询得到的List数据格式化为json能接受的list数据
# TODO: 每个字段都不一样，这里先只写Notice的，后期想办法重构
# param: data 包含所有查询结果的一个list，每个元素是数据库中的一条记录
def to_json_like_data(data:list):
    new_data = list()
    for item in data:
        record = dict()
        record.fromkeys(['NId', 'NTitle', 'NContent', 'NDate', 'NPublisherId'])
        record['NId'] = item.NId
        record['NTitle'] = item.NTitle
        record['NContent'] = item.NContent
        # 注意 item[3]是datetime.date对象
        record['NDate'] = str(item.NDate)  # like: 2019-10-1
        record['NPublisherId'] = item.NPublisherId

        new_data.append(record)
    return new_data


"""
模型
"""


class User(db.Model):
    __tablename__ = 'tb_user'
    # NOTE: 字段名必须与数据库的字段名一致
    Id = db.Column(db.String(20), primary_key=True)
    Pwd = db.Column(db.String(20))
    Privilege = db.Column(db.Integer)

    def __repr__(self):
        return '<User %r>' % self.uid


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


class Teacher(db.Model):
    __tablename__ = 'tb_teacher'
    TId = db.Column(db.String(20), primary_key=True)
    TName = db.Column(db.String(20))
    TBirth = db.Column(db.String(20))
    TSex = db.Column(db.String(20))
    TDept = db.Column(db.String(20))

    def __repr__(self):
        return '<Teacher %r>' % self.TId


class Course(db.Model):
    __tablename__ = 'tb_course'
    CId = db.Column(db.String(20), primary_key=True)
    CName = db.Column(db.String(20))
    CTeacherId = db.Column(db.String(20), db.ForeignKey('tb_teacher.TId'))
    CClassrome = db.Column(db.String(20))
    CTime = db.Column(db.String(20))
    CHours = db.Column(db.Integer)
    CVolum = db.Column(db.Integer)
    CRetake = db.Column(db.Integer)

    def __repr__(self):
        return '<Course %r>' % self.cname


class Grade(db.Model):
    __tablename__ = 'tb_grade'
    SId = db.Column(db.String(20), db.ForeignKey('tb_student.SId'), primary_key=True)
    CId = db.Column(db.String(20), db.ForeignKey('tb_course.CId'), primary_key=True)
    Grade = db.Column(db.Integer)

    # 重写这个方法，用orm查询得到的query对象结果就是这个方法的返回值，很方便
    # 可惜的是，返回值只能是str类型，我需要List类型，所以只能强制转换一下
    def __repr__(self):
        grades = list()
        grades.append(self.CId)
        grades.append(self.SId)
        # cname = Course.query.filter_by(CId=self.CId).one()[1]
        # cteacher_id = Course.query.filter_by(CId=self.CId).one()[2]
        # cteacher_name = Teacher.query.filter_by(TId=cteacher_id).one()[1]
        # grades.append(cname)
        # grades.append(cteacher_name)
        grades.append(self.Grade)
        return str(grades)


class Notice(db.Model):
    __tablename__ = 'tb_notice'
    NId = db.Column(db.String(20), primary_key=True)
    NTitle = db.Column(db.String(50))
    NContent = db.Column(db.String(200))
    NDate = db.Column(db.Date())
    NPublisherId = db.Column(db.String(20))
    # NPublisherName = db.Column(db.String(20))

    def __repr__(self):
        notices = list()
        notices.append(self.NId)
        notices.append(self.NTitle)
        notices.append(self.NContent)
        notices.append(self.NDate)
        return str(notices)



"""
视图
"""


# 启动服务器的第一个界面
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('signin.html')


# 进行登录验证，若正确，分发不同的身份界面；
# 若不正确，则返回login.html
# NOTE: 这里必须使用POST方法，对输入的内容 进行保护
# TODO: 记录用户登录状态，创建s会话
@app.route('/signin', methods=['POST'])
def login():
    # NOTE: 这里如果是get提交的，就使用request.args; 如果是post提交的，就使用request.form
    privilege = find_user(str(request.form['username']),
                          str(request.form['password'])
                          )
    if privilege and privilege[0] == 1:
        # print(privilege[0])
        session['username'] = request.form['username']
        # return render_template('s_index.html')		# 返回的是静态资源
        return redirect(url_for('s_index'))  # 这里使用重定向
    elif privilege and privilege[0] == 2:
        return redirect(url_for('t_index'))
    return render_template('signin.html', posts="用户名或密码错误")


# 用户注册
# 用户初始只有一张学生表、教师表， 必须注册之后，才会生成记录在user表中！
# TODO: 异常处理, 用户身份鉴别 -> 查询学生表和教师表，分配不同的权限
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error_msg = ""
    method = request.method
    # post 请求，则处理注册信息
    if method == 'POST':
        username = request.form['username']  # 学号为准
        password1 = request.form['password1']
        password2 = request.form['password2']
        if username and password1 and password2 and password1 == password2:

            # 用户id 检测
            if is_id_exist(username):
                flash("用户已经注册过！请直接登录", category="signup")
                return redirect(url_for('index'))

            # 用户身份甄别

            usr = User(Id=username, Pwd=password1, Privilege=1)
            try:
                db.session.add(usr)
                db.session.commit()
                flash("注册成功！现在登陆吧", category="signup")
                return redirect(url_for('index'))
            except pymysql.err.MySQLError:
                print("SQL ERROR: ")
                flash("数据库操作错误，检查你的输入！", category="signup")
                return redirect(url_for('index'))

        flash("信息填写错误，注册失败！", category="signup")
        return redirect(url_for('index'))

    # get 请求，则解析页面
    return render_template('signup.html')


# 学生用户主页
@app.route('/s_index')
def s_index():
    return render_template('s_index.html')


# 教师主页
# TODO: 完成页面分发, 这里暂时和学生主页内容设为一致的
@app.route('/t_index')
def t_index():
    return render_template('t_index.html')


# 专业课查询
# TODO: 时间字段正则匹配
@app.route('/course', methods=['GET', 'POST'])
def s_course():
    datas = get_table_data('tb_course')
    print(datas)

    # 这里数据库里的上课时间字段需要解析，使用正则匹配
    time_expr = ''
    for data in datas:
        time = data[4]

    return render_template('course.html', posts=datas)  # 把课程数据传过去


# **当前学生用户**
# 查询自己的所有成绩
# TODO: 多表查询
@app.route('/grade/<sid>')
def s_grade(sid):
    # grade = db.session.execute("SELECT * FROM tb_grade WHERE SId=" + sid)
    # 返回的是一个Grade对象列表
    grade_obj_list = Grade.query.filter_by(SId=sid).all()

    grades = list()
    for obj in grade_obj_list:
        grades.append(obj.to_list())
    return render_template('grade.html', posts=grades)


# 学生查看通知
@app.route('/s_notice')
def s_notice():
    notices = Notice.query.all()
    data = list()
    for notice in notices:
        data.append(notice.to_list())  # list contains a list
    return render_template("s_notice.html", posts=data)


# 教师管理通知
@app.route('/t_notice', methods=['GET', 'POST'])
def t_notice():
    if request.method == 'GET':
        data = to_json_like_data(list(Notice.query.all()))
        return render_template("t_notice.html", posts=data)
    elif request.method == 'POST':
        data = request.get_json()
        print(data)

        # TODO: 处理返回来的修改后的数据
        import datetime
        notice = Notice(
            NId=data['NId'],
            NTitle=data['NTitle'],
            NContent=data['NContent'],
            NDate=datetime.date.fromisoformat(data['NDate']),
            NPublisherId=data['NPublisherId']
        )

        notice2 = Notice.query.fliter_by(NId=data['NId']).one()

        return str(data)

@app.route('/test', methods=['GET','POST'])
def test():
    # data = request.get_json()
    data = request.get_json()
    print(data)
    return str(data)

@app.route('/signout')
def signout():
    session.pop("username")
    return render_template('signin.html', posts=['你已退出系统，欢迎再次登录！'])



if __name__ == "__main__":
    app.run(debug=False)
