# -*- coding: utf-8 -*-
"""
This is a simple code that converts scheme.txt into 3 different XMLs; code_field, field_name, and layer_name.
It reads and parse the text, then save each item to appropriate XML type.
Written by Taeyun Park
"""
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import parse


layer_dict = dict()
field_dict = dict()
code_dict = dict()
field_code = dict()
layer_tree = parse('layer_name.xml')
field_tree = parse('field_name.xml')
code_tree = parse('code_field.xml')
layer_root = layer_tree.getroot()
field_root = field_tree.getroot()
code_root = code_tree.getroot()
zero = dict()
one = dict()
thr = dict()

def apply_indent(elem, level=0):

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


def parsing():
    for elem in list(layer_root):
        layerName = elem.tag.strip()
        disp_name = elem.text.strip()
        layer_dict[layerName] = disp_name
    for elem in list(field_root):
        fieldName = elem.tag.strip()
        disp_name = elem.text.strip()
        field_dict[fieldName] = disp_name
    for elem in list(code_root):
        for key in list(elem):
            value = key.attrib['value']
            desc = key.attrib['desc']
            code_dict[value] = desc
            field_code[value] = elem.tag.strip()

def readfile():
    f = open('scheme.txt', 'r', encoding='UTF8')
    while True:
        line = f.readline()
        if not line:
            break

        lp = line.split("\t")

        if len(lp) == 4:
            zero[lp[0]] = lp[1]
            one[lp[2]] = lp[3]
        else:
            # No code_field
            if lp[4] == "":
                zero[lp[0]] = lp[1]
                one[lp[2]] = lp[3]
            else:
                zero[lp[0]] = lp[1]
                one[lp[2]] = lp[3]
                thr[lp[5].rstrip('\n')] = lp[5].rstrip('\n') + "(" +lp[4] + ")"
                field_code[lp[-1].rstrip('\n')] = lp[2]
    f.close()

def update():
    layer_dict.update(zero.items())
    field_dict.update(one.items())
    code_dict.update(thr.items())

def execode():
    x = input("Do you want to update the XML files? (Y/N)")
    if x == 'Y':

        #Layer_name
        layer_root.clear()
        for k, v in layer_dict.items():
            element = ET.SubElement(layer_root, k)
            element.text = v
        apply_indent(layer_root)
        layer_tree.write('layer_name.xml', encoding='utf-8', xml_declaration=True)

        #Field_name
        field_root.clear()
        for k, v in field_dict.items():
            element = ET.SubElement(field_root, k)
            element.text = v
            if '일시' in v:
                element.set('type', 'date')
        apply_indent(field_root)
        field_tree.write('field_name.xml', encoding='utf-8', xml_declaration=True)

        #Code_field
        code_root.clear()
        for k, v in field_code.items():
            elem_find = code_root.find(v)
            if elem_find is None:
                element = ET.SubElement(code_root, v)
            else:
                pass
            for k2, v2 in code_dict.items():
                if elem_find is None:
                    if k2 == k:
                        second_element = ET.SubElement(element, 'code')
                        second_element.set('value', k2)
                        second_element.set('desc', v2)
                else:
                    if k2 == k:
                        second_element = ET.SubElement(elem_find, 'code')
                        second_element.set('value', k2)
                        second_element.set('desc', v2)
        apply_indent(code_root, level=2)
        code_tree.write('code_field.xml', encoding='utf-8', xml_declaration=True)

        print("저장 완료")

    elif x == "N":
        # if N, close the program.
        print("종료")

    else:
        # ask again
        execode()


if __name__ == '__main__':
    parsing()
    readfile()
    update()
    execode()




