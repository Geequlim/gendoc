#!/usr/bin/python
# -*- coding: utf-8 -*-
import fnmatch
import os
import json
from breathe import parser

doxyxmldir = "_build{0}doxygen{0}xml".format(os.sep)



def globPath(path, pattern):
    result = []
    for root, subdirs, files in os.walk(path):
        for filename in files:
            if fnmatch.fnmatch(filename, pattern):
                result.append(os.path.join(root, filename))
    return result


def runDoxygen(meta):
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


def parseDoxygen():
    print("========== Parsing symbols ============")
    index = None
    compounds = []
    for xml in globPath(doxyxmldir, "*.xml"):
        print("parsing {}".format(xml))
        if xml.endswith("index.xml"):
            global index
            index = parser.index.parse(xml)
        else:
            compounds.append(parser.compound.parse(xml))

    symbols = {}
    for c in compounds:
        for section in c.compounddef.sectiondef:
            kind = section.kind
            members = []
            for member in section.memberdef:
                members.append(member)
            if kind not in symbols:
                symbols[kind] = members
            else:
                symbols[kind] += members
    print("finished...")
    return index, symbols


def genClasses(index, symbols, meta):
    print("========== Generating classes ============")

    apirst = ""
    classtmp = open("_templates/class.rst").read()

    apirst += "Classes\r\n"
    apirst += "-------\r\n"
    classes = []
    for c in index.compound:
        if c.kind in ["class", "struct"]:
            classes.append((c.name, c.kind))
    classes.sort()


    for c in classes:
        name = c[0]
        type = c[1]
        if name in meta["ignore"]["classes"] or "<" in name:
            continue
        print(name)
        if not os.path.isdir("prebuild/api/classes"):
            os.makedirs("prebuild/api/classes")
        classrst = classtmp.replace("${class}", name)
        classrst = classrst.replace("${type}", type)
        filename = "prebuild/api/classes/{}.rst".format(name.replace("::", "_"))
        classrstf = open(filename, "w")
        classrstf.write(classrst)
        classrstf.close()
        line = ":cpp:class:`{}`".format(name)
        apirst += line+"\r\n"
        apirst += '~'*len(line)+"\r\n"
    print("finished...")
    return apirst


def genSymbols(index, doxySymbols, meta):
    print("========== Generating other symbols ============")
    apirst = ""
    resovedCompounds = ["namespace", "group", "dir", "file", "module"]
    resovedMembers = ["define", "enum", "function", "typedef", "variable", "union"]
    aliasMap = {
        "function": "func",
        "variable": "var",
        "enumvalue": "enum",
    }
    symbols = {}
    for c in index.compound:
        kind = c.kind
        if kind in resovedCompounds:
            for m in c.member:
                k = m.kind
                if not symbols.has_key(k):
                    symbols[k] = []
                ak = k
                if k in aliasMap:
                    ak = aliasMap[k]
                rawmember = None
                for rm in doxySymbols[ak]:
                    if rm.id == m.refid:
                        rawmember = rm
                        break
                symbols[k].append((m.name, m, rawmember))

    for k in symbols:
        if meta["with_symbols"].has_key(k) and not meta["with_symbols"][k]:
            continue
        if len(symbols[k]) == 0:
            continue
        symbols[k].sort()
        apirst += "{}\r\n".format(k.capitalize())
        apirst += "-" * len(k) + "\r\n"
        for pair in symbols[k]:
            name = pair[0]
            m = pair[1]
            rawm = pair[2]
            if k == "function" and rawm is not None:
                name = rawm.definition.split(" ")[-1]
                name += rawm.argsstring
            if name in meta["ignore"]["symbols"]:
                continue
            apirst += ".. doxygen{}:: {}\r\n".format(k, name)
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
    runDoxygen(meta)
    index, symbols = parseDoxygen()

    apirst = "API Reference\r\n=============\r\n\r\n"
    apirst += genClasses(index, symbols, meta)
    apirst += genSymbols(index, symbols, meta)
    apirstf = open("prebuild/api.rst", "w")
    apirstf.write(apirst)
    apirstf.close()
    genSphinxCfg(meta)
