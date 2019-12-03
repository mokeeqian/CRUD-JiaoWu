from flask import Flask, request, render_template, flash
from flask import redirect
from flask import url_for
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
# 验证表单的函数
from wtforms.validators import DataRequired
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

pymysql.install_as_MySQLdb()

myApp = Flask(__name__)

myManager = Manager(myApp)

# 配置与数据库的连接
myApp.secret_key = 'sdfghjk'
myApp.config['WTF_CSRF_ENABLED'] = False
# 注意：虽然mysql中的建立的数据库可以不包含任何表，但是student数据库必须事先建立好，否则将无法创建连接。
myApp.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:990505@127.0.0.1:3306/jiaowu'
# 设置这一项为True后，每次请求结束后都会自动提交数据库中的变动。
# 设置为False后，每次使用commit来提交对数据库的最终修改是一种比较安全的做法。
myApp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

myDB = SQLAlchemy(myApp)

# 增加myDB命令到命令行
myMigrate = Migrate(myApp, myDB)
myManager.add_command('myDB', MigrateCommand)


# 创建班级表模型
class myClass(myDB.Model):
	__tablename__ = 'class'
	# 以下创建了表中的两个属性
	cid = myDB.Column(myDB.String(9), primary_key=True)
	cname = myDB.Column(myDB.String(20), unique=True)

	def __repr__(self):
		return '<myClass %r>' % self.cname

# 创建学生表模型
class myStudent(myDB.Model):
	__tablename__ = 'student'
	# 以下创建了 表中的四个属性
	sid = myDB.Column(myDB.String(9), primary_key=True)
	sname = myDB.Column(myDB.String(20), unique=True)
	sage = myDB.Column(myDB.Integer)
	cid = myDB.Column(myDB.String(9), myDB.ForeignKey('class.cid'))		# 作为class表的外键

	def __repr__(self):
		return '<myStudent %r>' % self.__name__


#  如果遇到E1101:Instance of 'SQLAlchemy' has no 'Integer' membe
# https://www.jianshu.com/p/ab72e830b2a9

# 为了简单期间，删除数据库中所有的表。
# myDB.drop_all()
# 然后重新根据数据模型创建数据库中的表。
# myDB.create_all()

# 下边给数据库添加几条记录
# 首先实例话几个对象，在内存中产生必要得数据。
Tom = myStudent(sid="s001", sname="Tom")
Jack = myStudent(sid="s002", sname="Jack")
Lucy = myStudent(sid="s003", sname="Lucy")
Kate = myStudent(sid="s004", sname="Kate")

# 将内存中实例化的对象持久化到数据库中
myDB.session.add(Tom)
myDB.session.add(Jack)
myDB.session.add(Lucy)
myDB.session.add(Kate)
# 最终向数据库提交最终的修改
myDB.session.commit()
# 到这里一共增加了4条记录
# 类似地，也可以删除记录
myDB.session.delete(Tom)
myDB.session.commit()

# 也可以查询所有的记录
myStudent.query.all()


myStudent.query.filter_by(sname="Lucy").all()

# 修改数据
Jack.sid = 100
myDB.session.commit()
# 以上，就是基于Flask框架直接使用python对数据库进行操作的代码。
# 更多的可以查询这里：
# https://blog.csdn.net/longting_/article/details/80658105


# 这里是启动web服务器的指令，相当于整个项目的入口。
if __name__ == '__main__':
	myApp.run(debug=True)

