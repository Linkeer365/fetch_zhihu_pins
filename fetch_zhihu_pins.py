import selenium
import re

# import win32con
# import win32gui
# import win32api

from PIL import Image

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

from selenium.common.exceptions import NoSuchElementException,TimeoutException

# 知乎那个总是加载不出来，所以只能强行点击你了...
from selenium.webdriver.common.action_chains import ActionChains


# 解决点不动的问题
# https://stackoverflow.com/questions/21350605/python-selenium-click-on-button

from selenium.webdriver.support.ui import WebDriverWait

# 一出现就马上点，这个操作好啊！！！

# https://stackoverflow.com/questions/62868434/button-click-only-works-when-time-sleep-added-for-selenium-python
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import os
import sys

import time
from PIL import Image

# target_dir=r"D:\zhihu_pins"
# target_path=r"D:\zhihu_pins\pins.txt"
# already_path=r"D:\zhihu_pins\already_fetch.txt"

qrcode_path=r"D:\AllDowns\zhihu.png"
yanzhengma_path=r"D:\AllDowns\yanzhengma.png"

firefox_path=r"C:\Program Files\Mozilla Firefox\geckodriver.exe"

options = Options()
options.headless = False
# options.headless=False

driver=webdriver.Firefox(options=options,executable_path=firefox_path)
max_delay=10

# while True:
#     tempt = win32api.GetCursorPos() # 记录鼠标所处位置的坐标
#     # x = tempt[0]-choose_rect[0] # 计算相对x坐标
#     # y = tempt[1]-choose_rect[1] # 计算相对y坐标
#     print(tempt)
#     time.sleep(2)

def find_elements_by_xpath2(patt):
    WebDriverWait(driver,max_delay).until(EC.presence_of_element_located((By.XPATH, patt)))
    return driver.find_elements_by_xpath(patt)

def find_element_by_xpath2(patt):
    return WebDriverWait(driver,max_delay).until(EC.presence_of_element_located((By.XPATH, patt)))

def login():
    login_url="https://www.zhihu.com/signin?next="
    driver.get(login_url)



    # passwd_login_node=find_element_by_xpath2("//div[@class='SignFlow-tab']")

    # 向节点的上面几层一个个试过去
    # 因为image,svg那些,被放到了下面的好几层，所以你点不到是很正常的...

    qrcode_node=driver.find_element_by_xpath("//div[@class='SignFlow-qrcodeTab']")

    # print(passwd_login_node.location)
    # print(qrcode_node.location)

    # 密码登录：(691,299)
    # 二维码位置：(969,291)

    # ActionChains(driver).move_to_element_with_offset(passwd_login_node,869-561+2,0).click().perform()



    
    # time.sleep(2)

    qrcode_node.click()
    qrcode_full_node=find_elements_by_xpath2("//img[@class='Qrcode-qrcode']")
    driver.save_screenshot(qrcode_path)
    img=Image.open(qrcode_path)
    img.show()
    # print("login!")

    # with open("d:/pp.txt","w",encoding="utf-8") as f:
    #     f.write(driver.page_source)

    # passwd_login_node=find_element_by_xpath2("//div[@class='SignFlow-tab']")
    # passwd_login_node.click()
    # time.sleep(1)

    # username_node=find_element_by_xpath2("//input[@name='username']")
    # passwd_node=find_element_by_xpath2("//input[@name='password']")

    # username="13959253604"
    # passwd="xm111737"

    # username_node.send_keys(username)
    # passwd_node.send_keys(passwd)
    # time.sleep(1)
    # quedingBtn=find_element_by_xpath2("//button[@type='submit']")

    # quedingBtn.click()

    # # passwd_node.send_keys(Keys.ENTER)

    # yanzhengma=find_element_by_xpath2("//img[@class='Captcha-englishImg']")

    # if yanzhengma:
    #     inputBox_node=find_element_by_xpath2("//div[@class='SignFlowInput']/label/input[@name='captcha']")
    #     driver.save_screenshot(yanzhengma_path)
    #     img=Image.open(yanzhengma_path)
    #     img.show()
    #     yanzhengma_input=input("Input yanzhengma:")
    #     inputBox_node.send_keys(yanzhengma_input)
    #     quedingBtn=find_element_by_xpath2("//button[@type='submit']")
    #     quedingBtn.click()

        # inputBox_node.send_keys(Keys.ENTER)
        
    # time.sleep(2)

    while not "signin" in driver.current_url:
        print("login!")

# login()
# sys.exit(0)

username=input("input username(zhihu.com/people/<username>/pins):")

target_dir=f"D:/zhihu_pins/{username}"
target_path=f"D:/zhihu_pins/{username}/pins.txt"
already_path=r"D:/zhihu_pins/{username}/already_fetch.txt"

user_pins_url=f"https://www.zhihu.com/people/{username}/pins"
print(user_pins_url)
driver.get(user_pins_url)
# num_str=driver.find_element_by_xpath("//a[@class='Tabs-link is-active']").get_attribute("meta")

