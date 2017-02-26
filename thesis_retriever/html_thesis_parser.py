"""Parse a HTML Page"""

from html.parser import HTMLParser

class HTMLThesisParser(HTMLParser):
    """HTMLThesisParser"""

    def __init__(self):
        super(HTMLThesisParser, self).__init__()
        self.reset_parameters()

    def reset_parameters(self):
        self.thesis = set()

    def get_thesis_list(self, html):
        """get_thesis_list

        :param html:
        """
        self.reset_parameters()
        self.feed(str(html))
        return self.thesis

    def error(self, message):
        print("An error occured while parsing date or text.", message)

    def handle_starttag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass
