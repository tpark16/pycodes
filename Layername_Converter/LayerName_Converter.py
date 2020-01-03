"""
This code executes exe file that easily edits LayerName.xml.

tpark16
"""

import base64
import xml.etree.ElementTree as ET

from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys, os, collections

_ui_path = 'LayerNameUI.ui'
FORM_CLASS, _ = uic.loadUiType(_ui_path)

class LayerName_Converter(QMainWindow, FORM_CLASS):
    def __init__(self):
        super().__init__()
        self.layerlist = collections.OrderedDict()
        self.tree = ET.parse('LayerName.xml')
        self.root = self.tree.getroot()
        self.setupUi(self)
        self.setUi()
        self.setSlot()
        self.show()

    def parsefile(self):
        for _elem in list(self.root):
            tag = _elem.tag.strip()
            value = _elem.text.strip()
            decoded = base64.b64decode(value).decode('utf-8')
            self.layerlist[tag] = decoded
        return self.layerlist

    def setUi(self):
        self.tableWidget.setEnabled(False)
        self.Btn_find.setVisible(False)
        self.lineEdit.setVisible(False)

    # 버튼 액션
    def setSlot(self):
        self.Btn_layername.clicked.connect(self.getLayerName)
        #self.Btn_loading.clicked.connect(self.parsefile_kor)
        self.Btn_save.clicked.connect(self.savefile)
        self.Btn_search.clicked.connect(self.search_dialog)
        self.Btn_insert.clicked.connect(self.insert)
        self.Btn_find.clicked.connect(self.search)
        self.Btn_remove.clicked.connect(self.remove)

    def getLayerName(self):
        self.tableWidget.setEnabled(True)
        self.tableWidget.setRowCount(len(self.parsefile()))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem('메세지번호'))
        self.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem('Text'))
        i = 0
        while i < len(self.parsefile()):
            for k, v in self.parsefile().items():
                self.tableWidget.setItem(i, 0, QTableWidgetItem(k))
                self.tableWidget.setItem(i, 1, QTableWidgetItem(v))
                i += 1
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
            if text in currentitem.text():
                currentitem.setSelected(True)
                self.tableWidget.scrollToItem(currentitem, 3)
                return self.search(count+1)
            else:
                if count == self.tableWidget.rowCount() - 1:
                    return
                count += 1



    def remove(self):
        itemrow = self.tableWidget.currentRow()
        itemcolumn = self.tableWidget.currentColumn()
        itemremoved = self.tableWidget.item(itemrow, itemcolumn)
        try:
            if itemremoved is None:
                self.tableWidget.removeRow(itemrow)
            if itemremoved.isSelected():
                self.tableWidget.removeRow(itemrow)
        except:
            return

    def insert(self):
        if self.tableWidget.isEnabled() is False:
            return
        else:
            rownum = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rownum)
            self.tableWidget.scrollToBottom()

    # save converted text file
    def savefile(self):
        self.root.clear()
        for i in range(self.tableWidget.rowCount()):
            tag = self.tableWidget.item(i, 0).text()
            text = self.tableWidget.item(i, 1).text()
            text = base64.b64encode(text.encode('utf-8'))
            text = text.decode('ascii')
            element = ET.SubElement(self.root, tag)
            element.text = text
        apply_indent(self.root)
        self.tree.write("LayerName.xml", encoding='utf-8', xml_declaration=True)

def apply_indent(elem, level=0):
    # tab = space * 2
    indent = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = indent + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = indent
        for elem in elem:
            apply_indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = indent
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = indent

if __name__ == "__main__":

    app = QApplication([])
    ex = LayerName_Converter()
    sys.exit(app.exec_())


