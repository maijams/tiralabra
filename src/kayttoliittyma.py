import pygame
from PIL import Image
from ruutu import Ruutu
from dijkstra import Dijkstra

MUSTA = (0,0,0)
VALKOINEN = (255,255,255)
PUNAINEN = (255,0,0)
VIHREA = (0,255,0)
SININEN = (0,0,255)

def kayttoliittyma():
    kuva = Image.open("kartta.png")
    pikselikartta = kuva.load()
    leveys, korkeus = kuva.size
    kuva.save("reitti.png")
    ruudukko = []
        
    # Luo ruudukko
    for y in range(korkeus):
        rivi = []
        for x in range(leveys):
            ruutu = Ruutu(y,x)
            # Ruutu on seinää jos sen RGB-arvojen summa on tarpeeksi suuri (=ruutu riittävän vaalea)
            if sum(pikselikartta[x,y]) > 735:
                ruutu.seina = True
            rivi.append(ruutu)
        ruudukko.append(rivi)

    # Lisää naapurit
    for y in range(korkeus):
        for x in range(leveys):
            ruutu = ruudukko[y][x]
            if not ruutu.seina:
                ruutu.lisaa_naapurit(ruudukko)
        
    # Aseta lähtöruutu manuaalisesti
    lahtoruutu = ruudukko[10][10]
    lahtoruutu.alku = True
    lahtoruutu.vierailtu = True

    # Aseta maaliruutu manuaalisesti
    maaliruutu = ruudukko[93][93]
    maaliruutu.maali = True
    
    pygame.init()
    pygame.display.set_caption("Reitinhaku")
    naytto = pygame.display.set_mode((2100, 1100))
    haku = Dijkstra(ruudukko, lahtoruutu, maaliruutu)
    etsi = True

    while True:
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.QUIT:
                exit()

        if etsi:
            etsi = haku.lyhin_dijkstra()

        naytto.fill(MUSTA)
        
        for y in range(leveys):
            for x in range(korkeus):
                ruutu = ruudukko[y][x]
                if ruutu.jonossa:
                    pikselikartta[x,y] = PUNAINEN
                if ruutu.vierailtu:
                    pikselikartta[x,y] = VIHREA
                if ruutu in haku.reitti:
                    pikselikartta[x,y] = SININEN
                if ruutu.alku:
                    pikselikartta[x,y] = (0,200,200)
                if ruutu.maali:
                    pikselikartta[x,y] = (200,200,0)
            
        kuva.save("reitti.png")
        kartta = pygame.transform.scale(pygame.image.load("reitti.png"), (900,900))
        naytto.blit(kartta, (100,100))
        
        pygame.display.flip()        
                

kayttoliittyma()
