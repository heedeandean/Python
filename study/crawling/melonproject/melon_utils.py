import requests
import json
import re
from bs4 import BeautifulSoup


def get_songInfo(songId):

    url = 'https://www.melon.com/song/detail.htm?songId=' + str(songId)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }

    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.text, 'html.parser')

    genre = soup.select_one(
        'div.entry > div.meta > dl > dd:nth-of-type(3)').text
    releaseDate = soup.select_one(
        'div.entry > div.meta > dl > dd:nth-of-type(2)').text.replace('.', '')
    album = soup.select_one(
        'div.entry > div.meta > dl > dd:nth-of-type(1) > a').text

    tempDic = {'releaseDate': releaseDate, "album": album, "genre": genre}

    return tempDic


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


def get_albumInfo(albumId):

    url = 'https://www.melon.com/album/detail.htm?albumId=' + str(albumId)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }

    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.text, 'html.parser')

    jsonUrl = "https://www.melon.com/commonlike/getAlbumLike.json?"
    rateUrl = "https://www.melon.com/album/albumGradeInfo.json?"

    jsonHeaders = {'Referer': url,
                   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
                   }

    jsonparams = {"contsIds": str(albumId)}
    rateparams = {'albumId': str(albumId)}

    jsonHtml = requests.get(jsonUrl, headers=jsonHeaders, params=jsonparams)
    jsonData = json.loads(jsonHtml.text)

    rateHtml = requests.get(rateUrl, headers=jsonHeaders, params=rateparams)
    rateData = json.loads(rateHtml.text)

    albumlike = jsonData['contsLike'][0]['SUMMCNT']
    rate = rateData["infoGrade"]["TOTAVRGSCORE"]
    agency = soup.select_one(
        'div.entry > div.meta > dl > dd:nth-of-type(4)').text
    albumtype = soup.select_one('div.entry > div.info > span').text.strip()
    albumtype = re.findall("\[(.*)\]", albumtype)[0].strip()

    tempDic = {"agency": agency, "albumId": albumId, "rate": rate,
               'albumlike': albumlike, 'albumtype': albumtype}

    return tempDic
