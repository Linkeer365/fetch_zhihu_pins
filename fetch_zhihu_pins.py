import selenium
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

from selenium.common.exceptions import NoSuchElementException,TimeoutException


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

target_dir=r"D:\zhihu_pins"
target_path=r"D:\zhihu_pins\pins.txt"
already_path=r"D:\zhihu_pins\already_fetch.txt"

pin_urls=[
    "https://www.zhihu.com/people/lin-ke-47-1/pins?page=1",
    "https://www.zhihu.com/people/lin-ke-47-1/pins?page=2",
    "https://www.zhihu.com/people/lin-ke-47-1/pins?page=3",
    "https://www.zhihu.com/people/lin-ke-47-1/pins?page=4",
    "https://www.zhihu.com/people/lin-ke-47-1/pins?page=5",
    "https://www.zhihu.com/people/lin-ke-47-1/pins?page=6",
    "https://www.zhihu.com/people/lin-ke-47-1/pins?page=7",
    "https://www.zhihu.com/people/lin-ke-47-1/pins?page=8",
    "https://www.zhihu.com/people/lin-ke-47-1/pins?page=9",
    "https://www.zhihu.com/people/lin-ke-47-1/pins?page=10",
    "https://www.zhihu.com/people/lin-ke-47-1/pins?page=11",
    "https://www.zhihu.com/people/lin-ke-47-1/pins?page=12",
    "https://www.zhihu.com/people/lin-ke-47-1/pins?page=13",
    "https://www.zhihu.com/people/lin-ke-47-1/pins?page=14",
    "https://www.zhihu.com/people/lin-ke-47-1/pins?page=15",
    "https://www.zhihu.com/people/lin-ke-47-1/pins?page=16",
    "https://www.zhihu.com/people/lin-ke-47-1/pins?page=17",
    # "https://www.zhihu.com/people/lin-ke-47-1/pins?page=18",
]

firefox_path=r"C:\Program Files\Mozilla Firefox\geckodriver.exe"

options = Options()
options.headless = True
# options.headless=False

driver=webdriver.Firefox(options=options,executable_path=firefox_path)
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

pins=[]
for each_link in pin_links:
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
    print("one done.")

pins_all_s="\n***===***\n".join(pins)
with open (target_path, "a", encoding="utf-8") as f:
    f.write(pins_all_s)
print("all done.")


