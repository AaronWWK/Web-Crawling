from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import pandas as pd
import time

import sqlalchemy as db
import pymysql
import datetime
import getpass

# =========================
USR = 'root'
PWD = 'SQL960910'
DB = 'indeed_jobs'
engine = engine = db.create_engine('mysql+pymysql://'+USR+':'+PWD+'@localhost/'+DB)
headers = {'user-agent' :'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'}

# get jobs that has already been found, identify them with their unique id
try:  ## if the table has not been created before, then start from scratch
    ids_db = pd.read_sql('select page_id from {}.indeed_jobs'.format(DB), engine)['page_id'].tolist()
except:
    ids_db = []
# count num to set index_num for new jobs
index_num = len(ids_db)+1
# for sending email to inform you how many new job do you got
count = 0

# =======================
url = 'https://cn.indeed.com/jobs?q=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90&start=10&advn=960025476939591'
page = urlopen(url)
soup = BeautifulSoup(page, 'lxml')

page_ids = soup.find_all('div', attrs = {'class':'jobToJobRec_Hide'} )

for id_ in page_ids:
    id = re.search('jobToJobRec_(\S+)_[so]j',id_['id']).group(1)
    if id in ids_db:
        pass
    else:
        job_url='https://cn.indeed.com/viewjob?jk={}&tk=1dd261drm7l68803&from=serp&vjs=3'.format(id)

        job_url ='https://cn.indeed.com/%E8%81%8C%E4%BD%8D%E6%98%BE%E7%A4%BA?jk=760f6ae15a98b1e6&tk=1dd3egdl37g9o800&from=serp&vjs=3'
        job_page = urlopen(job_url)
        job_soup = BeautifulSoup(job_page)
        job_detail = job_soup.find_all('div', attrs = {'class': 'jobsearch-JobComponent'})

        title = job_soup.body.h3.text

        title = job_detail[0].h3.text
        company = job_detail[0].a.text
        description = job_detail[0].find_all('div', attrs = {'id': 'jobDescriptionText'})[0].text
        print(description)
        loc = job_detail[0].div.div.div.children   # it is a generator, how to loop through it
        for item in loc:
            i = []
            i.append(item.text)
        location = i[-1]

        info =pd.DataFrame({
            'title': [title],
            'company': [company],
            'location': [location],
            'description': [description]
        })
        info.to_sql('data scientist', engine, if_exists='append', index = False)

        time.sleep(1)
