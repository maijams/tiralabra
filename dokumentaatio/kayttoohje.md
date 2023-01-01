# Käyttöohje

## Ohjelman asennus & testaus

Asenna projekti koneellesi komennolla:
```
git clone git@github.com:maijams/tiralabra.git
```
**tai** lataa projektin release zip-tiedostona.

Asenna projektin riippuvuudet juurihakemistossa komennolla:
```
poetry install
```

Siirry projektin virtuaaliympäristöön:
```
poetry shell
```

Suorituskykymittaus virtuaaliympäristössä:
```
invoke suorituskyky
```

Yksikkötestien ajaminen virtuaaliympäristössä:
```
invoke test
```

Yksikkötestien kattavuusraportti virtuaaliympäristössä:
```
invoke coverage-report
```

Pylint-raportti virtuaaliympäristössä:
```
invoke lint
```


## Ohjelman käyttö

Käynnistä ohjelma virtuaaliympäristössä komennolla:
```
invoke start
```

Graafinen käyttöliittymä sisältää sovelluksen käyttöä varten tarvittavat ohjeet:

![Screenshot from 2023-01-01 14-18-56](https://user-images.githubusercontent.com/96269683/210170346-04a949d9-5b3b-4c80-b548-4e094d608d3f.png)

**Käyttö tapahtuu siis seuraavasti:**

1. Valitse reitin alku- ja loppupiste klikkaamalla kartasta haluamiasi kohtia
2. Käynnistä haku haluamallasi algoritmilla näppäinkomennolla: Dijstra [D], A* [S], JPS [J]
3. Halutessasi nollaa haku [0] ja valitse uudet pisteet kartalta
4. Voit vaihtaa karttaa numeropainikkeilla 1-9
5. Aktivoi / deaktivoi animaatio: [A]

**Esimerkki reitinhaun tuloksesta:**
![Screenshot from 2023-01-01 14-25-42](https://user-images.githubusercontent.com/96269683/210170538-b98c8b7d-13b4-4692-bfbb-ad5d76f0c475.png)


**Ohjelmalle voi tehdä myös omia karttoja, tällöin tulee huomioida seuraavat seikat:**
- Kartaksi kelpaa mustavalkoinen PNG-kuva, jonka datapisteiden tulee olla RGB-formaatissa (tiet mustia, seinät valkoisia)
- Kartan reunoille tulee jättää vähintään yhden ruudun levyinen "seinä-bufferi", muuten ruudukon käsittelyn yhteydessä syntyy IndexError
- Skaalautuvuuden takia kartan sivujen tulee mielellään olla tasapituisia
- Luettavuuden kannalta ei kannata käyttää liian suuria karttoja. Ohjelmaa on testattu max. 500x500 px kartalla, näin suurella kartalle reitin havannointi alkaa olla jo turhan vaikeaa
