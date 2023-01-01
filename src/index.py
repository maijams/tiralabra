import pygame
from renderoija import Renderoija
from kayttoliittyma import Kayttoliittyma


def main():
    '''Alustaa ohjelman suorituksen liittyvät oliot & käynnistää ohjelman.'''
    
    ikkunan_leveys = 1700
    ikkunan_korkeus = 1100
    ikkuna = pygame.display.set_mode((ikkunan_leveys, ikkunan_korkeus))

    pygame.display.set_caption("Reitinhaku")
    pygame.init()

    renderoija = Renderoija(ikkuna)
    kayttoliittyma = Kayttoliittyma(renderoija)

    kayttoliittyma.kaynnista()


if __name__ == '__main__':
    main()
