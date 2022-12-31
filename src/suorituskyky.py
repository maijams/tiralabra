import time
import os
import csv
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


kartat = []

kartta_tiedostot = [
    "kartta100_1.png", "kartta100_2.png", "kartta100_3.png",
    "kartta200_1.png", "kartta200_2.png", "kartta200_3.png",
    "kartta300_1.png", "kartta300_2.png", "kartta300_3.png",
    "kartta400_1.png", "kartta400_2.png", "kartta400_3.png",
    "kartta500_1.png", "kartta500_2.png", "kartta500_3.png"
]

for i in range(14):
    kartta = {}
    kartta["tiedosto"] = kartta_tiedostot[i]
    kartta["dijkstra_aika"] = []
    kartta["astar_aika"] = []
    kartta["jps_aika"] = []
    kartta["astar_virheet"] = 0
    kartta["jps_virheet"] = 0
    kartta["astar_pituudet"] = []
    kartta["jps_pituudet"] = []
    kartta["pituudet"] = []
    kartat.append(kartta)


class Suorituskyky:
    def __init__(self, reitit_per_kartta, toistot_per_reitti):
        self.reitit_lkm = reitit_per_kartta
        self.toistot_lkm = toistot_per_reitti
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
            alku_y = randint(0, self.korkeus-1)
            alku_x = randint(0, self.leveys-1)
            if not self.ruudukko[alku_y][alku_x].seina:
                break
        while True:
            loppu_y = randint(0, self.korkeus-1)
            loppu_x = randint(0, self.leveys-1)
            if not self.ruudukko[loppu_y][loppu_x].seina:
                break
        return alku_y, alku_x, loppu_y, loppu_x

    def nollaa_haku(self):
        self.algoritmi = None
        self.etsi = False
        self.loytyi = False

        self.hae_kartta()
        self.luo_ruudukko()

    def hae_kartta(self):
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

            for _ in range(self.reitit_lkm):
                self.nollaa_haku()
                alku_y, alku_x, loppu_y, loppu_x = self.valitse_pisteet()
                self.aseta_alku(alku_y, alku_x)
                self.aseta_loppu(loppu_y, loppu_x)

                ajat = self.mittaus("Dijkstra")
                kartat[i]["dijkstra_aika"].append(mean(ajat))
                pituus_dijkstra = round(self.loppu.etaisyys, 0)
                kartat[i]["pituudet"].append(pituus_dijkstra)

                ajat = self.mittaus("A*")
                kartat[i]["astar_aika"].append(mean(ajat))
                pituus_astar = round(self.loppu.etaisyys, 0)
                if pituus_astar != pituus_dijkstra:
                    kartat[i]["astar_virheet"] += 1
                kartat[i]["astar_pituudet"].append(pituus_astar)

                ajat = self.mittaus("JPS")
                kartat[i]["jps_aika"].append(mean(ajat))
                pituus_jps = round(self.loppu.etaisyys, 0)
                if pituus_jps != pituus_dijkstra:
                    kartat[i]["jps_virheet"] += 1
                kartat[i]["jps_pituudet"].append(pituus_jps)

            print(kartat[i]["tiedosto"])
            print("dijkstra", mean(kartat[i]["dijkstra_aika"])*1000, "ms")
            print("astar", mean(kartat[i]["astar_aika"])*1000, "ms")
            print("jps", mean(kartat[i]["jps_aika"])*1000, "ms")
            print("astar virheet", kartat[i]["astar_virheet"], "kpl")
            print("jps virheet", kartat[i]["jps_virheet"], "kpl")
            print("pituus ka astar", mean(kartat[i]["astar_pituudet"]))
            print("pituus ka jps", mean(kartat[i]["jps_pituudet"]))
            print("pituus ka", mean(kartat[i]["pituudet"]))
            print("pituus min", min(kartat[i]["pituudet"]))
            print("pituus max", max(kartat[i]["pituudet"]))
            print()
            
        with open("data.csv", "w", newline="") as csvfile:
            otsikot = (
                'tiedosto,'
                'dijkstra_aika ms,'
                'astar_aika ms,'
                'jps_aika ms,'
                'astar virheet,'
                'jps virheet,'
                'pituus ka astar,'
                'pituus ka jps,'
                'pituus ka,'
                'pituus min,'
                'pituus max'
                '\n'
                )
            csvfile.write(otsikot)
            
            for kartta in kartat:
                csvfile.write(
                    f'{kartta["tiedosto"]},'
                    f'{mean(kartta["dijkstra_aika"])*1000},'
                    f'{mean(kartta["astar_aika"])*1000},'
                    f'{mean(kartta["jps_aika"])*1000},'
                    f'{kartta["astar_virheet"]},'
                    f'{kartta["jps_virheet"]},'
                    f'{mean(kartta["astar_pituudet"])},'
                    f'{mean(kartta["jps_pituudet"])},'
                    f'{mean(kartta["pituudet"])},'
                    f'{min(kartta["pituudet"])},'
                    f'{max(kartta["pituudet"])},'
                    f'\n')

    def mittaus(self, algoritmi):
        ajat = []
        for _ in range(self.toistot_lkm):
            self.nollaa_haku()
            self.etsi = True
            if algoritmi == "Dijkstra":
                self.haku = Dijkstra(self.ruudukko, self.alku)
            elif algoritmi == "A*":
                self.haku = AStar(self.ruudukko, self.alku, self.loppu)
            if algoritmi == "JPS":
                self.haku = JumpPointSearch(
                    self.ruudukko, self.alku, self.loppu)
            aika = self.suorita_haku()
            ajat.append(aika)
        return ajat

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
    testi = Suorituskyky(5, 3)
    testi.kaynnista()
