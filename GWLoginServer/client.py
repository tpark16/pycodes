# -*- coding:utf-8 -*-

import os
import json
from optparse import OptionParser
import requests

def request_login(url, user_id, user_pw):
	param = {'userId': user_id, 'userPwd': user_pw}
	response = requests.post(os.path.join(URL, 'user/auth/loginActionCs.do'), params=param)
	# print(response.status_code)
	# print(response.content)
	login_result_dict = json.loads(response.content)
	print(type(login_result_dict), login_result_dict)

	
def request_notice(url):
	response = requests.post(os.path.join(url, 'main/_noticeListCS.do'))
	# print(response.status_code)
	# print(response.content)
	notice_dict = json.loads(response.content)
	# print(type(notice_dict), notice_dict)


def main():
	usage = "Usage: %prog [options] filename"
	parser = OptionParser(usage=usage)
	parser.add_option('-r', '--url', dest='request_url', default=URL)
	parser.add_option('-u', '--user', dest='user_id', default=USER_ID)
	parser.add_option('-p', '--password', dest='user_pw', default=USER_PW)
	parser.add_option("-t", "--type", dest="request_type", default='n', help='[n]otice or [l]ogin')
	options, args = parser.parse_args()
	
	# print(type(options), options)
	# print(args)
	
	if options.request_type == 'n':
		request_notice(options.request_url)
	elif options.request_type == 'l':
		request_login(options.request_url, options.user_id, options.user_pw)
	else:
		return
	

if __name__ == '__main__':
	URL = 'http://localhost:8888/'
	USER_ID = 'thlee'
	USER_PW = 'passwd!@'
	main()
