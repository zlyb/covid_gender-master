#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib
import time
import ngender


def driver_open(author, affiliate):
    data = {"author": author, "affiliate": affiliate}
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    wd = urllib.parse.urlencode(data)
    driver.get("https://xueshu.baidu.com/usercenter/data/authorchannel?cmd=inject_page&" + wd)
    # 解决搜索结果中personalSearch_result元素display:none的问题
    js = "document.getElementById(\"personalSearch_result\").style.display='block';"
    # 调用js脚本
    driver.execute_script(js)
    time.sleep(2)
    content = driver.page_source.encode('utf-8')
    driver.close()
    soup = BeautifulSoup(content, 'lxml')
    return soup


def parse_author(soup):
    if len(soup.select('div.searchResult_text a.personName')) != 0:
        author_name = list(soup.select('div.searchResult_text a.personName')[0].stripped_strings)[0]
        # author_institution = list(soup.select('div.searchResult_text a.personInstitution')[0].stripped_strings)[0]
    else:
        author_name = "NA"
    return author_name


def gender_guess(author_name):
    return ngender.guess(author_name)


def crawler():
    author = "ZhangLin"
    affiliate = "山东科技大学"
    soup = driver_open(author, affiliate)
    author_name = parse_author(soup)
    if author_name == "NA":
        gender = "NA"
    else:
        gender = gender_guess(author_name)
    print(author_name)
    print(gender)


if __name__ == "__main__":
    crawler()
