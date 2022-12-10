import pygame
from PIL import Image
from ruutu import Ruutu
from dijkstra import Dijkstra
from jps import JumpPointSearch
from astar import AStar
import time
import os

MUSTA = (0,0,0)
VALKOINEN = (255,255,255)
PUNAINEN = (255,0,0)
VIHREA = (0,255,0)
SININEN = (0,0,255)
TURKOOSI = (0,200,200)
KELTAINEN = (200,200,0)
PINKKI = (235,52,189)


class Kayttoliittyma:
    def __init__(self, ikkuna):
        self.ikkuna = ikkuna
        self.ruudukko = []
        self.alku = None
        self.loppu = None


    def luo_ruudukko(self, korkeus, leveys):
        self.ruudukko = []
        for y in range(korkeus):
            rivi = []
            for x in range(leveys):
                ruutu = Ruutu(y,x)
                # Ruutu on seinää jos sen RGB-arvojen summa on tarpeeksi suuri (=ruutu riittävän vaalea)
                if sum(self.pikselikartta[x,y]) > 735:
                    ruutu.seina = True
                rivi.append(ruutu)
            self.ruudukko.append(rivi)
        if self.alku != None:
            self.aseta_alku(self.alku.y, self.alku.x)
        if self.loppu != None:
            self.aseta_loppu(self.loppu.y, self.loppu.x)
    
    
    def nollaa_haku(self):
        self.piirra = True
        self.etsi = False
        self.loytyi = False
        self.valittu_algo = None
        self.haku = None
    
    
    def alusta_kartta_ja_ruudukko(self, kartta):
        polku = os.path.dirname(__file__)
        kuva = os.path.join(polku, 'kartat', kartta)
        self.kuva = Image.open(kuva)
        self.kuva.save("reitti.png")
        self.pikselikartta = self.kuva.load()
        leveys, korkeus = self.kuva.size
        self.luo_ruudukko(korkeus, leveys)
        
        return leveys, korkeus
                    
    def aseta_alku(self, y, x):
        self.alku = self.ruudukko[y][x]
        self.alku.alku = True
        self.alku.etaisyys = 0
        
    def aseta_loppu(self, y, x):    
        self.loppu = self.ruudukko[y][x]
        self.loppu.maali = True
        
        
    def kaynnista(self):
        self.kartta = "kartta.png"
        leveys, korkeus = self.alusta_kartta_ja_ruudukko(self.kartta)
        
        self.nollaa_haku()
        
        fontti = pygame.font.SysFont("Arial", 24)
        ohjeteksti = "Valitse lähtöpiste klikkaamalla kartan mustalla alueella. Toinen klikkaus valitsee loppupisteen."
        ohje = fontti.render(ohjeteksti, True, VALKOINEN)
        ohjeteksti2 = "Käynnistä haku numeropainikkeilla:   1 = Dijkstra,   2 = A*,   3 = JPS,   5 = Nollaa haku"
        ohje2 = fontti.render(ohjeteksti2, True, VALKOINEN)
        positio_kartta = (100,100) #(x,y)
        skaalauskerroin = 900/korkeus
        skaalattu_kartta = (leveys*skaalauskerroin, korkeus*skaalauskerroin)
        

        while True:
            # Pygame käyttäjän komennot
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.MOUSEBUTTONDOWN:
                    x, y = tapahtuma.pos
                    x_kartta = round((x-positio_kartta[0]) / skaalauskerroin)
                    y_kartta = round((y-positio_kartta[1]) / skaalauskerroin)
                    
                    if x_kartta in range(leveys) and y_kartta in range(korkeus):
                        ruutu = self.ruudukko[y_kartta][x_kartta]
                        
                        # Aseta alkupiste
                        if self.alku == None and not ruutu.seina: 
                            self.aseta_alku(y_kartta, x_kartta)
                                    
                        # Aseta loppupiste
                        elif self.loppu == None and not ruutu.seina:
                            self.aseta_loppu(y_kartta, x_kartta) 
                                     
                         
                                
                # Valitse algoritmi
                elif tapahtuma.type == pygame.KEYDOWN and self.loppu != None:
                    if tapahtuma.key == pygame.K_7:
                        self.alusta_kartta_ja_ruudukko(self.kartta)
                        self.nollaa_haku()
                        self.valittu_algo = "Dijkstra"
                        jono = [(0, 0, self.alku)]
                        self.haku = Dijkstra(self.ruudukko, jono)
                        self.haku.etsi_naapurit()
                        self.etsi = True
                        
                    elif tapahtuma.key == pygame.K_8:
                        self.alusta_kartta_ja_ruudukko(self.kartta)
                        self.nollaa_haku()
                        self.valittu_algo = "A*"
                        jono = [(0, 0, self.alku)]
                        self.haku = AStar(self.loppu, self.ruudukko, jono)
                        self.haku.etsi_naapurit()
                        self.etsi = True
                            
                    elif tapahtuma.key == pygame.K_9:
                        self.alusta_kartta_ja_ruudukko(self.kartta)
                        self.nollaa_haku()
                        self.valittu_algo = "JPS"
                        jono = [(0, 0, self.alku)]
                        self.haku = JumpPointSearch(self.ruudukko, self.alku, self.loppu, jono)
                        self.etsi = True
                        
                    elif tapahtuma.key == pygame.K_0:
                        self.alku = None
                        self.loppu = None
                        self.alusta_kartta_ja_ruudukko(self.kartta)
                        self.nollaa_haku()
                        
                if tapahtuma.type == pygame.KEYDOWN:             
                    if tapahtuma.key == pygame.K_1:
                        if self.kartta == "kartta.png":
                            break
                        self.alku = None
                        self.loppu = None
                        self.kartta = "kartta.png"
                        self.alusta_kartta_ja_ruudukko(self.kartta)
                        self.nollaa_haku()
                        
                    elif tapahtuma.key == pygame.K_2:
                        if self.kartta == "kartta2.png":
                            break
                        self.alku = None
                        self.loppu = None
                        self.kartta = "kartta2.png"
                        self.alusta_kartta_ja_ruudukko(self.kartta)
                        self.nollaa_haku()   
                        
                if tapahtuma.type == pygame.QUIT:
                    exit()
            
            if self.etsi:  
                aika_alku = time.time()             
                while self.etsi:
                    self.loytyi = self.haku.etsi_lyhin()
                    if self.loytyi:
                        self.etsi = False
                aika_loppu = time.time()

            # Ikkunan piirtäminen
            self.ikkuna.fill(MUSTA)
            
            if self.piirra:
                for y in range(korkeus):
                    for x in range(leveys):
                        ruutu = self.ruudukko[y][x]
                        if self.valittu_algo != None:
                            if ruutu.jonossa:
                                self.pikselikartta[x,y] = KELTAINEN
                            if ruutu.vierailtu:
                                self.pikselikartta[x,y] = TURKOOSI
                            if ruutu in self.haku.reitti:
                                self.pikselikartta[x,y] = SININEN
                            if ruutu.jumppoint:
                                self.pikselikartta[x,y] = PINKKI
                                
                        if ruutu.alku:
                            self.pikselikartta[x,y] = PUNAINEN
                        if ruutu.maali:
                            self.pikselikartta[x,y] = VIHREA
                            
                self.kuva.save("reitti.png")
            
            
            if self.valittu_algo != None:
                self.ikkuna.blit(fontti.render(f'Valittu {self.valittu_algo}', True, VALKOINEN), (1200,300))
                
                
            if self.loytyi:
                
                self.piirra = False
                self.etsi = False
                
                pituus = f'Reitin pituus: {str(len(self.haku.reitti))} ruutua'
                tulos_pituus = fontti.render(pituus, True, VALKOINEN)
                self.ikkuna.blit(tulos_pituus, (1200,400))
        
                solmut = f'Vieraillut solmut: {str(len(self.haku.vieraillut))} kpl'
                tulos_solmut = fontti.render(solmut, True, VALKOINEN)
                self.ikkuna.blit(tulos_solmut, (1200,500))
                
                aika = f'Haun kesto: {((aika_loppu-aika_alku)*1000):.4f} ms'
                tulos_aika = fontti.render(aika, True, VALKOINEN)
                self.ikkuna.blit(tulos_aika, (1200, 600))
                
                
            kartta = pygame.transform.scale(pygame.image.load("reitti.png"), skaalattu_kartta)
            self.ikkuna.blit(kartta, positio_kartta)
            self.ikkuna.blit(ohje, (20,20))
            self.ikkuna.blit(ohje2, (20,60))
            
            if self.alku != None and self.loppu != None:
                alku = fontti.render(f'Alku     Y: {self.alku.y},  X: {self.alku.x}', True, VALKOINEN)
                self.ikkuna.blit(alku, (1200, 700))
                loppu = fontti.render(f'Loppu   Y: {self.loppu.y},  X: {self.loppu.x}', True, VALKOINEN)
                self.ikkuna.blit(loppu, (1200, 750))
                

            # Värien selitteet
            self.ikkuna.blit(fontti.render("lähtö", True, PUNAINEN), (100,1040))
            self.ikkuna.blit(fontti.render("maali", True, VIHREA), (200,1040))
            #self.ikkuna.blit(fontti.render("vierailtu", True, TURKOOSI), (300,1040))
            self.ikkuna.blit(fontti.render("jonossa", True, KELTAINEN), (300,1040))
            self.ikkuna.blit(fontti.render("reitti", True, SININEN), (420,1040))
            if self.valittu_algo == "JPS":
                self.ikkuna.blit(fontti.render("jump point", True, PINKKI), (520,1040))
        
            pygame.display.flip()        
                    

