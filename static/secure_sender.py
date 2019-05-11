#!/usr/bin/env python
import os
import sys
import requests
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():
    if (sys.platform.startswith('win32')):
        import subprocess
        from selenium import webdriver
        from webdriver_manager.chrome import ChromeDriverManager
        driver = webdriver.Chrome(ChromeDriverManager().install())
        uid = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
        print(uid)
        driver.get(("http://secureelogin.herokuapp.com/login"))
        time.sleep(1)
        username = driver.find_element_by_name('username')
        username.send_keys("bolexptk")
        password = driver.find_element_by_name('password')
        password.send_keys("password")
        password = driver.find_element_by_name('uid')
        password.send_keys(uid)
        submit = driver.find_element_by_class_name('submit')
        submit.click()

    elif (sys.platform.startswith('linux')):
        uid = os.system("cat /var/lib/dbus/machine-id")

        url = 'http://secureelogin.herokuapp.com/login'
        payload = uid
        browser = webdriver.Firefox()
        browser.get((url))
        time.sleep(1)
        username = browser.find_element_by_name('username')
        username.send_keys(uid)
        password = browser.find_element_by_id('password')
        password.send_keys(uid)
        submit = browser.find_element_by_id('submit')
        submit.click()


main()
