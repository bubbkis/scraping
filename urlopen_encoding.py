import sys
from urllib.request import urlopen

#f = urlopen('https://gihyo.jp/dp')
f = urlopen('https://google.co.jp')

encoding = f.info().get_content_charset(failobj="utf-8")
print('encoding:', encoding, file=sys.stderr)

text = f.read().decode(encoding)
print(text)
