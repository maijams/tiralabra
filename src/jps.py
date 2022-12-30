from heapq import heappush, heappop
from math import sqrt

class ReittiLoytyi(Exception):
    pass


class JumpPointSearch:
    def __init__(self, ruudukko, alku, loppu):
        self.nimi = "JPS"
        self.ruudukko = ruudukko
        self.loppu = loppu
        self.jono = [(0, 0, alku)]
        self.vieraillut = []
        self.reitti = []
        self.laskuri = 0


    def vaaka_ja_pystyhaku(self, alku, suunta_y, suunta_x):
        nyky_y = alku.y
        nyky_x = alku.x
        etaisyys = alku.etaisyys
        
        while True:
            nyky_y += suunta_y
            nyky_x += suunta_x
            etaisyys += 1
            ruutu = self.ruudukko[nyky_y][nyky_x]
            
            if not ruutu.seina and not ruutu.vierailtu:
                ruutu.vierailtu = True
                ruutu.edellinen = alku
                ruutu.etaisyys = etaisyys
                if ruutu.maali:
                    raise ReittiLoytyi()
            else:  # Jos törmätään seinään tai aiempiin tutkittuun osaan
                return
            
            # Tarkistetaan naapuriruutujen avulla onko nykyinen ruutu jump point
            suunnat = [1, -1]
            if suunta_y == 0:
                for suunta in suunnat:
                    if self.ruudukko[nyky_y+suunta][nyky_x].seina and not self.ruudukko[nyky_y+suunta][nyky_x+suunta_x].seina:
                        self.lisaa_jumppoint(ruutu)
                        return
            elif suunta_x == 0:    
                for suunta in suunnat:
                    if self.ruudukko[nyky_y][nyky_x+suunta].seina and not self.ruudukko[nyky_y+suunta_y][nyky_x+suunta].seina:
                        self.lisaa_jumppoint(ruutu)
                        return
                
                
    def diagonaalihaku(self, alku, suunta_y, suunta_x):
        nyky_y = alku.y
        nyky_x = alku.x
        etaisyys = alku.etaisyys
        
        while True:
            nyky_y += suunta_y
            nyky_x += suunta_x
            etaisyys += sqrt(2)
            ruutu = self.ruudukko[nyky_y][nyky_x]
            
            if not ruutu.seina and not ruutu.vierailtu:
                ruutu.vierailtu = True
                ruutu.edellinen = alku
                ruutu.etaisyys = etaisyys
                if ruutu.maali:
                    raise ReittiLoytyi()
            else:  # Jos törmätään seinään tai aiempiin tutkittuun osaan
                return

            # Tarkistetaan naapuriruutujen avulla onko nykyinen ruutu jump point
            if self.ruudukko[nyky_y-suunta_y][nyky_x].seina and not self.ruudukko[nyky_y-suunta_y][nyky_x+suunta_x].seina:
                self.lisaa_jumppoint(ruutu)
                return
            elif self.ruudukko[nyky_y][nyky_x-suunta_x].seina and not self.ruudukko[nyky_y+suunta_y][nyky_x-suunta_x].seina:
                self.lisaa_jumppoint(ruutu)
                return
            
            self.vaaka_ja_pystyhaku(ruutu, suunta_y, 0)      
            self.vaaka_ja_pystyhaku(ruutu, 0, suunta_x)
            
                
    def etsi_lyhin(self):
        if len(self.jono) > 0:
            etaisyys, laskuri, ruutu = heappop(self.jono)
            xy_suunnat = [(0,1), (1,0), (0,-1), (-1,0)]
            diag_suunnat = [(1,1), (-1,1), (-1,-1), (1,-1)]
            try:
                for suunta in xy_suunnat:
                    self.vaaka_ja_pystyhaku(ruutu, suunta[0], suunta[1])
                for suunta in diag_suunnat:
                    self.diagonaalihaku(ruutu, suunta[0], suunta[1])
                return False
            except ReittiLoytyi:
                self.palauta_vieraillut()
                self.palauta_koko_reitti(self.vieraillut)
                return True
     
    
    def lisaa_jumppoint(self, jumppoint):
        jumppoint.jumppoint = True
        etaisyys = jumppoint.etaisyys + abs(jumppoint.y-self.loppu.y) + abs(jumppoint.x-self.loppu.x)
        self.laskuri += 1                   
        heappush(self.jono, (etaisyys, self.laskuri, jumppoint))
                
    
    def palauta_vieraillut(self):
        ruutu = self.loppu
        while not ruutu.alku:
            self.vieraillut.append(ruutu)
            ruutu = ruutu.edellinen
        self.vieraillut.append(ruutu)
        self.vieraillut.reverse()
            
            
    def palauta_koko_reitti(self, vieraillut):
        ruutu_y = vieraillut[0].y        
        ruutu_x = vieraillut[0].x
        self.reitti.append(vieraillut[0])
        for i in range(len(vieraillut)-1):
            while ruutu_y != vieraillut[i+1].y or ruutu_x != vieraillut[i+1].x:
                ruutu_y += self.reitin_suunta(vieraillut[i+1].y - vieraillut[i].y)
                ruutu_x += self.reitin_suunta(vieraillut[i+1].x - vieraillut[i].x)
                self.reitti.append(self.ruudukko[ruutu_y][ruutu_x])
        
        
    def reitin_suunta(self, n):
        if n > 0: 
            return 1
        elif n < 0:
            return -1
        else:
            return 0
        
