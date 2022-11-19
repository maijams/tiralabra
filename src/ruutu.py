class Ruutu:
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.alku = False
        self.maali = False
        self.seina = False
        self.jonossa = False
        self.vierailtu = False
        self.edellinen = None
        self.naapurit = []
    
    # Lisää ruudulle sen pysty- ja vaakasuunnassa sijaitsevat naapurit   
    def lisaa_naapurit(self, ruudukko):
        suunnat = [(0,1), (1,0), (0,-1), (-1,0)]
        for suunta in suunnat:
            try:
                naapuri = ruudukko[self.y + suunta[0]][self.x + suunta[1]]
                if not naapuri.seina:
                    self.naapurit.append(naapuri)
            except:
                pass
        
    def __str__(self):
        return f"{(self.y, self.x)}"