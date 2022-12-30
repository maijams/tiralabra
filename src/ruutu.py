class Ruutu:
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.seina = False
        self.alku = False
        self.maali = False
        self.jonossa = False
        self.vierailtu = False
        self.edellinen = None
        self.naapurit = []
        self.etaisyys = None
        self.jumppoint = False

    def __str__(self):
        return f"{(self.y, self.x)}"
