import time
import re
from urllib.parse import unquote
import requests
import bs4
from .LinFormat import LinFormat


BBO_ID = 'iambot'
BBO_PWD = 'password'

BBO_BASE_URL = 'http://www.bridgebase.com/'
BBO_MYHAND_URL = BBO_BASE_URL + 'myhands/hands.php'
BBO_LOGIN_URL = BBO_BASE_URL + 'myhands/myhands_login.php'


def get_bbo_cookie(bboid=BBO_ID, password=BBO_PWD):
    res = requests.get(BBO_LOGIN_URL, allow_redirects=False)
    assert res.status_code == 200
    assert 'SRV' in res.cookies
    assert 'PHPSESSID' in res.cookies
    srv = res.cookies['SRV']
    phpsessid = res.cookies['PHPSESSID']
    cookie = 'PHPSESSID=' + phpsessid + '; SRV' + srv

    res = requests.post(BBO_LOGIN_URL,
                        params={
                            't': '/myhands/index.php?',
                            'count': 1,
                            'username': bboid,
                            'password': password,
                            'submit': 'Login',
                            'keep': 'on'},
                        headers={'cookie': cookie},
                        allow_redirects=False)
    assert res.status_code == 302
    assert 'myhands_token' in res.cookies
    return cookie + '; myhands_token=' + res.cookies['myhands_token']


def get_bbo_boards(bboid, cookie):
    end_time = int(time.time())
    start_time = end_time - 60 * 60 * 24 * 30  # 30 day
    offset = 0

    res = requests.post(BBO_MYHAND_URL,
                        params={
                            'username': bboid,
                            'start_time': start_time,
                            'end_time': end_time,
                            'offset': offset
                        },
                        headers={'cookie': cookie},
                        allow_redirects=True)
    assert res.status_code == 200
    return bbo_html_to_board(res.text)


def bbo_onclick_to_lin(text):
    return unquote(re.findall(r"'(.*?)'", text)[0].strip('\''))


def bbo_html_to_board(text):
    soup = bs4.BeautifulSoup(text, 'html.parser')

    ret = []
    # Find mbc
    for mbc in soup.select('tr.mbc'):
        # print(mbc)
        # handnum = mbc.find('td', class_='handnum').string
        # north = mbc.find('td', class_='north').string
        # south = mbc.find('td', class_='south').string
        # east = mbc.find('td', class_='east').string
        # west = mbc.find('td', class_='west').string
        result = mbc.find('td', class_='result').text
        point = float(mbc.find('td', class_=re.compile('score')).string)
        score = float(mbc.find_all('td', class_=re.compile('score'))[1].string)
        onclick = mbc.find('td', class_='movie').find('a')['onclick']
        if onclick:
            lin = bbo_onclick_to_lin(onclick)
            lin = LinFormat(lin)

        # print(north, south, east, west, result, score, lin)
        ret.append({'lin': lin, 'result': result, 'point': point, 'score': score})

    # Find Team

    # Find Tourney

    return ret
