import base64
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import parse

from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys, os, collections

default_path = '/Users/taeyunpark/Desktop/123456789-20191008T184829Z-001/123456789/eqmap/EQ_Map/res/message.xml'
_ui_path = 'ConverterUI.ui'
FORM_CLASS, _ = uic.loadUiType(_ui_path)

class Converter(QMainWindow, FORM_CLASS):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setUi()
        self.korList = collections.OrderedDict()
        self.engList = collections.OrderedDict()
        self.tree = parse(default_path)
        self.root = self.tree.getroot()
        self.setSlot()
        self.show()

    def parsefile_kor(self):
        tree = ET.parse('message.xml')
        root = tree.getroot()
        kor_elem = root.find("kor")
        kor_message_elem = kor_elem.find('message')
        self.kor_list = collections.OrderedDict()
        for _elem in list(kor_message_elem):
            kor_tag = _elem.tag.strip()
            kor_value = _elem.text.strip()
            kor_decoded = base64.b64decode(kor_value).decode('utf-8')
            self.kor_list[kor_tag] = kor_decoded
        return self.kor_list

    def parsefile_eng(self):
        tree = ET.parse('message.xml')
        root = tree.getroot()
        eng_elem =root.find("eng")
        eng_message_elem = eng_elem.find('message')
        self.BTS_eng_list = collections.OrderedDict()
        for _elem in list(eng_message_elem):
            BTS_eng_tag = _elem.tag.strip()
            BTS_eng_value = _elem.text.strip()
            eng_decoded = base64.b64decode(BTS_eng_value).decode('utf-8')
            self.BTS_eng_list[BTS_eng_tag] = eng_decoded
        return self.BTS_eng_list

    def test(self):
        self.korList.clear()
        for elem in self.root.find('kor').find('message'):
            layerName = elem.tag.strip()
            disp_Name = elem.text.strip()
            kor_decoded = base64.b64decode(disp_Name).decode('utf-8')
            self.korList[layerName] = kor_decoded

    def setUi(self):
        self.tableWidget.setEnabled(False)
        self.table_eng.setEnabled(False)
        self.Btn_find.setVisible(False)
        self.lineEdit.setVisible(False)

    # 버튼 액션
    def setSlot(self):
        self.Btn_test.clicked.connect(self.test)
        self.Btn_eng.clicked.connect(self.eng_tag)
        self.Btn_kor.clicked.connect(self.kor_tag)
        #self.Btn_loading.clicked.connect(self.parsefile_kor)
        self.Btn_save_kor.clicked.connect(self.savefile_kor)
        self.Btn_search.clicked.connect(self.search_dialog)
        self.Btn_save_eng.clicked.connect(self.savefile_eng)
        self.Btn_insert.clicked.connect(self.insert)
        self.Btn_find.clicked.connect(self.search)
        self.Btn_remove.clicked.connect(self.remove)

    def eng_tag(self):
        #self.tableWidget.clear()
        self.table_eng.setEnabled(True)
        self.table_eng.setRowCount(len(self.parsefile_eng()))
        self.table_eng.setColumnCount(2)
        self.table_eng.setHorizontalHeaderItem(0, QTableWidgetItem('메세지번호'))
        self.table_eng.setHorizontalHeaderItem(1, QTableWidgetItem('Text'))
        i = 0
        while i < len(self.parsefile_eng()):
            for k, v in self.parsefile_eng().items():
                self.table_eng.setItem(i, 0, QTableWidgetItem(k))
                self.table_eng.setItem(i, 1, QTableWidgetItem(v))
                i += 1
            # break
        self.table_eng.resizeColumnsToContents()
        self.table_eng.resizeRowsToContents()

    def kor_tag(self):
        self.tableWidget.setEnabled(True)
        self.tableWidget.setRowCount(len(self.parsefile_kor()))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem('메세지번호'))
        self.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem('Text'))
        i = 0
        while i < len(self.parsefile_kor()):
            for k, v in self.parsefile_kor().items():
                self.tableWidget.setItem(i, 0, QTableWidgetItem(k))
                self.tableWidget.setItem(i, 1, QTableWidgetItem(v))
                i += 1
            # break
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()

    def search_dialog(self):
        self.lineEdit.setVisible(True)
        self.Btn_find.setVisible(True)

    def search_box(self):
        self.lineEdit.setVisible(False)
        self.lineEdit.clear()
        self.Btn_find.setVisible(False)

    def search(self, count = 0):
        text = self.lineEdit.text()
        while count < self.tableWidget.rowCount():
            currentitem = self.tableWidget.item(count, 1)
            eng_item = self.table_eng.item(count, 1)
            if text in currentitem.text():
                #currentitem.setBackgroundColor(0, QColor.setRgb(170, 0, 127))
                #if self.table_eng.isEnabled(True):
                    #eng_item = self.table_eng.item(count, 1)
                    #return self.table_eng.scrollToItem(eng_item)
                currentitem.setSelected(True)
                eng_item.setSelected(True)
                self.tableWidget.scrollToItem(currentitem, 3)
                self.table_eng.scrollToItem(eng_item, 3)
                return self.search(count+1)
            else:
                if count == self.tableWidget.rowCount() - 1:
                    return
                count += 1

    def remove(self):
        itemremoved = self.tableWidget.currentItem()
        itemrow = itemremoved.row()
        try:
            if itemremoved.isSelected():
                self.tableWidget.removeRow(self.tableWidget.row(itemremoved))
                self.table_eng.removeRow(itemrow)
        except :
            return



    def insert(self):
        if self.tableWidget.isEnabled() is False or self.table_eng.isEnabled() is False:
            return
        else:
            rownum = self.tableWidget.rowCount()
            rownum2 = self.table_eng.rowCount()
            self.tableWidget.insertRow(rownum)
            self.table_eng.insertRow(rownum2)
            self.tableWidget.scrollToBottom()
            self.table_eng.scrollToBottom()

    # 파일 저장하기
    # 변환된 text파일을 저장
    def savefile_kor(self):
        tree = ET.parse('message.xml')
        root = tree.getroot()
        kor_elem = root.find("kor")
        tag_label = kor_elem.find('label')
        kor_message_elem = kor_elem.find('message')
        kor_message_elem.clear()
        for i in range(self.tableWidget.rowCount()):
            tag = self.tableWidget.item(i, 0).text()
            text = self.tableWidget.item(i, 1).text()
            text = base64.b64encode(text.encode('utf-8'))
            text = text.decode('ascii')
            #text = "<![CDATA[%s]]>" % text
            element = ET.SubElement(kor_message_elem, tag)
            element.text = text
        apply_indent(kor_message_elem)
        apply_indent(tag_label)
        tree.write("message.xml", encoding='utf-8', xml_declaration=True)

    def savefile_eng(self):
        tree = ET.parse('message.xml')
        root = tree.getroot()
        eng_elem = root.find("eng")
        eng_message_elem = eng_elem.find('message')
        eng_message_elem.clear()
        for i in range(self.table_eng.rowCount()):
            tag = self.table_eng.item(i, 0).text()
            text = self.table_eng.item(i, 1).text()
            text = base64.b64encode(text.encode('utf-8'))
            text = text.decode('ascii')
            #text = "![CDATA[%s]]" % text
            element = ET.SubElement(eng_message_elem, tag)
            element.text = text
        apply_indent(eng_message_elem)
        tree.write("message.xml", encoding='utf-8', xml_declaration=True)




def apply_indent(elem, level=4):
    # tab = space * 2
    indent = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = indent + "    "
        if not elem.tail or not elem.tail.strip():
            elem.tail = indent
        for elem in elem:
            apply_indent(elem, level + 2)
        if not elem.tail or not elem.tail.strip():
            elem.tail = indent
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = indent

if __name__ == "__main__":

    app = QApplication([])
    ex = Converter()
    sys.exit(app.exec_())


