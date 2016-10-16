### Description

Script to download articles from the 20minutos.es website.

### How to use

Simply run:
```
python es_minutos.py
```

and follow the instructions.

### Balises

**category**: The category of the article on the website

**title**: The title of the article.

**nsnippets**: The number of items in the snippet. See on [20 minutos](http://www.20minutos.es/noticia/2863500/0/trabajadores-cobran-menos-300-euros-aumentan-crisis/) to see what it looks like. If 0, it means that the snippet is the same as the beginning of the article.

**snippet**: A short description of the article which can be used as a summary.

**article**: The actual article.

### TODO

* Remove duplicates. For now just use:
```
fdupes -d -N 20minutos/
```
* Some erros occur when there is a unicode caracter. For now, do nothing with it.

### Use Cases

* Summarization using title and snippet
* Classification using the categories

### Getting Informations on the Dataset

Run:
```
python stats.py
```
