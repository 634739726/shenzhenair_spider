from selenium import webdriver
import os
from coreSession_gSign import get_js


class ChromeSupport:
    def __init__(self):
        self.url = os.path.abspath(__file__).rsplit('\\', 1)[0] + "\\chrome_supporter.html"
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(self.url)

    def get_cookie(self):
        ua, js = get_js()
        core_session, _g_sign = self.driver.execute_script(js)
        return core_session, _g_sign, ua


driver = ChromeSupport()

if __name__ == '__main__':
    print(driver.get_cookie())



