#!/usr/bin/env python
import os
import sys
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():
    if (sys.platform.startswith('win32')):
        import wmi
        c = wmi.WMI()
        for item in c.Win32_PhysicalMedia():
           print(item)

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
