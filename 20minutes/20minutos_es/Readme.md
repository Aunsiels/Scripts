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

### Results for 2013-2016

The corpus contains  930952  articles
The mean size of the titles is  100.20092335587657  bytes.
The mean size of the snippets is  283.46966546073264  bytes.
There are  207154  snippets which are hand written ( 22.251845422750044 %).
The mean size of hand written snippets is  301.2767892485783  bytes.
The mean size of the articles is  2502.5751413606718  bytes.
There are  80 categories, which are:
Girona   4484
Vizcaya   27371
MÃºsica   2741
   1
La Rioja   27085
Islas Baleares   45948
Teruel   2742
Lugo   2415
Gente   3285
Melilla   1796
Zaragoza   24216
A CoruÃ±a   35513
Soria   2645
Comunidad20   58
Siete por uno - Jaime JimÃ©nez   1
MÃ¡laga   30992
CÃ³rdoba   20138
Ciudad Real   6219
Toledo   31680
CÃ¡diz   17345
LeÃ³n   5108
Tarragona   3677
Ourense   2299
Burgos   4397
Segovia   3562
FormaciÃ³n y empleo   2183
Gastro   136
Navarra   22208
Salamanca   6268
Pontevedra   6878
Ciencia   2007
Salud   3063
Cantabria   41189
Valladolid   38326
Barcelona   7382
Granada   16043
Nacional   18137
Huesca   4004
CÃ¡ceres   5982
JaÃ©n   17209
Deportes   22477
HorÃ³scopo   2
Asturias   37093
EconomÃ­a   4851
Ãlava   6166
Zamora   2324
Viajes   1930
Guadalajara   3916
Motor   1275
Alacant   32
Libros   1654
Artes   2575
TelevisiÃ³n   3420
Las Palmas   16790
Alicante   5139
Murcia   41472
Valencia   41112
ValÃ¨ncia   470
Ceuta   1398
Internacional   19464
Cuenca   3932
Vivienda y hogar   2198
CastellÃ³n   4351
AlmerÃ­a   12492
Madrid   7379
CastellÃ³   17
Huelva   15220
GuipÃºzcoa   6151
Sevilla   103013
Palencia   2322
Santa Cruz de Tenerife   16130
TecnologÃ­a   3038
Ãvila   2275
Cine   3757
Badajoz   28779
Opiniones   473
Redes   345
Videojuegos   9
Lleida   4489
Albacete   4289
