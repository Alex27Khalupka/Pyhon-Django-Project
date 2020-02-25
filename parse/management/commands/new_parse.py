import feedparser
# from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from parse.models import Article
import sqlite3
import re


class Command(BaseCommand):
    help = 'Parses data from specified website'

    def change_special_symbols(self, _str):
        _str = _str.replace("&amp;", "&")
        _str = _str.replace("&gt;", ">")
        _str = _str.replace("&lt;", "<")
        _str = _str.replace("&#39;", "'")
        _str = _str.replace("&quot;", "'")
        return _str

    def get_image(self, data):
        image = data.split("img src=")[1].split('"')[1].split("http")
        return "http" + image[2]

    def get_item(self, item, data):
        if item == "image":
            return self.get_image(data)

        return re.sub("<[^>]+>", "", data)

    def add_arguments(self, parser):
        parser.add_argument('url', type=str, help=u'Website url')

    def handle(self, *args, **kwargs):
        website_url = kwargs["url"]
        d = feedparser.parse(website_url)

        news_list = list()
        parsed_item_amount = 0
        for item in d.entries:
            news = dict()
            parsed_item_amount += 1
            try:
                news["title"] = self.change_special_symbols(item.title_detail.value)
            except Exception:
                news["title"] = "There is no title"
            try:
                news["description"] = self.change_special_symbols(self.get_item("description", item.description))
            except Exception:
                news["description"] = "There is no description"
            try:
                news["link"] = self.change_special_symbols(item.link)
            except Exception:
                news["link"] = "There is no link"
            try:
                news["date"] = self.change_special_symbols(item.published)
            except Exception:
                news["date"] = "There is no date"
            try:
                news["image"] = self.change_special_symbols(self.get_item("image", item.description))
            except Exception:
                news["image"] = "https://images.tenanting.in/property/92af8afdbd7c380570a431c5001662e6.png"

            news_list.append(news)

        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        table_name = "parse_article"
        number_of_new_articles = 0

        cursor.execute("select title from " + table_name + ";")
        cached_data = cursor.fetchall()
        title_list = list()
        for cached_items in cached_data:
            title_list.append(cached_items[0])

        for item in news_list:
            print(item["title"])
            if item["title"] not in title_list:
                number_of_new_articles += 1
                a = Article(title=item["title"], description=item["description"], image=item["image"],
                            link=item["link"], date=item["date"])
                a.save()

        print("Data was successfully parsed")
        print("Number of new articles : {}".format(number_of_new_articles))
