#coding:utf-8

import ConfigParser
import codecs

# 配置文件(.conf)


class ConfigData(object):
	def __init__(self, config_file="config.conf"):
		self.cf = ConfigParser.ConfigParser()
		self.ip = "127.0.0.1"
		self.port = 18812
		self.attr_dict = [("logic.ability.hp", u"血量")]
		self.error = False
		try:
			self.config_file = config_file
			self.cf.readfp(codecs.open(self.config_file, "r", "utf-8-sig"))
			self.ip = self.cf.get("rpyc_conf", "ip")
			self.port = self.cf.getint("rpyc_conf", "port")
			self.attr_list = self.cf.items("attr")
			self.all_attr_list = self.cf.items("all_attr")
		except:
			import traceback
			traceback.print_exc()
			self.error = True

	def update_attr(self, new_attr_list):
		self.cf.remove_section("attr")
		self.cf.add_section("attr")
		for attr_pair in new_attr_list:
			self.cf.set("attr", attr_pair[0].encode('utf-8'), attr_pair[1].encode('utf-8'))
		self.cf.write(open(self.config_file, "w"))
		self.attr_list = new_attr_list

CONFIG_DATA = ConfigData()
	
if __name__ == '__main__':
	print CONFIG_DATA.error
	print CONFIG_DATA.ip
	print CONFIG_DATA.port
	print len(CONFIG_DATA.attr_list), CONFIG_DATA.attr_list
