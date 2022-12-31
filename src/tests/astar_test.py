import unittest
from ruutu import Ruutu
from astar import AStar


class TestAStar(unittest.TestCase):
    def setUp(self):
        ''' [########
             #....#.#,
             #.##...#,
             #.....##,
             ##.....#,
             #......#,
             #...#..#,
             ########] '''

        self.ruudukko = []
        for y in range(8):
            rivi = []
            for x in range(8):
                ruutu = Ruutu(y, x)
                rivi.append(ruutu)
            self.ruudukko.append(rivi)

        self.ruudukko[1][5].seina = True
        self.ruudukko[2][2].seina = True
        self.ruudukko[2][3].seina = True
        self.ruudukko[3][6].seina = True
        self.ruudukko[4][1].seina = True
        self.ruudukko[6][4].seina = True

        for i in range(8):
            self.ruudukko[0][i].seina = True
            self.ruudukko[7][i].seina = True
            self.ruudukko[i][0].seina = True
            self.ruudukko[i][7].seina = True

    def aseta_alku(self, y, x):
        self.alku = self.ruudukko[y][x]
        self.alku.alku = True
        self.alku.etaisyys = 0

    def aseta_loppu(self, y, x):
        self.loppu = self.ruudukko[y][x]
        self.loppu.maali = True

    def test_alustus_toimii(self):
        self.aseta_alku(1, 1)
        self.aseta_loppu(3, 1)
        astar = AStar(self.ruudukko, self.alku, self.loppu)

        self.assertNotEqual(astar, None)
        self.assertEqual(astar.nimi, "A*")
        self.assertEqual(astar.ruudukko, self.ruudukko)
        self.assertEqual(astar.loppu, self.loppu)
        self.assertEqual(astar.jono, [(0, 0, self.alku)])
        self.assertEqual(astar.vieraillut, [])
        self.assertEqual(astar.reitti, [])
        self.assertEqual(astar.laskuri, 0)

    def test_astar_metodi_etsi_lyhin_suora(self):
        self.aseta_alku(1, 1)
        self.aseta_loppu(3, 1)
        astar = AStar(self.ruudukko, self.alku, self.loppu)
        while True:
            tulos = astar.etsi_lyhin()
            if tulos:
                break

        self.assertTrue(tulos)
        self.assertEqual(self.loppu.etaisyys, 2)
        self.assertEqual(len(astar.reitti), 3)

    def test_astar_metodi_etsi_lyhin_diagonaali(self):
        self.aseta_alku(6, 1)
        self.aseta_loppu(4, 3)
        astar = AStar(self.ruudukko, self.alku, self.loppu)
        while True:
            tulos = astar.etsi_lyhin()
            if tulos:
                break

        self.assertTrue(tulos)
        self.assertAlmostEqual(self.loppu.etaisyys, 2.82, places=1)
        self.assertEqual(len(astar.reitti), 3)

    def test_astar_metodi_etsi_lyhin_seinan_ohitus(self):
        self.aseta_alku(1, 3)
        self.aseta_loppu(3, 3)
        astar = AStar(self.ruudukko, self.alku, self.loppu)
        while True:
            tulos = astar.etsi_lyhin()
            if tulos:
                break

        self.assertTrue(tulos)
        self.assertAlmostEqual(self.loppu.etaisyys, 2.82, places=1)
        self.assertEqual(len(astar.reitti), 3)

    def test_astar_metodi_etsi_lyhin_seinan_kierto(self):
        self.aseta_alku(1, 6)
        self.aseta_loppu(4, 5)
        astar = AStar(self.ruudukko, self.alku, self.loppu)
        while True:
            tulos = astar.etsi_lyhin()
            if tulos:
                break

        self.assertTrue(tulos)
        self.assertAlmostEqual(self.loppu.etaisyys, 3.41, places=1)
        self.assertEqual(len(astar.reitti), 4)
