#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Engines.py
# @Time      :2021/10/7 10:04
# @Author    :Amundsen Severus Rubeus Bjaaland


import logging
import re
import traceback
import chardet

from bs4 import BeautifulSoup as bs
import requests

from .Object import Analyzer, NetWork

HEADER = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84"
}


class Analyzer1(Analyzer):
    Finder_1 = re.compile("第\d+/(\d+)页")
    Finder_2 = re.compile("共(.*?)章")
    __Logger = logging.getLogger(__name__ + ".Analyzer1")

    @classmethod
    def GetCatalogue(cls, Response: NetWork) -> list:
        try:
            NumberOfChaptersText = Response.Bs.find("div", attrs={"class": "caption"}).find("span").text
            NumberOfChapters = int(cls.Finder_1.search(NumberOfChaptersText).group(1))
            Id = Response.Url.split("/")[-2].split("_")[0]
        except Exception:
            cls.__Logger.warning(f"解析{Response.Url}的内容失败。")
            traceback.print_exc()
            return []
        # Buffer = []
        for Counter in range(1, NumberOfChapters + 1):
            NewUrl = "https://www.rmxsba.com/" + Id + "_" + str(Counter) + "/"
            try:
                NewContent = bs(requests.get(NewUrl, headers=HEADER).text, "lxml")
                if Counter == 1:
                    List = NewContent.find_all("div", attrs={"class": "novel_list"})[1].find("dl").find_all("a")
                else:
                    List = NewContent.find_all("div", attrs={"class": "novel_list"})[0].find("dl").find_all("a")
            except Exception:
                cls.__Logger.warning(f"解析{NewUrl}的内容失败。")
                traceback.print_exc()
                continue
            for i in List:
                Data = (i.text, "https://www.rmxsba.com" + i["href"])
                yield Data
                # Buffer.append(Data)
        # return Buffer

    @classmethod
    def GetText(cls, Response: NetWork) -> str:
        try:
            Result = str(Response.Bs.find("div", attrs={"class": "content"}))
        except Exception:
            cls.__Logger.warning(f"解析{Response.Url}的内容失败。")
            traceback.print_exc()
            return ""
        Text = Result.split("\n")[2:]
        Buffer = ""
        for i in Text:
            text = "\t" + i.replace("<br/>", "").replace(" ", "").replace("\xa0", "") + "\n"
            Buffer = Buffer + text
        Buffer = Buffer.split("<p>")[0]
        return Buffer

    @classmethod
    def GetInfo(cls, Response: NetWork) -> dict:
        Buffer = {"BookName": Response.Bs.find("h1").text}
        Result = cls.Finder_2.search(Response.Bs.find("div", attrs={"class": "caption"}).text).group(1).strip(" ")
        Buffer["MaxChapterNumber"] = int(Result)
        return Buffer


class Analyzer2(Analyzer):
    Finder_1 = re.compile("<div.*?>.*?</div>")
    __Logger = logging.getLogger(__name__ + ".Analyzer2")

    @classmethod
    def GetInfo(cls, Content: bs, Source: str) -> dict:
        MaxChapterNumber = len(Content.find("div", attrs={"class": "list_box"}).find_all("li"))
        BookName = Content.find("h1").text
        return {"BookName": BookName, "MaxChapterNumber": MaxChapterNumber}

    @classmethod
    def GetCatalogue(cls, Content: bs, Source: str) -> list:
        AllChapterTag = Content.find("div", attrs={"class": "list_box"}).find_all("a")
        for i in AllChapterTag:
            Data = (i.text.lstrip("正文 "), "http://www.yunxs.com/tianmipengcidashushangehun/" + i.get("href"))
            yield Data

    @classmethod
    def GetText(cls, Content: bs, Source: str) -> str:
        DivText = str(Content.find("div", attrs={"class": "box_box"})).replace("\n", "")
        DivText = DivText[DivText.find(">") + 1: -6]
        Text = cls.Finder_1.split(DivText)[1]
        return Analyzer.TextNormalization(Text)


