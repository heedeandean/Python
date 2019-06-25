# 문항 1
* Naver 검색 API를 이용하여 "파이썬"으로 검색된 네이버 블로그의 게시글 100개를 최신 작성순으로 수집하여,  
데이터베이스(MySQL)에 블로거는 Blogger, 게시글은 BlogPost 테이블에 각각 저장하시오.
```python
import requests, json, pymysql
import re

url = "https://openapi.naver.com/v1/search/blog.json"

title = "파이썬"
params = {
    "query": title,
    "display": 100,
    "start": 1,
    "sort": "date"
}

headers = {
    "X-Naver-Client-Id": "RipMBIOxFKjXBa1uzZFn",
    "X-Naver-Client-Secret": "Y5KVx67qLC"
}

result = requests.get(url, params=params, headers=headers).text

jsonData = json.loads(result)

blogger_data = []
post_data = []

for i in range(100):
    title = jsonData['items'][i]['title'].replace('<b>','').replace('</b>','')
    link = jsonData['items'][i]['link']
    postdate = jsonData['items'][i]['postdate']

    bloggerlink = jsonData['items'][i]['bloggerlink']
    blogger_id = re.sub("(http(s)*|:|/|blog|naver)","", bloggerlink).replace('..','')
    bloggername = jsonData['items'][i]['bloggername']
    
    blogger_data.append((blogger_id, bloggername, bloggerlink))
    post_data.append((title, link, blogger_id, postdate))

# print(json.dumps(jsonData, ensure_ascii=False, indent=2))

blogger_data = list(set(blogger_data))
post_data = list(set(post_data))

def get_mysql_conn(db):
    return pymysql.connect(
        host= 'localhost',
        user='dooo',
        password='dooo!',
        port=3306,
        db=db,
        charset='utf8')

sql_Blogger = "insert into Blogger(id, bloggername, bloggerlink) values(%s,%s,%s)"
sql_BlogPost = "insert into BlogPost(title, link, blogger_id, postdate) values(%s,%s,%s,%s)"

conn = get_mysql_conn('dooodb')

with conn:
    cur = conn.cursor()

    cur.executemany(sql_Blogger, blogger_data)
    print("Blogger 테이블 반영된 수", cur.rowcount)

    cur.executemany(sql_BlogPost, post_data)
    print("BlogPost 테이블 반영된 수", cur.rowcount)
```
```mysql
create table Blogger(
	 id varchar(512),
	 bloggername varchar(512),
     	 bloggerlink varchar(512)
);

create table BlogPost(
	 title varchar(512),
     	 link varchar(512),
	 blogger_id varchar(512),
     	 postdate varchar(31)
);

ALTER TABLE BlogPost ADD FOREIGN KEY (blogger_id) REFERENCES Blogger(id);
```
# 문항2  
* 아래 html 내용을 파싱하여, DB에 저장하는 insert문을 자동생성하는 코드를 작성하시오.
```python
from bs4 import BeautifulSoup

html = '''
    <dl>
        <dt>국적</dt>
        <dd>대한민국</dd>

        <dt>활동장르</dt>
        <dd>Dance, Ballad, Drama</dd>
    
        <dt>데뷔</dt>
        <dd class="debut_song">
            <span class="ellipsis">
                2016.05.05
                <span class="bar">
                    TTT
                </span>
                <a href="#">TTTTTTTTTTTTT</a>
            </span>
        </dd>
        
        <dt>수상이력</dt>
        <dd class="awarded">
            <span class="ellipsis">
                2018 하이원 서울가요대상
                <span class="bar">|</span>본상
            </span>
        </dd>
    </dl>'''

soup = BeautifulSoup(html, "html.parser")

titles = soup.select("dt")
contents = soup.select("dd")

keys = []
values = []

for a in titles :
    keys.append(a.text)

for i in contents:
    dd_span = i.find('span')
    dd_a = i.find('a')
    if dd_span != None and dd_a != None :
        j = dd_span.next.strip() 
        
    elif dd_span != None and dd_a == None :
        j = dd_span.next.strip() + dd_span.next.next.next.strip() + dd_span.next.next.next.next.strip()

    else :
        j = i.text
    
    values.append(j)

col_names = {}

for i in range(len(keys)):
    col_names[keys[i]] = values[i]

insert = "inset into Singer(nation, genre, debut, award) values('{}','{}','{}','{}')".format(col_names['국적'], col_names['활동장르'],col_names['데뷔'],col_names['수상이력'])

print(insert)
```
