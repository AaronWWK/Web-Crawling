import requests
import pandas as pd
import re
import time
from lxml import etree

result = pd.DataFrame()
for i in range(0,250,25):
    header = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    url = 'https://book.douban.com/top250?start={}'
    html = requests.get(url.format(i), headers = header)  #（requests.get(web, headers, cookeis)

    # print(html.text[:200])

    bs = etree.HTML(html.text)
    bs.xpath('//tr[@class= "item"]/td[2]/p')[0].text
    bs.xpath('//tr[@class= "item"]')

    for item in bs.xpath('//tr[@class="item"]'):
        #the book name
        book_ch_name = item.xpath('td[2]/div[1]/a[1]/@title')[0]
        #rating
        score = item.xpath('td[2]/div[2]/span[2]')[0].text
        #book info
        book_info = item.xpath('td[2]/p[@class="pl"]')[0].text
        #rating amount is not standard, so we have to make it a standard format
        comment_num = re.findall('(\d+\S+)',item.xpath('td[2]/div[2]/span[3]')[0].text)[0]
        #brief summary of the book_info
        #some books do not have brief
        try:
            brief = item.xpath('td[2]/p[@class="quote"]/span')[0].text
        except:
            brief = None
        #cache save the result for every i
        cache = pd.DataFrame({'Chinese Name':[book_ch_name],
                              'Book Info':[book_info],
                              'Rating Amount': [comment_num],
                              'Rating': [score],
                              'Brief':[brief]})
        result = pd.concat([result, cache])

        time.sleep(5)

result.head()

result.to_csv('Douban.csv')
