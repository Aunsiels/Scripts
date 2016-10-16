""" This module allows you to retrieve artcles from the 20minutes website """

#!/usr/bin/env python3

import sys
import os
import getopt
import urllib.request
from html.parser import HTMLParser
from threading import Thread
from threading import Lock
import html2text

RAWURL = "http://www.20minutes.fr"
RAWURLARCHIVE = "http://www.20minutes.fr/archives/"
MONTHS = ["",
          "janvier",
          "fevrier",
          "mars",
          "avril",
          "mai",
          "juin",
          "juillet",
          "aout",
          "septembre",
          "octobre",
          "novembre",
          "decembre"]

# Possible categories
CATEGORIES = set(['montpellier',
                  'marseille',
                  'sciences',
                  'nice',
                  'high-tech',
                  'culture',
                  'web',
                  'insolite',
                  'france',
                  'mode',
                  'monde',
                  'economie',
                  'cinema',
                  'paris',
                  'sante',
                  'gastronomie',
                  'lille',
                  'toulouse',
                  'archives',
                  'television',
                  'politique',
                  'livres',
                  'societe',
                  'planete',
                  'strasbourg',
                  'sport',
                  'bordeaux',
                  'lyon',
                  'nantes',
                  'article',
                  'people',
                  'rennes',
                  'medias',
                  'elections'])


def get_categorie(url):
    """get_categorie
    Get the categorie of the article at a given url
    :param url: URL of the article
    """
    cat = []
    count = len(RAWURL) + 1
    while count < len(url) and url[count] != "/":
        cat.append(url[count])
        count += 1
    return "".join(cat)

def get_html_page(url, tries=3):
    """get_html_page
    This gets the html text of a page
    :param url: the url of the page to retrieve
    :param tries: number of tries to get a page
    """
    print(url)
    try:
        with urllib.request.urlopen(url) as response:
            html = response.read()
    except urllib.error.HTTPError:
        print("Problem with the url : ", url, ". Cannot get the page.")
        if tries == 0:
            exit()
        else:
            return get_html_page(url, tries - 1)
    return html.decode("utf-8")

class TextHTMLParser(HTMLParser):
    """TextHTMLParser : finds text and date inside a html document"""

    def __init__(self):
        super(TextHTMLParser, self).__init__()
        self.found = False
        self.counter = 0
        self.text = []
        self.date = None
        self.paragraph = False
        self.buzz = False
        self.is_title = False
        self.title = []
        self.is_snippet = False
        self.snippet = []
        self.is_cat = False
        self.cat = []

    def error(self, message):
        print("An error occured while parsing date or text.", message)

    def handle_starttag(self, tag, attrs):
        has_attribute = False
        for attr in attrs:
            has_attribute = True
            if self.found and attr[0] == "datetime" and self.date is None:
                self.date = attr[1]
            if attr[0] == "role" and attr[1] == "main":
                self.found = True
                self.counter = 0
            if self.found and attr[0] == "class" and attr[1] == "buzz-title":
                self.buzz = True
            if tag == "h1" and attr[0] == "itemprop" and attr[1] == "headline":
                self.is_title = True
            if tag == "span" and attr[0] == "class" and attr[1] == "hat-summary":
                self.is_snippet = True
            if tag == "span" and attr[0] == "class" and attr[1] == "content":
                self.is_cat = True
        if self.found and tag == "div":
            self.counter += 1
        if self.found and (tag == "p" or tag == "h3"):
            self.paragraph = not has_attribute
    def handle_endtag(self, tag):
        if self.found and tag == "div":
            self.counter -= 1
        if self.counter == 0 and self.found:
            self.found = False
        if tag == "p" or tag == "h3":
            self.paragraph = False
        if tag == "h1":
            self.is_title = False
        elif tag == "span":
            self.is_snippet = False
            self.is_cat = False
    def handle_data(self, data):
        if self.found and self.paragraph and not self.buzz:
            self.text.append(data)
        elif self.is_title:
            self.title.append(data)
        elif self.is_snippet:
            self.snippet.append(data)
        elif self.is_cat:
            self.cat.append(data)

def find_text_page(html):
    """find_text_page
    Finds text part of an article page and returns the text
    :param html: the html of the article page
    """
    parser = TextHTMLParser()
    parser.feed(str(html))
    return " ".join(parser.cat), " ".join(parser.title), " ".join(parser.snippet), " ".join(parser.text)

def find_date_page(html):
    """find_date_page
    Finds date in an article page and returns the date
    :param html: the html of the article page
    """
    parser = TextHTMLParser()
    parser.feed(str(html))
    return parser.date

class LinkHTMLParser(HTMLParser):
    """LinkHTMLParser Finds all articles links in a page"""

    def __init__(self):
        super(LinkHTMLParser, self).__init__()
        self.found = False
        self.links = []

    def error(self, message):
        print("An error occured while parsing links.", message)

    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if tag == "li" and attr[0] == "class" and "mn-item" in attr[1]:
                self.found = True
            if self.found and tag == "a" and attr[0] == "href":
                self.found = False
                self.links.append(RAWURL+attr[1])

def find_url_links(html):
    """find_url_links
    Finds the urls in an article and returns a list of links
    :param html: the html page where urls can be found
    """
    parser = LinkHTMLParser()
    parser.feed(str(html))
    return parser.links

