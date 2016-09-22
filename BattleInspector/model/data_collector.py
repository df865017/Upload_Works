# -*- coding: utf-8 -*-
# 2016-05-27 23:08
__author__ = 'gzdaifeng'
from common_data import CommonData
import model_global_list
from config_data import CONFIG_DATA
import socket
import rpyc
import util
import os
from logger import LOGGER
import time
import xlwt
# -------------------------------------------------------------------------------------------------------------------- #
# rpyc_输入输出的接口
# entity_data_list
# 	["Avatar", self.avatar_list],
# 	["Sprite", self.sprite_list],
# 	["Monster", self.monster_list],
# entity_list
#
# -------------------------------------------------------------------------------------------------------------------- #


class DataCollector:
	def __init__(self):
		self.conn_error = True
		self.last_error_time = 0
		self.avatar_list = []
		self.monster_list = []
		self.sprite_list = []
		self.id_to_entity = {}
		com_data = CommonData()

		self.get_seq_tabs = com_data.get_seq_tabs
		self.set_seq_tabs = com_data.set_seq_tabs
		self.get_point_tab = com_data.get_point_tab
		self.set_point_tab = com_data.set_point_tab
		self.get_slider_order = com_data.get_slider_order
		self.set_slider_order = com_data.set_slider_order
		self.removal_seq_tabs = com_data.removal_seq_tabs

	# =====================================================#
	# 属性的存取
	# =====================================================#
	def get_conn_error(self):
		return self.conn_error

	def set_conn_error(self, val):
		self.conn_error = val
	# =====================================================#
	# rpyc数据的存取
	# =====================================================#

	def test_connect(self, ip="127.0.0.1", port=18812):
		try:
			rpyc.classic.connect(ip, port)
			return True
		except (socket.error, EOFError):
			self.conn_error = True
			return False

	def _read_entity(self, ip="127.0.0.1", port=18812):
		if time.time() - self.last_error_time < 10:
			return
		try:
			self.ip = ip
			self.port = port
			self.id_to_entity = {}
			self.avatar_list = []
			self.monster_list = []
			self.sprite_list = []
			if self.conn_error:
				self.conn = rpyc.classic.connect(self.ip, self.port)
			# ent_mgr = self.conn.modules.common.EntityManager
			entities = self.conn.modules.common.EntityManager.EntityManager._entities
			# self.conn.module.common.EntityManager.EntityManager
			Avatar = self.conn.modules.entities.Avatar.Avatar
			AvatarAliance = self.conn.modules.entities.AvatarAliance.AvatarAliance
			Monster = self.conn.modules.entities.Monster.Monster
			Sprite = self.conn.modules.entities.Sprite.Sprite

			for id, e in entities.items():
				if isinstance(e, Avatar) or isinstance(e, AvatarAliance):
					self.avatar_list.append(e)
					self.id_to_entity[str(id)] = id
				elif isinstance(e, Monster):
					self.monster_list.append(e)
					self.id_to_entity[str(id)] = id
				elif isinstance(e, Sprite):
					self.sprite_list.append(e)
					self.id_to_entity[str(id)] = id

			self.sort_entity_list(self.avatar_list)
			self.sort_entity_list(self.monster_list)
			self.sort_entity_list(self.sprite_list)
		except (socket.error, EOFError):
			self.conn_error = True
			self.last_error_time = time.time()
			LOGGER.error("_read_entity, rpyc connect error, please open the game client!")
			return
		self.conn_error = False

	@staticmethod
	def sort_entity_list(entity_list):
		# 对相同实体的不同对象名进行排序，冒泡排序
		for i in xrange(len(entity_list) - 1):
			for j in xrange(i + 1, len(entity_list)):
				if cmp(str(entity_list[i].id), str(entity_list[j].id)) > 0:
					entity_list[i], entity_list[j] = entity_list[j], entity_list[i]

	def update_entity(self):
		# 更新实体数据，返回ui表格数据
		self._read_entity()
		entity_data_list = [
			["Avatar", self.avatar_list],
			["Sprite", self.sprite_list],
			["Monster", self.monster_list],
		]
		point_tab = self._init_ui_tab(entity_data_list, CONFIG_DATA.all_attr_list)
		return point_tab

	def _get_entity_name(self, e):
		# 获取实体的名称
		try:
			if self.conn_error:
				self.conn = rpyc.classic.connect(self.ip, self.port)
			Avatar = self.conn.modules.entities.Avatar.Avatar
			AvatarAliance = self.conn.modules.entities.AvatarAliance.AvatarAliance
			Monster = self.conn.modules.entities.Monster.Monster
			Sprite = self.conn.modules.entities.Sprite.Sprite

			if isinstance(e, Avatar) or isinstance(e, AvatarAliance):
				# return e.char_name.decode("utf-8")
				return util.to_unicode(e.char_name)
			elif isinstance(e, Sprite):
				# return e.sprite_dict["name"].decode("utf-8")
				return util.to_unicode(e.sprite_dict["name"])
			elif isinstance(e, Monster):
				# return e.monster_data["name"].decode("utf-8")
				return util.to_unicode(e.monster_data["name"])
		except (socket.error, EOFError):
			self.conn_error = True
			self.avatar_list = []
			self.monster_list = []
			self.sprite_list = []
			return
		self.conn_error = False

	@staticmethod
	def _add_col_titles(attr_list):
		# 添加列标题, 输入为配置文件中列标题的中文名称
		index_j = 0
		temp_titles = {}
		for attr_pair in attr_list:
			if index_j == 0:
				# temp_titles[index_j] = util.get_now_time()
				temp_titles[index_j] = "entity_value"
				index_j += 1
			try:
				temp_titles[index_j] = util.to_unicode(attr_pair[1])  # util.toUnicode(attr_pair[1])
			except:
				LOGGER.error("_init_avatar_tab, cannot decode the avatar_data :"+attr_pair[1])
			index_j += 1
		return temp_titles

	@staticmethod
	def _add_row(row_name, attr_list, e):
		# 添加表格数据一行,输入为$1: 行首实体名,$2: 配置文件中变量的同名字符串, $3: 数据实体，
		index_j = 0
		temp_row = {}
		for attr_pair in attr_list:
			if index_j == 0:
				temp_row[index_j] = row_name  # self._getEntityName(e)
				index_j += 1
			try:
				temp_row[index_j] = str(eval("e.%s" % attr_pair[0]))
			except:
				# 补充空白
				temp_row[index_j] = None
				# LOGGER.war("_add_row, have no attribute value; " + "give the None to " + attr_pair[0])
			index_j += 1
		return temp_row

	def _init_ui_tab(self, entity_data_list, attr_list):
		# 初始化ui_tab, 返回ui_tab的dict类型数据,$1: 实体数据， $2: 列属性顶定制
		ui_tab = {}
		# 表格的行脚标变量
		index_i = 0
		for entity_type_i in xrange(len(entity_data_list)):
			for e in entity_data_list[entity_type_i][1]:

				if index_i == 0:
					# 添加列标题
					temp_titles = self._add_col_titles(attr_list)
					ui_tab[index_i] = temp_titles
					index_i += 1

					# 添加第一行
					entity_name = self._get_entity_name(e)
					# 未断开连接，添加数据
					if entity_name is not None:
						temp_row = self._add_row(util.update_entity_name(entity_name, e.id), attr_list, e)
						ui_tab[index_i] = temp_row
						index_i += 1
				else:
					# 添加第i行
					entity_name = self._get_entity_name(e)
					if entity_name is not None:
						temp_row = self._add_row(util.update_entity_name(entity_name, e.id), attr_list, e)
						ui_tab[index_i] = temp_row
						index_i += 1
		return ui_tab

	def read_tabs_interface(self, slider_order=None):
		# 读取rpyc数据的接口，无返回值
		time_seq_tabs = self._read_tabs()
		self.set_seq_tabs(time_seq_tabs)
		if slider_order is not None:
			time_point_tab = time_seq_tabs[slider_order]
			self.set_point_tab(time_point_tab)

	def _read_tabs(self):
		# 更新所有实体的数据，返回time_seq_tabs数据
		self._read_entity()
		entity_data_list = [
			["Avatar", self.avatar_list],
			["Sprite", self.sprite_list],
			["Monster", self.monster_list],
		]
		point_tab = self._init_ui_tab(entity_data_list, CONFIG_DATA.all_attr_list)
		# self.set_point_tab(point_tab)
		self.set_seq_tabs(point_tab, self.get_slider_order())
		return self.get_seq_tabs()

	def write_tabs_interface(self, time_seq_tabs, slider_order=None):
		# 写入表格数据的接口,无返回值
		if slider_order is None:
			self.set_seq_tabs(time_seq_tabs)
		else:
			point_tab = time_seq_tabs
			self.set_point_tab(point_tab, slider_order)

	@staticmethod
	def _search_variable_name(v_name, attr_list):
		# 查找变量名
		for attr_pair in attr_list:
			if attr_pair[1] == v_name:
				return attr_pair[0]
		LOGGER.war("_search_variable_name, cannot find variable_name in all_attr_list!")

	def update_entity_cell(self, row_items, col_items, value):

		search_entity_name = row_items
		entity_id_str = util.parse_entity_name(search_entity_name)
		if entity_id_str:
			entity_id = self.id_to_entity[entity_id_str]
			e = self._get_entity(entity_id)
			variable_name = self._search_variable_name(col_items, CONFIG_DATA.all_attr_list)

			tag = "e." + variable_name
			self.execute_statement(tag, value, e)

	def update_entity_tab(self, xy_items_vlaue):
		# ui_tab数据的修改，写入到服务器端
		for index in xrange(len(xy_items_vlaue)):
			row_items, col_items, value = xy_items_vlaue[index]
			self.update_entity_cell(row_items, col_items, value)

	@staticmethod
	def execute_statement(tag, value, e):
		# 对于不同类型数据，进行不同数值转换赋值
		data = eval("%s" % tag)
		try:
			if isinstance(data, float):
				exec('%s = %f' % (tag, float(value)))
			elif isinstance(data, str):
				exec('%s = str(value)' % tag)
			elif isinstance(data, bool):
				exec('%s = bool(value)' % tag)
			elif isinstance(data, int):
				exec('%s = int(value)' % tag)
			elif isinstance(data, list):
				exec('%s = list(value)' % tag)
			elif isinstance(data, dict):
				exec('%s = dict(value)' % tag)
			else:
				LOGGER.war("execute_statement, connot find  " + tag + " type in [ float, bool, int, list, dict ] ")
		except:
			LOGGER.war("execute_statement, connot give the collect type to " + tag)

	@staticmethod
	def excel_list(seq_tabs):
		# excel 输出0~99帧的point_tab文件数据
		workbook = xlwt.Workbook()
		if len(seq_tabs) == model_global_list.g_slider_max:
			for index_i in xrange(len(seq_tabs)):
				sheet_name = "tab" + str(index_i)
				point_tab = seq_tabs[index_i]
				sheet = workbook.add_sheet(sheet_name, cell_overwrite_ok=True)
				if len(point_tab) > 0:
					for i in xrange(len(point_tab)):
						for j in xrange(len(point_tab[i])):
							sheet.write(i, j, point_tab[i][j])
			file_name = util.get_now_time() + model_global_list.g_file_type
			file_path = model_global_list.g_file_dir + file_name
			full_file = os.path.join(file_path)
			try:
				workbook.save(full_file)
			except:
				LOGGER.error("excel_list, please close the .xls file before running the program!")

	def _get_entity(self, entity_id):
		# 通过实体id 获取实体对象
		ent_manager = self.conn.modules.common.EntityManager.EntityManager
		return ent_manager.getentity(entity_id)

	def identify_entity(self, item_name):
		# 高亮识别操作的实体数据
		try:
			entity_id_str = util.parse_entity_name(item_name)
			if entity_id_str:
				entity_id = self.id_to_entity[entity_id_str]
				entity = self._get_entity(entity_id)

				effect_mgr = self.conn.modules.h2.effect_manager
				path = 'combat\light\light_zt_fukong.sfx'
				buffer = 'buff1'
				effect_mgr.play_effect_mount_to_model(entity.visual, 0, path, buffer)
			else:
				LOGGER.error("identify_entity(self, item_name), cannot get the entity_id_str!")
		except:
			LOGGER.error("identify_entity(self, item_name), fail to execute dm47.h2 namespace function h2.effect_manager.play_effect_mount_to_model!")

	def connect_namespace(self, ip='127.0.0.1', port=18812):
		# 访问命名空间
		if self.test_connect(ip, port):
			from namespace_utils import NamespaceManager
			try:
				# 通过ip和命名空间连接上数据
				result = NamespaceManager.connect(host=ip, namespace='dm47')
				if result is not None:
					# print '$set connected True'
					return result
				else:
					# print '$connect failed'
					return False
			except Exception as ex:
				# print '$connect Exception'
				return False
