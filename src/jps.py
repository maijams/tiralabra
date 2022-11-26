import heapq

class ReittiLoytyi(Exception):
    pass


class Jps:
    def __init__(self):
        self.ruudukko = None
        self.alku = None
        self.loppu = None
        self.jono = []
        self.reitti = []
    

    def vaaka_ja_pystyhaku(self, alku, suunta_y, suunta_x):
        nykyinen_y = alku[0]
        nykyinen_x = alku[1]
        etaisyys = self.ruudukko[nykyinen_y][nykyinen_x]
        
        while True:
            nykyinen_y += suunta_y
            nykyinen_x += suunta_x
            etaisyys += 1
            
            if not self.ruudukko[nykyinen_y][nykyinen_x].seina:
                self.ruudukko[nykyinen_y][nykyinen_x].etaisyys = etaisyys
                self.ruudukko[nykyinen_y][nykyinen_x].edellinen = alku
                self.ruudukko[nykyinen_y][nykyinen_x].vierailtu = True
                if nykyinen_y == self.loppu[0] and nykyinen_x == self.loppu[1]:
                    raise ReittiLoytyi()
            else:  # Jos törmätään seinään tai aiempiin tutkittuun osaan
                return None
            
            # Tarkistetaan naapuriruutujen avulla onko nykyinen ruutu jump point
            if suunta_y == 0:
                if self.ruudukko[nykyinen_y+1][nykyinen_x].seina and not self.ruudukko[nykyinen_y+1][nykyinen_x+suunta_x].seina:
                    return nykyinen_y, nykyinen_x
                if self.ruudukko[nykyinen_y-1][nykyinen_x].seina and not self.ruudukko[nykyinen_y-1][nykyinen_x+suunta_x].seina:
                    return nykyinen_y, nykyinen_x
            elif suunta_x == 0:    
                if self.ruudukko[nykyinen_y][nykyinen_x+1].seina and not self.ruudukko[nykyinen_y+suunta_y][nykyinen_x+1].seina:
                    return nykyinen_y, nykyinen_x
                if self.ruudukko[nykyinen_y][nykyinen_x-1].seina and not self.ruudukko[nykyinen_y+suunta_y][nykyinen_x-1].seina:
                    return nykyinen_y, nykyinen_x
                
                
    def diagonaalihaku(self, alku, suunta_x, suunta_y):
        nykyinen_y = alku[0]
        nykyinen_x = alku[1]
        etaisyys = self.ruudukko[nykyinen_y][nykyinen_x]
        
        while True:
            nykyinen_y += suunta_y
            nykyinen_x += suunta_x
            etaisyys += 1
            
            if not self.ruudukko[nykyinen_y][nykyinen_x].seina:
                self.ruudukko[nykyinen_y][nykyinen_x].etaisyys = etaisyys
                self.ruudukko[nykyinen_y][nykyinen_x].edellinen = alku
                self.ruudukko[nykyinen_y][nykyinen_x].vierailtu = True
                if nykyinen_y == self.loppu[0] and nykyinen_x == self.loppu[1]:
                    raise ReittiLoytyi()
            else:  # Jos törmätään seinään tai aiempiin tutkittuun osaan
                return None
    
            if self.ruudukko[nykyinen_y+suunta_y][nykyinen_x].seina and not self.ruudukko[nykyinen_y+suunta_y][nykyinen_x+suunta_x].seina:
                return (nykyinen_y, nykyinen_x)
            else:
                y, x = self.vaaka_ja_pystyhaku((nykyinen_y, nykyinen_x), suunta_y, 0)
                heapq.heappush(self.jono, (self.ruudukko[y][x].etaisyys, self.ruudukko[y][x]))
            if self.ruudukko[nykyinen_y][nykyinen_x+suunta_x].seina and not self.ruudukko[nykyinen_y+suunta_y][nykyinen_x+suunta_x].seina:
                return (nykyinen_y, nykyinen_x)
            else:
                y, x = self.vaaka_ja_pystyhaku((nykyinen_y, nykyinen_x), 0, suunta_x)
                heapq.heappush(self.jono, (self.ruudukko[y][x].etaisyys, self.ruudukko[y][x]))
                
    
    def lyhin_jps(self):
        while len(self.jono) > 0:
            etaisyys, ruutu = heapq.heappop(self.jono)
            
            xy_suunnat = [(0,1), (1,0), (0,-1), (-1,0)]
            diag_suunnat = [(1,1), (-1,1), (-1,-1), (1,-1)]
            
            try:
                for suunta in xy_suunnat:
                    y, x = self.vaaka_ja_pystyhaku((ruutu[0], ruutu[1]), suunta[0], suunta[1])
                    heapq.heappush(self.jono, (self.ruudukko[y][x].etaisyys, self.ruudukko[y][x]))
                for suunta in diag_suunnat:
                    y, x = self.diagonaalihaku((ruutu[0], ruutu[1]), suunta[0], suunta[1])
                    heapq.heappush(self.jono, (self.ruudukko[y][x].etaisyys, self.ruudukko[y][x]))
            except ReittiLoytyi:
                return 
                
    
    def palauta_reitti(self):
        ruutu = self.loppu
        while ruutu.edellinen != self.alku:
            self.reitti.append(ruutu.edellinen)
            ruutu = ruutu.edellinen
        return self.reitti