from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from parse.models import Article
# import argparse
# import json
# https://news.yahoo.com/rss/
import argparse
import json
import urllib.request
import urllib.request
import re
import sqlite3


class Command(BaseCommand):
    help = 'Parses data from specified website'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str, help=u'Website url')

    def get_image(self, data):
            if "<description>" not in data:
                return ""
            description = re.search("<description>" + ".+" + "</description>", data).group()
            image = description.split("img src=")[1].split('`')[1].split("http")
            return "http" + image[2]

    def change_special_symbols(self, _str):
        _str = _str.replace("&amp;", "&")
        _str = _str.replace("&gt;", ">")
        _str = _str.replace("&lt;", "<")
        _str = _str.replace("'", "`")
        _str = _str.replace('"', "`")
        return _str

    def get_item(self, item, data):
        if item == "image":
            return self.get_image(data)

        open_item = "<" + item + ">"
        close_item = "</" + item + ">"

        if open_item not in data:
            return ""

        tmp = re.search(open_item + ".+" + close_item, data).\
            group().\
            replace(open_item, "").\
            replace(close_item, "")

        return re.sub("<[^>]+>", "", tmp)

    def handle(self, *args, **kwargs):
        help = u'Parse data from specified website'
        website_url = kwargs["url"]

        try:
            response = urllib.request.urlopen(website_url)
        except Exception:
            print("url open error")
            response = None
            exit()

        rss_data = str(response.read())
        draft_items = rss_data.split("<item>")
        item_list = []
        item_amount = len(draft_items)

        item = dict()
        number_of_new_articles = 0
        for i in range(item_amount):
            draft_items[i] = self.change_special_symbols(draft_items[i])
            item["title"] = self.get_item("title", draft_items[i])
            item["description"] = self.get_item("description", draft_items[i])
            if i:
                item["image"] = self.get_item("image", draft_items[i])
            item["link"] = self.get_item("link", draft_items[i])
            item["date"] = self.get_item("pubDate", draft_items[i])
            item_list.append(item)
            item = {}

        parsed_data = item_list[1:]

        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        table_name = "parse_article"

        for item in parsed_data:
            cursor.execute("select * from " + table_name + ";")
            cached_data = cursor.fetchall()

            title_list = list()
            for cached_items in cached_data:
                title_list.append(cached_items[1])

            if item["title"] not in title_list:
                number_of_new_articles += 1
                a = Article(title=item["title"], description=item["description"], image=item["image"], link=item["link"],
                            date=item["date"])
                a.save()

        print("Data was successfully parsed")
        print("Number of new articles : {}".format(number_of_new_articles))
