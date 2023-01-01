# Viikkoraportti 7

Loppupalautusta varten projektin viimeisille viikoille riitti vielä paljon tehtävää. Aikaa vievimmät osuudet liittyivät algoritmien toiminnan korjauksiin, refaktorointiin, suorituskykymittaukseen, testaukseen ja dokumentaation kirjoittamiseen. Sain parannettua JPS-algoritmin toimintaa huomattavasti, virheitä löytyi mm. muuttujien nimien virheellisestä käytöstä. Kävi kuitenkin ilmi että JPS:n toimintaa ei ole mahdollista saada täydelliseksi, vaan reitinhaun suosiessa suoria linjoja saattaa algoritmi ohittaa reitin joka olisi sen löytämää reittiä lyhyempi. Virheen mahdollisuus kasvaa mitä suurempi verkko on ja mitä enemmän vaihtoehtoisia reittejä on olemassa. Sekä A*:lle että JPS:lle kokeilin useita eri heuristiikoita, mutta kovin suurta vaikutusta heuristiikan valinnalle en havainnut. Yhdellä reitillä saattoi tietty heuristiikka toimia toisia paremmin mutta toisella reitillä tilanne oli päinvastainen. Lopullisiksi heuristiikoiksi valikoitui A*:lle Chebyshev ja JPS:lle linnuntie.

Palautin ohjelmaan edellisessä välipalautuksessa poistamani reitinhaun animointimahdollisuuden. Nyt käyttäjä voi valita, haluaako animoinnin näkyviin vai ei. JPS:n kohdalla animaation eteneminen on tosin niin nopeaa ettei sitä etenkään pienemmillä kartoilla ehdi juuri havannoida.

Suorituskykymittausta varten loin oman tiedoston. Koodissa olevalle luokalle voi antaa haluamansa arvot joiden mukaan mittaus suoritetaan arvojen osoittaman lukumäärän verran. Algoritmien analyysia varten suoritettiin jokaisella algoritmillä 20 satunnaista reitinhakua per kartta, jokainen mittaus toistettiin 10 kertaa. Mittauksen suoritus hidastui huomattavasti suurempien karttojen kohdalla, oman aikansa vei varmasti satunnaisesti valittujen alku- ja loppupisteiden löytäminen. Mittauksen kokonaiskesto vei sen verran kauan aikaa (+10min), että uskoisin saadun mittausdatan olevan suhteellisen edustavaa ja ainakin saadut tulokset vaikuttivat loogisilta.

Kaiken kaikkiaan olen projektin lopulliseen versioon suhteellisen tyytyväinen. Asia mikä jäi hieman harmittamaan oli A* algoritmin reitinhaussa välillä esiintyvät ylimääräiset "mutkat", joita en heuristiikan vaihdoista huolimatta saanut karsittua pois. Algoritmin suhteellisen yksinkertaisesta toteutuksesta huolimatta en onnistunut löytämään keinoa jolla tuon ominaisuuden olisi saanut korjattua. Parannettavia kohtia olisi varmasti ollut muuallakin, esim. käyttöliittymän ulkonäköä olisi voinut vielä hioa mutta tuo ei kuitenkaan ole kovin tärkeä seikka algoritmien toiminnan kannalta. Oman ohjelmointiuran ollessa vielä varsin tuore, projektin aikana tuli opittua taas paljon uutta sekä algoritmeista että itse ohjelmoinnista.


Viikkojen työtunnit: 55 h