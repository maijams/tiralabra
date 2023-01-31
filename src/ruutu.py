class Ruutu:
    '''Yksittäisen ruudun ominaisuuksista vastaava luokka.

    Parametrit:
        y: Ruudun y-koordinaatti kartassa
        x: Ruudun x-koordinaatti kartassa
    '''

    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.seina = False
        self.alku = False
        self.maali = False
        self.jonossa = False
        self.vierailtu = False
        self.jumppoint = False
        self.edellinen = None
        self.etaisyys = 10**9

    def __str__(self):
        return f"{(self.y, self.x)}"
