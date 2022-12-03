import pygame
from PIL import Image
from ruutu import Ruutu
from dijkstra import Dijkstra
from jps import Jps
from heapq import heappush, heappop


# RGB-värejä
MUSTA = (0,0,0)
VALKOINEN = (255,255,255)
PUNAINEN = (255,0,0)
VIHREA = (0,255,0)
SININEN = (0,0,255)
TURKOOSI = (0,200,200)
KELTAINEN = (200,200,0)
PINKKI = (235,52,189)


def luo_ruudukko(korkeus, leveys, pikselikartta):
    ruudukko = []
    for y in range(korkeus):
        rivi = []
        for x in range(leveys):
            ruutu = Ruutu(y,x)
            # Ruutu on seinää jos sen RGB-arvojen summa on tarpeeksi suuri (=ruutu riittävän vaalea)
            if sum(pikselikartta[x,y]) > 735:
                ruutu.seina = True
            rivi.append(ruutu)
        ruudukko.append(rivi)
    return ruudukko


def kayttoliittyma():
    # Kartan & reitin piirtämisen alustus
    kuva = Image.open("kartta.png")
    kuva.save("reitti.png")
    pikselikartta = kuva.load()
    leveys, korkeus = kuva.size
    
    ruudukko = luo_ruudukko(korkeus, leveys, pikselikartta)

    # Lisää naapurit
    for y in range(korkeus):
        for x in range(leveys):
            ruutu = ruudukko[y][x]
            if not ruutu.seina:
                ruutu.lisaa_naapurit(ruudukko)
    
    pygame.init()
    IKKUNAN_LEVEYS = 2100
    IKKUNAN_KORKEUS = 1100
    ikkuna = pygame.display.set_mode((IKKUNAN_LEVEYS, IKKUNAN_KORKEUS))
    pygame.display.set_caption("Reitinhaku")
    fontti = pygame.font.SysFont("Arial", 24)
    ohjeteksti = "Valitse Dijkstra painamalla 1 tai JPS painamalla 2 (JPS-algoritmissa ongelmia)."
    ohje = fontti.render(ohjeteksti, True, VALKOINEN)
    ohjeteksti2 = "Tämän jälkeen valitse lähtöpiste klikkaamalla hiirellä kartan mustalla alueella. Toinen klikkaus valitsee maalin ja kolmas klikkaus käynnistää haun."
    ohje2 = fontti.render(ohjeteksti2, True, VALKOINEN)
    positio_kartta = (100,100) #(x,y)
    skaalauskerroin = 9
    skaalattu_kartta = (leveys*skaalauskerroin, korkeus*skaalauskerroin)
    
    hae = True
    etsi = False
    piirra = True
    haku = None
    valittu_algo = None
    valittu_alku = False
    valittu_loppu = False

    while True:
        # Pygame käyttäjän komennot
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.QUIT:
                exit()
            # Valitse algoritmi
            if tapahtuma.type == pygame.KEYDOWN and valittu_algo == None:
                if tapahtuma.key == pygame.K_1:
                    haku = Dijkstra()
                    haku.ruudukko = ruudukko
                    valittu_algo = "dijkstra"
                elif tapahtuma.key == pygame.K_2:
                    haku = Jps()
                    haku.ruudukko = ruudukko
                    valittu_algo = "jps"
            elif tapahtuma.type == pygame.MOUSEBUTTONDOWN and valittu_algo != None:
                x, y = tapahtuma.pos
                x_kartta = round((x-positio_kartta[0]) / skaalauskerroin)
                y_kartta = round((y-positio_kartta[1]) / skaalauskerroin)
                # Aseta alkupiste
                if pygame.mouse.get_pressed()[0] and not valittu_alku:
                    if x_kartta in range(leveys) and y_kartta in range(korkeus):
                        ruutu = ruudukko[y_kartta][x_kartta]
                        if not ruutu.seina:
                            ruutu.alku = True
                            ruutu.vierailtu = True
                            haku.alku = ruutu
                            ruutu.etaisyys = 0
                            if valittu_algo == "dijkstra":
                                heappush(haku.jono, (0, ruutu))
                            elif valittu_algo == "jps":
                                heappush(haku.jono, (0, 0, ruutu))
                            #haku.jono.append(ruutu)
                            valittu_alku = True
                # Aseta loppupiste
                elif pygame.mouse.get_pressed()[0] and valittu_alku and not valittu_loppu:
                    if x_kartta in range(leveys) and y_kartta in range(korkeus):
                        ruutu = ruudukko[y_kartta][x_kartta]
                        if not ruutu.seina:
                            haku.loppu = ruutu
                            ruutu.maali = True
                            valittu_loppu = True
                # Käynnistä haku & animaatio
                elif pygame.mouse.get_pressed()[0] and valittu_alku and valittu_loppu:
                    etsi = True           
                            
        if etsi and valittu_algo == "dijkstra":
            hae = haku.lyhin_dijkstra()
            
        elif etsi and valittu_algo == "jps":
            hae = haku.lyhin_jps()

        # Ikkunan piirtäminen
        ikkuna.fill(MUSTA)
        
        if piirra and valittu_algo:
            for y in range(korkeus):
                for x in range(leveys):
                    ruutu = ruudukko[y][x]
                    if ruutu.jonossa:
                        pikselikartta[x,y] = KELTAINEN
                    if ruutu.vierailtu:
                        pikselikartta[x,y] = TURKOOSI
                    if ruutu.jumppoint:
                        pikselikartta[x,y] = PINKKI
                    if ruutu in haku.reitti:
                        pikselikartta[x,y] = SININEN
                    if ruutu.alku:
                        pikselikartta[x,y] = PUNAINEN
                    if ruutu.maali:
                        pikselikartta[x,y] = VIHREA
            kuva.save("reitti.png")
        
        if hae == False:
            piirra = False
            etsi = False
            if valittu_algo == "dijkstra":
                pituus = f'Reitin pituus: {str(len(haku.reitti))} ruutua'
                tulos_pituus = fontti.render(pituus, True, VALKOINEN)
                ikkuna.blit(tulos_pituus, (1200,400))
            elif valittu_algo == "jps":
                pituus = f'Reitin pituus: {str(haku.loppu.etaisyys)} ruutua'
                tulos_pituus = fontti.render(pituus, True, VALKOINEN)
                ikkuna.blit(tulos_pituus, (1200,400))
                solmut = f'Vieraillut solmut: {str(len(haku.reitti))} kpl'
                tulos_solmut = fontti.render(solmut, True, VALKOINEN)
                ikkuna.blit(tulos_solmut, (1200,500))
            
            
        kartta = pygame.transform.scale(pygame.image.load("reitti.png"), skaalattu_kartta)
        ikkuna.blit(kartta, positio_kartta)
        ikkuna.blit(ohje, (20,20))
        ikkuna.blit(ohje2, (20,60))
        
        if valittu_algo == "dijkstra":
            ikkuna.blit(fontti.render("Valittu Dijkstra", True, VALKOINEN), (1200,300))
        elif valittu_algo == "jps":
            ikkuna.blit(fontti.render("Valittu JPS", True, VALKOINEN), (1200,300))
        
        # Värien selitteet
        ikkuna.blit(fontti.render("lähtö", True, PUNAINEN), (100,1040))
        ikkuna.blit(fontti.render("maali", True, VIHREA), (200,1040))
        #ikkuna.blit(fontti.render("vierailtu", True, TURKOOSI), (300,1040))
        ikkuna.blit(fontti.render("jonossa", True, KELTAINEN), (300,1040))
        ikkuna.blit(fontti.render("reitti", True, SININEN), (420,1040))
        if valittu_algo == "jps":
            ikkuna.blit(fontti.render("jump point", True, PINKKI), (520,1040))
    
        pygame.display.flip()        
                

kayttoliittyma()
