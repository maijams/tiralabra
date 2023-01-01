import pygame


MUSTA = (0, 0, 0)
VALKOINEN = (255, 255, 255)
PUNAINEN = (255, 0, 0)
VIHREA = (0, 255, 0)
SININEN = (0, 0, 255)
TURKOOSI = (0, 200, 200)
KELTAINEN = (200, 200, 0)
PINKKI = (235, 52, 189)


class Renderoija:
    '''Pygame-ikkunan piirtämisestä vastaava luokka.

    Parametrit:
        ikkuna: Pygame-ikkuna
    '''

    def __init__(self, ikkuna):
        self._ikkuna = ikkuna
        self._fontti = pygame.font.SysFont("Arial", 24)

    def renderoi(self, animoitu, algoritmi, alku, loppu, loytyi, aika):
        '''Ikkunnan pääelementtien piirtäminen.

        Paramterit:
            animoitu: Boolean-arvo joka kertoo onko animaatio-toiminto aktiivinen
            algoritmi: Algoritmi-olio tai None-arvo
            alku: Alkupisteen Ruutu-olio
            loppu: Loppupisteen Ruutu-olio
            loytyi: Boolean-arvo joka kertoo onko haku löytänyt reitin
            aika: Reitinhakuun kulunut aika
        '''

        self._ikkuna.fill(MUSTA)

        self._aseta_kartta()
        self._piirra_kayttoohje(animoitu)
        self._piirra_varien_selitteet(algoritmi)

        if alku is not None:
            self._piirra_alkupisteen_tiedot(alku)
        if loppu is not None:
            self._piirra_loppupisteen_tiedot(loppu)
        if algoritmi is not None:
            self._piirra_valittu_algo(algoritmi)
        if loytyi:
            self._piirra_hakutulos(loppu, algoritmi, aika)

        pygame.display.flip()

    def _aseta_kartta(self):
        '''Asettaa kartan annettuun ikkunan kohtaan.'''

        positio_kartta = (100, 100)  # (x,y)
        kartta = pygame.transform.scale(
            pygame.image.load("reitti.png"), (900, 900))
        self._ikkuna.blit(kartta, positio_kartta)

    def _piirra_hakutulos(self, loppu, algoritmi, aika):
        '''Piirtää hakuun liittyvät mittaustulokset.

        Parametrit:
            loppu: Loppupisteen Ruutu-olio
            algoritmi: Algoritmi-olio
            aika: Reitinhakuun kulunut aika
        '''

        pituus = f'Reitin pituus: {(loppu.etaisyys):.2f}'
        tulos_pituus = self._fontti.render(pituus, True, VALKOINEN)
        self._ikkuna.blit(tulos_pituus, (1200, 400))

        solmut = f'Vieraillut solmut: {len(algoritmi.vieraillut)} kpl'
        tulos_solmut = self._fontti.render(solmut, True, VALKOINEN)
        self._ikkuna.blit(tulos_solmut, (1200, 500))

        aika = f'Haun kesto: {(aika*1000):.4f} ms'
        tulos_aika = self._fontti.render(aika, True, VALKOINEN)
        self._ikkuna.blit(tulos_aika, (1200, 600))

    def _piirra_varien_selitteet(self, algoritmi):
        '''Piirtää kartan värien selitteet kartan alapuolelle.

        Parametrit:
            algoritmi: Algoritmi-olio
        '''

        self._ikkuna.blit(self._fontti.render(
            "lähtö", True, PUNAINEN), (100, 1040))
        self._ikkuna.blit(self._fontti.render(
            "maali", True, VIHREA), (200, 1040))
        self._ikkuna.blit(self._fontti.render(
            "jonossa", True, KELTAINEN), (300, 1040))
        self._ikkuna.blit(self._fontti.render(
            "reitti", True, SININEN), (420, 1040))
        if algoritmi is not None:
            if algoritmi.nimi == "JPS":
                self._ikkuna.blit(self._fontti.render(
                    "jump point", True, PINKKI), (520, 1040))

    def _piirra_valittu_algo(self, algoritmi):
        '''Piirtää valitun algoritmin nimen.

        Parametrit:
            algoritmi: Algoritmi-olio
        '''

        self._ikkuna.blit(self._fontti.render(
            f'Valittu {algoritmi.nimi}', True, VALKOINEN), (1200, 300))

    def _piirra_alkupisteen_tiedot(self, alku):
        '''Piirtää alkupisteen koordinaatit mikäli alkupiste on valittu.

        Parametrit:
            Alku: Alkupisteen Ruutu-olio
        '''

        alkupiste = self._fontti.render(
            f'Alku     Y: {alku.y},  X: {alku.x}', True, VALKOINEN)
        self._ikkuna.blit(alkupiste, (1200, 700))

    def _piirra_loppupisteen_tiedot(self, loppu):
        '''Piirtää loppupisteen koordinaatit mikäli loppupiste on valittu.

        Parametrit:
            Loppu: Loppupisteen Ruutu-olio
        '''

        loppupiste = self._fontti.render(
            f'Loppu   Y: {loppu.y},  X: {loppu.x}', True, VALKOINEN)
        self._ikkuna.blit(loppupiste, (1200, 750))

    def _piirra_kayttoohje(self, animoitu):
        '''Piirtää ohjelman käyttöohjeet.

        Parametrit:
            animoitu: Boolean-arvo joka kertoo onko animaatio-toiminto aktiivinen'''

        ohjeteksti = "Valitse lähtöpiste klikkaamalla kartan mustalla alueella. Toinen klikkaus valitsee loppupisteen."
        ohjeteksti2 = "Käynnistä haku komennoilla:   [D]: Dijkstra,   [S]: A*,   [J]: JPS,   0 = Nollaa haku"
        ohjeteksti3 = "Valitse kartta painikkeilla [1-9]"
        ohje = self._fontti.render(ohjeteksti, True, VALKOINEN)
        ohje2 = self._fontti.render(ohjeteksti2, True, VALKOINEN)
        ohje3 = self._fontti.render(ohjeteksti3, True, VALKOINEN)

        animaatio = self._fontti.render(
            f'Animaatio [A]: {animoitu}', True, VALKOINEN)

        self._ikkuna.blit(ohje, (80, 20))
        self._ikkuna.blit(ohje2, (80, 60))
        self._ikkuna.blit(ohje3, (1150, 60))
        self._ikkuna.blit(animaatio, (1200, 150))
