# get token from website
import selenium
from typing import Any
from selenium import webdriver
import time
import keyboard
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import permissions

class WebToken(object):
    """WebToken get token from spotify web site
    kwargs:
        spotify_token_url: 'https://developer.spotify.com/console/get-album-tracks/'
        web_browser: 'firefox' or 'chrome'
        browser_profile_path:'C:\\Users\\Akorz\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\ukml7b3k.automation'
        firefox_binary_path: "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
        webdriver_exec_path: "C:\\Users\\akorz\\Downloads\\geckodriver-v0.29.1-win64\\geckodriver.exe"
    """

    permission_dict = permissions.permission_dict
    def __init__(self, *args, **kwargs):
        super(WebToken, self).__init__()
        self.spotify_token_url = kwargs.get('spotify_token_url', 'https://developer.spotify.com/console/get-album-tracks/')
        self.web_browser = kwargs.get('web_browser', 'firefox')
        self.browser_profile_path = kwargs.get('browser_profile_path', 'C:\\Users\\Akorz\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\ukml7b3k.automation')
        self.firefox_binary_path = kwargs.get('firefox_binary_path', "C:\\Program Files\\Mozilla Firefox\\firefox.exe")
        self.webdriver_exec_path =kwargs.get('webdriver_exec_path', "C:\\Users\\akorz\\Downloads\\geckodriver-v0.29.1-win64\\geckodriver.exe")
		
    def get_token(self, ):
        '''return token, if browser incorrect return None'''
        
        if(self.web_browser == 'chrome'):
            options = webdriver.ChromeOptions()
            options.add_argument(f"user-data-dir={self.browser_profile_path}")
            driver = webdriver.Chrome(executable_path=self.webdriver_exec_path, chrome_options=options)
            driver.get(self.spotify_token_url)

        if(self.web_browser == 'firefox'):
            binary = FirefoxBinary(self.firefox_binary_path)
            profile = FirefoxProfile(self.browser_profile_path)
            driver = webdriver.Firefox(firefox_profile=profile, firefox_binary=binary, executable_path=self.webdriver_exec_path)
            driver.get(self.spotify_token_url)
        else: 
            print("not a suitable browser")
            return None
        # wait till page loads up
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//button[@data-target="#oauth-modal"]')))
        self.driver = driver
        # close cookie window
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'onetrust-close-btn-container')))
            cci = driver.find_element_by_id('onetrust-close-btn-container')
            cci.click()
        except selenium.common.exceptions.ElementNotInteractableException:
            print('coockie window not found')
            # send keys tab tab tab enter
        except selenium.common.exceptions.TimeoutException:
            print('coockie window not loaded')
        # wait till window animation ends
        time.sleep(1)
        try:
            # click get token bth to activate hidden menu
            get_token_btn = driver.find_element_by_xpath('//button[@data-target="#oauth-modal"]')
            get_token_btn.click()
        except selenium.common.exceptions.ElementClickInterceptedException:
            # if we here means that cookie window still open
            [keyboard.send("Tab") for _ in range(3)]
            keyboard.send("Enter")
            time.sleep(1)
            get_token_btn = driver.find_element_by_xpath('//button[@data-target="#oauth-modal"]')
            get_token_btn.click()
            # so i gave up at this pont
            print('coockie window was closed with keyboard lib')

        # clik checkboxes with requered permissions
        permission_list = list(self.permission_dict.values())

        chb = driver.find_elements_by_class_name('control-indicator')
        for num, i in enumerate(chb):
            # max 18 perm-s
            if num >= len(permission_list): break 
            if permission_list[num]: chb[num].click()

        # click bth to gen token with req-d permissions   
        btn = driver.find_element_by_id('oauthRequestToken')
        btn.click()
        
        # copy token into var
        WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="OAuth Access Token"]')))
        content = driver.find_element_by_xpath('//input[@placeholder="OAuth Access Token"]')
        token = content.get_attribute("value")

        # our job here is done
        
        driver.close()
        return token
    def close(self, ):
        self.driver.close()
        return 0

if __name__ == '__main__':
    t = WebToken(
        browser_profile_path=r'C:\Users\Akorz\AppData\Roaming\Mozilla\Firefox\Profiles\rwe75su1.auto',
        webdriver_exec_path=r'C:\Users\Akorz\Desktop\Python_code\SPOTIFY_pl\webdrivers\geckodriver.exe',
        firefox_binary_path=r"C:\Program Files\Mozilla Firefox\firefox.exe",
        web_browser='firefox'
    )
    print(t.get_token())
# geckodriver: add to PATH or put in C:/webdrivers
# about:profiles
# auth window will appear if profile not logged in
# it will be 5 min to logon 