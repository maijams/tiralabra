import time
import os
from random import randint
from statistics import mean
from PIL import Image
from ruutu import Ruutu
from astar import AStar
from dijkstra import Dijkstra
from jps import JumpPointSearch

'''
Toteutus
- Yhteensä 15 karttaa, 3 per koko. Koot 100-500
- Satunnaiset alku- & loppupisteet 100x ?
- 3 algoritmia
- Toistomittaus 10x per skenaario?
-> 15 x 100 x 3 x 10 = 45000 mittausta
- Suositeltu kesto

Tallennus
- 15 x 3 = 45 -> eroja samassa karttakoossa?
-  5 x 3 = 15 -> kuvaajaan
- Epäonnistuneiden lkm ja laatu -> %
- Reittien pituudet, vierailtujen solmujen lkm?

'''

reitit_per_kartta = 1
toistot_per_reitti = 1

kartta100_1 = {}
kartta100_2 = {}
kartta100_3 = {}
kartta200_1 = {}
kartta200_2 = {}
kartta200_3 = {}
kartta300_1 = {}
kartta300_2 = {}
kartta300_3 = {}
kartta400_1 = {}
kartta400_2 = {}
kartta400_3 = {}
kartta500_1 = {}
kartta500_2 = {}
kartta500_3 = {}

kartat = [
    kartta100_1, kartta100_2, kartta100_3,
    kartta200_1, kartta200_2, kartta200_3,
    kartta300_1, kartta300_2, kartta300_3,
    kartta400_1, kartta400_2, kartta400_3,
    kartta500_1, kartta500_2, kartta500_3,
]

kartta_tiedostot = [
    "kartta100_1.png", "kartta100_2.png", "kartta100_3.png",
    "kartta200_1.png", "kartta200_2.png", "kartta200_3.png",
    "kartta300_1.png", "kartta300_2.png", "kartta300_3.png",
    "kartta400_1.png", "kartta400_2.png", "kartta400_3.png",
    "kartta500_1.png", "kartta500_2.png", "kartta500_3.png"
]

for i in range(14):
    kartat[i]["tiedosto"] = kartta_tiedostot[i]
    kartat[i]["dijkstra_aika"] = []
    kartat[i]["astar_aika"] = []
    kartat[i]["jps_aika"] = []
    kartat[i]["astar_virheet"] = 0
    kartat[i]["jps_virheet"] = 0
    kartat[i]["pituudet"] = []


class Suorituskyky:
    def __init__(self):
        self.ruudukko = []
        self.alku = None
        self.loppu = None
        self.kartta = ""

    def luo_ruudukko(self):
        self.ruudukko = []
        for y in range(self.korkeus):
            rivi = []
            for x in range(self.leveys):
                ruutu = Ruutu(y, x)
                # Ruutu on seinää jos sen RGB-arvojen summa on tarpeeksi suuri
                if sum(self.pikselikartta[x, y]) > 735:
                    ruutu.seina = True
                rivi.append(ruutu)
            self.ruudukko.append(rivi)
        if self.alku is not None:
            self.aseta_alku(self.alku.y, self.alku.x)
        if self.loppu is not None:
            self.aseta_loppu(self.loppu.y, self.loppu.x)

    def valitse_pisteet(self):
        while True:
            alku_y = randint(0, self.leveys-1)
            alku_x = randint(0, self.leveys-1)
            if not self.ruudukko[alku_y][alku_x].seina:
                break
        while True:
            loppu_y = randint(0, self.leveys-1)
            loppu_x = randint(0, self.leveys-1)
            if not self.ruudukko[loppu_y][loppu_x].seina:
                break
        return alku_y, alku_x, loppu_y, loppu_x

    def nollaa_haku(self):
        self.algoritmi = None
        self.etsi = False
        self.loytyi = False

        self.alusta_kartta()
        self.luo_ruudukko()

    def alusta_kartta(self):
        polku = os.path.dirname(__file__)
        kuva = os.path.join(polku, 'kartat', self.kartta)
        self.kuva = Image.open(kuva)
        self.kuva.save("reitti.png")
        self.pikselikartta = self.kuva.load()
        self.leveys, self.korkeus = self.kuva.size

    def aseta_alku(self, y, x):
        self.alku = self.ruudukko[y][x]
        self.alku.alku = True
        self.alku.etaisyys = 0

    def aseta_loppu(self, y, x):
        self.loppu = self.ruudukko[y][x]
        self.loppu.maali = True

    def kaynnista(self):
        for i in range(14):
            self.kartta = kartat[i]["tiedosto"]

            for _ in range(reitit_per_kartta):
                self.nollaa_haku()
                alku_y, alku_x, loppu_y, loppu_x = self.valitse_pisteet()
                self.aseta_alku(alku_y, alku_x)
                self.aseta_loppu(loppu_y, loppu_x)

                ajat = []
                for _ in range(toistot_per_reitti):
                    self.nollaa_haku()
                    self.etsi = True
                    self.haku = Dijkstra(self.ruudukko, self.alku)
                    aika = self.suorita_haku()
                    ajat.append(aika)
                kartat[i]["dijkstra_aika"].append(mean(ajat))
                pituus_dijkstra = len(self.haku.reitti)
                kartat[i]["pituudet"].append(pituus_dijkstra)

                ajat = []
                for _ in range(toistot_per_reitti):
                    self.nollaa_haku()
                    self.etsi = True
                    self.haku = AStar(self.ruudukko, self.alku, self.loppu)
                    aika = self.suorita_haku()
                    ajat.append(aika)
                kartat[i]["astar_aika"].append(mean(ajat))
                if len(self.haku.reitti) != pituus_dijkstra:
                    kartat[i]["astar_virheet"] += 1

                ajat = []
                for _ in range(toistot_per_reitti):
                    self.nollaa_haku()
                    self.etsi = True
                    self.haku = JumpPointSearch(
                        self.ruudukko, self.alku, self.loppu)
                    aika = self.suorita_haku()
                    ajat.append(aika)
                kartat[i]["jps_aika"].append(mean(ajat))
                if len(self.haku.reitti) != pituus_dijkstra:
                    kartat[i]["jps_virheet"] += 1

            print(kartat[i]["tiedosto"])
            print("dijkstra", mean(kartat[i]["dijkstra_aika"])*1000, "ms")
            print("astar", mean(kartat[i]["astar_aika"])*1000, "ms")
            print("jps", mean(kartat[i]["jps_aika"])*1000, "ms")
            print("astar virheet", kartat[i]["astar_virheet"], "kpl")
            print("jps virheet", kartat[i]["jps_virheet"], "kpl")
            print("pituus ka", mean(kartat[i]["pituudet"]))
            print("pituus min", min(kartat[i]["pituudet"]))
            print("pituus max", max(kartat[i]["pituudet"]))
            print()

    def suorita_haku(self):
        if self.etsi:
            aika_alku = time.time()
            while self.etsi:
                self.loytyi = self.haku.etsi_lyhin()
                if self.loytyi:
                    self.etsi = False
            aika_loppu = time.time()
        return aika_loppu-aika_alku


if __name__ == "__main__":
    testi = Suorituskyky()
    testi.kaynnista()
