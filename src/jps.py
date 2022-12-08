from heapq import heappush, heappop
from math import sqrt

class ReittiLoytyi(Exception):
    pass


class JumpPointSearch:
    def __init__(self, ruudukko, alku, loppu, jono):
        self.ruudukko = ruudukko
        self.alku = alku
        self.loppu = loppu
        self.jono = jono
        self.reitti = []
        self.laskuri = 0


    def vaaka_ja_pystyhaku(self, alku, suunta_y, suunta_x):
        nykyinen_y = alku[0]
        nykyinen_x = alku[1]
        etaisyys = self.ruudukko[nykyinen_y][nykyinen_x].etaisyys
        
        while True:
            nykyinen_y += suunta_y
            nykyinen_x += suunta_x
            etaisyys += 1
            
            if not self.ruudukko[nykyinen_y][nykyinen_x].seina and not self.ruudukko[nykyinen_y][nykyinen_x].vierailtu:
                self.ruudukko[nykyinen_y][nykyinen_x].etaisyys = etaisyys
                self.ruudukko[nykyinen_y][nykyinen_x].edellinen = self.ruudukko[alku[0]][alku[1]]
                self.ruudukko[nykyinen_y][nykyinen_x].vierailtu = True
                if nykyinen_y == self.loppu.y and nykyinen_x == self.loppu.x:
                    raise ReittiLoytyi()
            else:  # Jos törmätään seinään tai aiempiin tutkittuun osaan
                return None
            
            # Tarkistetaan naapuriruutujen avulla onko nykyinen ruutu jump point
            if suunta_y == 0:
                if self.ruudukko[nykyinen_y+1][nykyinen_x].seina and not self.ruudukko[nykyinen_y+1][nykyinen_x+suunta_x].seina:
                    self.ruudukko[nykyinen_y][nykyinen_x].jumppoint = True
                    return nykyinen_y, nykyinen_x
                if self.ruudukko[nykyinen_y-1][nykyinen_x].seina and not self.ruudukko[nykyinen_y-1][nykyinen_x+suunta_x].seina:
                    self.ruudukko[nykyinen_y][nykyinen_x].jumppoint = True
                    return nykyinen_y, nykyinen_x
            elif suunta_x == 0:    
                if self.ruudukko[nykyinen_y][nykyinen_x+1].seina and not self.ruudukko[nykyinen_y+suunta_y][nykyinen_x+1].seina:
                    self.ruudukko[nykyinen_y][nykyinen_x].jumppoint = True
                    return nykyinen_y, nykyinen_x
                if self.ruudukko[nykyinen_y][nykyinen_x-1].seina and not self.ruudukko[nykyinen_y+suunta_y][nykyinen_x-1].seina:
                    self.ruudukko[nykyinen_y][nykyinen_x].jumppoint = True
                    return nykyinen_y, nykyinen_x
                
                
    def diagonaalihaku(self, alku, suunta_y, suunta_x):
        nykyinen_y = alku[0]
        nykyinen_x = alku[1]
        etaisyys = self.ruudukko[nykyinen_y][nykyinen_x].etaisyys
        
        while True:
            nykyinen_y += suunta_y
            nykyinen_x += suunta_x
            etaisyys += sqrt(2)
            
            if not self.ruudukko[nykyinen_y][nykyinen_x].seina and not self.ruudukko[nykyinen_y][nykyinen_x].vierailtu:
                self.ruudukko[nykyinen_y][nykyinen_x].etaisyys = etaisyys
                self.ruudukko[nykyinen_y][nykyinen_x].edellinen = self.ruudukko[alku[0]][alku[1]]
                self.ruudukko[nykyinen_y][nykyinen_x].vierailtu = True
                if nykyinen_y == self.loppu.y and nykyinen_x == self.loppu.x:
                    raise ReittiLoytyi()
            else:  # Jos törmätään seinään tai aiempiin tutkittuun osaan
                return None
            
            uusi = self.vaaka_ja_pystyhaku((nykyinen_y, nykyinen_x), suunta_y, 0)
            if uusi is not None:
                y, x = uusi
                ruutu = self.ruudukko[y][x]
                etaisyys = ruutu.etaisyys + sqrt(abs(ruutu.y-self.loppu.y)**2 + abs(ruutu.x-self.loppu.x)**2)
                self.laskuri += 1
                heappush(self.jono, (etaisyys, self.laskuri, self.ruudukko[y][x]))
                
            uusi = self.vaaka_ja_pystyhaku((nykyinen_y, nykyinen_x), 0, suunta_x)
            if uusi is not None:
                y, x = uusi
                ruutu = self.ruudukko[y][x]
                etaisyys = ruutu.etaisyys + sqrt(abs(ruutu.y-self.loppu.y)**2 + abs(ruutu.x-self.loppu.x)**2)
                self.laskuri += 1
                heappush(self.jono, (etaisyys, self.laskuri, self.ruudukko[y][x]))

            # Tarkistetaan naapuriruutujen avulla onko nykyinen ruutu jump point
            if self.ruudukko[nykyinen_y-suunta_y][nykyinen_x].seina and not self.ruudukko[nykyinen_y-suunta_y][nykyinen_x+suunta_x].seina:
                self.ruudukko[nykyinen_y][nykyinen_x].jumppoint = True
                return nykyinen_y, nykyinen_x
                

            elif self.ruudukko[nykyinen_y][nykyinen_x-suunta_x].seina and not self.ruudukko[nykyinen_y+suunta_y][nykyinen_x-suunta_x].seina:
                self.ruudukko[nykyinen_y][nykyinen_x].jumppoint = True
                return nykyinen_y, nykyinen_x
            
                
                    
    
    def etsi_lyhin(self):
        while len(self.jono) > 0:
            etaisyyss, laskuri, ruuutu = heappop(self.jono)
            #print(ruuutu)
            #print(self.jono)
            xy_suunnat = [(0,1), (1,0), (0,-1), (-1,0)]
            diag_suunnat = [(1,1), (-1,1), (-1,-1), (1,-1)]
            
            try:
                for suunta in diag_suunnat:
                    uusi = self.diagonaalihaku((ruuutu.y, ruuutu.x), suunta[0], suunta[1])
                    if uusi is not None:
                        y, x = uusi
                        ruuutu = self.ruudukko[y][x]
                        etaisyyss = ruuutu.etaisyys + sqrt(abs(ruuutu.y-self.loppu.y)**2 + abs(ruuutu.x-self.loppu.x)**2)
                        self.laskuri += 1                   
                        heappush(self.jono, (etaisyyss, self.laskuri, self.ruudukko[y][x]))
                for suunta in xy_suunnat:
                    uusi = self.vaaka_ja_pystyhaku((ruuutu.y, ruuutu.x), suunta[0], suunta[1])
                    if uusi is not None:
                        y, x = uusi
                        ruuutu = self.ruudukko[y][x]
                        etaisyyss = ruuutu.etaisyys + sqrt(abs(ruuutu.y-self.loppu.y)**2 + abs(ruuutu.x-self.loppu.x)**2)
                        self.laskuri += 1
                        heappush(self.jono, (etaisyyss, self.laskuri, self.ruudukko[y][x]))
                return False
            
            except ReittiLoytyi:
                self.palauta_reitti()
                return True
                
    
    def palauta_reitti(self):
        ruutu = self.loppu
        #print(ruutu.etaisyys)
        while ruutu.edellinen != self.alku:
            self.reitti.append(ruutu.edellinen)
            ruutu = ruutu.edellinen
        
        
