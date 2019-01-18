#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import requests

movieList = []

def getTargetContent(_str, _start, _end):
	sIndex = _str.find(_start)
	eIndex = _str.find(_end, sIndex)
	return _str[sIndex:eIndex]

def analyseMovie(_str):
	mLen = 10
	sIndex = 0
	eIndex = 0
	sStr = '<span class="title">'
	eStr = '</span>'
	tsStr = '<br>'
	esStr = '&nbsp'
	for num in range(25):
		movie = {'name':'', 'time':''}
		sIndex = _str.find(sStr, eIndex)
		eIndex = _str.find(eStr, sIndex)
		movie['name'] = _str[sIndex+len(sStr):eIndex].replace(' ', '')
		sIndex = _str.find(tsStr, eIndex)
		eIndex = _str.find(esStr, sIndex)
		movie['time'] = _str[sIndex+len(tsStr):eIndex].replace(' ', '')
		movieList.append(movie)

# 获取列表时间排序
def takeSecond(elem):
	return elem['time']

for i in range(10):
	resp = requests.get('https://movie.douban.com/top250?start=' + str(25*i) + '&filter=') 
	tContent = getTargetContent(resp.content, '<ol class="grid_view">', '</ol>')
	#print tContent
	analyseMovie(tContent)

print len(movieList)
# 指定第二个元素排序
movieList.sort(key=takeSecond, reverse=True)
testNum = 1
for movie in movieList :
	print testNum
	print movie['name'] + ',' + movie['time']
	print ''
	testNum += 1




