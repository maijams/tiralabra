import pygame
from PIL import Image
from ruutu import Ruutu
from dijkstra import Dijkstra


def kayttoliittyma():
    kuva = Image.open("kartta.png")
    pikselikartta = kuva.load()
    leveys, korkeus = kuva.size
    kuva.save("reitti.png")
    ruudukko = []
        
    # Luo ruudukko
    for i in range(korkeus):
        rivi = []
        for j in range(leveys):
            ruutu = Ruutu(i,j)
            if pikselikartta[i,j] == (255,255,255):
                ruutu.seina = True
            rivi.append(Ruutu(i,j))
        ruudukko.append(rivi)

    # Lisää naapurit
    for i in range(korkeus):
        for j in range(leveys):
            if not ruudukko[i][j].seina:
                ruudukko[i][j].lisaa_naapurit(ruudukko)

    # Aseta lähtöruutu manuaalisesti
    lahtoruutu = ruudukko[10][10]
    lahtoruutu.alku = True
    lahtoruutu.vierailtu = True

    # Aseta maaliruutu manuaalisesti
    maaliruutu = ruudukko[93][93]
    maaliruutu.maali = True
    
    pygame.init()
    pygame.display.set_caption("Reitinhaku")
    naytto = pygame.display.set_mode((1000, 800))

    while True:
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.QUIT:
                exit()

        haku = Dijkstra(ruudukko, lahtoruutu, maaliruutu)
        haku.lyhin_dijkstra()

        naytto.fill((0,0,0))
        
        for i in range(leveys):
            for j in range(korkeus):
                ruutu = ruudukko[i][j]
                if ruutu.jonossa:
                    pikselikartta[i,j] = (200,0,0)
                if ruutu.vierailtu:
                    pikselikartta[i,j] = (0,200,0)
                if ruutu in haku.reitti:
                    pikselikartta[i,j] = (0,0,200)
                if ruutu.alku:
                    pikselikartta[i,j] = (0,200,200)
                if ruutu.maali:
                    pikselikartta[i,j] = (200,200,0)
            
        kuva.save("reitti.png")
        kartta = pygame.transform.scale(pygame.image.load("reitti.png"), (500,500))
        naytto.blit(kartta, (100,100))
        
        pygame.display.flip()        
                
