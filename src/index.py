import pygame
from kayttoliittyma import Kayttoliittyma


def main():
    IKKUNAN_LEVEYS = 1700
    IKKUNAN_KORKEUS = 1100
    ikkuna = pygame.display.set_mode((IKKUNAN_LEVEYS, IKKUNAN_KORKEUS))
    
    pygame.display.set_caption("Reitinhaku")
    
    kayttoliittyma = Kayttoliittyma(ikkuna)
    
    pygame.init()
    kayttoliittyma.kaynnista()
    
    
if __name__ == '__main__':
    main()