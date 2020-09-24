from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=13&ncvContSeq=&contSeq=&board_id=&gubun=")  # 전국
html_kk = urlopen("https://www.gg.go.kr/contents/contents.do?ciIdx=1150&menuId=2909")  # 경기도

soup = BeautifulSoup(html, "html.parser")
soup_kk = BeautifulSoup(html_kk, "html.parser")


# 전국
for city, count in zip(soup.find_all(scope="row"), soup.find_all(headers="status_con s_type1")):
    print(city.text.strip(), count.text.strip())
    
print()

# 경기
table_kk = soup_kk.find('div', {'class': 'mt-4 zone'})

for city, count in zip(table_kk.find_all('dt'), table_kk.find_all('strong')):
    print(city.text.strip(), count.text.strip())