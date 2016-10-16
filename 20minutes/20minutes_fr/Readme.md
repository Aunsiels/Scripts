### Description

Script to download articles from the 20minutes website.

### How to use

Simply run:
```
python minutes.py
```

and follow the instructions.

### Balises

**category**: The category of the article on the website
**title**: The title of the article.
**snippet**: A short description of the article which can be used as a summary.
**article**: The actual article.

### TODO

* Remove duplicates. For now just use:
```
fdupes -d -N 20minutes/
```
### Use Cases

* Summarization using title and snippet
* Classification using the categories

### Getting Informations on the Dataset

Run:
```
python stats.py
```

### Results 2013-2016

The corpus contains  181062  articles
The mean size of the titles is  73.11135964476257  bytes.
The mean size of the snippets is  101.88879499839834  bytes.
The mean size of the articles is  1947.3565132385593  bytes.
There are  37 categories, which are:
Médias   1826
Elections   1703
Nice   2330
Vous interviewez   214
T'as vu ?   8538
Monde   19092
Sport   26640
Montpellier   3122
Web   1505
People   2796
France   260
Livres   2890
Bordeaux   5064
Automobile   189
Société   25276
Politique   8817
Gourmandises   354
Lyon   5931
Nantes   5592
Paris   4291
Toulouse   6037
Strasbourg   5332
Marseille   5093
Emploi   15
High-Tech   4479
Cinéma   4395
Santé   2596
Culture   6052
Planète   2182
Economie   1
Style   842
Rennes   4890
   21
Grenoble   535
Télévision   5325
Sciences   1404
Lille   5433

