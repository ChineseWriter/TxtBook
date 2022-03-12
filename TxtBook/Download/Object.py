#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Object.py
# @Time      :2021/10/7 10:01
# @Author    :Amundsen Severus Rubeus Bjaaland


from urllib.parse import urlparse
import logging
import time
import copy

import requests
import chardet
from bs4 import BeautifulSoup as bs

HEADER = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84"
}


class NetWork(object):
    __Logger = logging.getLogger(__name__ + ".NetWork")

    def __init__(self, Url: str, Retry: int = 5, DealException=lambda: time.sleep(5), **Headers):
        self.__Url = Url
        self.__Response = None
        self.__Content = None
        self.__Retry = Retry
        self.__Encoding = None
        self.__Get(Headers, DealException)

    def __Get(self, Headers: dict, DealException) -> None:
        Header = copy.deepcopy(HEADER)
        Header = {**Header, **Headers}
        Counter = 0
        while True:
            if Counter == 5:
                raise Exception("Network connection error.")
            if self.__GetResponse(Header):
                break
            else:
                DealException()
                Counter += 1
        return None

    def __GetResponse(self, Header: dict) -> bool:
        try:
            self.__Response = requests.get(self.__Url, headers=Header)
            if self.__Response.status_code != 200:
                return False
        except Exception:
            self.__Logger.warning(f"请求失败({self.__Url})")
            return False
        else:
            self.__Content = self.__Response.content
            self.__Encoding = chardet.detect(self.__Content)["encoding"]
            return True

    def GetNextUrl(self, Href: str) -> str:
        if Href[0: 4] == "http":
            return Href
        elif Href[0] == "/":
            Parse = urlparse(self.__Url)
            return Parse.scheme + "://" + Parse.netloc + Href
        else:
            return self.__Url + Href

    def SetEncoding(self, Encoding):
        self.__Encoding = Encoding
        return None

    @property
    def Url(self) -> str:
        return self.__Url

    @property
    def Response(self):
        return self.__Response

    @property
    def Content(self) -> bytes:
        return self.__Content

    @property
    def Text(self) -> str:
        self.__Content: bytes
        try:
            return self.__Content.decode(self.__Encoding)
        except UnicodeDecodeError:
            return self.__Response.text

    @property
    def Bs(self) -> bs:
        self.__Content: bytes
        try:
            return bs(self.__Content.decode(self.__Encoding), "lxml")
        except UnicodeDecodeError:
            return bs(self.__Response.text, "lxml")

    @property
    def Encode(self):
        return self.__Encoding

    @property
    def Language(self):
        self.__Content: bytes
        return chardet.detect(self.__Content)["language"]


class Analyzer(object):
    __Logger = logging.getLogger(__name__ + ".Analyzer")

    @classmethod
    def GetInfo(cls, Response: NetWork) -> dict:
        return {}

    @classmethod
    def GetCatalogue(cls, Response: NetWork) -> list:
        return []

    @classmethod
    def GetText(cls, Response: NetWork) -> str:
        return ""

    @staticmethod
    def TextNormalization(Text: str) -> str:
        DealtText = Text.replace("\r", "")
        DealtText = DealtText.replace("\n", "")
        DealtText = DealtText.replace("\xa0", " ")
        DealtText = DealtText.replace("<br/>", "\r\n")
        DealtText = DealtText.replace("\r\n\r\n", "\r\n")
        DealtText = DealtText.replace("    ", "\t")
        return DealtText

    @staticmethod
    def FindInfo(Response: NetWork, Attrs: dict, Element: str = "div", Number: int = 0) -> dict:
        MaxChapterNumber = len(Response.Bs.find_all(Element, attrs=Attrs)[Number].find_all("a"))
        BookName = Response.Bs.find("h1").text
        return {"BookName": BookName, "MaxChapterNumber": MaxChapterNumber}

    @staticmethod
    def FindChapterList(Response: NetWork, Attrs: dict, Element: str = "div", Number: int = 0):
        ChapterList = Response.Bs.find_all(Element, attrs=Attrs)[Number].find_all("a")
        for i in ChapterList:
            Data = (i.text, Response.GetNextUrl(i.get("href")))
            yield Data

    @staticmethod
    def FindText(Response: NetWork, Attrs: dict, Element: str = "div"):
        DivText = str(Response.Bs.find(Element, attrs=Attrs))
        DivText = DivText[DivText.find(">") + 1: -6]
        return DivText
