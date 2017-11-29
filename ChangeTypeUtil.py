#coding=utf-8
#上面一句是定义python的编码，必须写在第一句

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os
from xml.dom.minidom import parse
import xml.dom.minidom
from mylib.biplist import *


PLIST_PATH = "res\changetype\game_res"  # plist路径
CSB_PATH = "res\changetype\game_csb"     # csb路径
OUT_PATH = "res\changetype\out_csb"      # 输入csb路径
# 过滤路径
FILT_PATH = {
    "hall_bg_1.jpg",
    "hall_bg_2.jpg",
    "login_denglujiemian.png"
}


# 获取png文件名
def getPngName(_pngPath):
    pngName = _pngPath
    lastIndex = _pngPath.rfind("/")
    if lastIndex != -1 :
        pngName = pngName[lastIndex + 1 :]
    return pngName

# 获取csb文件名
def getCsbName(_csbPath):
    csbName = _csbPath
    lastIndex = _csbPath.rfind("\\")
    if lastIndex != -1:
        csbName = _csbPath[lastIndex + 1: ]
    return csbName

# 图片名是否在plist里面
def isInPlist(_plistPath, _png):
    plist = readPlist(_plistPath)
    frames = plist.get('frames')
    pngList = frames.keys()
    for png in pngList:
        if png == _png:
            return True
    return False

# 图片是否过滤
def isFilt(_png):
    for filt in FILT_PATH:
        if filt == _png:
            return True
    return False

# 检测plist
def getPlistName(_plistPath, _png):
    # print "checkPList"
    files = os.listdir(_plistPath)
    for fi in files:
        fi_d = os.path.join(_plistPath, fi)
        if os.path.isdir(fi_d):
            getPlistName(fi_d, _png)
        else:
            if fi_d.find(".plist") != -1 and isInPlist(fi_d, _png):
                return fi;
    return ""

# 替换文本
def alter(file,old_str,new_str):
    """
    将替换的字符串写到一个新的文件中，然后将原文件删除，新文件改为原来文件的名字
    :param file: 文件路径
    :param old_str: 需要替换的字符串
    :param new_str: 替换的字符串
    :return: None
    """
    with open(file, "r") as f1,open("%s.bak" % file, "w") as f2:
        for line in f1:
            if old_str in line:
                line = line.replace(old_str, new_str)
            f2.write(line)
    os.remove(file)
    os.rename("%s.bak" % file, file)

# 修改数据
def changeData(_gameProjectFile, _dataName):
    fileDataList = _gameProjectFile.getElementsByTagName(_dataName)
    for fileData in fileDataList:
        pngPath = fileData.getAttribute("Path")
        pngName = getPngName(pngPath)
        plistName = getPlistName(PLIST_PATH, pngName)
        if plistName != "" and not isFilt(pngName):
            fileData.setAttribute("Path", pngName)
            fileData.setAttribute("Type", "PlistSubImage")
            fileData.setAttribute("Plist", "game_res/%s"%(plistName))
        elif isFilt(pngName):
            fileData.setAttribute("Path", "game_res/bg/%s"%(pngName))

# 修改文件
def changeCsb(_csbPath):
    print ("changeCsb: %s"%(_csbPath))
    DOMTree = xml.dom.minidom.parse(_csbPath)
    gameProjectFile = DOMTree.documentElement
    changeData(gameProjectFile, "FileData")
    changeData(gameProjectFile, "ImageFileData")
    changeData(gameProjectFile, "NormalFileData")
    changeData(gameProjectFile, "DisabledFileData")
    changeData(gameProjectFile, "PressedFileData")

    csbName = getCsbName(_csbPath)
    # outPath = os.path.join(OUT_PATH, csbName)
    outPath = _csbPath.replace('game_csb','out_csb')
    outDir = outPath.replace(csbName, "")
    print("outPath: %s" % (outPath))
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    f = file(outPath, "w")
    DOMTree.writexml(f)
    f.close()

    alter(outPath, '<?xml version="1.0" ?>', "")


# 遍历filepath下所有文件，包括子目录
def changeAllCsb(_path):
    files = os.listdir(_path)
    for fi in files:
        fi_d = os.path.join(_path, fi)
        # 如果是文件夹，继续遍历
        if os.path.isdir(fi_d):
            changeAllCsb(fi_d)
        # 如果是文件，修改文件
        else:
            changeCsb(fi_d)

def test():
    return

# 主函数
if __name__ == "__main__":
    # print getCsbName("res/changetype/game_csb/activity/activity_node.csd")
    changeAllCsb(CSB_PATH)
    print "ok"
