#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Controller.py
# @Time      :2021/9/4 12:24
# @Author    :Amundsen Severus Rubeus Bjaaland


import logging

from .FileManager import SaveToOneTxt, SaveToManyTxt
from .Download import DownloadChapters, GetBookInfo


LOGGER = logging.getLogger(__name__)


def Download(Source: str, Path: str = "./", SaveToOneFile: bool = True):
    BookInfo = GetBookInfo(Source)
    if BookInfo is None:
        LOGGER.critical(f"解析URL({Source})失败")
        return None
    BookName = BookInfo["BookName"]
    MaxChapterNumber = BookInfo["MaxChapterNumber"]
    ChapterList = DownloadChapters(Source)
    if SaveToOneFile:
        SaveToOneTxt(Path, BookName, MaxChapterNumber, ChapterList)
    else:
        SaveToManyTxt(Path, BookName, MaxChapterNumber, ChapterList)
    return None
