#!/usr/bin/python
# -*- coding: utf-8 -*-
import fnmatch
import os
import sys
import xml.etree.ElementTree as ET
import json


def genDoxygen(meta):
    print("========== Generating doxygen xml ============")
    content = open("_templates/doxygen.cfg").read()
    for k in meta:
        content = content.replace("${"+k+"}", meta[k])
    f = open("prebuild/doxygen.cfg", "w")
    f.write(content)
    f.close()
    os.system("doxygen prebuild/doxygen.cfg")


def globPath(path, pattern):
    result = []
    for root, subdirs, files in os.walk(path):
        for filename in files:
            if fnmatch.fnmatch(filename, pattern):
                result.append(os.path.join(root, filename))
    return result


def genClasses():
    print("========== Generating classes ============")
    classfiles = globPath("_build/doxygen/xml", "class*.xml")
    classfiles += globPath("_build/doxygen/xml", "struct*.xml")
    apirst = "API Reference\r\n=============\r\n\r\n"
    classtmp = open("_templates/class.rst").read()

    classes = []
    for f in classfiles:
        root = ET.parse(f).getroot()
        name = root.find("compounddef/compoundname").text
        classes.append((name, f.startswith("_build/doxygen/xml/struct")))

    classes.sort()
    for c in classes:
        name = c[0]
        typename = c[1] and "struct" or "class"
        print(name)
        print(c[1])
        classrst = classtmp.replace("${class}", name)
        classrst = classrst.replace("${type}", typename)
        filename = ("prebuild/api/{}.rst".format(name.replace("::", "_").lower()))
        classrstf = open(filename, "w")
        classrstf.write(classrst)
        classrstf.flush()
        line = ":cpp:class:`{}`".format(name)
        apirst += line+"\r\n"
        apirst += '-'*len(line)+"\r\n"

    apirstf = open("prebuild/api.rst", "w")
    apirstf.write(apirst)
    apirstf.flush()
    print("finished...")


def genSphinxCfg(meta):
    print("========== Generating conf.py ============")
    content = open("_templates/conf.py").read()
    for k in meta:
        content = content.replace("${"+k+"}", meta[k])
    f = open("conf.py", "w")
    f.write(content)
    f.close()
    print("finished...")


if __name__ == '__main__':
    if not os.path.isdir("prebuild/api"):
        os.makedirs("prebuild/api")
    meta = json.load(open("doc.json"))
    genDoxygen(meta)
    genClasses()
    genSphinxCfg(meta)
