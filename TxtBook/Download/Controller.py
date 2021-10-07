#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Controller.py
# @Time      :2021/10/7 10:05
# @Author    :Amundsen Severus Rubeus Bjaaland


from urllib.parse import urlparse
import logging

from .Engines import MAP
from .Object import NetWork



def DownloadChapters(Source: str):
    Logger = logging.getLogger(__name__ + ".DownloadChapters")
    ParsedResult = urlparse(Source)
    DomainName = ParsedResult.netloc
    if DomainName not in MAP:
        Logger.error(f"该URL的域名不在支持范围内。")
        return None
    CatalogueResponse = NetWork(Source)
    for i in MAP[DomainName].GetCatalogue(CatalogueResponse):
        TextResponse = NetWork(i[1])
        Data = MAP[DomainName].GetText(TextResponse)
        if Data is None:
            Logger.warning("网络错误。")
            continue
        Data = (i[0], Data)
        yield Data


def GetBookInfo(Source: str):
    Logger = logging.getLogger(__name__ + ".GetBookInfo")
    ParsedResult = urlparse(Source)
    DomainName = ParsedResult.netloc
    if DomainName not in MAP:
        Logger.error(f"该URL的域名不在支持范围内。")
        return None
    InfoResponse = NetWork(Source)
    return MAP[DomainName].GetInfo(InfoResponse)
