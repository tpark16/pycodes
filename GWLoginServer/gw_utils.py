# -*- coding:utf-8 -*-

import codecs
import json


class GWUtils:
	
	def __init__(self):
		pass
	
	@staticmethod
	def dict_to_json(path, dict_value):
		try:
			with codecs.open(path, 'w', encoding='utf-8') as fh:
				fh.write(json.dumps(dict_value, ensure_ascii=False, indent=4, sort_keys=False))
		except Exception as e:
			print(e)
			return False
		return True
	
	@staticmethod
	def json_file_to_dict(path):
		try:
			with codecs.open(path, 'r', encoding='utf-8') as fh:
				json_value = fh.read()
				json_value = json.loads(json_value)
		except Exception as e:
			print(e)
			return False
		return json_value
