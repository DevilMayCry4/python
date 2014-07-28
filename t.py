
# -*- coding: utf-8 -*-
import urllib2  
import urllib  
import re  
import thread  
import time 
import os
import hashlib
import cookielib  
import string  
import re


BBSURL = 'http://174.127.195.166/bbs/'
def  login():
	#设置一个cookie处理器，它负责从服务器下载cookie到本地，并且在发送请求时带上本地的cookie  
	cj = cookielib.LWPCookieJar()  
	cookie_support = urllib2.HTTPCookieProcessor(cj)  
	opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)  
	urllib2.install_opener(opener)  
	postdata = urllib.urlencode({
		'formhash'   :'9f5eb7fe',
		'loginfield' :'username',
		'username'   :'wusky777',
		'password'   :'19900317', 
		'cookietime' :'2592000',
		'referer'    :'index.php',
		'loginsubmit':'true',
		'questionid' :'0',
		})
	req = urllib2.Request(
		url = BBSURL + 'logging.php?action=login',
		data = postdata
		)
	print(BBSURL + 'logging.php?action=login')
	result = urllib2.urlopen(req)
	page = result.read()
	f = file('/Users/virgil/Documents/python/html/login.html','w')
	f.write(page)
	f.close()

def downloadImg(url,name):
	print('get img '+url)
	req = urllib2.Request(url)
	req.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/536.30.1 (KHTML, like Gecko) Version/6.0.5 Safari/536.30.1')
	req.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
	response = urllib2.urlopen(req)
	the_page = response.read()  

	f = file('/Users/virgil/Documents/python/html/'+name+'.jpg','w')
	f.write(the_page)
	f.close()

def getTorrent(url):
	req = urllib2.Request(url)  
	response = urllib2.urlopen(req)  
	the_page = response.read()
	md5Url = hashlib.md5(url).hexdigest().upper()
	file_object = open('/Users/virgil/Documents/python/url.txt', 'a')
	file_object.write(md5Url+':'+url+'\n')
	file_object.close( )

	f = file('/Users/virgil/Documents/python/html/'+md5Url+'.html','w')
	f.write(the_page)
	f.close()

	unicodePage = the_page.decode("gbk") 
	preString = '<br />\r\n<img src="'
	LastString = '" border' 
	myItems = re.findall(preString+'.*?" border',unicodePage,re.S)
	print(myItems)
	for item in myItems:
		if (item.find('.jpg') != -1):  
		    print(item)      
		    tmp = item.replace(preString,'')
		    newItem = tmp.replace(LastString,'')
		    downloadImg(urllib.quote(newItem, ":/"),md5Url+"%u"%a)

	print('finish '+url)
 

def  getHtml(url):	
	req = urllib2.Request(url)  
	response = urllib2.urlopen(req)  
	the_page = response.read()
	unicodePage = the_page.decode("gbk") 
	preString = '<td class="folder"><a href="'
	myItems = re.findall(preString+'.*?.html',unicodePage,re.S)               
	for item in myItems:        
	    newItem = item.replace(preString,BBSURL)
	    print('start get'+newItem)
	    getTorrent(newItem)
	    

if __name__ == '__main__':
	downloadImg('http://img169.com/images/2014/07/24/HODV 20994.jpg','test')
	login()
	for a in xrange(2,1000):
		url = 'forum-58-'+"%u"%a+'.html'
		print('get url:'+BBSURL+url)
		getHtml(BBSURL+url)
    
	 




