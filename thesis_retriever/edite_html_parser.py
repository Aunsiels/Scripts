from html_thesis_parser import HTMLThesisParser
from thesis import Thesis
import re

HEAD_EDITE = "https://edite-de-paris.fr"
SPACE_RE = re.compile("[\s\\n\\r]")

class EDITEHTMLParser(HTMLThesisParser):
    """EDITEHTMLParser"""

    def __init__(self):
        super(EDITEHTMLParser, self).__init__()
        self.state = 0
        self.div_counter = 0
        self.description = ""
        self.name = ""
        self.entity = ""


    def reset_parameters(self):
        super(EDITEHTMLParser, self).reset_parameters()
        self.state = 0
        self.div_counter = 0
        self.description = ""
        self.name = ""
        self.entity = ""

    def handle_starttag(self, tag, attrs):
        if tag == "div":
            for attr in attrs:
                if attr[1] == "contenu" and self.state == 0:
                    self.state = 1
            if self.state > 0:
                self.div_counter += 1
        if tag == "li" and self.state == 1:
            self.state = 2
        if tag == "a":
            if self.state == 2:
                self.state = 3
            elif self.state == 5:
                self.state = 6
                for attr in attrs:
                    if attr[0] == "href":
                        self.description = HEAD_EDITE + attr[1]
        if tag == "span":
            if self.state == 3:
                self.state = 4
            elif self.state == 4:
                self.state = 5

    def handle_endtag(self, tag):
        if tag == "div" and self.state > 0:
            self.div_counter -= 1
            if self.div_counter < 0:
                self.state = 0
                self.div_counter = 0
        if tag == "a" and self.state == 6:
            self.state = 1
            self.thesis.add(Thesis(self.name, self.description, self.entity))
            self.name = ""
            self.description = ""
            self.entity = ""

    def handle_data(self, data):
        if self.state == 4:
            self.entity += SPACE_RE.sub("", data)
        elif self.state == 5:
            self.entity = self.entity + " " + SPACE_RE.sub("", data)
        elif self.state == 6:
            self.name = data
