#coding=utf-8
import sys
import os
reload(sys)
sys.setdefaultencoding('gbk')
import requests
from lxml import etree
# from urllib.request import urlretrieve

#漫画首页
comicIndex = "http://comic2.kukudm.com/comiclist/2035/index.htm"
downloadPath = "d:/comic/"

#截取内容方法
def getTargetContent(_str, _start, _end, _isInclude):
	sIndex = _str.find(_start)
	eIndex = _str.find(_end, sIndex)
	if _isInclude:
		endLen = len(_end)
		return _str[sIndex:eIndex+endLen]
	else:
		startLen = len(_start)
		return _str[sIndex+startLen:eIndex]
	return 

#下载一话
def downloadPage(_url, _downPath):
	resp = requests.get(_url) 
	#总页数
	totalPage = int(getTargetContent(resp.content, '共', '页', False).strip())
	# html = etree.HTML(resp.content)
	for i in range(totalPage):
		page = i + 1
		lastIndex = _url.rfind('/')
		downURL = _url[0:lastIndex+1] + str(page) + '.htm'
		print downURL
		resp = requests.get(downURL) 
		html = etree.HTML(resp.content)
		print resp.content
		print imgPath
		

#主方法
if __name__ == '__main__':
	resp = requests.get(comicIndex) 
	# htmlstr = getTargetContent(resp.content, "<html", "html/>")
	html = etree.HTML(resp.content)
	fileNames = html.xpath('//dl[@id="comiclistn"]/dd/a[position()=1]/text()')
	downPages = html.xpath('//dl[@id="comiclistn"]/dd/a[position()=3]/@href')
	for i, text in enumerate(fileNames):
		if i == 1:
			break
		fileName = text.encode('gbk')
		filePath = (downloadPath + '{:0>3d} ' + fileName).format(i+1)
		if not os.path.exists(filePath):
			os.makedirs(filePath)
		downloadPage(downPages[i], filePath)

