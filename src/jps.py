from heapq import heappush, heappop
from math import sqrt


class ReittiLoytyi(Exception):
    pass


class JumpPointSearch:
    '''Luokka joka huolehtii JPS-algoritmin toiminnasta.
    
    Parametrit:
        ruudukko: Matriisi reitinhakua varten
        alku: Reitinhaun aloitusruutu
        loppu: Reitinhaun lopetusruutu
    '''
    
    def __init__(self, ruudukko, alku, loppu):
        self.nimi = "JPS"
        self.ruudukko = ruudukko
        self.loppu = loppu
        self.jono = [(0, 0, alku)]
        self.vieraillut = []
        self.reitti = []
        self.laskuri = 0

    def _vaaka_ja_pystyhaku(self, alku, suunta_y, suunta_x):
        '''Yksittäisestä ruudusta etenevä vaaka- ja pystyhaku.
        Palataan jos törmätään seinään, aiemmin tutkittuun osaan tai jumppointiin.
        
        Parametrit:
            alku: Haun aloitusruutu
            suunta_y: Vertikaalisuunta johon ruudusta edetään
            suunta_x: Horisontaalinen suunta johon ruudusta edetään
        '''
        
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
                    if self.ruudukko[nyky_y+suunta][nyky_x].seina:
                        if not self.ruudukko[nyky_y+suunta][nyky_x+suunta_x].seina:
                            self._lisaa_jumppoint(ruutu)
                            return
            elif suunta_x == 0:
                for suunta in suunnat:
                    if self.ruudukko[nyky_y][nyky_x+suunta].seina:
                        if not self.ruudukko[nyky_y+suunta_y][nyky_x+suunta].seina:
                            self._lisaa_jumppoint(ruutu)
                            return

    def _diagonaalihaku(self, alku, suunta_y, suunta_x):
        '''Yksittäisestä ruudusta etenevä diagonaalihaku.
        Palataan jos törmätään seinään, aiemmin tutkittuun osaan tai jumppointiin.
        Jokaisesta läpikäydystä ruudusta aloitetaan uusi vaaka- ja pystyhaku.
        
        Parametrit:
            alku: Haun aloitusruutu
            suunta_y: Vertikaalisuunta johon ruudusta edetään
            suunta_x: Horisontaalinen suunta johon ruudusta edetään
        '''
        
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
            if self.ruudukko[nyky_y-suunta_y][nyky_x].seina:
                if not self.ruudukko[nyky_y-suunta_y][nyky_x+suunta_x].seina:
                    self._lisaa_jumppoint(ruutu)
                    return
            elif self.ruudukko[nyky_y][nyky_x-suunta_x].seina:
                if not self.ruudukko[nyky_y+suunta_y][nyky_x-suunta_x].seina:
                    self._lisaa_jumppoint(ruutu)
                    return

            self._vaaka_ja_pystyhaku(ruutu, suunta_y, 0)
            self._vaaka_ja_pystyhaku(ruutu, 0, suunta_x)

    def etsi_lyhin(self):
        '''Algoritmin suoritus.
        
        Palauttaa True jos reitti löytyy, False jos reittiä ei löydy.
        '''
        
        if len(self.jono) > 0:
            ruutu = heappop(self.jono)[2]
            xy_suunnat = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            diag_suunnat = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
            try:
                for suunta in xy_suunnat:
                    self._vaaka_ja_pystyhaku(ruutu, suunta[0], suunta[1])
                for suunta in diag_suunnat:
                    self._diagonaalihaku(ruutu, suunta[0], suunta[1])
                return False
            except ReittiLoytyi:
                self._palauta_vieraillut()
                self._palauta_koko_reitti()
                return True

    def _lisaa_jumppoint(self, jumppoint):
        '''Lisää jumppointin läpikäytävien ruutujen prioritetttilistalle.
        
        Parametrit:
            jumppoint: Listalle lisättävä Ruutu-olio
        '''
        
        jumppoint.jumppoint = True
        etaisyys = jumppoint.etaisyys + \
            sqrt((jumppoint.y-self.loppu.y)**2 +
                 (jumppoint.x-self.loppu.x)**2)
        self.laskuri += 1
        heappush(self.jono, (etaisyys, self.laskuri, jumppoint))

    def _palauta_vieraillut(self):
        '''Käy läpi reitin varrella olevat jumppointit ja 
        lisää ne vierailtujen listaan.'''
        
        ruutu = self.loppu
        while not ruutu.alku:
            self.vieraillut.append(ruutu)
            ruutu = ruutu.edellinen
        self.vieraillut.append(ruutu)
        self.vieraillut.reverse()

    def _palauta_koko_reitti(self):
        '''Käy jumpppointien avulla läpi kaikki reitin varrella olevat 
        ruudut ja lisää ne reitti-listaan.'''
        
        ruutu_y =self.vieraillut[0].y
        ruutu_x =self.vieraillut[0].x
        self.reitti.append(self.vieraillut[0])
        for i in range(len(self.vieraillut)-1):
            while ruutu_y !=self.vieraillut[i+1].y or ruutu_x !=self.vieraillut[i+1].x:
                ruutu_y += self._reitin_suunta(
                   self.vieraillut[i+1].y - self.vieraillut[i].y)
                ruutu_x += self._reitin_suunta(
                   self.vieraillut[i+1].x - self.vieraillut[i].x)
                self.reitti.append(self.ruudukko[ruutu_y][ruutu_x])

    def _reitin_suunta(self, erotus):
        '''Kertoo mihin suuntaan reitin palautuksen on edettävä.'''
        
        if erotus > 0:
            return 1
        if erotus < 0:
            return -1
        return 0
