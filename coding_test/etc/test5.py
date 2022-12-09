# https://www.python.org/search 파이썬 사이트에서 
# response라고 검색했을 때의 웹페이지를 출력하는 파이썬 코드를 작성하시오.

import urllib.request

url = 'https://www.python.org/search'
values = {'q': 'response'}
data = urllib.parse.urlencode(values).encode('utf-8')

req = urllib.request.urlopen(url, data)
result = req.read()
print(result)
