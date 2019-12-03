#  Copyright (c) 2019.  MIT license
#  Jipeng Qian.
#  This is a copyrighted source code under MIT license,
#  you should receive a copy of the copyright,
#  together with this source code.
#  Have fun with your favor!


import chardet
import pandas as pd
from sqlalchemy import create_engine


def getAllUsersFromExcel(filename: str):
	with open(filename, "rb") as f:
		# data_frame = pd.read_csv(f)
		encoding = chardet.detect(f.read())['encoding']
	print(encoding)

	with open(filename, "r", encoding=encoding, errors='replace') as fo:
		data_info = pd.read_csv(fo)

	# print(data_info['学号'])

	return data_info[['学号', '姓名', '性别', '出生日期', '专业', '院系名称', '身份证件号']]


def allToDB(dataframe):
	connection = create_engine(
		"mysql+pymysql://{}:{}@{}/{}?charset={}"
			.format('root', '990505', '127.0.0.1:3306', 'jiaowu', 'utf8')
	) \
		.connect()

	# to_sql() 必须要使用sqlAlchemy或者sqlite连接
	dataframe.to_sql(name='tb_student', con=connection, if_exists='append', index=False)

# 生成数据库表
if __name__ == '__main__':
	data = getAllUsersFromExcel("2.csv")
	data.rename(columns={'学号': 'SId',
						 '姓名': 'SName',
						 '性别': 'SSex',
						 '出生日期': 'SBirth',
						 '专业': 'SMajor',
						 '院系名称': 'SDept',
						 '身份证件号': 'SIDNum',
						 },
				inplace=True)
	print(data[:1])

	allToDB(data)
