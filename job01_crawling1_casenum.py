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

casenum = 1
threadLocal = threading.local()


def getCaseNum(html): # 판례번호 받아오기
    global casenum
    bs = BS(html, "lxml")
    csnum = bs.find_all("a", {"class": "layer_pop_open"})
    arr = []
    for i in csnum:
        cs = i.get('id')
        cs = cs.replace("py_", "")
        arr += [[casenum, int(cs)]]
        print(casenum, cs)
        casenum += 1
    return arr


def get_driver():
    driver = getattr(threadLocal, 'driver', None) # 객체에 driver의 속성값을 가져온다. 디폴트값은 None으로 준다.
    if driver is None: # driver가 default라면...
        options = webdriver.ChromeOptions()
        prefs = {'profile.default_content_setting_values': {'cookies': 2, 'images': 2, 'javascript': 2,
                                                            'plugins': 2, 'popups': 2, 'geolocation': 2,
                                                            'notifications': 2, 'auto_select_certificate': 2,
                                                            'fullscreen': 2,
                                                            'mouselock': 2, 'mixed_script': 2, 'media_stream': 2,
                                                            'media_stream_mic': 2, 'media_stream_camera': 2,
                                                            'protocol_handlers': 2,
                                                            'ppapi_broker': 2, 'automatic_downloads': 2,
                                                            'midi_sysex': 2,
                                                            'push_messaging': 2, 'ssl_cert_decisions': 2,
                                                            'metro_switch_to_desktop': 2,
                                                            'protected_media_identifier': 2, 'app_banner': 2,
                                                            'site_engagement': 2,
                                                            'durable_storage': 2}}
        # options.add_argument('headless')
        # options.add_experimental_option('prefs', prefs)
        options.add_argument("start-maximized")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
        driver = webdriver.Chrome(path, chrome_options=options)
        setattr(threadLocal, 'driver', driver) # 새로운 속성을 부여함 threadlocal.driver=> driver라는 의미이다.
    return driver # driver 값을 반환한다.


path = "./chromedriver"
url = "https://glaw.scourt.go.kr/wsjo/panre/sjo050.do"
url2 = "https://glaw.scourt.go.kr/wsjo/panre/sjo100.do?contId="

checknum = 1


def CaseNum(): # 판례 번호 받기
    global checknum
    # 1.대법원 사이트 접속
    case = list()
    driver = get_driver()
    driver.get(url)
    time.sleep(2)
    search_box = driver.find_element_by_name("srchw") # 검색어 위치 연결
    search_box.send_keys("대법원") # 검색어 보내기
    driver.find_element_by_xpath('//*[@id="search"]/div[2]/fieldset/a[1]').click()# 검색버튼
    driver.find_element_by_xpath('//*[@id="search"]/div[2]/fieldset/div/p/a').click() # 자동완성 창 닫기
    driver.find_element_by_xpath('//*[@id="groupList"]/li[5]/ul/li[1]/a').click()
    driver.find_element_by_xpath('//*[@id="tabwrap"]/div/div/div[1]/div[3]/fieldset/ul/li[2]/a/span[1]').click()

    # 2. 판례 번호 크롤링
    for i in range(1888):
        if i == 0:
            html = driver.page_source # html은 driver.page_source
            case += getCaseNum(html) # 홈페이지에 있는 모든 판례번호 받아오기
            time.sleep(0.3)
            driver.find_element_by_xpath('//*[@id="tabwrap"]/div/div/div[1]/div[3]/div/fieldset/p/a[1]').click() # 다음페이지

        elif (i >= 1 and i <= 9):
            html = driver.page_source
            case += getCaseNum(html) # 판례번호 받아오기
            time.sleep(0.5)
            driver.find_element_by_xpath('//*[@id="tabwrap"]/div/div/div[1]/div[3]/div/fieldset/p/a[2]').click() # 다음 페이지

        elif (i >= 10 and i < 1887):
            try:
                html = driver.page_source
                case += getCaseNum(html) # 판례번호 받아오기
                time.sleep(0.5)
                driver.find_element_by_xpath('//*[@id="tabwrap"]/div/div/div[2]/div[3]/div[2]/div/fieldset/input').clear()
                time.sleep(1)
                driver.find_element_by_xpath('//*[@id="tabwrap"]/div/div/div[2]/div[3]/div[2]/div/fieldset/input').send_keys(i+1)
                time.sleep(1)
                driver.find_element_by_xpath('//*[@id="tabwrap"]/div/div/div[2]/div[3]/div[2]/div/fieldset/a').click()
            except:
                print('error')


    f = open("casenum.csv", mode="w", encoding='utf-8', newline='') # 쓰기 모드로 열기
    wr = csv.writer(f)
    for cs in case: # case 리스트에서 cs를 뽑아서
        wr.writerow([cs[0], cs[1]]) # 1차원 리스트에 대한 열저장
    f.close() # 닫는다.

CaseNum()

f = open('casenum.csv', mode='r', encoding='utf-8') # 읽기 모드로 열기
rd = csv.reader(f)
arr = list(rd)  # casenum 리스트
f.close()




