#!/usr/bin/env/python

#
#   FILE:       SingleURLSubmissionTest.py
#   AUTHOR:     mmiddleton
#   DATE:       1 MAR 2018
#
#   DESCRIPTION:   
#   This unittest submits a single URL to the landing page and selects the 
#

import unittest
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class SingleURLSubmissionTest (unittest.TestCase):
    url = None
    driver = None

    def setUp (self):
        self.url = "http://" + os.environ['BROWSERSTACK_USER'] + ":" + os.environ['BROWSERSTACK_ACCESS_KEY'] + "@hub.browserstack.com:80/wd/hub"

    def test_input_of_invalid_link (self):
        self.initializeConnection ('Single URL Submission - Test Invalid Link')
        driver = self.driver
        driver.get ("http://localhost:5000/")
        elem = driver.find_element_by_tag_name ("textarea")
        elem.send_keys ("https://www.google.com")
        elem.submit ()
        elementValue = driver.find_element_by_tag_name ("h1")
        self.assertIn ("Uh Oh!", elementValue.text)

    # def test_input_of_valid_link (self):
    #     self.assertTrue (True)

    def initializeConnection (self, testName):
        desiredCapabilities = {
            'os' : 'Windows',
            'os_version' : '10',
            'browserstack.timezone' : 'UTC-05:00',
            'browserstack.selenium_version' : '3.5.2',  
            'browser' : 'Chrome',
            'browser_version' : '64.0',
            'project' : 'SMOSS',
            'browserstack.local' : 'true',
            'name' : testName,
        }
        
        self.driver = webdriver.Remote (command_executor = self.url, desired_capabilities = desiredCapabilities)


    def tearDown (self):
        self.driver.quit ()


if __name__ == "__main__":
    unittest.main ()