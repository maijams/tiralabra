# Määrittelydokumentti

**Opinto-ohjelma**: Tietojenkäsittelytieteen kandidaatti 

**Projektissa käytettävä ohjelmointikieli**: Python

**Vertaisarviointiin soveltuvat kielet**: Python

**Dokumentaation kieli**: suomi


## Aihe

Harjoitustyön aiheena on eri reitinhakualgoritmien vertailu lyhimmän reitin löytämiseksi kartassa. Kartat ovat käsin piirrettyjä musta-valkokarttoja (PNG-kuvia). Reitinhakujen visualisointiin ja algoritmien toiminnan varmentamiseksi ohjelmalla on graafinen käyttöliittymä.

## Käytettävät algoritmit ja tietorakenteet

Reitinhakuvertailu suoritetaan Dijkstran, A*:n ja JPS:n (Jump Point Search) välillä. Tiedon tallennuksessa käytetään matriisia ja algoritmien suorituksen yhteydessä prioriteettijonoa.

## Aika- ja tilavaativuudet

Dijkstran algoritmin aikavaativuus on O(E+V log V), jossa V on solmujen määrä ja E solmujen välillä olevien kaarien määrä. Tilavaatimus on O(V), kun kukin solmu lisätään prioriteettijonoon maksimissaan yhden kerran.

A* pahimman tapauksen aikavaativuus on O(E), jossa E on verkossa olevien kaarien lukumäärä. Tilavaativuus on Dijkstran tavoin O(V).

JPS aikavaativuus on O(b^d), jossa b on verkon solmujen määrä ja d on polun pituus. Tilavaativuus O(V).

## Lähteet

- https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
- https://en.wikipedia.org/wiki/A*_search_algorithm
- https://encyclopedia.pub/entry/24246