# -*- coding: utf-8 -*-
# 2016-05-27 23:08
__author__ = 'gzdaifeng'

import logging
import os
# -------------------------------------------------------------------------------------------------------------------- #
# 程序入口 --- 日志的模块
# -------------------------------------------------------------------------------------------------------------------- #


class Logger(object):
	def __init__(self, path='./tmp/test.log', c_level=logging.DEBUG, f_level=logging.DEBUG):
		# 文件的新建
		if not os.path.isdir("./tmp/"):
			os.mkdir("./tmp/")
		self.logger = logging.getLogger(path)
		self.logger.setLevel(logging.DEBUG)
		# [%(filename)s] [line:%(lineno)d] 也可以添加这两行
		fmt = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
		# 设置CMD日志
		sh = logging.StreamHandler()
		sh.setFormatter(fmt)
		sh.setLevel(c_level)
		# 设置文件日志
		fh = logging.FileHandler(path)
		fh.setFormatter(fmt)
		fh.setLevel(f_level)
		self.logger.addHandler(sh)
		self.logger.addHandler(fh)

	def debug(self, message):
		self.logger.debug(message)

	def info(self, message):
		self.logger.info(message)

	def war(self, message):
		self.logger.warn(message)

	def error(self, message):
		self.logger.error(message)

	def cri(self, message):
		self.logger.critical(message)

LOGGER = Logger()

if __name__ == "__main__":
	str = '一个debug信息'
	LOGGER.debug(str.decode('utf-8'))

