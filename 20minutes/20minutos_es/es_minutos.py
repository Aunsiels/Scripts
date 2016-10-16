""" This module allows you to retrieve artcles from the 20minutos website
It was adapted from the french version of the website"""

#!/usr/bin/env python3

import sys
import os
import getopt
import urllib.request
from html.parser import HTMLParser
from threading import Thread
from threading import Lock
import html2text

RAWURL = "http://www.20minutos.es"
RAWURLARCHIVE = "http://www.20minutos.es/archivo/"

# Possible categories
CATEGORIES = set(['almería',
                  'burgos',
                  'ceuta',
                  'pintor de dinero',
                  'lugo',
                  'girona',
                  'vivienda y hogar',
                  'santiago de compostela',
                  'toledo',
                  'pamplona',
                  'león',
                  'madrid',
                  'música',
                  'cine',
                  'granada',
                  'nacional',
                  'san sebastián',
                  'ávila',
                  'guadalajara',
                  'huelva',
                  'logroño',
                  'economía',
                  'lleida',
                  'cádiz',
                  'eclipse de sol',
                  'albacete',
                  'huesca',
                  'deportes',
                  'palencia',
                  'zaragoza',
                  'motor',
                  'gente',
                  'santa cruz de tenerife',
                  'vigo',
                  'marbella',
                  'viajes',
                  'melilla',
                  'zamora',
                  'valladolid',
                  'bilbao',
                  'vitoria',
                  'ciencia',
                  'jaén',
                  'sevilla',
                  'teruel',
                  'murcia',
                  'badajoz',
                  'salud',
                  'córdoba',
                  'artrend',
                  'libros',
                  'ciudad real',
                  'pontevedra',
                  'cuenca',
                  'televisión',
                  'jerez de la frontera',
                  'gijón',
                  'cartagena',
                  'formación y empleo',
                  'tarragona',
                  'santander',
                  'cáceres',
                  'salamanca',
                  'fotos y ocio',
                  'alicante',
                  'a coruña',
                  'tecnología',
                  'soria',
                  'oviedo',
                  'artistas y maniquíes',
                  'segovia',
                  'elche',
                  'internacional',
                  'valencia',
                  'barcelona',
                  'ourense',
                  'las palmas',
                  'desabotonando la moda',
                  'castellón',
                  'gastro',
                  'palma de mallorca',
                  'málaga'])


def get_html_page(url, tries=3):
    """get_html_page
    This gets the html text of a page
    :param url: the url of the page to retrieve
    :param tries: number of tries to get a page
    """
    try:
        with urllib.request.urlopen(url) as response:
            html = response.read()
    except urllib.error.HTTPError:
        print("Problem with the url : ", url, ". Cannot get the page.")
        if tries == 0:
            exit()
        else:
            return get_html_page(url, tries - 1)
    return html.decode("iso-8859-1")

# pylint: disable=too-many-instance-attributes
class TextHTMLParser(HTMLParser):
    """TextHTMLParser : finds text inside a html document"""

    def __init__(self):
        super(TextHTMLParser, self).__init__()
        self.found = False
        self.counter = 0
        self.text = []
        self.paragraph = False
        self.is_title = False
        self.title = []
        self.is_snippet = False
        self.snippet = []
        self.is_cat = False
        self.cat = []
        self.n_snippets = 0

    def error(self, message):
        print("An error occured while parsing text.", message)

    def handle_starttag(self, tag, attrs):
        has_attribute = False
        for attr in attrs:
            has_attribute = True
            if tag == "div" and attr[0] == "class" and attr[1] == "article-content":
                self.found = True
                self.counter = 0
            if tag == "div" and attr[0] == "class" and attr[1] == "lead":
                self.is_snippet = True
            if tag == "h1" and attr[0] == "class" and attr[1] == "article-title":
                self.is_title = True
            if tag == "h2" and attr[0] == "class" and attr[1] == "section-name":
                self.is_cat = True
        if self.found and tag == "div":
            self.counter += 1
        if self.found and (tag == "p" or tag == "h2"):
            self.paragraph = not has_attribute
        if self.is_snippet and tag == "li":
            self.n_snippets += 1
    def handle_endtag(self, tag):
        if self.found and tag == "div":
            self.counter -= 1
        if self.counter == 0 and self.found:
            self.found = False
        if tag == "p" or tag == "h2":
            self.paragraph = False
        if tag == "div":
            self.is_snippet = False
        if tag == "h1":
            self.is_title = False
        if tag == "h2":
            self.is_cat = False
    def handle_data(self, data):
        if self.found and self.paragraph:
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
    return (" ".join(parser.cat), " ".join(parser.title),
            " ".join(parser.snippet), " ".join(parser.text),
            parser.n_snippets)

