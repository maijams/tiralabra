from heapq import heappush, heappop

class Dijkstra:
    def __init__(self):
        self.alku = None
        self.loppu = None
        self.jono = []
        self.reitti = []
        self.laskuri = 0
    
    def lyhin_dijkstra(self):
        while len(self.jono) > 0:
            etaisyys, ruutu = heappop(self.jono)
            ruutu.vierailtu = True
            if ruutu.maali:
                while ruutu.edellinen != self.alku:
                    self.reitti.append(ruutu.edellinen)
                    ruutu = ruutu.edellinen
                return False
            else:
                for naapuri in ruutu.naapurit:
                    if not naapuri.jonossa:
                        self.laskuri += 1
                        naapuri.edellinen = ruutu
                        naapuri.jonossa = True
                        heappush(self.jono, (self.laskuri, naapuri))
                        #self.jono.append(naapuri)
                return True
        
