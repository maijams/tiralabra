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
                ruutu.etaisyys = etaisyys
                ruutu.edellinen = alku
                ruutu.vierailtu = True
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
                ruutu.etaisyys = etaisyys
                ruutu.edellinen = alku
                ruutu.vierailtu = True
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
        #print("haku")
        while len(self.jono) > 0:
            etaisyys, laskuri, ruutu = heappop(self.jono)
            #print(ruuutu)
            #print(etaisyyss)
            #print(self.jono)
            xy_suunnat = [(0,1), (1,0), (0,-1), (-1,0)]
            diag_suunnat = [(1,1), (-1,1), (-1,-1), (1,-1)]
            if ruutu.alku:
                ruutu.vierailtu = True
            
            try:
                for suunta in xy_suunnat:
                    #print(suunta, ruutu, etaisyys)
                    self.vaaka_ja_pystyhaku(ruutu, suunta[0], suunta[1])
                for suunta in diag_suunnat:
                    #print(suunta, ruutu, etaisyys)
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
        self.vieraillut = [self.loppu]
        while ruutu.edellinen != self.alku:
            self.vieraillut.append(ruutu.edellinen)
            ruutu = ruutu.edellinen
        self.vieraillut.append(self.alku)
        self.vieraillut.reverse()
            
            
    def palauta_koko_reitti(self, solmut):
        ruutu_y = solmut[0].y        
        ruutu_x = solmut[0].x
        self.reitti = [solmut[0]]
        for i in range(len(solmut)-1):
            while ruutu_y != solmut[i+1].y or ruutu_x != solmut[i+1].x:
                ruutu_y += self.reitin_suunta(solmut[i+1].y - solmut[i].y)
                ruutu_x += self.reitin_suunta(solmut[i+1].x - solmut[i].x)
                self.reitti.append(self.ruudukko[ruutu_y][ruutu_x])
        
        
    def reitin_suunta(self, n):
        if n > 0: 
            return 1
        elif n < 0:
            return -1
        else:
            return 0
        
