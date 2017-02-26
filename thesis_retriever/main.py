from retrieve_page import PageRetriever
from edite_html_parser import EDITEHTMLParser
import pickle

def process(url, name, parser):
    page_retriever = PageRetriever(url)
    h_test = page_retriever.read()
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

# EDITE of Paris

process("https://edite-de-paris.fr/spip/spip.php?page=phdproposals", \
        "edite", \
        EDITEHTMLParser())
