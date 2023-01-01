# Toteutusdokumentti

## Ohjelman yleisrakenne 

Ohjelman graafinen käyttöliittymä on toteutettu Pythonin Pygame-kirjaston avulla. Reitinhaun karttoina käytetään kuvankäsittelyohjelmalla piirrettyjä mustavalkoisia PNG-kuvia, joiden avulla piirretään vuorotellen eri hakualgoritmien eteneminen.

## Suorituskykyvertailu

Algoritmien suorituskykyä testattiin 15 eri kartan avulla, viidessä eri kokoluokassa. Jokaisessa kartassa tehtiin 20 reitinhakua, erikseen jokaiselle algoritmille. Yksittäiset mittaukset toistettiin 10 kertaa mittausvirheen minimoimiseksi. Suorituskyvyn mittaamiseksi tehtiin siten yhteensä `15*20*3*10 = 9000` reitinhakua. Kartan ominaisuuksien vaikutusta tuloksiin haluttiin pienentää käyttämällä useampaa erilaista karttaa samassa karttakoossa.

Tulosten perusteella A* oli kaikissa kokoluokissa n. 2 kertaa Dijkstraa nopeampi, siinä missä JPS tehokkuus verrattuna A* kasvoi kartan koon kasvaessa. 100x100 kartassa JPS oli kaksi kertaa A* nopeampi, kun 500x500 kartassa nopeusero oli JPS hyväksi lähes kolminkertainen. JPS ja Dijkstran välillä tehokkuusero korostui vielä tätä enemmän. 100x100 kartassa JPS oli n. 4,5 kertaa Dijkstraa nopeampi, ja 500x500 kartassa lähes 7 kertaa nopeampi.

![Screenshot from 2023-01-01 01-29-41](https://user-images.githubusercontent.com/96269683/210158070-8ab2e6da-00f1-4829-b520-b2f6b803c3db.png)

![Screenshot from 2023-01-01 01-08-20](https://user-images.githubusercontent.com/96269683/210158081-5c0948c9-d072-4aed-a6e1-402b63cf22b7.png)

Tuloksissa huomionarvoista on se, että A* ja JPS eivät aina onnistuneet lyhyimmän reitin löytämisessä. Tämä on havaittavissa myös sovelluksen empiirisen testauksen yhteydessä. Oikeellisuuden tulkinta riippuu kuitenkin osin siitä, miten etäisyyttä mitataan. Jos etäisyydeksi käsitetään reitissä tapahtuvien ruutujen välisten siirtymien määrä, Dijkstra ja A* päätyvät aina samaan tulokseen. Kuitenkin jos halutaan käyttää reitin todellista pituutta (vaaka- ja pystysiirtymien kustannus = 1, diagonaalisiirtymä = sqrt(2)), A* löytämä reitti on usein hiukan Dijkstraa pidempi. 

Sekä A* että JPS kohdalla kokeiltiin useaa eri heuristiikkaa (euclidean, manhattan, octile & Chebyshev), mutta heuristiikan valinnalla ei lopulta vaikuttanut olevan kovin suurta vaikutusta lopputulokseen. Lopullisiksi heuristiikoiksi valikoituvat A*:lle Chebyshev ja JPS:lle euclidean. Graafista käyttöliittymää kokeilemalla voi havaita että A* virheelliset tulokset johtuvat pienistä ylimääräisistä mutkista reitin varrella, jotka johtunevat heuristiikan aiheuttamasta reitin "nojautumisesta" loppupisteen suuntaan. 

Sekä A* että JPS kohdalla virheellisten reittien määrä kasvoi kartan koon kasvaessa. JPS valitettaviin ominaisuuksiin kuuluu, että algoritmin tehokkuuden kustannuksella lyhyin reitti jää välillä löytymättä. Kyseinen algoritmi suosii verkkoja jossa se voi edetä kerralla pidempiä suoria osuuksia, tällöin riskinä on että haku "ohittaa" risteyksen, jonka kautta olisi ollut mahdollista muodostaa lyhyempi reitti. Vaihtoehtoisten reittien määrän kasvaessa virheen riski kasvaa sitä suuremmaksi, mitä suurempi verkko on ja mitä pidempi kuljettava reitti on. Virheellisten reittien osuus JPS kohdalla oli pahimmillaan jopa 45%, keskiarvon ollessa n. 20%. Näistä suurilta kuulostavilta luvuista huolimatta absoluuttiset erot eri algoritmien löytämien reittien pituuksissa eivät olleet kovin suuria. A* löytämät reitit olivat keskimäärin 0,85% ja JPS löytämät 1,76% Dijkstraa pidempiä.

## Työn puutteet ja parannusehdotukset

Työn puutteena on edellä mainitut ongelmat algoritmien toiminnassa lyhyimmän reitin löytämisessä. JPS kohdalla tämä on enemmän ominaisuus, mutta A* olisi mahdollisesti ollut vielä jotenkin optimoitavissa niin ettei reittiin synny ylimääräisiä mutkia. Graafisen käyttöliittymän toteutuksen osalta jäi uupumaan JPS-haun animointi.

## Lähteet

- http://users.cecs.anu.edu.au/~dharabor/data/papers/harabor-grastien-aaai11.pdf
- https://web.archive.org/web/20140310022652/https://zerowidth.com/2013/05/05/jump-point-search-explained.html
