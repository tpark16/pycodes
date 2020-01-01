# -*- coding:utf-8 -*-

import json

import tornado.ioloop
import tornado.web

from gw_utils import GWUtils

# LAYERS = ['bml_admb_ls', 'bml_badm_as', 'bml_bldg_as', 'bml_carc_as', 'bml_elev_ls', 'bml_elev_ps', 'bml_etcp_ps', 'bml_grnd_as', 'bml_hadm_as', 'bml_i005_as', 'bml_i010_as', 'bml_i025_as', 'bml_i050_as', 'bml_pole_ps', 'bml_rail_ls', 'bml_rivr_as', 'bml_symb_ps', 'bml_wall_ls', 'gj_1997_1', 'gj_2001_1', 'gj_2002_1', 'gj_2008_1', 'gj_2010_1', 'gj_2011_1', 'gj_2013_1', 'gj_2014_1', 'gj_2016_1', 'gj_2017_1', 'lt_c_uq111', 'lt_c_uq112', 'lt_c_uq113', 'lt_c_uq114', 'rdl_admn_as', 'rdl_brdg_as', 'rdl_busl_ls', 'rdl_bycp_ls', 'rdl_byst_ps', 'rdl_cctv_ps', 'rdl_cmdt_as', 'rdl_conv_ps', 'rdl_cros_ps', 'rdl_ctlr_ls', 'rdl_etct_as', 'rdl_etct_ls', 'rdl_etct_ps', 'rdl_evrd_as', 'rdl_exbn_ls', 'rdl_excv_as', 'rdl_expl_as', 'rdl_exsb_as', 'rdl_help_as', 'rdl_mdst_ls', 'rdl_moas_ps', 'rdl_nspv_as', 'rdl_ocup_as', 'rdl_ocup_ls', 'rdl_ocup_ps', 'rdl_over_as', 'rdl_ovps_as', 'rdl_pakp_ps', 'rdl_pave_as', 'rdl_pdcr_as', 'rdl_prot_ls', 'rdl_rbln_ls', 'rdl_rbln_ls_2', 'rdl_rdar_as', 'rdl_rdsn_ps', 'rdl_refr_ls', 'rdl_refr_ps', 'rdl_rmir_ps', 'rdl_rnum_ps', 'rdl_rout_ls', 'rdl_sbwy_as', 'rdl_scho_as', 'rdl_sclt_ps', 'rdl_sdhp_as', 'rdl_sepc_ps', 'rdl_sget_ps', 'rdl_smrw_ls', 'rdl_soil_ps', 'rdl_spdm_ls', 'rdl_sqar_as', 'rdl_stat_ps', 'rdl_stlt_ps', 'rdl_swlk_ls', 'rdl_tbrd_as', 'rdl_tfsn_ps', 'rdl_trct_ps', 'rdl_tree_ps', 'rdl_trnl_as', 'rdl_trsn_ps', 'rdl_ugrd_as', 'rdl_uprl_ls', 'rdl_urbc_ps', 'rdl_walk_ps', 'swl_aodp_as', 'swl_aodr_as', 'swl_clay_ps', 'swl_clpi_lm', 'swl_conn_ls', 'swl_dept_ps', 'swl_dodp_as', 'swl_dodr_as', 'swl_dran_ps', 'swl_manh_ps', 'swl_meas_ps', 'swl_pipe_as', 'swl_pipe_lm', 'swl_pres_ps', 'swl_pump_ps', 'swl_rsph_ls', 'swl_side_ls', 'swl_spew_ps', 'swl_spot_ps', 'swl_vent_ps', 'swl_vswd_ls', 'tl_scco_sig', 'tl_scco_sig_label', 'tl_spbd_buld', 'tl_spbd_entrc', 'tl_sprd_intrvl', 'tl_sprd_manage', 'tl_sprd_rw', 'ufl_bcon_as', 'ufl_bcon_lm', 'ufl_bman_ps', 'ufl_bopc_ps', 'ufl_bpip_lm', 'ufl_bpip_ps', 'ufl_bpol_ps', 'ufl_btrs_ps', 'ufl_bvnt_ps', 'ufl_glpi_lm', 'ufl_gman_ps', 'ufl_gmnt_ps', 'ufl_gpip_lm', 'ufl_gprs_ps', 'ufl_gval_ps', 'ufl_havt_ps', 'ufl_hhnd_ps', 'ufl_hlek_ps', 'ufl_hman_ps', 'ufl_hpip_lm', 'ufl_hpip_ps', 'ufl_kman_ps', 'ufl_kpip_ls', 'ufl_kpip_ps', 'ufl_kpol_ps', 'wtl_aral_as', 'wtl_aras_as', 'wtl_bare_as', 'wtl_clos_ps', 'wtl_clpi_lm', 'wtl_conn_ps', 'wtl_fire_ps', 'wtl_flow_ps', 'wtl_gain_ps', 'wtl_gand_as', 'wtl_gbnd_as', 'wtl_head_ps', 'wtl_leak_ps', 'wtl_manh_ps', 'wtl_meta_as', 'wtl_meta_ps', 'wtl_omet_ps', 'wtl_pinf_ps', 'wtl_pipe_lm', 'wtl_pipe_ps', 'wtl_pres_ps', 'wtl_prga_ps', 'wtl_ptcn_ps', 'wtl_puri_as', 'wtl_refr_ls', 'wtl_refr_ps', 'wtl_rfid_ps', 'wtl_rsrv_ps', 'wtl_serv_ps', 'wtl_sply_ls', 'wtl_stpi_ps', 'wtl_supp_ls', 'wtl_valv_ps', 'wtl_wcln_ps']
# LAYER_LIST = list()
# for layer_name in LAYERS:
# 	LAYER_LIST.append({'tableNm': layer_name, 'write': 'y'})
# USER_INFO = {'aprState': 'Y', 'changPwDate': '2017-08-01 00:00:00.0', 'contIp': '1.234.21.200', 'gbnL': '시청', 'gbnM': '도시재생국(시청)', 'gbnS': '토지정보과', 'lastLogin': '2019-04-25 17:28:46', 'memNo': '1', 'misscnt': '2', 'roleId': 'R0001', 'userClass': '', 'userEmail': '', 'userId': 'admin', 'userName': '관리자', 'userPwd': '279849cf01a0bb33f0e25c3f33972e99', 'userTel': '609-4592'}


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
