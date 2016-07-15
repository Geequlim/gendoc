#!/usr/bin/python
# -*- coding: utf-8 -*-
import fnmatch
import os
import sys
import xml.etree.ElementTree as ET
import json


def genDoxygen(meta):
    print("========== Generating doxygen xml ============")
    if not os.path.isdir("prebuild"):
        os.makedirs("prebuild")
    content = open("_templates/doxygen.cfg").read()
    for k in meta:
        if isinstance(meta[k], unicode) or isinstance(meta[k], str):
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
    apirst = ""
    classfiles = globPath("_build/doxygen/xml", "class*.xml")
    classfiles += globPath("_build/doxygen/xml", "struct*.xml")
    classtmp = open("_templates/class.rst").read()
    apirst += "Classes\r\n"
    apirst += "-------\r\n"
    classes = []
    for f in classfiles:
        try:
            root = ET.parse(f).getroot()
            name = root.find("compounddef/compoundname").text
            if "<" in name:
                continue
            if "ignore" in meta and "classes" in meta["ignore"]:
                if name in meta["ignore"]["classes"]:
                    continue
            classes.append((name, f.startswith("_build/doxygen/xml/struct")))
        except Exception as e:
            print(e)
    classes.sort()
    for c in classes:
        name = c[0]
        print(name)
        typename = c[1] and "struct" or "class"
        if not os.path.isdir("prebuild/api/classes"):
            os.makedirs("prebuild/api/classes")
        classrst = classtmp.replace("${class}", name)
        classrst = classrst.replace("${type}", typename)
        filename = ("prebuild/api/classes/{}.rst".format(name.replace("::", "_").lower()))
        classrstf = open(filename, "w")
        classrstf.write(classrst)
        classrstf.close()
        line = ":cpp:class:`{}`".format(name)
        apirst += line+"\r\n"
        apirst += '~'*len(line)+"\r\n"
    print("finished...")
    return apirst


def genSymbols():
    print("========== Generating other symbols ============")
    apirst = ""
    root = ET.parse("_build/doxygen/xml/index.xml").getroot()
    symbols = {
        "define": [],
        "enum": [],
        "enumvalue": [],
        "function": [],
        "property": [],
        "typedef": [],
        "variable": [],
    }
    for compound in root:
        if compound.get("kind") in ["file", "namespace"]:
            for m in compound:
                if m.tag == "member":
                    kind = m.get("kind")
                    name = m.find("name").text
                    symbols[kind].append(name)
    for k in symbols:
        if len(symbols[k]) == 0:
            continue
        print("{}s:".format(k))
        symbols[k].sort()
        apirst += "{}\r\n".format(k.capitalize())
        apirst += "-" * len(k) + "\r\n"
        # if not os.path.isdir("prebuild/api/{}".format(k)):
        #     os.makedirs("prebuild/api/{}".format(k))
        for s in symbols[k]:
            print("    {}".format(s))
            apirst += ".. doxygen{}:: {}\r\n".format(k, s)
        apirst += "\r\n"
    print("finished...")
    return apirst


def genSphinxCfg(meta):
    print("========== Generating conf.py ============")
    content = open("_templates/conf.py").read()
    for k in meta:
        if isinstance(meta[k], unicode) or isinstance(meta[k], str):
            content = content.replace("${"+k+"}", meta[k])
    f = open("conf.py", "w")
    f.write(content)
    f.close()
    print("finished...")


if __name__ == '__main__':
    meta = json.load(open("doc.json"))
    genDoxygen(meta)
    apirst = "API Reference\r\n=============\r\n\r\n"
    apirst += genClasses()
    apirst += genSymbols()
    apirstf = open("prebuild/api.rst", "w")
    apirstf.write(apirst)
    apirstf.close()
    genSphinxCfg(meta)
