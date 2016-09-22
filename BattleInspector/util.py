#coding:utf-8
from logger import LOGGER
import time
from model import model_global_list
from PyQt4 import QtCore
# -------------------------------------------------------------------------------------------------------------------- #
# 工具类的操作
# -------------------------------------------------------------------------------------------------------------------- #


class Singleton(type):
	_instances = {}

	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
		return cls._instances[cls]


def to_unicode(s):
	# 中文统一转换成unicode
	if isinstance(s, unicode):
		return s
	# if isinstance(s, str):
	# 	return s.decode("ascii")
	if isinstance(s, QtCore.QString):
		return unicode(QtCore.QString(s))
	try:
		return unicode(s, "utf-8")
	except:
		LOGGER.error("toUnicode, cannot unicode the utf-8 str :" + s)
	try:
		return unicode(s, "gbk")
	except:
		LOGGER.error("toUnicode, cannot unicode the gbk str :" + s)
	return None


def get_now_time():
	# 返回当前时间
	return time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime(time.time()))


def slider_add_one():
	if model_global_list.g_slider_index < model_global_list.g_slider_max:
		model_global_list.g_slider_index += 1
	else:
		model_global_list.g_slider_index = model_global_list.g_slider_max


def str_match(str_src, str_dst):
	# 字符串匹配到出错位
		length = min(len(str_src), len(str_dst))
		for index in xrange(length):
			if str_dst[index] != str_src[index]:
				return index
		return index+1


# def update_entity_name(entity_name, name_list):
# 	# 查找entity_name对应的数值,标记为_加上个数数字，"entity_name_1" , "entity_name_2" ....
# 	equal_num = name_list.count(entity_name)
# 	if name_list.count(entity_name) == 0:
# 		return entity_name
# 	else:
# 		return entity_name + "_" + str(equal_num)
def update_entity_name(entity_name, entity_id):
	change_entity_name = entity_name + "(" + str(entity_id) + ")"
	return to_unicode(change_entity_name)


def parse_entity_name(entity_name):
	begin = 0
	end = 0
	for index_i in xrange(len(entity_name)):
		if entity_name[index_i] == "(":
			begin = index_i
		elif entity_name[index_i] == ")":
			end = index_i
	if end > begin:
		return entity_name[begin+1:end]
	else:
		return None

