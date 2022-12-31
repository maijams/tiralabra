import time
import os
from random import randint
from statistics import mean
from PIL import Image
from ruutu import Ruutu
from astar import AStar
from dijkstra import Dijkstra
from jps import JumpPointSearch


kartat = []

kartta_tiedostot = [
    "kartta100_1.png", "kartta100_2.png", "kartta100_3.png",
    "kartta200_1.png", "kartta200_2.png", "kartta200_3.png",
    "kartta300_1.png", "kartta300_2.png", "kartta300_3.png",
    "kartta400_1.png", "kartta400_2.png", "kartta400_3.png",
    "kartta500_1.png", "kartta500_2.png", "kartta500_3.png"
]

for kartta_tiedosto in kartta_tiedostot:
    kartta = {}
    kartta["tiedosto"] = kartta_tiedosto
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
        self.kartta = ""
        self.ruudukko = []
        self.alku = None
        self.loppu = None
        self.algoritmi = None
        self.etsi = False
        self.loytyi = False
        self.kuva = None
        self.pikselikartta = None
        self.leveys = None
        self.korkeus = None

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
        for kartta in kartat:
            self.kartta = kartta["tiedosto"]

            for _ in range(self.reitit_lkm):
                self.nollaa_haku()
                alku_y, alku_x, loppu_y, loppu_x = self.valitse_pisteet()
                self.aseta_alku(alku_y, alku_x)
                self.aseta_loppu(loppu_y, loppu_x)

                ajat = self.mittaus("Dijkstra")
                kartta["dijkstra_aika"].append(mean(ajat))
                pituus_dijkstra = round(self.loppu.etaisyys, 0)
                kartta["pituudet"].append(pituus_dijkstra)

                ajat = self.mittaus("A*")
                kartta["astar_aika"].append(mean(ajat))
                pituus_astar = round(self.loppu.etaisyys, 0)
                if pituus_astar != pituus_dijkstra:
                    kartta["astar_virheet"] += 1
                kartta["astar_pituudet"].append(pituus_astar)

                ajat = self.mittaus("JPS")
                kartta["jps_aika"].append(mean(ajat))
                pituus_jps = round(self.loppu.etaisyys, 0)
                if pituus_jps != pituus_dijkstra:
                    kartta["jps_virheet"] += 1
                kartta["jps_pituudet"].append(pituus_jps)

            self.tulosta_tulokset(kartta)

        self.tallenna_tiedostoon(kartat)

    def tulosta_tulokset(self, kartta):
        print(kartta["tiedosto"])
        print("reitit:", self.reitit_lkm, "kpl")
        print("dijkstra:", mean(kartta["dijkstra_aika"])*1000, "ms")
        print("astar:", mean(kartta["astar_aika"])*1000, "ms")
        print("jps:", mean(kartta["jps_aika"])*1000, "ms")
        print("astar virheet:", kartta["astar_virheet"], "kpl")
        print("jps virheet:", kartta["jps_virheet"], "kpl")
        print("jps virhe-%:", kartta["jps_virheet"]/self.reitit_lkm*100, "%")
        print("pituus dijkstra ka:", mean(kartta["pituudet"]))
        print("pituus astar ka:", mean(kartta["astar_pituudet"]))
        print("pituus jps ka:", mean(kartta["jps_pituudet"]))
        print("pituus min:", min(kartta["pituudet"]))
        print("pituus max:", max(kartta["pituudet"]))
        print()

    def tallenna_tiedostoon(self, kartat):
        with open("data.csv", "w", newline="") as csvfile:
            otsikot = (
                'tiedostonimi,'
                'reitit lkm,'
                'dijkstra_aika ms,'
                'astar_aika ms,'
                'jps_aika ms,'
                'astar virheet,'
                'jps virheet,'
                'jps virhe-%,'
                'pituus dijkstra ka,'
                'pituus astar ka,'
                'pituus jps ka,'
                'pituus min,'
                'pituus max'
                '\n'
            )
            csvfile.write(otsikot)

            for kartta in kartat:
                csvfile.write(
                    f'{kartta["tiedosto"]},'
                    f'{self.reitit_lkm},'
                    f'{mean(kartta["dijkstra_aika"])*1000},'
                    f'{mean(kartta["astar_aika"])*1000},'
                    f'{mean(kartta["jps_aika"])*1000},'
                    f'{kartta["astar_virheet"]},'
                    f'{kartta["jps_virheet"]},'
                    f'{kartta["jps_virheet"]/self.reitit_lkm*100},'
                    f'{mean(kartta["pituudet"])},'
                    f'{mean(kartta["astar_pituudet"])},'
                    f'{mean(kartta["jps_pituudet"])},'
                    f'{min(kartta["pituudet"])},'
                    f'{max(kartta["pituudet"])},'
                    f'\n')

    def mittaus(self, algoritmi):
        ajat = []
        for _ in range(self.toistot_lkm):
            self.nollaa_haku()
            self.etsi = True
            if algoritmi == "Dijkstra":
                self.algoritmi = Dijkstra(self.ruudukko, self.alku)
            elif algoritmi == "A*":
                self.algoritmi = AStar(self.ruudukko, self.alku, self.loppu)
            if algoritmi == "JPS":
                self.algoritmi = JumpPointSearch(
                    self.ruudukko, self.alku, self.loppu)
            aika = self.suorita_haku()
            ajat.append(aika)
        return ajat

    def suorita_haku(self):
        if self.etsi:
            aika_alku = time.time()
            while self.etsi:
                self.loytyi = self.algoritmi.etsi_lyhin()
                if self.loytyi:
                    self.etsi = False
            aika_loppu = time.time()
        return aika_loppu-aika_alku


if __name__ == "__main__":
    testi = Suorituskyky(20, 10)
    testi.kaynnista()
