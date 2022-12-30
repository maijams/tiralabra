from heapq import heappush, heappop
from math import sqrt


class Dijkstra:
    def __init__(self, ruudukko, alku):
        self.nimi = "Dijkstra"
        self.ruudukko = ruudukko
        self.jono = [(0, 0, alku)]
        self.vieraillut = []
        self.reitti = []
        self.laskuri = 0

    def etsi_lyhin(self):
        while len(self.jono) > 0:
            etaisyys, laskuri, ruutu = heappop(self.jono)
            if ruutu.vierailtu:
                continue
            ruutu.vierailtu = True
            self.vieraillut.append(ruutu)
            if ruutu.maali:
                while not ruutu.alku:
                    self.reitti.append(ruutu.edellinen)
                    ruutu = ruutu.edellinen
                self.reitti.append(ruutu)
                return True
            else:
                suunnat = [(0, 1), (1, 0), (0, -1), (-1, 0),
                           (1, 1), (-1, 1), (-1, -1), (1, -1)]
                for suunta in suunnat:
                    naapuri = self.ruudukko[ruutu.y +
                                            suunta[0]][ruutu.x+suunta[1]]
                    if not naapuri.seina and not naapuri.jonossa and not naapuri.vierailtu:
                        self.laskuri += 1
                        if (ruutu.y - naapuri.y) == 0 or (ruutu.x - naapuri.x) == 0:
                            uusi = 1
                        else:
                            uusi = sqrt(2)
                        naapuri.etaisyys = ruutu.etaisyys + uusi
                        naapuri.edellinen = ruutu
                        naapuri.jonossa = True
                        heappush(self.jono, (naapuri.etaisyys,
                                 self.laskuri, naapuri))
                return False
