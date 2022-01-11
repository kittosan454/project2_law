import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup as BS
from multiprocessing.pool import Pool, ThreadPool
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# from selenium.common.exceptions import TimeoutException
import threading
import re
import csv
import pandas as pd

options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('lang=ko_KR')
options.add_argument('disable_gpu')

driver = webdriver.Chrome('./chromedriver', options=options)


df =  pd.read_csv('./casenum2.csv')
df.info()

df.reset_index(inplace=True)
df.to_csv('reset_casnum.csv')
list_df = list(df['casenum'])


casenum = []
titles = []
laws = []





for  j in range(802, len(list_df)):
    link = "https://glaw.scourt.go.kr/wsjo/panre/sjo100.do?contId={}".format(df.iloc[j,2])
    driver.get(link)
    time.sleep(0.5)
    time.sleep(0.5)
    try:
        title =driver.find_element_by_xpath('//*[@id="bmunStart"]/h2').text


        # law = driver.find_element_by_xpath('//*[@id="areaDetail"]/div[2]/div').text()
        # laws.append(law)
        law = driver.find_element_by_xpath('//*[@id="areaDetail"]/div[2]/div').text

        # append는 마지막에 넣는게 좋다 각각의 데이터 개수를 맞추기 위해서
        laws.append(law)
        casenum.append(df.iloc[j, 2])
        titles.append(title)

        print(j)
    except:
        print('error')

    if j % 50 == 0:
        df_law50 = pd.DataFrame({'casenum': casenum, 'titles': titles, 'laws': laws})
        df_law50.to_csv('./crawling_data/law_{}_{}.csv'.format(j-49, j), index=False)
        casenum = []
        titles = []
        laws = []

df_law50 = pd.DataFrame({'casenum': casenum, 'titles': titles, 'laws': laws})
df_law50.to_csv('./crawling_data/law_remain.csv', index=False)