import time
import os
import pygame
from PIL import Image
from ruutu import Ruutu
from dijkstra import Dijkstra
from jps import JumpPointSearch
from astar import AStar


PUNAINEN = (255, 0, 0)
VIHREA = (0, 255, 0)
SININEN = (0, 0, 255)
TURKOOSI = (0, 200, 200)
KELTAINEN = (200, 200, 0)
PINKKI = (235, 52, 189)

kartat = [
    "kartta100_1.png", "kartta100_2.png", "kartta100_3.png",
    "kartta200_1.png", "kartta200_2.png", "kartta200_3.png",
    "kartta300_1.png", "kartta300_2.png", "kartta300_3.png",
    "kartta400_1.png", "kartta400_2.png", "kartta400_3.png",
    "kartta500_1.png", "kartta500_2.png", "kartta500_3.png"
]


class Kayttoliittyma:
    '''Luokka joka sisältää ohjelman käyttöliittymän.

    Parametrit:
        renderoija: Pygame-ikkunan piirtämisestä huolehtiva olio.
    '''

    def __init__(self, renderoija):
        self.renderoija = renderoija
        self.kartta = kartat[0]
        self.ruudukko = []
        self.alku = None
        self.loppu = None
        self.aika = None
        self.animoitu = False
        self.algoritmi = None
        self.paivita_karttaa = True
        self.etsi = False
        self.loytyi = False
        self.animaatio_valmis = False
        self.kuva = None
        self.pikselikartta = None
        self.leveys = None
        self.korkeus = None
        self.skaalauskerroin = None

        self._hae_kartta()
        self._luo_ruudukko()

    def kaynnista(self):
        '''Huolehtii ohjelman perusloopista.'''

        while True:
            self._kasittele_tapahtumat()
            if self.etsi:
                self.aika = self._suorita_algoritmi()
            if self.animoitu and not self.animaatio_valmis and self.algoritmi is not None:
                self._suorita_animaatio()
            if self.paivita_karttaa:
                self._paivita_kartta()

            self.renderoija.renderoi(
                self.animoitu, self.algoritmi, self.alku, self.loppu, self.loytyi, self.aika)

            if self.loytyi:
                self.paivita_karttaa = False

    def _kasittele_tapahtumat(self):
        '''Käyttäjän antamien komentojen käsittely.'''

        positio_kartta = (100, 100)  # (x,y)
        for tapahtuma in pygame.event.get():
            # Alku- ja loppupisteen valinta
            if tapahtuma.type == pygame.MOUSEBUTTONDOWN:
                x, y = tapahtuma.pos
                x_kartta = round((x-positio_kartta[0]) / self.skaalauskerroin)
                y_kartta = round((y-positio_kartta[1]) / self.skaalauskerroin)

                if x_kartta in range(self.leveys) and y_kartta in range(self.korkeus):
                    ruutu = self.ruudukko[y_kartta][x_kartta]
                    if self.alku is None and not ruutu.seina:
                        self._aseta_alku(y_kartta, x_kartta)
                    elif self.loppu is None and not ruutu.seina:
                        self._aseta_loppu(y_kartta, x_kartta)

            # Algoritmim valinta
            elif tapahtuma.type == pygame.KEYDOWN and self.loppu is not None:
                if tapahtuma.key == pygame.K_0:
                    self.alku = None
                    self.loppu = None
                    self._nollaa_haku()
                elif tapahtuma.key in (pygame.K_d, pygame.K_s, pygame.K_j):
                    self._nollaa_haku()
                    self.etsi = True
                    if tapahtuma.key == pygame.K_d:
                        self.algoritmi = Dijkstra(self.ruudukko, self.alku)
                    elif tapahtuma.key == pygame.K_s:
                        self.algoritmi = AStar(
                            self.ruudukko, self.alku, self.loppu)
                    elif tapahtuma.key == pygame.K_j:
                        self.algoritmi = JumpPointSearch(
                            self.ruudukko, self.alku, self.loppu)

            # Kartan valinta
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_1:
                    self._valitse_kartta(kartat[0])
                elif tapahtuma.key == pygame.K_2:
                    self._valitse_kartta(kartat[1])
                elif tapahtuma.key == pygame.K_3:
                    self._valitse_kartta(kartat[2])
                elif tapahtuma.key == pygame.K_4:
                    self._valitse_kartta(kartat[3])
                elif tapahtuma.key == pygame.K_5:
                    self._valitse_kartta(kartat[4])
                elif tapahtuma.key == pygame.K_6:
                    self._valitse_kartta(kartat[5])
                elif tapahtuma.key == pygame.K_7:
                    self._valitse_kartta(kartat[6])
                elif tapahtuma.key == pygame.K_8:
                    self._valitse_kartta(kartat[7])
                elif tapahtuma.key == pygame.K_9:
                    self._valitse_kartta(kartat[8])
                elif tapahtuma.key == pygame.K_a:
                    if self.animoitu:
                        self.animoitu = False
                    else:
                        self.animoitu = True

            if tapahtuma.type == pygame.QUIT:
                exit()

    def _nollaa_haku(self):
        '''Nollaa reitinhakuun liittyvät parametrit kartan ja algoritmin vaihdon yhteydessä.
        Samalla alustetaan uusi kartta ja luodaan ruudukko reitinhakua varten.'''

        self.algoritmi = None
        self.paivita_karttaa = True
        self.etsi = False
        self.loytyi = False
        self.animaatio_valmis = False

        self._hae_kartta()
        self._luo_ruudukko()

    def _hae_kartta(self):
        '''Hakee kartan tiedoston ja tallentaa siitä kopion tiedostoon "reitti.png".
        Otetaan talteen pikselikartta ja kartan koko.'''

        polku = os.path.dirname(__file__)
        kuva = os.path.join(polku, 'kartat', self.kartta)
        self.kuva = Image.open(kuva)
        self.kuva.save("reitti.png")
        self.pikselikartta = self.kuva.load()
        self.leveys, self.korkeus = self.kuva.size
        self.skaalauskerroin = 900/self.korkeus

    def _luo_ruudukko(self):
        '''Alustetaan uutta reitinhakua varten koskematon
        ruudukkomatriisi, joka koostuu Ruutu-olioista.'''

        self.ruudukko = []
        for y in range(self.korkeus):
            rivi = []
            for x in range(self.leveys):
                ruutu = Ruutu(y, x)
                # Ruutu on seinää jos sen RGB-arvojen summa on tarpeeksi suuri
                if sum(self.pikselikartta[x, y]) > 735:
                    ruutu.seina = True
                rivi.append(ruutu)
            self.ruudukko.append(rivi)
        if self.alku is not None:
            self._aseta_alku(self.alku.y, self.alku.x)
        if self.loppu is not None:
            self._aseta_loppu(self.loppu.y, self.loppu.x)

    def _aseta_alku(self, y, x):
        '''Päivittää alkupisteen tiedot yhdelle ruudukon Ruutu-oliolle.

        Parametrit:
            y: Alkupisteen y-koordinaatti kartalla
            x: Alkupisteen x-koordinaatti kartalla
        '''

        self.alku = self.ruudukko[y][x]
        self.alku.alku = True
        self.alku.etaisyys = 0

    def _aseta_loppu(self, y, x):
        '''Päivittää loppupisteen tiedot yhdelle ruudukon Ruutu-oliolle.

        Parametrit:
            y: Loppupisteen y-koordinaatti kartalla
            x: Loppupisteen x-koordinaatti kartalla
        '''

        self.loppu = self.ruudukko[y][x]
        self.loppu.maali = True

    def _suorita_algoritmi(self):
        '''Algoritmin suoritus ja aikamittaus.

        Palauttaa:
            Algoritmin suoritukseen kulunut aika
        '''

        aika_alku = time.time()
        while self.etsi:
            self.loytyi = self.algoritmi.etsi_lyhin()
            if self.loytyi:
                self.etsi = False
        aika_loppu = time.time()
        return aika_loppu - aika_alku

    def _suorita_animaatio(self):
        '''Animaation suorittaminen.'''

        if self.loytyi:
            algoritmi = self.algoritmi.nimi
            self._nollaa_haku()

            if algoritmi == "Dijkstra":
                self.algoritmi = Dijkstra(self.ruudukko, self.alku)
            elif algoritmi == "A*":
                self.algoritmi = AStar(self.ruudukko, self.alku, self.loppu)
            elif algoritmi == "JPS":
                self.algoritmi = JumpPointSearch(
                    self.ruudukko, self.alku, self.loppu)

        if not self.loytyi:
            self.loytyi = self.algoritmi.etsi_lyhin()
            if self.loytyi:
                self.animaatio_valmis = True

    def _paivita_kartta(self):
        '''Pikselikartan värittäminen ruudukon sisältämien Ruutu-olioiden
        ominaisuuksien perusteella. Väritetty kuva tallennetaan "reitti.png"-
        tiedostoon.'''

        for y in range(self.korkeus):
            for x in range(self.leveys):
                ruutu = self.ruudukko[y][x]
                if self.algoritmi is not None:
                    if ruutu.jonossa:
                        self.pikselikartta[x, y] = KELTAINEN
                    if ruutu.vierailtu:
                        self.pikselikartta[x, y] = TURKOOSI
                    if ruutu in self.algoritmi.reitti:
                        self.pikselikartta[x, y] = SININEN
                    if ruutu.jumppoint:
                        self.pikselikartta[x, y] = PINKKI
                if ruutu.alku:
                    self.pikselikartta[x, y] = PUNAINEN
                if ruutu.maali:
                    self.pikselikartta[x, y] = VIHREA
        self.kuva.save("reitti.png")

    def _valitse_kartta(self, kartta):
        '''Kartan vaihtamiseen liittyvien parametrin päivitys & haun nollaus.'''

        if self.kartta == kartta:
            return
        self.kartta = kartta
        self.alku = None
        self.loppu = None
        self._nollaa_haku()
