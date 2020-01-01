# -*- coding:utf-8 -*-
import asyncio
import json
import sys, shutil
import tornado

from server import start_server

from PyQt5.QtCore import Qt
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import *

from gw_utils import GWUtils

_ui_path = 'GWLoginServerUI.ui'
FORM_CLASS, _ = uic.loadUiType(_ui_path)


class ThreadClass(QtCore.QThread):
    def __init__(self, parent= None):
        super(ThreadClass, self).__init__(parent)

    def run(self):
        while True:
            asyncio.set_event_loop(asyncio.new_event_loop())
            start_server()

class main(QMainWindow, FORM_CLASS):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setUi()
        self.setSlot()
        self.threadclass = ThreadClass()
        self.show()


    def setUi(self):
        self.listWidget.clear()
        #notice
        self.noticeDict = dict()
        self.result = GWUtils.json_file_to_dict('res/notice.json')
        self.temp_notice = list(self.result.values())[0]
        for i in range(len(self.temp_notice)):
            self.listWidget.addItem(self.temp_notice[i].get('ntTitle'))
            self.noticeDict[self.temp_notice[i].get('ntTitle')] = self.temp_notice[i].get('ntContent')


        # login
        self.loginInfo = GWUtils.json_file_to_dict('./user_info.json')
        self.loginTable.setRowCount(0)
        for row, (k, v) in enumerate(self.loginInfo.items()):
            userId = k
            userPwd = v.get('password')
            roleId = v.get('roleId')
            self.loginTable.insertRow(row)
            item1, item2, item3 = QTableWidgetItem(), QTableWidgetItem(), QTableWidgetItem()
            item1.setData(Qt.DisplayRole, '{0}'.format(userId))
            item2.setData(Qt.DisplayRole, '{0}'.format(userPwd))
            item3.setData(Qt.DisplayRole, '{0}'.format(roleId))
            self.loginTable.setItem(row, 0, item1)
            self.loginTable.setItem(row, 1, item2)
            self.loginTable.setItem(row, 2, item3)

        #Layer
        layer = GWUtils.json_file_to_dict('res/layer.json')
        for i in reversed(range(len(layer))):
            layerName = layer[i].get('tableNm')
            write = layer[i].get('write')
            self.layerTable.insertRow(row)
            item1 = QTableWidgetItem()
            item1.setData(Qt.DisplayRole, '{0}'.format(layerName))
            if write == 'y':
                item1.setCheckState(Qt.Checked)
            else:
                item1.setCheckState(Qt.Unchecked)
            self.layerTable.setItem(row, 0, item1)

    #버튼 액션
    def setSlot(self):
        self.startServer.clicked.connect(self.onClickedStart)
        self.listWidget.itemClicked.connect(self.notice)
        self.addLogin.clicked.connect(self.loginAdd)
        self.savLogin.clicked.connect(self.loginSave)
        self.delLogin.clicked.connect(self.loginDel)
        self.addNotice.clicked.connect(self.noticeAdd)
        self.savNotice.clicked.connect(self.noticeSave)
        self.delNotice.clicked.connect(self.noticeDel)
        self.editLayer.clicked.connect(self.layerEdit)
        self.savLayer.clicked.connect(self.layerSav)
        self.uploadFile.clicked.connect(self.fileUpload)

    def notice(self, item):
        self.noticeText.setText(self.noticeDict.get(item.text()))

    def noticeAdd(self):
        self.listWidget.addItem('새 공지사항')
        self.listWidget.item(self.listWidget.count() - 1).setSelected(True)
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            item.setFlags(item.flags() | Qt.ItemIsEditable)
        self.noticeText.clear()
        self.noticeText.setPlaceholderText('편집 후 저장 필수')
        self.noticeText.setReadOnly(False)

    def noticeDel(self):
        for item in self.listWidget.selectedItems():
            title = self.listWidget.takeItem(self.listWidget.row(item))
            for i in range(len(self.temp_notice)):
                if self.temp_notice[i]['ntTitle'] == title.text():
                    del self.temp_notice[i]
                    break
        self.result['resultList'] = self.temp_notice
        GWUtils.dict_to_json('res/notice.json', self.result)
        self.noticeText.clear()

    def noticeSave(self):
        item = self.listWidget.selectedItems()[0]
        row = self.listWidget.row(item)
        tv = self.noticeText.toPlainText()
        temp_dict = dict()
        temp_dict['ntTitle'] = item.text()
        temp_dict['ntContent'] = tv

        #check
        if len(self.temp_notice) < (row + 1):
            self.temp_notice.append(temp_dict)
        elif len(self.temp_notice) >= (row + 1):
            self.temp_notice[row] = temp_dict

        self.result['resultList'] = self.temp_notice
        GWUtils.dict_to_json('res/notice.json', self.result)
        self.setUi()
        # return QMessageBox.information('알림', '성공적으로 저장했습니다.')

    def loginAdd(self):
        row = self.loginTable.rowCount()
        self.loginTable.insertRow(row)
        item1, item2, item3 = QTableWidgetItem(), QTableWidgetItem(), QTableWidgetItem()
        item1.setData(Qt.DisplayRole, '')
        item2.setData(Qt.DisplayRole, '')
        item3.setData(Qt.DisplayRole, '')
        self.loginTable.setItem(row, 0, item1)
        self.loginTable.setItem(row, 1, item2)
        self.loginTable.setItem(row, 2, item3)
        self.loginTable.setCurrentCell(row, 0)
        self.loginTable.scrollToBottom()
        self.loginTable.setEditTriggers(QAbstractItemView.DoubleClicked)

    def loginSave(self):
        self.loginInfo.clear()
        for i in range(self.loginTable.rowCount()):
            id, pw, role = self.loginTable.item(i, 0).text(), self.loginTable.item(i, 1).text(), self.loginTable.item(i, 2).text()
            if id == "":
                continue
            self.loginInfo.update({id: {'password': pw, 'roleId': role}})
        GWUtils.dict_to_json('./user_info.json', self.loginInfo)
        self.setUi()
        return QMessageBox.information(self, '알림', '성공적으로 저장했습니다.')

    def loginDel(self):
        for item in self.loginTable.selectedItems():
            row = self.loginTable.row(item)
            self.loginTable.removeRow(row)
        self.loginInfo.clear()
        temp = dict()
        for i in range(self.loginTable.rowCount()):
            id, pw, role = self.loginTable.item(i, 0).text(), self.loginTable.item(i, 1).text(), self.loginTable.item(i, 2).text()
            if id == "":
                continue
            temp['password'] = pw
            temp['roleId'] = role
            self.loginInfo[id] = temp
        GWUtils.dict_to_json('res/user_info.json', self.loginInfo)



    def fileUpload(self):
        fname = QFileDialog.getOpenFileName(self)
        print(fname)
        shutil.copy(fname[0], './static')
        self.fileName.setText(fname[0])

        return QMessageBox.information(self, '알림', '성공적으로 업로드했습니다.')

    # Layer
    def layerEdit(self):
        row = self.layerTable.rowCount()
        self.layerTable.insertRow(row)
        item1 = QTableWidgetItem()
        item1.setCheckState(Qt.Unchecked)
        item1.setData(Qt.DisplayRole, '')
        self.layerTable.setItem(row, 0, item1)
        self.layerTable.setCurrentCell(row, 0)
        self.layerTable.scrollToBottom()
        self.layerTable.setEditTriggers(QAbstractItemView.DoubleClicked)

    def layerSav(self):
        # layer_dict = dict()
        layer_list = []
        for row in range(self.layerTable.rowCount()):
            layerName = self.layerTable.item(row, 0).data(Qt.DisplayRole)

            if not layerName:
                return QMessageBox.information(self, '알림', '유효하지 않은 레이어 이름입니다.')

            if self.layerTable.item(row, 0).checkState() == Qt.Checked:
                write = 'y'
            else:
                write = 'n'

            layer_list.append({'tableNm': layerName, 'write': write})

        # print(layer_list)
        GWUtils.dict_to_json('res/layer.json', layer_list)
        # self.setUi()

        return QMessageBox.information(self, '알림', '성공적으로 저장했습니다.')

    def onClickedStart(self):
        self.threadclass.start()
        self.startServer.blockSignals(True)

        return QMessageBox.information(self, '알림', '성공적으로 실행했습니다.')


        # t = threading.Thread(target=start_server())
        # t.daemon = True
        # t.start()

if __name__ == "__main__":

    app = QApplication([])
    ex = main()
    sys.exit(app.exec_())