class LinkHTMLParser(HTMLParser):
    """LinkHTMLParser Finds all articles links in a page"""

    def __init__(self, categories):
        super(LinkHTMLParser, self).__init__()
        self.links = []
        self.categories = categories
        """Values for state :
            0 : Not in the url list
            1 : Wait for the beginning of a category list
            2 : Check the categories
            3 : Record links
            4 : Not the right category
        """
        self.state = 0
        self.ul_counter = 0

    def error(self, message):
        print("An error occured while parsing links.", message)

    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if self.state == 0 and tag == "ul" and attr[0] == "class" and "normal-list" in attr[1]:
                self.state = 1
            if self.state == 3 and tag == "a" and attr[0] == "href":
                self.links.append(attr[1])
        if self.state != 0 and tag == "ul":
            self.ul_counter += 1
        elif self.state == 1 and tag == "li":
            self.state = 2

    def handle_endtag(self, tag):
        if self.state != 0 and tag == "ul":
            self.ul_counter -= 1
        if self.ul_counter == 0:
            self.state = 0
        if (self.state == 4 or self.state == 3) and tag == "ul":
            self.state = 1

    def handle_data(self, data):
        if self.state == 2:
            data_low = data.lower()
            found_cat = (len(self.categories) == 0)
            for cat in self.categories:
                if cat in data_low:
                    found_cat = True
            if found_cat:
                self.state = 3
            else:
                self.state = 4

def find_url_links(html, categories):
    """find_url_links
    Finds the urls in an article and returns a list of links
    :param html: the html page where urls can be found
    :param categories: Wanted categories
    """
    parser = LinkHTMLParser(categories)
    parser.feed(str(html))
    return parser.links

LOCK = Lock()

def write_page(url, number, date):
    """write_page
    Write the text in a html page in a file.
    The file name is composed of the date and a number.
    :param url: The url where the page can be found
    :param number: A number to make files unique
    :param date: Date of the article
    """
    html = get_html_page(url)
    cat, title, snippet, text, n_snippets = find_text_page(html)
    text = html2text.html2text(text).replace("\\n", " ")
    text = text.replace("\\r", "").replace("\n", " ").replace("\u2014", " ")
    title = html2text.html2text(title).replace("\\n", " ")
    title = title.replace("\\r", "").replace("\n", " ").replace("\u2014", " ")
    snippet = html2text.html2text(snippet).replace("\\n", " ")
    snippet = snippet.replace("\\r", "").replace("\n", " ").replace("\u2014", " ")
    cat = html2text.html2text(cat).replace("\\n", " ")
    cat = cat.replace("\\r", "").replace("\n", " ").replace("\u2014", " ")
    print("Writing file number ", str(number).zfill(3), url)
    fstream = open("20minutos/"+date+"-"+str(number).zfill(3), "w", encoding="ISO-8859-1")
    fstream.write("<category>\n")
    fstream.write(cat)
    fstream.write("\n<\\category>\n")
    fstream.write("<title>\n")
    fstream.write(title)
    fstream.write("\n<\\title>\n")
    fstream.write("<nsnippets>\n")
    fstream.write(str(n_snippets))
    fstream.write("\n<\\nsnippets>\n")
    fstream.write("<snippet>\n")
    fstream.write(snippet)
    fstream.write("\n<\\snippet>\n")
    fstream.write("<article>\n")
    fstream.write(text)
    fstream.write("\n<\\article>")
    fstream.close()

    #print("Writing file number ", str(number).zfill(3), url)
    #fstream = open("20minutos/"+date+"-"+str(number).zfill(3), "w", encoding="ISO-8859-1")
    #text_final = html2text.html2text(text).replace("\\n", " ").replace("\\r", " ")
    #text_final = text_final.replace("\r", " ").replace("\n", " ").replace("\u2014", " ")
    #fstream.write(text_final)
    #fstream.close()

def write_page_date(date, categories):
    """write_page_date
    Write all the articles for a given date in files
    :param date: the date as a string, format is "01-janvier-2015"
    :param categories: Wanted categories
    """
    print("Preparing to get all archives from ", date)
    html = get_html_page(RAWURLARCHIVE+date)
    links = find_url_links(html, categories)
    print("Found", len(links), "links")
    index = 0
    l_thd = []
    date_transform = date.replace("/", "-")
    for url in links:
        thd = Thread(target=write_page, args=(url, index, date_transform,))
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
                dates.append(str(current_year)+"/"+str(current_month)+"/"+str(i))
        current_month += 1
        if current_month == 13:
            current_year += 1
            current_month = 1
    for i in cal.itermonthdays(current_year, current_month):
        if i != 0:
            dates.append(str(current_year)+"/"+str(current_month)+"/"+str(i))
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

    if not os.path.exists("20minutos"):
        os.mkdir("20minutos")

    get_pages_from_dates(YEARS, MONTHSTART, YEARE, MONTHE, CATS)
    print("All articles have been retrieve with success. Enjoy ;)")
