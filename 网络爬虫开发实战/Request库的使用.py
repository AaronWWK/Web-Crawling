import requests

r = requests.get('http://httpbin.org/get')
print(r.text)
print(type(r))
print(type(r.text))

data = {
    'name':'germey',
    'age':22
}
r = requests.get('http://httpbin.org/get', params=data)
r_dict = r.json()
type(r_dict)

for key, value in r_dict.items():
    print(str(key) +'===' + str(value))

## 抓取网页
import requests
import re

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
r = requests.get('https://www.zhihu.com/explore', headers = headers)
pattern = re.compile('explore-feed.*?question_link.*?>(.*?)</a>', re.S)
titles = re.findall(pattern, r.text)
titles

## 抓取二进制数据
import requests
r = requests.get('https://github.com/favicon.ico')
print(r.text)
print(r.content)
with open('favicon.ico', 'wb') as f:
    f.write(r.content)

## POST 请求
data = { 'name':'germey','age':22}
r = requests.post('http://httpbin.org/post', data = data)
print(r.text)


## 响应

r = requests.get('http://www.jianshu.com', headers = headers)
exit() if not r.status_code == requests.codes.ok else print('Request Successfully')

print(type(r.status_code), r.status_code)
print(type(r.headers))
print(r.headers)
print(type(r.cookies),r.cookies)

print(requests.codes.all_ok)
print(requests.codes.all_good)


## cookies
r = requests.get('https://www.baidu.com', headers = headers)
cookies = r.cookies
print(cookies.items()[0])
for key, value in cookies.items():
    print(key + '=' + value)
for item in cookies.items():
    print(item)


### SSL 证书验证

r = requests.get('https://www.12306.cn', verify = False)
r.status_code

from requests.packages import urllib3
urllib3.disable_warnings()  #关闭warning， 就没有上面的提示没有验证证书
r = requests.get('https://www.12306.cn', verify = False)
r.status_code


##  Timeout
r = requests.get('https://www.google.co.uk', timeout = None)
