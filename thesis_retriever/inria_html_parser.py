from html_thesis_parser import HTMLThesisParser
from thesis import Thesis
import re

INRIA_HEAD = "https://www.inria.fr"

class INRIAHTMLParser(HTMLThesisParser):

    def __init__(self):
        super(INRIAHTMLParser, self).__init__()
        self.state = 0
        self.description = ""
        self.name = ""
        self.entity = ""


    def reset_parameters(self):
        super(INRIAHTMLParser, self).reset_parameters()
        self.state = 0
        self.description = ""
        self.name = ""
        self.entity = ""

    def handle_starttag(self, tag, attrs):
        if tag == "a0:a":
            for attr in attrs:
                if attr[0] == "title" and attr[1] == "Click here to see the job description":
                    self.state = 1
                    for attr2 in attrs:
                        if attr2[0] == "href":
                            self.description += INRIA_HEAD + attr2[1]


    def handle_endtag(self, tag):
        if tag == "a0:a" and self.state == 1:
            self.state = 0
            self.thesis.add(Thesis(self.name, self.description, self.entity))
            self.description = ""
            self.name = ""
            self.entity = ""

    def handle_data(self, data):
        if self.state == 1:
            self.name = data
