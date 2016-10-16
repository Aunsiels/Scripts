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
