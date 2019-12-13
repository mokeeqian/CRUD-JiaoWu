#  Copyright (c) 2019.  MIT license
#  Jipeng Qian.
#  This is a copyrighted source code under MIT license,
#  you should receive a copy of the copyright,
#  together with this source code.
#  Have fun with your favor!

import os.path
import configparser


class ConfigLoader:
	def __init__(self):
		self.config_file = ".\config.conf"
		self.config = dict()

	def get_all_config(self):
		cf = configparser.ConfigParser()
		cf.read(self.config_file)

		self.config['db_name'] = str( cf.get('db', 'db_name') )
		self.config['db_user'] = str( cf.get('db', 'db_user') )
		self.config['db_password'] = str( cf.get('db', 'db_password') )

		return self.config

if __name__ == '__main__':
	config = ConfigLoader().get_all_config()
	print(config)