#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Main.py
# @Time      :2021/8/29 14:02
# @Author    :Amundsen Severus Rubeus Bjaaland


import logging

from TxtBook import Download

logging.basicConfig(
    format="[%(asctime)s](%(levelname)s)%(name)s: %(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
    level=logging.WARNING
)


Download("https://www.rmxsba.com/19540_7/", SaveToOneFile=False)