class Analyzer3(Analyzer):
    Finder_1 = re.compile("<p>.*?</p>")
    __Logger = logging.getLogger(__name__ + ".Analyzer3")

    @classmethod
    def GetInfo(cls, Content: bs, Source: str) -> dict:
        URL = Source.replace(".html", "/list.html")
        Response = requests.get(URL, headers=HEADER)
        HTML = bs(Response.content.decode(chardet.detect(Response.content)["encoding"]), "lxml")
        MaxChapterNumber = len(HTML.find("dl", attrs={"class": "panel-body panel-chapterlist"}).find_all("dd"))
        BookName = Content.find("h1").text
        return {"BookName": BookName, "MaxChapterNumber": MaxChapterNumber}

    @classmethod
    def GetCatalogue(cls, Content: bs, Source: str) -> list:
        URL = Source.replace(".html", "/list.html")
        Response = requests.get(URL, headers=HEADER)
        HTML = bs(Response.content.decode(chardet.detect(Response.content)["encoding"]), "lxml")
        ChapterList = HTML.find("dl", attrs={"class": "panel-body panel-chapterlist"}).find_all("a")
        for i in ChapterList:
            Data = (i.text, "https://www.jingcaiyuedu6.com" + i.get("href"))
            yield Data

    @classmethod
    def GetText(cls, Content: bs, Source: str) -> str:
        DivText = str(Content.find("div", attrs={"id": "htmlContent"})).replace("\r", "").replace("\n", "")
        DivText = DivText[DivText.find(">") + 1: -6]
        Text = cls.Finder_1.split(DivText)[1]
        Text = Analyzer.TextNormalization(Text)
        Text = "".join(Text.split("\r\n")[2:])
        return Text


class Analyzer4(Analyzer):
    __Logger = logging.getLogger(__name__ + ".Analyzer4")

    @classmethod
    def GetInfo(cls, Response: NetWork) -> dict:
        return Analyzer.FindInfo(Response, {"id": "list"})

    @classmethod
    def GetCatalogue(cls, Response: NetWork) -> list:
        for i in Analyzer.FindChapterList(Response, {"id": "list"}):
            yield i

    @classmethod
    def GetText(cls, Response: NetWork) -> str:
        return Analyzer.TextNormalization(Analyzer.FindText(Response, {"id": "content"}))


class Analyzer5(Analyzer):
    @classmethod
    def GetInfo(cls, Response: NetWork) -> dict:
        MaxChapterNumber = len(Response.Bs.find("ul", attrs={"id": "booklist"}).find_all("a"))
        BookName = str(Response.Bs.find("h1"))
        BookName = BookName[BookName.find(">")+1:-5]
        BookName = BookName[:BookName.find("<")].rstrip(" ")
        return {"BookName": BookName, "MaxChapterNumber": MaxChapterNumber}

    @classmethod
    def GetCatalogue(cls, Response: NetWork) -> list:
        for i in Analyzer.FindChapterList(Response, {"id": "booklist"}, "ul"):
            yield i

    @classmethod
    def GetText(cls, Response: NetWork) -> str:
        return Analyzer.TextNormalization(Analyzer.FindText(Response, {"id": "content"}))


class Analyzer6(Analyzer):
    @classmethod
    def GetInfo(cls, Response: NetWork) -> dict:
        return Analyzer.FindInfo(Response, {"class": "mulu_list"}, "ul")

    @classmethod
    def GetCatalogue(cls, Response: NetWork) -> list:
        for i in Analyzer.FindChapterList(Response, {"class": "mulu_list"}, "ul"):
            yield i

    @classmethod
    def GetText(cls, Response: NetWork) -> str:
        Text = Analyzer.FindText(Response, {"id": "htmlContent"})
        Text = Analyzer.TextNormalization(Text)
        return "\r\n".join(Text.split("\r\n")[1:])


class Analyzer7(Analyzer):
    Finder_1 = re.compile("<div.*?>.*?</div>")
    @classmethod
    def GetInfo(cls, Response: NetWork) -> dict:
        return Analyzer.FindInfo(Response, {"class": "novel_list"})

    @classmethod
    def GetCatalogue(cls, Response: NetWork) -> list:
        return Analyzer.FindChapterList(Response, {"class": "novel_list"})

    @classmethod
    def GetText(cls, Response: NetWork) -> str:
        Text = Analyzer.FindText(Response, {"id": "content"})
        Text = cls.Finder_1.split(Text)[1]
        Text = Analyzer.TextNormalization(Text)
        return Text


