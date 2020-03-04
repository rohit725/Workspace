#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  selenium_test.py
#  
#  Copyright 2019 Unknown <rpandey@dev-master>
#  
#  
from selenium import webdriver
import pandas as pd
import re


def main(args):
    browser = webdriver.Chrome(executable_path ="/home/rpandey/Downloads/chromedriver")
    print("Driver Loaded.")
    df = pd.read_csv("/home/rpandey/Workspace/Practice/Files/filtered_pastebin_tweets.csv", encoding='utf-8')
    print("Dataframe Loaded")
    for index, row in df.iterrows():
        browser.maximize_window()
        url = eval(row["ip_domain_urls"])[0]
        print("Opening url: %s" % url)
        browser.get(url)
        key = re.findall(r"([^\/?]+)(?:\?.+)?$", url)
        if "raw" not in url:
            text = browser.find_element_by_class_name("text").text
        else:
            text = browser.find_element_by_tag_name("body").text
        with open("%s-pastebin-%s.txt" % (row["user_name"], key), "w") as f:
            f.write(text)
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
