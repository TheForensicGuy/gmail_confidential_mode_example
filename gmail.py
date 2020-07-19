#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## This code demonstrates how you can automate sending confidential mode gmail 
##
## Use the gmail API to send email unless you need to use the new "Confidential" mode
## "Confidential" mode is not yet available via the gmail API so extra effort is needed
## 
## Requirements for this example script to work on Linux or OSX
## 1. download chromedriver from https://chromedriver.storage.googleapis.com/index.html?path=84.0.4147.30/
##    unzip and ensure chromedriver is in $PATH perhaps by using "mv chromedriver /usr/local/bin"
## 2. pip install selenium 
## 3. if the sending gmail account is brand new then sugget you login a couple 
@@    of times manually to get past any initial welcome or guidance popups
##
## this example created 2020-07-19 
## https://github.com/TheForensicGuy/gmail_confidential_mode_example
##

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, sys

def send_using_confidential_mode(send_from_email ="",send_from_pw="",send_to="",add_attachment="",send_subject="",send_body=""):
    return_message = ""
    try:
        driver = webdriver.Chrome()
        driver.get("https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin")
        email = driver.find_element_by_xpath('//*[@id="identifierId"]')
        email.clear()
        email.send_keys(send_from_email)
        email.send_keys(Keys.RETURN)
        time.sleep(1)
        try:
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')))
        finally:
            password = driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
            password.clear()
            password.send_keys(send_from_pw)
            password.send_keys(Keys.RETURN)
        time.sleep(4)
        ## now logged in and ready to start new email by clicking the compose button
        driver.find_element_by_css_selector(".T-I-KE").click()
        time.sleep(3)
        driver.find_element_by_name("to").send_keys(send_to)
        driver.find_element_by_name("subjectbox").send_keys(subject_email)
        driver.find_element_by_xpath("//div[@aria-label='Message Body']").send_keys(body_email)
        if filename_to_attach != "":  ## skip attaching file if no file was specified
            driver.find_element_by_name("Filedata").send_keys(filename_to_attach)
            time.sleep(1)
        driver.find_element_by_xpath("//div[@aria-label='Turn confidential mode on / off']").click()
        time.sleep(1)
        driver.find_element_by_xpath("//button[@name='locker_controls_dialog_save']").click()
        time.sleep(1)
        driver.find_element_by_xpath("//div[@aria-label='Send ‪(⌘Enter)‬']").click()
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        return_message = template.format(type(ex).__name__, ex.args)
        pass
    return return_message

if __name__ == "__main__":
    if sys.version_info.major<3:
        print("needs python3 or higher")
    assert sys.version_info >= (3, 0)

    # example to send gmail using confidential mode
    from_email="xxxx@gmail.com"  ## the gmail address used to send this email
    from_pw = "xxxx"  ## password for above email account - ideally pull this from your secrets source
    to_email = ""  ## destination email address(es) 
    filename_to_attach = "" ## full path to file to attach to email
    subject_email = "Testing automated sending of confidential mode gmail with attachment" ## email subject
    body_email = "gmail content body." ## email body can be plain text or can be html formatted content
    send_result = send_using_confidential_mode(from_email,from_pw,to_email,filename_to_attach,subject_email,body_email)
    if send_result != "":
        print(send_result)  ## reveal any error that occured
    time.sleep(5) # brief delay just so you can see webpage message that email was sent (if viewing interactive)

