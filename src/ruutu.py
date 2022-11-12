class Ruutu:
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.alku = False
        self.maali = False
        self.seina = False
        self.jonossa = False
        self.vierailtu = False
        self.edellinen = None
        self.naapurit = []
        
    def lisaa_naapurit(self, ruudukko):
        naapurit = [(0,1), (1,0), (0,-1), (-1,0)]
        for naapuri in naapurit:
            try:
                ruutu = ruudukko[self.x + naapuri[0]][self.y + naapuri[1]]
                if not ruutu.seina:
                    self.naapurit.append(ruutu)
            except:
                pass
        
    def __str__(self):
        return f"{(self.x, self.y)}"