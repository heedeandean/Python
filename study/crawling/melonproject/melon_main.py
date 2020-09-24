import requests
import json
import re
import pymysql
from bs4 import BeautifulSoup

from song_info import get_songInfo
from album_info import get_albumInfo
from get_songlike import get_songLike

url = "https://www.melon.com/chart/index.htm"

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}


html = requests.get(url, headers=headers)
soup = BeautifulSoup(html.text, 'html.parser')
trs1 = soup.select('#lst50')
trs2 = soup.select('#lst100')


top100list = []
songinfolist = []
albuminfolist = []
singerList = []
sslist = []


def get_list(trs):

    for td in trs:

        dataSongNo = td.attrs['data-song-no']
        rank = td.select('td:nth-of-type(2) > div > span.rank')[0].text
        name = td.select(
            'td:nth-of-type(6) > div > div > div.ellipsis.rank01 > span > a')[0].text
        artists = td.select(
            'td:nth-of-type(6) > div > div > div.ellipsis.rank02 > a')
        artist = ", ".join([a.text for a in artists])
        likeCnt = get_songLike(dataSongNo)

        href = td.select('td:nth-of-type(4) > div > a')[0].attrs['href']
        albumId = re.findall("\'(.*)\'", href)[0]

        top100 = (int(rank), dataSongNo, name, artist, likeCnt, albumId)
        top100list.append(top100)

        songInfoDic = get_songInfo(dataSongNo)

        releaseDate = songInfoDic['releaseDate']
        album = songInfoDic['album']
        genre = songInfoDic['genre']

        songinfos = (releaseDate, dataSongNo, albumId,
                     album, genre, likeCnt, name, artist)
        songinfolist.append(songinfos)

        albumInfoDic = get_albumInfo(albumId)

        albumlike = albumInfoDic['albumlike']
        agency = albumInfoDic['agency']
        rate = albumInfoDic['rate']
        albumtype = albumInfoDic['albumtype']

        albuminfos = (releaseDate, agency, albumId, album,
                      rate, albumlike, albumtype, artist)
        albuminfolist.append(albuminfos)

        for singer in artists:
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
        host='34.85.124.225',
        user='root',
        password='11',
        port=3306,
        db=db,
        charset='utf8')


sql_dailyList = "insert into DailyList(rank, song_id, title, singer, likecnt, album_id) values(%s,%s,%s,%s,%s,%s)"

sql_dupl_album = "insert into AlbumInfo(release_date, agency, album_id, album_name, rate, album_likecnt, type, singer) values(%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE release_date=release_date, agency=agency, album_id=album_id, album_name=album_name, type=type, singer=singer "

sql_dupl_song = "insert into SongInfo(release_date, song_id, album_id, album_name, genre, likecnt, title, singer) values(%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE song_id=song_id, title = title, album_name = album_name, album_id = album_id , genre =genre,release_date=release_date, singer=singer;"

sql_dupl_singer = "insert ignore into Singer(singer_id, singer_name) values(%s, %s)"

sql_dupl_ss = "insert ignore into MappingSongArtist (song_id, title, singer_name, singer_id) values(%s, %s, %s, %s)"

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
