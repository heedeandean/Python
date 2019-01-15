# 문항 1
* 아래 사이트(멜론 Top100)에서 1위부터 100위까지의 곡들에 대한,   
순위, 곡 이름, 가수명, 좋아요 수를 스크래핑하는 프로그램을 작성하시오.
```python
from bs4 import BeautifulSoup
import requests
import json 

url_top100= 'http://www.melon.com/chart/index.htm'
url_json = "https://www.melon.com/commonlike/getSongLike.json?contsIds=31549966%2C31532643%2C31532438%2C31554317%2C31477685%2C31406357%2C31417871%2C31506637%2C31492319%2C31448480%2C31388145%2C31556500%2C31399721%2C30962526%2C31403163%2C31373277%2C31266290%2C31455159%2C31495659%2C31542508%2C31314144%2C31453551%2C31346009%2C31417922%2C31433084%2C31356458%2C31304766%2C31532642%2C31151836%2C31492321%2C31551385%2C31402611%2C31492322%2C31062863%2C31399726%2C31316695%2C31085237%2C31399725%2C31399728%2C31399724%2C31399731%2C31551382%2C30244931%2C31526249%2C31340985%2C31399730%2C31399727%2C31266289%2C31399729%2C31399722%2C31553909%2C30637982%2C31510409%2C31388213%2C31486544%2C30699142%2C30806536%2C31554809%2C31266282%2C31266291%2C31403156%2C31131273%2C3087601%2C30568338%2C31144690%2C31085238%2C31286161%2C31331745%2C31314142%2C31470006%2C30725482%2C30314784%2C31478848%2C31175119%2C30809895%2C31302310%2C31133898%2C31266288%2C31457611%2C8235260%2C30960341%2C31541154%2C31344113%2C31113240%2C30672529%2C31219546%2C31085244%2C30669593%2C30859584%2C31433086%2C31433089%2C30884950%2C31266286%2C31356799%2C31524320%2C31433085%2C30717645%2C31433087%2C31356451%2C31539246%2C30930312"


header = { "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98   Safari/537.36"}

header_json = { 'referer' : "http://www.melon.com/chart/index.htm",
"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}

html = requests.get(url_top100, headers=header)
html_json = requests.get(url_json, headers=header_json)

soup = BeautifulSoup(html.text, "html.parser")

jsonData = json.loads(html_json.text)

cnt_rank = 0

artist = soup.find_all(name="div", attrs={"class":"ellipsis rank02"})
title = soup.find_all(name="div", attrs={"class":"ellipsis rank01"})
songNo50 = soup.find_all(name="tr", attrs={'id':'lst50'})
songNo100 = soup.find_all(name="tr", attrs={'id':'lst100'})

dic = {}

for i in range(0, int(len(title)/2)):
    cnt_rank += 1
    title1 = title[i].text.strip()
    artist1 = artist[i].find('a').text.strip()
    songid =  songNo50[i].attrs['data-song-no']
    rank =  str(cnt_rank)

    tempDic = { 'rank' : rank + '위' , "CONTSID" : songid, "title" : title1, "artist" : artist1 , "likecnt" : '' }

    dic[songid] = tempDic

for i in range(int(len(title)/2), len(title)):
    ii = i - 50
    cnt_rank += 1
    title1 = title[i].text.strip()
    artist1 = artist[i].find('a').text.strip()
    songid =  songNo100[ii].attrs['data-song-no']
    rank =  str(cnt_rank)

    tempDic = { 'rank' : rank + '위' , "CONTSID" : songid, "title" : title1, "artist" : artist1 , "likecnt" : '' }

    dic[songid] = tempDic

for j in jsonData['contsLike']:
    k = str(j['CONTSID'])
    dicK = dic.get(k)
    if dicK == None :
        continue
    dicK['likecnt'] = j['SUMMCNT']

for song in dic.keys():
    aa = dic[song]
    print(aa)
```

