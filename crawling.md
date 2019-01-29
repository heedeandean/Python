# 문항 1
```python
import requests, json, pymysql
import re
from bs4 import BeautifulSoup

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
```
