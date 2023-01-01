# Testausdokumentti

## Yksikkötestaus

Ohjelmalle on tehty yksikkötestausta algoritmien toiminnan kannalta oleellisiin tiedostoihin. Yksikkötestauksen ulkopuolelle on jätetty käyttöliittymään ja suorituskykymittaukseen liittyvät tiedostot. 

Testikattavuusraportti:
![Screenshot from 2022-12-31 23-59-03](https://user-images.githubusercontent.com/96269683/210156360-efa144bf-f2e1-49ca-bf8f-c3b4ed11a252.png)

Yksikkötestit voi suorittaa projektin virtuaaliympäristössä komennolla:

``` invoke test ```

Yksikkötestien kattavuusraportin saa toistettua komennolla:

``` invoke coverage-report ```

Yksikkötestien tulisi havaita, mikäli algoritmien toiminnassa tapahtuu sellaisia muutoksia jotka vaikuttavat lyhyimmän reitin löytymiseen. Testaus toteutettiin luomalla pieni ruudukko, jossa reitinhakua testataan eri suuntiin ja erilaisten esteiden yhteydessä. Tuloksista tarkastetaan sekä löydetyn reitin pituus että reitin varrella kuljettujen ruutujen määrä.

## Empiirinen testaus

Algoritmien toimintaa voi testata graafisen käyttöliittymän avulla. Valittavissa on runsaasti erilaisia karttoja, joista käyttäjä voi valita haluamansa alku- ja loppupisteet manuaalisesti. Eri algoritmeja voi testata kartalle vuorotellen ja reitin löytymisen jälkeen näytölle tulostuu aina löydetyn reitin pituus ja algoritmin suoritukseen kulunut aika. Halutessaan reitinhaun etenemistä voi havannoida myös animaation avulla, tosin JPS:n kohdalla animaatio on niin nopea ettei etenkään lyhyimmillä reiteillä etenemistä ehdi juuri havannoida.

Empiirisen testauksen avulla havaittiin ohjelman kehityksen aikana useita virheitä algoritmien toiminnassa, ja graafisen toteutuksen avulla ongelmia oli helpompi lähteä ratkomaan. 

Esimerkki empiirisen testauksen yhteydessä havaitusta ongelmasta, JPS-algoritmin löytämä reitti ei ole lyhyin mahdollinen:

### A*
![Screenshot from 2023-01-01 13-00-38](https://user-images.githubusercontent.com/96269683/210168411-4f397ce8-23c8-4177-acc2-f2f0d5c523f8.png)

### JPS
![Screenshot from 2023-01-01 13-00-50](https://user-images.githubusercontent.com/96269683/210168422-1f354bae-1abc-4b1a-805e-6446ed7ddcb1.png)

## Suorituskykymittaus

Suorituskykymittaus on toteutettu tiedostossa suorituskyky.py. Toteutuksessa on käytetty osin samoja funktioita kuin ohjelman käyttöliittymässä. Testauksessa on mukana 15 erilaista karttaa, kooltaan 100x100 - 500x500 ruutua. Jokaiselle kartalle suoritetaan 20 reitinhakua satunnaisesti valittujen alku- ja loppupisteiden avulla. Kaikkia algoritmeja testataan jokaiselle reitille ja yksittäinen mittaus toistetaan 10 kertaa mittausepävarmuuden minimoimiseksi. Mittaustulokset tulostetaan sekä tallennetaan CSV-tiedostoon. Suorituskykymittauksen tuloksista lisää tiedostossa Toteutusdokumentti. Mittauksen voi toistaa projektin virtuaaliympäristössä komennolla:

``` invoke suorituskyky ```

Esimerkki suorituskykymittauksen aikana syntyvästä tulosteesta:

![Screenshot from 2023-01-01 12-46-29](https://user-images.githubusercontent.com/96269683/210168039-467de401-5d25-47a7-b5b4-ec023a151cc9.png)

Esimerkki suorituskykymittauksen yhteydessä luotavasta CSV-datasta:

![Screenshot from 2023-01-01 12-52-01](https://user-images.githubusercontent.com/96269683/210168172-f2d0388b-fcfb-4555-bfbe-1b06230e1d47.png)

