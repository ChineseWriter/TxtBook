#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Tools.py
# @Time      :2021/8/29 14:03
# @Author    :Amundsen Severus Rubeus Bjaaland


import requests
from bs4 import BeautifulSoup as bs

HEADER = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84"
}


def GetContent(Url: str, Parse):
    return Parse(bs(requests.get(Url, headers=HEADER).text, "lxml"))
