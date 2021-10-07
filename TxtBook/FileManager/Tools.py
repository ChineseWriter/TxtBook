#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Tools.py
# @Time      :2021/10/7 11:56
# @Author    :Amundsen Severus Rubeus Bjaaland


import os


def MakeDir(Path):
    try:
        os.mkdir(Path)
    except FileExistsError:
        pass