class Analyzer8(Analyzer):
    Finder_1 = re.compile("<p>.*?</p>")

    @classmethod
    def GetInfo(cls, Response: NetWork) -> dict:
        return Analyzer.FindInfo(Response, {"class": "novel_list"})

    @classmethod
    def GetCatalogue(cls, Response: NetWork) -> list:
        return Analyzer.FindChapterList(Response, {"class": "novel_list"})

    @classmethod
    def GetText(cls, Response: NetWork) -> str:
        Text = Analyzer.FindText(Response, {"class": "content"})
        Text = cls.Finder_1.split(Text)[0]
        Text = Analyzer.TextNormalization(Text)
        return "".join(Text.split("\r\n")[1:])


class Analyzer9(Analyzer):
    Finder_1 = re.compile("<p.*?>.*?</p>")

    @classmethod
    def GetInfo(cls, Response: NetWork) -> dict:
        a = Analyzer.FindInfo(Response, {"class": "pc_list"}, "div", 1)
        return Analyzer.FindInfo(Response, {"class": "pc_list"}, "div", 1)

    @classmethod
    def GetCatalogue(cls, Response: NetWork) -> list:
        return Analyzer.FindChapterList(Response, {"class": "pc_list"}, "div", 1)

    @classmethod
    def GetText(cls, Response: NetWork) -> str:
        Text = Analyzer.FindText(Response, {"id": "content1"})
        Text = cls.Finder_1.split(Text)[1]
        Text = Analyzer.TextNormalization(Text)
        Text = "\r\n".join(["\t"+i for i in Text.split("\r\n")])
        return Text


class Analyzer10(Analyzer):
    Finder_1 = re.compile("<div.*?>.*?</div>")

    @classmethod
    def GetInfo(cls, Response: NetWork) -> dict:
        return Analyzer.FindInfo(Response, {"class": "showInfo"}, "div", 1)

    @classmethod
    def GetCatalogue(cls, Response: NetWork) -> list:
        return Analyzer.FindChapterList(Response, {"class": "showInfo"}, "div", 1)

    @classmethod
    def GetText(cls, Response: NetWork) -> str:
        Text = Analyzer.FindText(Response, {"id": "content"})
        Text = cls.Finder_1.split(Text)[1]
        Text = Analyzer.TextNormalization(Text)
        return "".join(Text.split("\r\n")[:-1])


class Analyzer11(Analyzer):
    Finder_1 = re.compile("<dt>.*?</dt>")
    Finder_2 = re.compile("<div.*?>.*?</div>")
    Finder_3 = re.compile("<script>.*?</script>")

    @classmethod
    def GetInfo(cls, Response: NetWork) -> dict:
        Response.SetEncoding("GBK")
        HTML = Response.Bs
        ListText = str(HTML.find("div", attrs={"class": "listmain"}).find("dl")).lstrip("<dl>").rstrip("</dl>")
        List = bs(cls.Finder_1.split(ListText)[2], "lxml").find_all("dd")
        return {"BookName": HTML.find("h1").text, "MaxChapterNumber": len(List)}

    @classmethod
    def GetCatalogue(cls, Response: NetWork) -> list:
        Response.SetEncoding("GBK")
        HTML = Response.Bs
        ListText = str(HTML.find("div", attrs={"class": "listmain"}).find("dl")).lstrip("<dl>").rstrip("</dl>")
        List = bs(cls.Finder_1.split(ListText)[2], "lxml").find_all("a")
        for i in List:
            Data = (i.text, Response.GetNextUrl(i.get("href")))
            yield Data

    @classmethod
    def GetText(cls, Response: NetWork) -> str:
        Response.SetEncoding("GBK")
        Text = Analyzer.FindText(Response, {"id": "content"})
        Text = cls.Finder_2.split(Text)[1].replace("\r", "")\
            .replace("<br/>", "\n").replace("\xa0", " ")\
            .replace("    ", "\t").replace("\t\t", "\t").replace(" ", "").replace("\n\n", "\n")
        Text = cls.Finder_3.split(Text)[0]
        return Text.rstrip("\n")



MAP = {
    "www.rmxsba.com": Analyzer1,
    "www.yunxs.com": Analyzer2,
    "www.jingcaiyuedu6.com": Analyzer3,
    "www.81zw.com": Analyzer4,
    "www.biquwx.la": Analyzer4,
    "www.luoxiabook.com": Analyzer5,
    "www.yueshuxsw.com": Analyzer6,
    "www.xfjxs.com": Analyzer7,
    "www.kubiji.net": Analyzer8,
    "www.kankezw.com": Analyzer9,
    "www.wurexs.com": Analyzer10,
    "www.zhhtxt.com": Analyzer11
}

