from retrieve_page import PageRetriever
from edite_html_parser import EDITEHTMLParser
from inria_html_parser import INRIAHTMLParser
import pickle
from contextlib import closing
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait

def process(url, name, parser):
    print("Get Page for", name)
    page_retriever = PageRetriever(url)
    h_test = page_retriever.read()
    print("Parse")
    l_edite = parser.get_thesis_list(h_test)
    try:
        with open(name + ".pickle", "rb") as f_open:
            previous_thesis = pickle.load(f_open)
    except FileNotFoundError:
        previous_thesis = set()
    with open(name + ".pickle", "wb") as f_open:
        pickle.dump(previous_thesis.union(l_edite), f_open)
    for thesis in l_edite - previous_thesis:
        print(thesis)
    print(len(l_edite - previous_thesis), "new thesis proposal for", name)

def process2(url, name, parser):
    # They have JS in the page...
    print("Get Page for", name)
    browser = Firefox()
    browser.get(url)
    h_test = browser.page_source
    browser.quit()
    print("Parse")
    l_edite = parser.get_thesis_list(h_test)
    try:
        with open(name + ".pickle", "rb") as f_open:
            previous_thesis = pickle.load(f_open)
    except FileNotFoundError:
        previous_thesis = set()
    with open(name + ".pickle", "wb") as f_open:
        pickle.dump(previous_thesis.union(l_edite), f_open)
    for thesis in l_edite - previous_thesis:
        print(thesis)
    print(len(l_edite - previous_thesis), "new thesis proposal for", name)
    print(len(previous_thesis), "previously")
    print(len(l_edite), "found")
# EDITE of Paris

process("https://edite-de-paris.fr/spip/spip.php?page=phdproposals", \
                "edite", \
        EDITEHTMLParser())

# INRIA

process2("https://www.inria.fr/institut/recrutement-metiers/offres/doctorants/doctorants?page=/institut/recrutement-metiers/offres/doctorants/doctorants/(view)/details.html&id=PGTFK026203F3VBQB6G68LONZ&LOV5=4509&LG=FR&Resultsperpage=1000&pagenum=1&option=52&sort=DESC",
         "inria",
         INRIAHTMLParser())
