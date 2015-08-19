import urllib2
import datetime
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
from check import send_report, run_test, push_test

downloaded_files = []
class HSTest(unittest.TestCase):
    def get_remote_js(self, driver):
        global downloaded_files
        scripts = driver.find_elements_by_tag_name("script")
        for script in scripts:
            type_ = script.get_attribute('type')
            source_ = script.get_attribute('src')
            if type_ == 'text/javascript' and 'cloudfront' in source_:
                downloaded_files.append(source_)

    def setUp(self):
        self.driver = webdriver.PhantomJS()
        #self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://secure.helpscout.net/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_h_s(self):
        driver = self.driver
        driver.get(self.base_url + "/members/login")
        self.get_remote_js(driver)
 
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
 
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
 
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

def test_HS_latency():
    try:
        unittest.main(exit=False)
        return True, True, None
    except Exception, e:
        return False, False, None

def test_cloudfront_latency():
    try:
        for downloaded_file in downloaded_files:
            response = urllib2.urlopen(downloaded_file)
            html = response.read()
        return True, True, None
    except Exception, e:
        return False, False, None

results = []
results.append(run_test(test_HS_latency, 5))
results.append(run_test(test_cloudfront_latency, 5))

push_test('Help Scout-cloudfront status %s' % datetime.datetime.now(), results)
