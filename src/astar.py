from heapq import heappush, heappop
from math import sqrt


class AStar:
    def __init__(self, loppu, ruudukko, jono):
        self.loppu = loppu
        self.ruudukko = ruudukko
        self.jono = jono
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
                for naapuri in ruutu.naapurit:
                    if not naapuri.jonossa:
                        self.laskuri += 1
                        naapuri.etaisyys = ruutu.etaisyys + 1
                        euklidinen = sqrt((naapuri.y-self.loppu.y)**2 + (naapuri.x-self.loppu.x)**2)
                        naapuri.edellinen = ruutu
                        naapuri.jonossa = True
                        heappush(self.jono, (naapuri.etaisyys + euklidinen, self.laskuri, naapuri))
                return False
        
        
    def etsi_naapurit(self):
        korkeus = len(self.ruudukko)
        leveys = len(self.ruudukko[0])
        
        for y in range(korkeus):
            for x in range(leveys):
                ruutu = self.ruudukko[y][x]
                if not ruutu.seina:
                    ruutu.lisaa_naapurit(self.ruudukko)