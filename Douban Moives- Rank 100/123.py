import requests
from lxml import etree
import time
header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

'''
film=selector.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[1]/a/span[1]/text()')
pingfen=selector.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/div/span[2]/text()')
print(pingfen)
'''
res=requests.get(url,headers=header)
selector=etree.HTML(res.text)
selector
film=selector.xpath('//*[@id="content"]/div/div[1]/ol/li')
film
title=sector.xpath('div/div[2]/div[1]/a/span[1]/text()')[0]
pingfen=div.xpath('div/div[2]/div[2]/div/span[2]/text()')[0]
jianjie=div.xpath('div/div[2]/div[2]/p[2]/span/text()')[0]
daoyan=div.xpath('div/div[2]/div[2]/p[1]/text()')[0].strip()


total=[]
def getdetails(url):
    try:
        res=requests.get(url,headers=headers)
        selector=etree.HTML(res.text)
        film=selector.xpath('//*[@id="content"]/div/div[1]/ol/li')
        #每部电影包含所有内容的总标签，可以相连并排在一起的
        #单个内容去除循环的部分，开头不要带斜杠
        for div in film:
            title=div.xpath('div/div[2]/div[1]/a/span[1]/text()')[0]
            pingfen=div.xpath('div/div[2]/div[2]/div/span[2]/text()')[0]
            jianjie=div.xpath('div/div[2]/div[2]/p[2]/span/text()')[0]
            daoyan=div.xpath('div/div[2]/div[2]/p[1]/text()')[0].strip()
            total.append({'title':title,
                          'pingfen':pingfen,
                          'jianjie':jianjie,
                          'daoyan':daoyan})
    except:
        print('抓取失败')
    return total

if __name__=='__main__':
    for i in range(10):
        url='https://movie.douban.com/top250?start={}*25&filter='.format(i)
        getdetails(url)
        print('第{}页抓取完毕'.format(i))
        time.sleep(1)
'''
for info in total:
    try:
        f=open('film.txt','w+')
        f.write(info['title']+'\n')
        f.write(info['pingfen']+'\n')
        f.write(info['jianjie']+'\n')
        f.write(info['daoyan']+'\n')
        f.close()
    except UnicodeEncodeError:
        pass
'''
import pandas as pd
ff=pd.DataFrame(total)
ff.to_excel('film.xls')
