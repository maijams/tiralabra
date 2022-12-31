# Testausdokumentti

## Yksikkötestaus

Ohjelmalle on tehty yksikkötestausta algoritmien toiminnan kannalta oleellisiin tiedostoihin. Yksikkötestauksen ulkopuolelle on jätetty käyttöliittymään ja suorituskykymittaukseen liittyvät tiedostot. 

Testikattavuusraportti:
![Screenshot from 2022-12-31 23-59-03](https://user-images.githubusercontent.com/96269683/210156360-efa144bf-f2e1-49ca-bf8f-c3b4ed11a252.png)

Yksikkötestit voi suorittaa projektin virtuaaliympäristössä komennolla:

``` invoke test ```

Yksikkötestien kattavuusraportin saa toistettua komennolla:

``` invoke coverage-report ```

Yksikkötestien tulisi havaita, mikäli algoritmien toiminnassa tapahtuu sellaisia muutoksia jotka vaikuttavat lyhyimmän reitin löytymiseen.

## Empiirinen testaus

Algoritmien toimintaa voi testata graafisen käyttöliittymän avulla. Valittavissa on runsaasti erilaisia karttoja, joista käyttäjä voi valita haluamansa alku- ja loppupisteet manuaalisesti. Eri algoritmeja voi testata kartalle vuorotellen ja reitin löytymisen jälkeen näytölle tulostuu aina löydetyn reitin pituus ja algoritmin suoritukseen kulunut aika. Dijkstran ja A* kohdalla reitinhaun etenemistä voi havannoida myös animaation avulla.

## Suorituskykymittaus

Suorituskykymittaus on toteutettu tiedostossa suorituskyky.py. Toteutuksessa on käytetty osin samoja funktioita kuin käyttöliittymässä. Testauksessa on mukana 15 erilaista karttaa, kooltaan 100x100 - 500x500 ruutua. Jokaiselle kartalle suoritetaan 20 satunnaista reitinhakua. Kaikkia algoritmeja testataan jokaiselle reitille ja yksittäinen mittaus toistetaan 10 kertaa mittausepävarmuuden vähentämiseksi
