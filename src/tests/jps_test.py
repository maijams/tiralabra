import unittest
from ruutu import Ruutu
from jps import JumpPointSearch


class TestJumpPointSearch(unittest.TestCase):
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
        jps = JumpPointSearch(self.ruudukko, self.alku, self.loppu)

        self.assertNotEqual(jps, None)
        self.assertEqual(jps.nimi, "JPS")
        self.assertEqual(jps.ruudukko, self.ruudukko)
        self.assertEqual(jps.loppu, self.loppu)
        self.assertEqual(jps.jono, [(0, 0, self.alku)])
        self.assertEqual(jps.vieraillut, [])
        self.assertEqual(jps.reitti, [])
        self.assertEqual(jps.laskuri, 0)

    def test_jps_metodi_etsi_lyhin_suora(self):
        self.aseta_alku(1, 1)
        self.aseta_loppu(3, 1)
        jps = JumpPointSearch(self.ruudukko, self.alku, self.loppu)
        while True:
            tulos = jps.etsi_lyhin()
            if tulos:
                break

        self.assertTrue(tulos)
        self.assertEqual(self.loppu.etaisyys, 2)
        self.assertEqual(len(jps.reitti), 3)

    def test_jps_metodi_etsi_lyhin_diagonaali(self):
        self.aseta_alku(6, 1)
        self.aseta_loppu(4, 3)
        jps = JumpPointSearch(self.ruudukko, self.alku, self.loppu)
        while True:
            tulos = jps.etsi_lyhin()
            if tulos:
                break

        self.assertTrue(tulos)
        self.assertAlmostEqual(self.loppu.etaisyys, 2.82, places=1)
        self.assertEqual(len(jps.reitti), 3)

    def test_jps_metodi_etsi_lyhin_seinan_ohitus(self):
        self.aseta_alku(1, 3)
        self.aseta_loppu(3, 3)
        jps = JumpPointSearch(self.ruudukko, self.alku, self.loppu)
        while True:
            tulos = jps.etsi_lyhin()
            if tulos:
                break

        self.assertTrue(tulos)
        self.assertAlmostEqual(self.loppu.etaisyys, 2.82, places=1)
        self.assertEqual(len(jps.reitti), 3)

    def test_jps_metodi_etsi_lyhin_seinan_kierto(self):
        self.aseta_alku(1, 6)
        self.aseta_loppu(4, 5)
        jps = JumpPointSearch(self.ruudukko, self.alku, self.loppu)
        while True:
            tulos = jps.etsi_lyhin()
            if tulos:
                break

        self.assertTrue(tulos)
        self.assertAlmostEqual(self.loppu.etaisyys, 3.41, places=1)
        self.assertEqual(len(jps.reitti), 4)
