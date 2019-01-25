import requests, json, re, pymysql
from bs4 import BeautifulSoup
import berry_utils as bu

url = "http://vlg.berryservice.net:8099/melon/list"

html = requests.get(url)
soup = BeautifulSoup(html.text, 'html.parser')
trs1 = soup.select('#lst50')
trs2 = soup.select('#lst100')


top100list = []
songinfolist = []
albuminfolist = []
singerList = []
sslist = []

def get_list (trs) :
        
    for td in trs:

        # Top100 구성
        dataSongNo = td.attrs['data-song-no']
        rank = td.select('td:nth-of-type(2) > div > span.rank')[0].text
        name = td.select('td:nth-of-type(6) > div > div > div.ellipsis.rank01 > span > a')[0].text
        artists = td.select('td:nth-of-type(6) > div > div > div.ellipsis.rank02 > a')
        artist = ", ".join([a.text for a in artists])
        likeCnt = bu.get_songLike(dataSongNo)

        href = td.select('td:nth-of-type(4) > div > a')[0].attrs['href']
        albumId = re.findall("\'(.*)\'", href)[0]
        
        top100 = (int(rank), dataSongNo, name , artist, likeCnt, albumId)
        top100list.append(top100)

        # 노래 정보 구성
        songInfoDic = bu.get_songInfo(dataSongNo)
       
        releaseDate = songInfoDic['releaseDate']
        album = songInfoDic['album']
        genre = songInfoDic['genre'] 

        songinfos = (releaseDate , dataSongNo, albumId, album, genre, likeCnt, name, artist)
        songinfolist.append(songinfos)

        # 앨범 정보 구성
        albumInfoDic =  bu.get_albumInfo(albumId)

        albumlike = albumInfoDic['albumlike']
        agency = albumInfoDic['agency']
        rate = albumInfoDic['rate'] 
        albumtype = albumInfoDic['albumtype']

        albuminfos = (releaseDate, agency, albumId, album, rate, albumlike, albumtype, artist)
        albuminfolist.append(albuminfos)
        
        # 가수, 매핑(노래-가수) 구성
        for singer in artists :
            sid = singer.attrs["href"]
            sid = re.findall("\'(.*)\'", sid)[0]
            
            al = (sid, singer.text)
            singerList.append(al)

            sl = (dataSongNo, name, singer.text, sid)
            sslist.append(sl)
    

get_list(trs1)
get_list(trs2)

albuminfolist = (list(set(albuminfolist)))
singerList = list(set(singerList))
sslist = list(set(sslist))


# mysql에 데이터 넣기.
def get_mysql_conn(db):
    return pymysql.connect(
        host= '34.85.124.225',
        user='root',
        password='11',
        port=3306,
        db=db,
        charset='utf8')


sql_dailyList = "insert into DailyList(rank, song_id, title, singer, likecnt, album_id) values(%s,%s,%s,%s,%s,%s)"

sql_dupl_album = "insert into AlbumInfo(release_date, agency, album_id, album_name, rate, album_likecnt, type, singer) values(%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE release_date=release_date, agency=agency, album_id=album_id, album_name=album_name, type=type, singer=singer "

sql_dupl_song = "insert into SongInfo(release_date, song_id, album_id, album_name, genre, likecnt, title, singer) values(%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE song_id=song_id, title = title, album_name = album_name, album_id = album_id , genre =genre,release_date=release_date, singer=singer;"

sql_dupl_singer = "insert ignore into Singer(singer_id, singer_name) values(%s, %s)"

sql_dupl_ss = "insert ignore into MappingSS (song_id, title, singer_name, singer_id) values(%s, %s, %s, %s)"

conn = get_mysql_conn('hjdb')

with conn:
    cur = conn.cursor()

    cur.executemany(sql_dupl_album, albuminfolist)
    print("반영된 수", cur.rowcount)

    cur.executemany(sql_dupl_song, songinfolist)
    print("반영된 수", cur.rowcount)
   
    cur.executemany(sql_dailyList, top100list)
    print("반영된 수", cur.rowcount)
    
    cur.executemany(sql_dupl_singer, singerList)
    print("반영된 수", cur.rowcount)

    cur.executemany(sql_dupl_ss, sslist)
    print("반영된 수", cur.rowcount)
