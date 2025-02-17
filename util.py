import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import requests
import base64

def waitUntilLoad(driver, target, timeout = 10, refresh = False, by = By.XPATH):
    elem = False
    while elem == False:
        try:
            print(target + "正在查找")
            elem = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, target)))
            print(target + "找到")
        except TimeoutException:
            elem = False
            if refresh == True:
                print(target + "超时并刷新")
                driver.refresh()
                elem = waitUntilLoad(driver, target, timeout, refresh)
            else:
                print(target + "超时")

    return elem

def sendMenssage(receiver_email, messageSubject = "抢票成功"):
    sender_email = ""

    # 创建邮件
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = messageSubject

    # 添加邮件正文
    message.attach(MIMEText("这是通知邮件", "plain"))
    try:
        with smtplib.SMTP("smtp.sina.cn", 25) as server:
            server.starttls()
            server.login(sender_email, "3a6341")
            server.sendmail(sender_email, receiver_email, message.as_string())
    except:
        print("发送失败")

def sendMenssage2(receiver_email, messageSubject = "抢票成功"):
    sender_email = ""

    # 创建邮件
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = messageSubject

    # 添加邮件正文
    message.attach(MIMEText("这是通知邮件", "plain"))
    try:
        with smtplib.SMTP("smtp.126.com", 25) as server:
            server.starttls()
            server.login(sender_email, "WDN3")
            server.sendmail(sender_email, receiver_email, message.as_string())
    except:
        print("发送失败")