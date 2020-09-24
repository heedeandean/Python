import requests
import json
import re
from bs4 import BeautifulSoup


def get_songLike(songid):

    jsonUrl = "https://www.melon.com/commonlike/getSongLike.json?"

    jsonHeaders = {'Referer': 'https://www.melon.com/chart/index.htm',
                   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
                   }

    jsonparams = {"contsIds": songid}

    jsonHtml = requests.get(jsonUrl, headers=jsonHeaders, params=jsonparams)
    jsonData = json.loads(jsonHtml.text)

    likecnt = jsonData['contsLike'][0]['SUMMCNT']

    return likecnt


def get_songInfo(songId):

    url = ' http://vlg.berryservice.net:8099/melon/songdetail?songId=' + \
        str(songId)

    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    genre = soup.select_one(
        'div.entry > div.meta > dl > dd:nth-of-type(3)').text
    releaseDate = soup.select_one(
        'div.entry > div.meta > dl > dd:nth-of-type(2)').text.replace('.', '')
    album = soup.select_one(
        'div.entry > div.meta > dl > dd:nth-of-type(1) > a').text

    tempDic = {'releaseDate': releaseDate, "album": album, "genre": genre}

    return tempDic


def get_albumInfo(albumId):

    url = 'http://vlg.berryservice.net:8099/melon/detail?albumId=' + \
        str(albumId)

    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    jsonUrl = "http://vlg.berryservice.net:8099/melon/albumlikejson?albumId=" + \
        str(albumId)
    rateUrl = "http://vlg.berryservice.net:8099/melon/albumratejson?albumId=" + \
        str(albumId)

    jsonHtml = requests.get(jsonUrl).text
    jsonData = json.loads(jsonHtml)

    rateHtml = requests.get(rateUrl).text
    rateData = json.loads(rateHtml)

    albumlike = jsonData['contsLike'][0]['SUMMCNT']
    rate = rateData["infoGrade"]["TOTAVRGSCORE"]
    agency = soup.select_one(
        'div.entry > div.meta > dl > dd:nth-of-type(4)').text
    albumtype = soup.select_one('div.entry > div.info > span').text.strip()
    albumtype = re.findall("\[(.*)\]", albumtype)[0].strip()

    tempDic = {"agency": agency, "albumId": albumId, "rate": rate,
               'albumlike': albumlike, 'albumtype': albumtype}

    return tempDic
