from selenium import webdriver
from selenium.common import NoSuchElementException,ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import random
import pyautogui
import keyboard
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from util import waitUntilLoad, sendMenssage

#设置
'''
print("输入时间 比如: 19 00")
bookingTime = input().split(" ")
bookingTime = int(bookingTime[0]) * 3600 + int(bookingTime[1]) * 60
'''

bookingTime = [1, 10]  #5点10分
bookingTime = int(bookingTime[0]) * 3600 + int(bookingTime[1]) * 60

loginUrl = "https://ticket.yes24.com/Pages/English/Member/FnLoginNew.aspx?ReturnURL=http://ticket.yes24.com/Pages/English/Perf/FnPerfDeail.aspx?IdPerf=51057"
dateXPATH = '//*[@id="2024-10-20"]'
timeXPATH = '//*[@id="ulTime"]/li[1]' #'//*[@id="ulTime"]/li[2]'

#['Floor', 'B1', 'B2', 'D1', 'D2', 'C1C2', 'C3', 'A2', 'A3A4', 'E2', 'E3E4']
bookRegions = ['C1C2', 'C3', 'A2', 'A3A4', 'E2', 'E3E4']

emails = [
        "4970@qq.com",
        ]
password = "123."

print("输入账号编号")
emailNum = int(input())

region2Click = {'Floor': (851, 226),
                'B1': (798, 221),
                'B2': (798, 256),
                'D1': (900, 220),
                'D2': (900, 260),
                'C1C2': (824, 288),
                'C3': (882, 285),
                'A2': (773, 215),
                'A3A4': (773, 242),
                'E2': (927, 217),
                'E3E4': (927, 240),
                }

region2Seat = {'Floor': (146, 237, 607, 666),
                'B1': (38, 256, 197, 581),
                'B2': (87, 289, 224, 615),
                'D1': (541, 255, 687, 580),
                'D2': (541, 295, 652, 605),
                'C1C2': (43, 355, 584, 682),
                'C3': (378, 358, 651, 670),
                'A2': (82, 400, 222, 551),
                'A3A4': (84, 245, 230, 618),
                'E2': (425, 400, 562, 552),
                'E3E4': (440, 249, 582, 626),
               }

colors = [(85, 41, 221), (153, 0, 201), (0, 224, 224), (206, 0, 151) , (204, 255, 0), (206, 53, 0)]

def clickRegionAndGetSeat(region):
    pyautogui.click(region2Click[region])
    time.sleep(0.1)

    bFindNullSeat = False
    matching_coordinates = []

    for i in range (0, 10):
        screenshot = pyautogui.screenshot()
        for x in range(region2Seat[region][0], region2Seat[region][2]):
            for y in range(region2Seat[region][1], region2Seat[region][3]):
                pixel_rgb = screenshot.getpixel((x, y))
                if pixel_rgb in colors:
                    matching_coordinates.append((x, y))
                elif pixel_rgb == (225, 225, 225):
                    bFindNullSeat = True

        if len(matching_coordinates) == 0 and bFindNullSeat == False:
            time.sleep(i * 0.1)
        else:
            break

    if matching_coordinates:
        random_coordinate = random.choice(matching_coordinates)
        pyautogui.click(*random_coordinate)
        time.sleep(0.1)
        pyautogui.click((863, 696))
        time.sleep(0.2)
        print(region)
        print(datetime.today())

        try:
            alert = driver.switch_to.alert
            if alert:
                alert.accept()
                print("出现警告1")
                return
        except:
            print("无弹窗1")

        time.sleep(0.2)
        try:
            alert = driver.switch_to.alert
            if alert:
                alert.accept()
                print("出现警告2")
                return
        except:
            print("无弹窗2")

        sendMenssage("40@qq.com")
        sendMenssage("0@qq.com")
        time.sleep(10000)


#开始执行

driver = webdriver.Edge()
driver.maximize_window()
driver.get(loginUrl)

consice_login_element = waitUntilLoad(driver, '//*[@id="txtEmail"]', 30, True)
consice_login_element.send_keys(emails[emailNum])
s_member_id_element = waitUntilLoad(driver, '//*[@id="txtPassword"]', 30)
s_member_id_element.send_keys(password)
s_member_id_element = waitUntilLoad(driver, '//*[@id="btnLogin"]', 30)
s_member_id_element.click()
time.sleep(3)

while True:
    currentTime = str(datetime.now().time())
    currentTime = currentTime.split(":")
    currentTime = int(currentTime[0]) * 3600 + int(currentTime[1]) * 60 + int(currentTime[2].split(".")[0])
    if currentTime >= bookingTime:
        break

driver.refresh()
ticket = waitUntilLoad(driver, '//*[@id="hlkPurchase"]', 30, True)
if ticket:
    print("开始book")
    ticket.click()
    print("等待窗口")
    while len(driver.window_handles) <= 1:
        driver.implicitly_wait(1)
    print("转至book窗口..")
    driver.switch_to.window(driver.window_handles[1])
    print("成功转到book窗口" + driver.title)

    while True:
        try:
            dateBtn = waitUntilLoad(driver, dateXPATH)
            dateBtn.click()
            break
        except:
            pass

    while True:
        try:
            timeBtn = waitUntilLoad(driver, timeXPATH)
            timeBtn.click()
            break
        except:
            pass

    while True:
        try:
            seatBtn = waitUntilLoad(driver, '//*[@id="btnSeatSelect"]')
            seatBtn.click()
            break
        except:
            pass


    driver.maximize_window()
    tryCount = 0
    while True:
        try:
            for bookRegion in bookRegions:
                clickRegionAndGetSeat(bookRegion)
                time.sleep(random.randint(100, 500) / 500.0)
        except:
            print("找座位出错")

        tryCount +=1
        if tryCount > 10:
            tryCount = 0
            time.sleep(random.randint(100, 500) / 20.0)
else:
    print("找不到预定入口")

time.sleep(100000)