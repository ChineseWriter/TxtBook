#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Save.py
# @Time      :2021/9/5 12:37
# @Author    :Amundsen Severus Rubeus Bjaaland


import os
import logging

from alive_progress import alive_bar
from alive_progress.animations import scrolling_spinner_factory

from .Tools import MakeDir


def OneTxt(Path: str, BookName: str, MaxChapterNumber: int, ChapterList) -> bool:
    assert os.path.exists(Path)
    Logger = logging.getLogger(__name__ + ".OneTxt")
    Path = Path.replace("\\", "/").rstrip("/") + "/"
    Logger.info(f"开始下载：{BookName}")
    with alive_bar(MaxChapterNumber,
                   spinner=scrolling_spinner_factory(chars=BookName, length=25, background="·")) as Bar:
        for i in ChapterList:
            Logger.info(f"下载：{i[0]}")
            with open(Path + BookName + ".txt", "a+", encoding="UTF-8") as File:
                File.write(i[0].replace(BookName, ""))
                File.write("\n")
                File.write(i[1])
                File.write("\n")
            Bar()
    return True


def ManyTxt(Path: str, BookName: str, MaxChapterNumber: int, ChapterList):
    LOGGER = logging.getLogger(__name__ + ".ManyTxt")
    Path = Path.replace("\\", "/").rstrip("/") + "/"
    MakeDir(Path + BookName)
    MakeDir(Path + BookName + "/第1章节")
    MakeDir(Path + BookName + "/第1章节/第1部")
    Counter_1 = 1
    Counter_2 = 1
    Counter_3 = 1
    Counter_4 = 1
    LOGGER.info(f"开始下载：{BookName}")
    with alive_bar(MaxChapterNumber,
                   spinner=scrolling_spinner_factory(chars=BookName, length=25, background="·")) as Bar:
        for i in ChapterList:
            LOGGER.info(f"下载：{i[0]}")
            with open(Path + BookName + f"/第{Counter_4}章节/第{Counter_3}部/第{Counter_2}部分.txt", "a+",
                      encoding="UTF-8") as File:
                File.write(i[0].replace(BookName, ""))
                File.write("\n")
                File.write(i[1])
                File.write("\n")
            if Counter_3 % 10 == 0 and Counter_2 % 10 == 0 and Counter_1 % 10 == 0:
                Counter_4 += 1
                Counter_3 = 0
                Counter_2 = 0
                Counter_1 = 0
                MakeDir(Path + BookName + f"/第{Counter_4}章节")
            if Counter_2 % 10 == 0 and Counter_1 % 10 == 0:
                Counter_3 += 1
                Counter_2 = 0
                Counter_1 = 0
                MakeDir(Path + BookName + f"/第{Counter_4}章节/第{Counter_3}部")
            if Counter_1 % 10 == 0:
                Counter_2 += 1
                Counter_1 = 0
            Counter_1 += 1
            Bar()
