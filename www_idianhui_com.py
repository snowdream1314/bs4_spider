#-*-coding:utf-8-*-
#-------------------------------------
# Name:     www_idianhui_com.py
# Purpose: 
# Author:   xuxiaoqing
# Date:     2015.7.29
# Note:     need to import BeautifulSoup
#-------------------------------------

import urllib, urllib2, re, json, codecs
from bs4 import BeautifulSoup 

class Article_Spider:
    
    def __init__(self):

        pass

        
    def Get_Article_Page(self):
        url = 'http://www.idianhui.com/article/list.html?code=zxdt'
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        mypage = response.read()
        unicodepage = mypage.decode("utf-8")
        
        publishtimes = re.findall('<ul class="list_li_1">(.*?)</ul>',unicodepage,re.S)
        publishtime = re.findall('<li>(.*?)<a.*?>.*?</a></li>',publishtimes[0],re.S)
        
        # print publishtime，调试用
        
        myitems = re.findall('<ul class="list_li_1">(.*?)</ul>',unicodepage,re.S)
        myitem = re.findall('<li>(.*?)<a href="(.*?)".*?>(.*?)</a></li>', myitems[0],re.S)
        
        #print "begin 0"
        return myitem    
        
        
    def Get_Article(self):
        pageitem = self.Get_Article_Page()
        a = []
        for item in pageitem:
            pagetime = item[0].encode('utf-8')
            pagetitle = item[2]
            pageurl = item[1]
            
            # print pagetime
            url = 'http://www.idianhui.com/article/'+ pageurl
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            mypage = response.read()
            unicodepage = mypage.decode("utf-8")
            
            soup = BeautifulSoup(mypage)
        
            title = soup.find('div',class_='content_h3').get_text()#文章标题
            
            detaildiv = soup.find('div', class_='content_ro2')#文章内容
            detail = detaildiv.find('table').get_text().replace("\n","").replace("\r","").replace("\t","").replace(" ","")
            
            article = {}
            article['btitle'] = title
            article['detail'] = detail
            article['url'] = url 
            article['apublishtime'] = pagetime
            
            #print "begin:"调试用，其它同            
            a.append(article)
                
        #把article中的内容以json格式写入文件
        filename = 'article.txt'
        with codecs.open(filename, 'w+', 'utf-8') as f:
            f.write(json.dumps(a,indent=4,sort_keys=True,ensure_ascii=False))
            f.close()

    
            
    def start (self):
    
        print u"开始爬取文章"
        self.Get_Article()
        print u"爬取结束"
        

class Invest_Spider:
    
    def __init__(self):
        
        #起始url
        self.starturls = ['http://www.idianhui.com/invest/index.html?status=1',
                        'http://www.idianhui.com/invest/index.html?status=10',
                        'http://www.idianhui.com/invest/index.html?status=8']
        
    
    #获取每一起始页中的url
    def Get_Invest_Page(self):
        items = []
        for url in self.starturls:            
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            mypage = response.read()
            unicodepage = mypage.decode("utf-8")
            myitems = re.findall('<h4>.*?<a href="(.*?)">.*?</a>.*?</h4>',unicodepage,re.S)
            
            for item in myitems:
                items.append(item)
            
            #print "begin 0"调试用
        return items
        
        
    def Get_Invest(self):
        pageitem = self.Get_Invest_Page()
        
        b = []
        for item in pageitem:
            #print "begin item"调试用，其它同
            url = 'http://www.idianhui.com'+ item
            req = urllib2.Request(url)            
            response = urllib2.urlopen(req)
            mypage = response.read()
            unicodepage = mypage.decode("utf-8")

            #print "begin:"
            req = urllib2.Request(url)
            
            response = urllib2.urlopen(req)
            mypage = response.read()
            unicodepage = mypage.decode("utf-8")
            soup = BeautifulSoup(mypage)

            invest = {}
            title = soup.find('h1').get_text()#标名称
            
            tenderId = soup.find('span', class_='float_left pl10').get_text()#标编号
            
            capitalli = soup.find('li', class_='account')
            capital = capitalli.find('p').get_text()#标金额
            
            profitli = soup.find('li', class_='apr')
            profit = profitli.find('p').get_text()#年利率
            
            timeli = soup.find('li', class_='time')
            time = timeli.find('p').get_text()#借款期限
            
            repaymodeul = soup.find('ul', class_='clearfix')
            repaymodeli = repaymodeul.get_text()
            
            repaymode = re.search(u"还款方式.*",repaymodeli).group()#还款方式
            statenow = re.search(u"当前状态.*",repaymodeli).group().replace("\n","").replace("\r","").replace("\t","").replace(" ","")#当前状态
            
            starttime = re.search(u"开始时间.*",repaymodeli)#开始时间
            if starttime:
                starttime = starttime.group()
                invest['estarttime'] = starttime
                
            stoptime = re.search(u"结束时间.*",repaymodeli)#结束时间
            if stoptime:
                stoptime = stoptime.group()
                invest['fstoptime'] = stoptime
                
            reviewtime = re.search(u"复审时间.*",repaymodeli)#复审时间
            if reviewtime:
                reviewtime = reviewtime.group()
                invest['greviewtime'] = reviewtime   
            
            detaildiv = soup.find('div', class_='tab-content')#产品详情
            productdetaildiv = detaildiv.find('div',class_='list-tab-con')
            productdetail = productdetaildiv.find('div').get_text().replace("\n","").replace("\r","").replace("\t","").replace(" ","")
            
            riskcontroldiv  = soup.find('div',class_='list-tab-con',style='display:none;')#风险控制
            riskcontrol  = riskcontroldiv.find('p').get_text().replace("\n","").replace("\r","").replace("\t","").replace(" ","")
            
            invest['atitle'] =title
            invest['btenderId'] = tenderId
            invest['capital'] = capital
            invest['dprofit'] = profit
            invest['htime'] =time
            invest['irepaymode'] = repaymode
            invest['kstatenow'] = statenow
            invest['lproductdetail'] = productdetail
            invest['jriskcontrol'] = riskcontrol
            invest['url'] = url
            
            b.append(invest)
        
        #把文章以json格式写入文件
        filename ='invest.txt'
        with codecs.open(filename, 'w+', 'utf-8') as f:
            f.write(json.dumps(b,indent=4,sort_keys=True,ensure_ascii=False))
            f.close()

        
    def start (self):    
        print u"开始爬取投资文章"
        self.Get_Invest()
        print u"投资文章爬取结束"
        
        
articlespider = Article_Spider()
investspider = Invest_Spider()
articlespider.start()
investspider.start()