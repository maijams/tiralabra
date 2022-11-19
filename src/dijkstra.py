class Dijkstra:
    def __init__(self, ruudukko, alku, maali):
        self.ruudukko = ruudukko
        self.alku = alku
        self.maali = maali
        self.jono = [alku]
        self.reitti = []
    
    def lyhin_dijkstra(self):
        if len(self.jono) > 0:
            ruutu = self.jono.pop(0)
            ruutu.vierailtu = True
            if ruutu == self.maali:
                while ruutu.edellinen != self.alku:
                    self.reitti.append(ruutu.edellinen)
                    ruutu = ruutu.edellinen
                return False
            else:
                for naapuri in ruutu.naapurit:
                    if not naapuri.jonossa:
                        naapuri.edellinen = ruutu
                        naapuri.jonossa = True
                        self.jono.append(naapuri)
                return True
        
