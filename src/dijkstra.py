from heapq import heappush, heappop
from math import sqrt


class Dijkstra:
    '''Luokka joka huolehtii Dijkstran algoritmin toiminnasta.

    Parametrit:
        ruudukko: Matriisi reitinhakua varten
        alku: Reitinhaun aloitusruutu
    '''

    def __init__(self, ruudukko, alku):
        self.nimi = "Dijkstra"
        self.ruudukko = ruudukko
        self.jono = [(0, 0, alku)]
        self.vieraillut = []
        self.reitti = []
        self.laskuri = 0

    def etsi_lyhin(self):
        '''Algoritmin suoritus.

        Palauttaa True jos reitti löytyy, False jos reittiä ei löydy.
        '''

        while len(self.jono) > 0:
            ruutu = heappop(self.jono)[2]
            if ruutu.vierailtu:
                continue
            ruutu.vierailtu = True
            self.vieraillut.append(ruutu)
            if ruutu.maali:
                self._palauta_reitti(ruutu)
                return True
            suunnat = [(0, 1), (1, 0), (0, -1), (-1, 0),
                       (1, 1), (-1, 1), (-1, -1), (1, -1)]
            for suunta in suunnat:
                naapuri = self.ruudukko[ruutu.y +
                                        suunta[0]][ruutu.x+suunta[1]]
                if not naapuri.seina:
                    self.laskuri += 1
                    if (ruutu.y - naapuri.y) == 0 or (ruutu.x - naapuri.x) == 0:
                        paino = 1
                    else:
                        paino = sqrt(2)
                    uusi_etaisyys = ruutu.etaisyys + paino
                    if uusi_etaisyys < naapuri.etaisyys:
                        naapuri.etaisyys = uusi_etaisyys
                        naapuri.edellinen = ruutu
                        naapuri.jonossa = True
                        heappush(self.jono, (naapuri.etaisyys,
                                         self.laskuri, naapuri))
            return False

    def _palauta_reitti(self, ruutu):
        '''Käy läpi reitin varrella olevat ruudut ja lisää ne listaan.'''

        while not ruutu.alku:
            self.reitti.append(ruutu)
            ruutu = ruutu.edellinen
        self.reitti.append(ruutu)
