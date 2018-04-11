from Config.config import *
import selenium.webdriver.support.ui as ui
import time

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait

def login_taobao():
    firefox_capabilities = DesiredCapabilities.FIREFOX
    # firefox_capabilities['marionette'] = True
    driver = webdriver.Firefox(capabilities=firefox_capabilities,
                               executable_path='D:/geckodriver')
    wait = ui.WebDriverWait(driver, 10)
    driver.maximize_window() #将浏览器最大化显示
    driver.delete_all_cookies()
    driver.get("https://login.taobao.com/member/login.jhtml")
    element = WebDriverWait(driver, 60).until(lambda driver :
    driver.find_element_by_xpath("//*[@id='J_Quick2Static']"))
    element.click()
    driver.implicitly_wait(20)
    username=driver.find_element_by_name("TPL_username")
    if not username.is_displayed:
        driver.implicitly_wait(20)
        driver.find_element_by_xpath("//*[@id='J_Quick2Static']").click()
    driver.implicitly_wait(20)
    username.send_keys(taobao_username)
    driver.find_element_by_name("TPL_password").send_keys(taobao_password)
    driver.implicitly_wait(20)
    driver.find_element_by_xpath("//*[@id='J_SubmitStatic']").click()
    #以下是获得cookie代码
    # cookie = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]
    # cookiestr = ';'.join(item for item in cookie)
    time.sleep(3)
    return driver
