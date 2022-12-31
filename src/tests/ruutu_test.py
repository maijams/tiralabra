import unittest
from ruutu import Ruutu


class TestRuutu(unittest.TestCase):
    def setUp(self):
        self.ruutu = Ruutu(10, 5)

    def test_alustus_toimii(self):
        self.assertNotEqual(self.ruutu, None)

    def test_alustuksen_parametrit_oikein(self):
        self.assertEqual(self.ruutu.y, 10)
        self.assertEqual(self.ruutu.x, 5)
        self.assertFalse(self.ruutu.seina)
        self.assertFalse(self.ruutu.alku)
        self.assertFalse(self.ruutu.maali)
        self.assertFalse(self.ruutu.jonossa)
        self.assertFalse(self.ruutu.vierailtu)
        self.assertFalse(self.ruutu.jumppoint)
        self.assertEqual(self.ruutu.edellinen, None)
        self.assertEqual(self.ruutu.etaisyys, None)

    def test_string_oikein(self):
        self.assertEqual(str(self.ruutu), "(10, 5)")
