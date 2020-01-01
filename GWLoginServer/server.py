# -*- coding:utf-8 -*-

import json

import tornado.ioloop
import tornado.web

from gw_utils import GWUtils

LAYER_LIST = GWUtils.json_file_to_dict('./res/layer.json')
USER_INFO = GWUtils.json_file_to_dict('./res/user_info.json')
NOTICE = GWUtils.json_file_to_dict('./res/notice.json')
UPDATE_URL = 'http://localhost:8888/static/update.zip'


class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("Hello, world")


class NoticeHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("Hello, Notice")
	
	def post(self):
		self.write(json.dumps(NOTICE, ensure_ascii=False))


class LoginHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("Hello, Login")
	
	def post(self):
		user_id = self.get_argument('userId')
		user_pwd = self.get_argument('userPwd')
		print(user_id, '/', user_pwd)
		response = {'yn': 'y', 'pluginVer': '1.0.0', 'updateUrl': UPDATE_URL, 'layerList': LAYER_LIST,
		            'loginVO': USER_INFO}
		self.write(json.dumps(response, ensure_ascii=False))


def make_app():
	return tornado.web.Application([
		(r"/", MainHandler),
		(r"/main/_noticeListCS.do", NoticeHandler),
		(r"/user/auth/loginActionCs.do", LoginHandler),
		(r"/static/(.*)", tornado.web.StaticFileHandler, {'path': './static'}),
	])

def start_server():
	app = make_app()
	app.listen(8888)
	tornado.ioloop.IOLoop.current().start()
