
from lxml import etree
import re
import pandas as pd
import requests
import time

import sqlalchemy as db
import getpass
import pymysql
import datetime

from mail import send_email

def find_jobs(job_title, page_nums):
    # USR = getpass.getpass('Database user name:')
    # PWD = getpass.getpass('Database password:')
    USR = 'root'
    PWD = 'SQL960910'
    DB = 'indeed_jobs'
    engine = engine = db.create_engine('mysql+pymysql://'+USR+':'+PWD+'@localhost/'+DB)
    headers = {'user-agent' :'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'}

    # if there is a spance in the job_title, it will be problemic to name the table
    job_title = re.sub('\s', '_', job_title)
    # get jobs that has already been found, identify them with their unique id
    try:  ## if the table has not been created before, then start from scratch
        ids_db = pd.read_sql('select page_id from {}.{}'.format(DB, job_title), engine)['page_id'].tolist()
    except:
        ids_db = []
    # count num to set index_num for new jobs
    index_num = len(ids_db)+1
    count = 0

    for i in range(0, page_nums):
        ## after searching, the page that retrived was not the one with detailed info for each job,
        ## so we have to find the page_id for each and open the page with that job
        url1 = 'https://cn.indeed.com/jobs?q={}&start={}'
        res1 = requests.get(url1.format(job_title,i*10), headers = headers)
        content1 = etree.HTML(res1.text)

        pages = content1.xpath('//*[@class="jobToJobRec_Hide"]/@id')

        for page in pages:

            #check if the job has been found before

            id = re.search('jobToJobRec_(\S+)_[so]j', page).group(1)
            if id in ids_db:
                pass
            else:
                print('searching page {}, getting the {} th job'.format(i+1, count+1 ))

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
                    if loc[0] == '-' or len(loc) == 0:  ## ====>> locations are not in the same div
                        loc = content2.xpath('/html/body/div[1]/div[2]/div[3]/div/div/div[1]/div[1]/div[1]/div[1]/div/div[4]/text()')

                    return loc
                loc = find_location()

                # job description
                destription = ' '.join(content2.xpath('//*[@id="jobDescriptionText"]//text()'))

                # save all the info into DataFrame
                info = pd.DataFrame({
                    'index_num' : [index_num],
                    'title':title,
                    'company':company,
                    'location':loc,
                    'description':destription,
                    'link': [url2.format(id)],
                    'page_id': id
                })

                # export infos to database
                info.to_sql(job_title, con = engine, if_exists = 'append', index = False)
                index_num += 1
                count += 1
                time.sleep(1)
    print('Done searching, {} new jobs has been found,sending email now...'.format(count))
    send_email('There are {} new jobs found for the last {} pages'.format(count, page_nums))



def main():
    '''h -> hour，m -> minute'''

    job_title =input('Please tell me what kind of job do you want:')
    page_nums = int(input('How many pages do you want me to search:'))

    #
    # h = hour
    # m = minute
    # while True:
    #     # check if it's time to start
    #     while True:
    #         now = datetime.datetime.now()
    #         # quit the inner loop if
    #         if now.hour==h and now.minute==m:
    #             break
    #         # wait for 20s and then check again
    #         time.sleep(20)
        # find the job I want
    find_jobs(job_title, page_nums)
if __name__ == '__main__':
    # hour = input('Set the hour:')
    # minute = input('Set the minute:')
    main()
