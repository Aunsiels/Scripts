""" Some stats on the dataset """

import os

CATEGORIES = dict()
L_TITLE = 0
L_SNIPPET = 0
L_ARTICLE = 0
# When we know that it is hand written
L_SNIPPET_SUM = 0
N_SNIPPET_SUM = 0

def compute_text(file_name):
    """compute_text Update stats for a given text

    :param file_name: path to the file to compute
    """
    f_text = open(file_name, "r", encoding="utf-16")
    is_category = False
    is_title = False
    is_snippet = False
    is_article = False
    is_nsnippets = False
    nsnippets = 0
    l_t = 0
    l_s = 0
    l_a = 0
    category = ""
    for i in f_text:
        if "<category>" in i:
            is_category = True
        elif "<\\category>" in i:
            is_category = False
        elif "<title>" in i:
            is_title = True
        elif "<\\title>" in i:
            is_title = False
        elif "<snippet>" in i:
            is_snippet = True
        elif "<\\snippet>" in i:
            is_snippet = False
        elif "<article>" in i:
            is_article = True
        elif "<\\article>" in i:
            is_article = False
        elif "<nsnippets>" in i:
            is_article = True
        elif "<\\nsnippets>" in i:
            is_article = False
        else:
            if is_category:
                category = i
            elif is_title:
                l_t += len(i)
            elif is_snippet:
                l_s += len(i)
            elif is_article:
                l_a += len(i)
            elif is_nsnippets:
                nsnippets = int(i)
    f_text.close()
    return [category, l_t, l_s, l_a, nsnippets]

FILES = os.listdir("./20minutes")
for f_name in FILES:
    res = compute_text("./20minutes/" + f_name)
    if res[0] in CATEGORIES:
        CATEGORIES[res[0]] += 1
    else:
        CATEGORIES[res[0]] = 1
    L_TITLE += res[1]
    L_SNIPPET += res[2]
    L_ARTICLE += res[3]
    if res[4] > 0:
        N_SNIPPET_SUM += 1
        L_SNIPPET_SUM += res[2]

print("The corpus contains ", len(FILES), " articles")
print("The mean size of the titles is ", L_TITLE / len(FILES), " bytes.")
print("The mean size of the snippets is ", L_SNIPPET / len(FILES), " bytes.")
print("There are ", N_SNIPPET_SUM, " snippets which are hand written (",
      N_SNIPPET_SUM / len(FILES) * 100, "%).")
print("The mean size of hand written snippets is ", L_SNIPPET_SUM / N_SNIPPET_SUM, " bytes.")
print("The mean size of the articles is ", L_ARTICLE / len(FILES), " bytes.")
print("There are ", len(CATEGORIES), "categories, which are:")
print(" ".join(CATEGORIES))
