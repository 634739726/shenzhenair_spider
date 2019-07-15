import requests
from create_driver import driver
import re


class ShenZhenAir:
    def __init__(self, airline, form_data):
        self.airline = airline
        self.form_data = form_data
        self.index_url = "http://www.shenzhenair.com"
        self.flight_search = "http://www.shenzhenair.com/szair_B2C/flightSearch.action"
        self.core_session, self._g_sign, self.ua = driver.get_cookie()
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Host': 'www.shenzhenair.com',
            'Proxy-Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': self.ua
        }
        self.session = requests.session()
        # self.session.proxies = {}  # 代理添加

    # get_sign_flight, get_sign_cookie
    def get_index(self):
        response = self.session.get(self.index_url, headers=self.headers, verify=False)
        sign_flight = re.findall('''cookie' : "(\w+)",''', response.text)[0]
        self.session.cookies.set('sign_flight', sign_flight, domain='www.shenzhenair.com')

    def get_core_session(self):
        self.session.cookies.set('CoreSessionId', self.core_session)
        self.session.cookies.set('_g_sign', self._g_sign)

    def get_JSESSIONID(self):
        headers = {
            'Origin': 'http://www.shenzhenair.com',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': self.ua,
            'Accept': '*/*',
            'Referer': 'http://www.shenzhenair.com/',
            'X-Requested-With': 'XMLHttpRequest',
            'Proxy-Connection': 'keep-alive'
        }
        self.session.post('http://www.shenzhenair.com/szair_B2C/login/loginInformation.action', headers=headers)

    def get_flights(self):
        response = self.session.post(self.flight_search, headers=self.headers, data=self.form_data, verify=False)
        return response.text

    def main(self):
        self.get_index()
        self.get_core_session()
        self.get_JSESSIONID()
        return self.get_flights()


if __name__ == '__main__':
    airline = {
        'hcType': 'DC',
        'constId': '',
        'type': '单程',
        'orgCity': '深圳',
        'orgCityCode': 'SZX',
        'dstCity': '北京',
        'dstCityCode': 'PEK',
        'orgDate': '2019-07-19',
        'dstDate': '2019-07-19',
        'quiz': ['Y', '1']
    }
    form_data = {
        'condition.orgCityCode': 'SZX',
        'condition.dstCityCode': 'PEK',
        'condition.hcType': 'DC',
        'condition.orgDate': '2019-07-19',
        'condition.dstDate': '2019-07-19',
        'condition.constId': ''
    }
    print(ShenZhenAir(airline, form_data).main())
    driver.driver.quit()
