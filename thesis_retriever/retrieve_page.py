""" Retriver of url pages """

import urllib.request
import ssl


class PageRetriever(object):
    """PageRetriever"""

    def __init__(self, url, name=""):
        self.url = url
        self.name = name

    def read(self):
        """read"""
        # This restores the same behavior as before.
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(self.url, context=context) as response:
            return response.read().decode("utf-8")