# 문항 2
* 본인이 정한 사이트를 크롤하여 데이터 수집을 하는 프로그램의 수집 계획서 및 코드를 작성하시오.
```
<데이터 수집 계획>
목적 : yes24 공연 예매 사이트에서 공연을 선택하여 잔여 좌석 개수를 확인한다. 
      더 나아가, 잔여 좌석 중 좋은 자리를 선정해 자동으로 예매한다.
순서 :
    1. 본인이 원하는 공연을 선택한다.
    2. 공연의 날짜와 회차를 선택해 idHall과 idTime 값을 추출한다.
    3. 해당 idHall과 idTime을 이용해 yes24 좌석 서버에 접속한다.
    4. 잔여 좌석수를 파악한다.
    5. 좌석이 남아있다면 남은 좌석 중 좋은 좌석(앞 쪽)을 선택해 자동 예매한다.
```
```python
# idHall과 idTime 가져오기

import requests
from bs4 import BeautifulSoup

session = requests.session()

loginUrl = "https://www.yes24.com/Templates/FTLogin.aspx"

headers = {
    "Referer": 'http://ticket.yes24.com/',
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
}

login_info = {
        'LoginType': '',
        'FBLoginSub$ReturnURL': 'http://ticket.yes24.com/Pages/Perf/Detail/DetailSpecial.aspx' ,
        'FBLoginSub$ReturnParams': 'IdPerf=32098' ,
        'RefererUrl': '', 
        'AutoLogin': '1' ,
        'LoginIDSave': 'Y' ,
        'FBLoginSub$NaverCode': '' ,
        'FBLoginSub$NaverState': '' ,
        'FBLoginSub$Facebook': '' ,
        'SMemberID': '본인 아이디' ,
        'SMemberPassword': '본인 비밀번호'
}

res = session.post(loginUrl, data=login_info, headers=headers)
res.raise_for_status()


#접근할 페이지 1
res = session.get('http://ticket.yes24.com/Pages/Perf/Sale/PerfSaleProcess.aspx?IdPerf=32098')
res.raise_for_status()

soup1 = BeautifulSoup(res.text, "html.parser")


date = soup1.select_one('#tk_day').text
print(date)


exit()


#접근할 페이지 2

page2_headers = { 'Referer': 'http://ticket.yes24.com/Pages/Perf/Sale/PerfSaleProcess.aspx?IdPerf=32098' ,
"X-Requested-With" : "XMLHttpRequest",
'Host': 'ticket.yes24.com',
'Origin': 'http://ticket.yes24.com',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}


# ToDo 공연마다 회차정보(날짜) 받아서 pDay에 넣기
# ToDo 공연마다 회차정보(공연번호) 받아서 pIdPerf에 넣기
page2_params = {
    'pDay': '20190427',
    'pIdPerf': '32098',
    'pIdCode': '', 
    'pIsMania': '0'
}

res2 =  session.post('http://ticket.yes24.com/Pages/Perf/Sale/Ajax/Perf/PerfTime.aspx',headers=page2_headers, data=page2_params)
res2.raise_for_status()





#idHall과 idTime 추출
soup2 = BeautifulSoup(res2.text, "html.parser")

idHall = soup2.select_one('ul#ulTimeData >li').attrs['idhall']
idTime = soup2.select_one('ul#ulTimeData >li').attrs['value']
saleclose = soup2.select_one('ul#ulTimeData >li').attrs['saleclose']

print(idHall)
print(idTime)
print(saleclose)
```
```python
# 좌석수 추출하는 것에 필요한 모듈

def split_1(_seat):

    seat_list = _seat.split('^')

    real_seat_list = []

    for i in seat_list :
        sl = i.split('@')
        real_seat_list.append(sl)

    for j, k in enumerate(real_seat_list):
        
        if real_seat_list[j][0] == '' :
            continue
        else :
            aa = real_seat_list[j][4] + ' ' + real_seat_list[j][2] + '원' + " " + real_seat_list[j][3] + '석'

        print(aa)


def split_2(_seat):

    seat_list = _seat.split('^')

    real_seat_list = []

    for i in seat_list:
        sl = i.split('@')
        real_seat_list.append(sl)

    for j, k in enumerate(real_seat_list):
        
        if real_seat_list[j][0] == '' :
            continue
        else :
            aa = real_seat_list[j][0] + ' ' + real_seat_list[j][1] + '/' + real_seat_list[j][2] + '석'

        print(aa)
```
```python
# nct 콘서트로 실행해보기

import requests
from bs4 import BeautifulSoup
import ticket_module as tm

session = requests.session()



#url = "http://ticket.yes24.com/OSIF/Book.asmx/GetHallMapRemain"
url = "http://ticket.yes24.com/OSIF/Book.asmx/GetHallMapRemainFN"

headers = {
    "Referer": "http://ticket.yes24.com/OSIF/Book.asmx?op=GetHallMapRemainFN",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
}

params = {
    'idHall': '8531',
    'idTime': '985109'
}

res = session.post(url, data=params, headers=headers)
res.raise_for_status()

soup = BeautifulSoup(res.text, "html.parser")

seat_info = soup.find('regend').get_text()
seat_info2 = soup.find('section').get_text()


tm.split_1(seat_info)
print("--------------")
tm.split_2(seat_info2)
```
```python
#  뮤지컬 지킬 앤 하이드로 실행해보기

import requests
from bs4 import BeautifulSoup
import ticket_module as tm

session = requests.session()



url = "http://ticket.yes24.com/OSIF/Book.asmx/GetHallMapRemainFN"

headers = {
    "Referer": "http://ticket.yes24.com/OSIF/Book.asmx?op=GetHallMapRemainFN",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
}

idHall = '8531'
idTime = '971101'

params = {
    'idHall': idHall,
    'idTime': idTime
}

res = session.post(url, data=params, headers=headers)
res.raise_for_status()

soup = BeautifulSoup(res.text, "html.parser")

seat_info1 = soup.find('regend').get_text()
seat_info2 = soup.find('section').get_text()


tm.split_1(seat_info1)
print("---------")
tm.split_2(seat_info2)
```
```python
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup


USER = "본인 아이디"
PASS = "본인 비번"

browser = webdriver.Chrome()
browser.implicitly_wait(3)

# 로그인 페이지에 접근하기. 
url_login = "https://www.yes24.com/Templates/FTLogin.aspx?ReturnURL=http://ticket.yes24.com/Pages/Perf/Detail/Detail.aspx&&ReturnParams=IdPerf=30862"
browser.get(url_login)
print("로그인 페이지에 접근합니다.")

# 아이디와 비밀번호 입력하기.
e = browser.find_element_by_id("SMemberID")
e.clear()
e.send_keys(USER)
e = browser.find_element_by_id("SMemberPassword")
e.clear()
e.send_keys(PASS)

# 입력 양식 전송해서 로그인하기.
form = browser.find_element_by_css_selector("button#btnLogin").submit()
print("로그인 버튼을 클릭합니다.")

# 예매버튼 클릭.
reserve_bt = browser.find_element_by_class_name("rbt_reserve").click()
print("예매 버튼을 클릭합니다.")

# 팝업 창으로 전환.
browser.switch_to.window(browser.window_handles[1])

# 날짜 선택하기(26일)
date_sel = browser.find_element_by_id("2019-01-17").click()
sleep(1)

# '좌석선택' 버튼 클릭.
res = browser.find_element_by_css_selector("div.fr img").click()

#좌석 선택하기

browser.switch_to.frame(browser.find_element_by_name("ifrmSeatFrame"))


browser.find_element_by_id('t800012').click()

browser.find_element_by_class_name('booking').click()

print("좌석선택완료")

browser.switch_to_default_content()

print("다시원래창으로 돌아옴")

browser.find_element_by_xpath('//*[@id="StepCtrlBtn03"]/a[2]/img').click()

print("할인쿠폰 다음버튼")

sleep(3)
browser.find_element_by_xpath('//*[@id="StepCtrlBtn04"]/a[2]/img').click()

browser.find_element_by_id('rdoPays22').click()

browser.find_element_by_xpath('//*[@id="selBank"]/option[5]').click()



browser.find_element_by_xpath('//*[@id="cbxCancelFeeAgree"]').click()
browser.find_element_by_xpath('//*[@id="chkinfoAgree"]').click()

pic = browser.save_screenshot("pic.png")

browser.find_element_by_xpath('//*[@id="imgPayEnd"]').click()

# for i in seat:
#     a = i.text
#     print(i)


# print(seat)
# # for s in seat:
# #     print("-", s.text)





# 브라우저 닫음
# browser.close()
```
