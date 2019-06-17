
# url1 = 'https://cn.indeed.com/jobs?q=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90&start={}'
# headers = {'user-agent' :'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'}
#
# title_info = pd.DataFrame()
#
# for i in range(10):
#     res = requests.get(url1.format(i*10), headers = headers)
#     content = etree.HTML(res.text)
#
#     titles = content.xpath('//*[@class="title"]')
#     summaries = content.xpath('//*[@class="summary"]')
#     company_names = content.xpath('//*[@class="sjcl"]/div[1]/span')
#     company_locs = content.xpath('//*[@class="sjcl"]/div[2]')  # 有一些loc在div[3] 的span，但是不全， div3里面的loc是全面的
#
#     for i in range(len(titles)):
#         title = titles[i].xpath('a/text()')[0].strip()
#         company_name = company_names[i].xpath('text()')[0].strip()
#         company_loc = company_locs[i].xpath('@data-rc-loc')[0].strip()  #直接选取属性值
#         temp = pd.DataFrame(
#             {
#                 'title': [title],
#                 'company_name': company_name,
#                 'company_loc': company_loc
#             }
#         )
#         title_info= pd.concat([title_info, temp])
#     time.sleep(1)
#

# get title information from web

from lxml import etree
import re
import pandas as pd
import requests
import time

import sqlalchemy as db
import getpass
import pymysql



def find_jobs(job_title, page_nums):
    USR = 'root'
    PWD = 'SQL960910'
    DB = 'indeed_jobs'
    engine = engine = db.create_engine('mysql+pymysql://'+USR+':'+PWD+'@localhost/'+DB)
    headers = {'user-agent' :'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'}

    for i in range(0, page_nums):
        ## after searching, the page that retrived was not the one with detailed info for each job,
        ## so we have to find the page_id for each and open the page with that job
        url1 = 'https://cn.indeed.com/jobs?q={}&start={}'
        # get jobs that has already been found, identify them with their unique id
        try:  ## if the table has not been created before, then start from scratch
            ids_db = pd.read_sql('select page_id from {}.indeed_jobs'.format(DB), engine)['page_id'].tolist()
        except:
            ids_db = []
        res1 = requests.get(url1.format(job_title,i*10), headers = headers)
        content1 = etree.HTML(res1.text)

        pages = content1.xpath('//*[@class="jobToJobRec_Hide"]/@id')

        for page in pages:
            #check if the job has been found before

            id = re.search('jobToJobRec_(\S+)_[so]j', page).group(1)
            if id in ids_db:
                pass
            else:
                # start search titles in a page
                url2 = 'https://cn.indeed.com/viewjob?jk={}&tk=1dd261drm7l68803&from=serp&vjs=3'
                res2 = requests.get(url2.format(id), headers = headers)
                content2 = etree.HTML(res2.text)

                # job title
                title = content2.xpath('/html/body/div[1]/div[2]/div[3]/div/div/div[1]/div[1]/div[1]/h3/text()')

                # company name
                def find_company():  #company names are not in the same place in HTML
                    company = content2.xpath('/html/body/div[1]/div[2]/div[3]/div/div/div[1]/div[1]/div[1]/div[1]/div/div[1]/a/text()')
                    if len(company) == 0:
                        company = content2.xpath('/html/body/div[1]/div[2]/div[3]/div/div/div[1]/div[1]/div[1]/div[1]/div/div[1]/text()')
                    return company
                company = find_company()
                # working location
                def find_location():  # locations are not in the same place in HTML
                    loc = content2.xpath('/html/body/div[1]/div[2]/div[3]/div/div/div[1]/div[1]/div[1]/div[1]/div/div[3]/text()')
                    if len(loc) == 0:  ## ====>> some locations are missing, still do not know how to fix it
                        loc = content2.xpath('/html/body/div[1]/div[2]/div[3]/div/div/div[1]/div[1]/div[1]/div[1]/div/div[4]/text()')
                    return loc
                loc = find_location()

                # job description
                destription = ' '.join(content2.xpath('//*[@id="jobDescriptionText"]//text()'))

                # save all the info into DataFrame
                info = pd.DataFrame({
                    'title':title,
                    'company':company,
                    'location':loc,
                    'description':destription,
                    'link': [url2.format(id)],
                    'page_id': id
                })

                # export infos to database
                info.to_sql(job_title, con = engine, if_exists = 'append', index = False)
                time.sleep(1)

# job_title =input('Please tell me what kind of job do you want:')
# page_nums = int(input('How many pages do you want me to search:'))

def main():
    '''h -> hour，m -> minute'''

    job_title =input('Please tell me what kind of job do you want:')
    page_nums = int(input('How many pages do you want me to search:'))
    h = hour
    m = minute
    while True:
        # check if it's time to start
        while True:
            now = datetime.datetime.now()
            # quit the inner loop if
            if now.hour==h and now.minute==m:
                break
            # wait for 20s and then check again
            time.sleep(20)
        # find the job I want
        find_jobs(job_title, page_nums)
if __name__ == '__main__':
    hour = input('Set the hour:')
    minute = input('Set the minute:')
    main()