LOCK = Lock()

def write_page(url, number):
    """write_page
    Write the text in a html page in a file.
    The file name is composed of the date and a number.
    :param url: The url where the page can be found
    :param number: A number to make files unique
    """
    html = get_html_page(url)
    date = find_date_page(html)
    if date:
        cat, title, snippet, text = find_text_page(html)
        text = html2text.html2text(text).replace("\\n", " ")
        text = text.replace("\\r", "").replace("\n", " ")
        title = html2text.html2text(title).replace("\\n", " ")
        title = title.replace("\\r", "").replace("\n", " ")
        snippet = html2text.html2text(snippet).replace("\\n", " ")
        snippet = snippet.replace("\\r", "").replace("\n", " ")
        cat = html2text.html2text(cat).replace("\\n", " ")
        cat = cat.replace("\\r", "").replace("\n", " ")
        print("Writing file number ", str(number).zfill(3), url)
        fstream = open("20minutes/"+date+"-"+str(number).zfill(3), "w", encoding="utf-16")
        fstream.write("<category>\n")
        fstream.write(cat)
        fstream.write("\n<\\category>\n")
        fstream.write("<title>\n")
        fstream.write(title)
        fstream.write("\n<\\title>\n")
        fstream.write("<snippet>\n")
        fstream.write(snippet)
        fstream.write("\n<\\snippet>\n")
        fstream.write("<article>\n")
        fstream.write(text)
        fstream.write("\n<\\article>")
        fstream.close()

def contains_categorie(url, categories):
    """contains_categorie
    Check that the url contains at least one categorie
    :param url: The URL to check
    :param categories: list of categories
    """
    begin_index = len(RAWURL) + 1
    for cat in categories:
        if cat in url[begin_index:begin_index+len(cat)]:
            return True
    return len(categories) == 0

def write_page_date(date, categories):
    """write_page_date
    Write all the articles for a given date in files
    :param date: the date as a string, format is "01-janvier-2015"
    :param categories: Wanted categories
    """
    print("Preparing to get all archives from ", date)
    html = get_html_page(RAWURLARCHIVE+date)
    links = find_url_links(html)
    print("Found", len(links), "links")
    index = 0
    l_thd = []
    for url in links:
        if not contains_categorie(url, categories):
            continue
        thd = Thread(target=write_page, args=(url, index,))
        l_thd.append(thd)
        thd.start()
        index += 1
        if index%40 == 0:
            for thd in l_thd:
                thd.join()
            l_thd = []
    for thd in l_thd:
        thd.join()

def get_all_dates(year_start, month_start, year_end, month_end):
    """get_all_dates
    Get all the dates between two dates.
    :param year_start: The starting year
    :param month_start: The starting month
    :param year_end: The ending year
    :param month_end: The ending month
    """
    assert (year_start < year_end or year_start == year_end and
            month_start <= month_end), "Start date before end date"
    import calendar
    cal = calendar.TextCalendar()
    current_year = year_start
    current_month = month_start
    dates = []
    while current_year != year_end or current_month != month_end:
        for i in cal.itermonthdays(current_year, current_month):
            if i != 0:
                dates.append(str(i)+"-"+MONTHS[current_month]+"-"+str(current_year))
        current_month += 1
        if current_month == 13:
            current_year += 1
            current_month = 1
    for i in cal.itermonthdays(current_year, current_month):
        if i != 0:
            dates.append(str(i)+"-"+MONTHS[current_month]+"-"+str(current_year))
    return dates

def get_pages_from_dates(year_start, month_start, year_end, month_end, categories):
    """get_pages_from_dates
    Get all articles between two points in time.
    :param year_start: The starting year
    :param month_start: The starting month
    :param year_end: The ending year
    :param month_end: The ending month
    :param categories: Wanted categories
    """
    assert (year_start < year_end or year_start == year_end and
            month_start <= month_end), "Start date before end date"
    dates = get_all_dates(year_start, month_start, year_end, month_end)
    print("Get all articles from ", dates[0], " to ", dates[-1])
    print("For a total of ", len(dates), " days.")
    for date in dates:
        write_page_date(date, categories)

def usage():
    """usage Print how to use the program"""
    print("To choose the categories you want to use, type -c \"categorie1 categorie2...\"")
    print("Examples of categories :", ", ".join(list(CATEGORIES)))

if __name__ == "__main__":
    CATS = list()
    try:
        OPTS, VALUES = getopt.getopt(sys.argv[1:], 'c:h')
    except getopt.GetoptError:
        usage()
        sys.exit()

    for opt, arg in OPTS:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt == "-c":
            CATS += arg.lower().split(" ")
            print("Choosen categories :", ", ".join(CATS))
        else:
            usage()
            sys.exit()

    print("Welcome to a wonderful program to get articles from 20 minutes :)")
    print("Made with <3 by Julien Romero")
    YEARS = int(input('Please type the starting year : '))
    MONTHSTART = int(input('Please type the starting month : '))
    YEARE = int(input('Please type the ending year : '))
    MONTHE = int(input('Please type the ending month : '))

    if not os.path.exists("20minutes"):
        os.mkdir("20minutes")

    get_pages_from_dates(YEARS, MONTHSTART, YEARE, MONTHE, CATS)
    print("All articles have been retrieve with success. Enjoy ;)")