# 返回一个selenium.common.exceptions.TimeoutException，表示需要登录才能爬取...
try:
    num_str_node=find_element_by_xpath2("//a[contains(@href,'pins')]")
    num_str=num_str_node.get_attribute("meta")
except TimeoutException:
    print("need to login!")
    login()


if "," in num_str:
    num_str=num_str.replace(",","")
amount=int(num_str)

print(num_str)
if amount%20==0:
    page_num=amount//20
elif amount%20!=0:
    page_num=amount//20+1

pin_urls=[user_pins_url+f"?page={each}" for each in range(1,page_num+1)]



# pin_urls=[
#     "https://www.zhihu.com/people/lin-ke-47-1/pins?page=1",
#     "https://www.zhihu.com/people/lin-ke-47-1/pins?page=2",
#     "https://www.zhihu.com/people/lin-ke-47-1/pins?page=3",
#     "https://www.zhihu.com/people/lin-ke-47-1/pins?page=4",
#     "https://www.zhihu.com/people/lin-ke-47-1/pins?page=5",
#     "https://www.zhihu.com/people/lin-ke-47-1/pins?page=6",
#     "https://www.zhihu.com/people/lin-ke-47-1/pins?page=7",
#     "https://www.zhihu.com/people/lin-ke-47-1/pins?page=8",
#     "https://www.zhihu.com/people/lin-ke-47-1/pins?page=9",
#     "https://www.zhihu.com/people/lin-ke-47-1/pins?page=10",
#     "https://www.zhihu.com/people/lin-ke-47-1/pins?page=11",
#     "https://www.zhihu.com/people/lin-ke-47-1/pins?page=12",
#     "https://www.zhihu.com/people/lin-ke-47-1/pins?page=13",
#     "https://www.zhihu.com/people/lin-ke-47-1/pins?page=14",
#     "https://www.zhihu.com/people/lin-ke-47-1/pins?page=15",
#     "https://www.zhihu.com/people/lin-ke-47-1/pins?page=16",
#     "https://www.zhihu.com/people/lin-ke-47-1/pins?page=17",
#     # "https://www.zhihu.com/people/lin-ke-47-1/pins?page=18",
# ]

max_delay=5

pin_links=[]

# def login():
#     login_url="https://www.zhihu.com/signin?next=%2F"
#     driver.get(login_url)
#     find_elements_by_xpath2("//image[starts-with(@xlink:href,'data:image/png;')]").click()
#     driver.save_screenshot()

def find_elements_by_xpath2(patt):
    WebDriverWait(driver,max_delay).until(EC.presence_of_element_located((By.XPATH, patt)))
    return driver.find_elements_by_xpath(patt)

def find_element_by_xpath2(patt):
    WebDriverWait(driver,max_delay).until(EC.presence_of_element_located((By.XPATH, patt)))
    return driver.find_element_by_xpath(patt)

for each_url in pin_urls:
    driver.get(each_url)
    link_nodes=find_elements_by_xpath2("//div[@class='ContentItem-time']/a[starts-with(@href,'//www.zhihu.com/pin')]")
    links=[each.get_attribute("href") for each in link_nodes]
    pin_links.extend(links)
    # print(links)

if os.path.exists(already_path):
    with open(already_path,"r",encoding="utf-8") as f:
        already_links=[each.strip("\n") for each in f.readlines() if each!="\n"]
        already_links_set=set(already_links)

pins=[]
for each_link in pin_links:
    if each_link in already_links_set:
        continue
    pin_id=each_link.rsplit("/",maxsplit=2)[-1]
    driver.get(each_link)
    body=driver.find_element_by_xpath("//span[@class='RichText ztext CopyrightRichText-richText']").text
    try:
        repost_link_node=driver.find_element_by_xpath("//a[@class='link-box']")
        repost_link=repost_link_node.get_attribute ("href")
        repost_link_info_node=driver.find_element_by_xpath("//span[@class='title PinItem-contentTitle']")
        repost_link_info=repost_link_info_node.text
        repost=f"\nLink: [{repost_link_info}]({repost_link})\n"
    except NoSuchElementException or TimeoutException:
        # 这里注意要import Exception不然无法识别...
        # 纯想法，无转发内容
        repost=""
    body+=repost
    comment_nodes=driver.find_elements_by_xpath("//div[@class='RichText ztext']")
    comments=[each.text+"\n" for each in comment_nodes]
    body2=""
    for comment in comments:
        body2+=comment
    pin=f"Body:\n{body}\nComment:\n{body2}\n"
    pins.append(pin)

    with open(f"{target_dir}{os.sep}{pin_id}.txt","w",encoding="utf-8") as f:
        f.write(pin)
    
    with open(already_path,"a",encoding="utf-8") as f:
        f.write("\n\n")
        f.write(each_link)
        f.write("\n\n")
    print("one done.")

pins_all_s="\n***===***\n".join(pins)
with open (target_path, "a", encoding="utf-8") as f:
    f.write(pins_all_s)
print("all done.")


