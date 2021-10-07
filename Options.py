#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Options.py
# @Time      :2021/8/29 14:02
# @Author    :Amundsen Severus Rubeus Bjaaland


import logging

from TxtBook import Download

logging.basicConfig(
    format="[%(asctime)s](%(levelname)s)%(name)s: %(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
    level=logging.WARNING
)

# Download(
#     "https://www.rmxsba.com/55794/",
#     SaveToOneFile=False
# )
# Download(
#     "https://www.rmxsba.com/19540_7/",
#     SaveToOneFile=False
# )
# Download("https://www.rmxsba.com/11437/")
# Download("http://www.yunxs.com/tianmipengcidashushangehun/", SaveToOneFile=False)
# Download("https://www.jingcaiyuedu6.com/novel/CniVu3.html", SaveToOneFile=False)
# Download("https://www.81zw.com/book/45973/", SaveToOneFile=False)
# Download("https://www.biquwx.la/24_24918/", SaveToOneFile=False)
# Download("https://www.81zw.com/book/54721/", SaveToOneFile=False)
# Download("https://www.luoxiabook.com/dujiajiyi/", SaveToOneFile=False)
Download("https://www.yueshuxsw.com/book_50740/", SaveToOneFile=False)
