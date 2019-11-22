import unittest
from app.dame_genderguesser import DameGenderGuesser


class TddInPythonExample(unittest.TestCase):

    def test_genderguesser_list(self):
        dgg = DameGenderGuesser()
        g1 = dgg.guess("Sara", binary=False)
        self.assertEqual(g1, "female")
        g2 = dgg.guess("Sara", binary=True)
        self.assertEqual(g2, 0)
        g3 = dgg.guess("Laura", binary=False)
        self.assertEqual(g3, "female")
        g4 = dgg.guess("Laura", binary=True)
        self.assertEqual(g4, 0)

    def test_dame_genderguesser_gender_list(self):
        dgg = DameGenderGuesser()
        gl = dgg.gender_list()
        self.assertEqual(gl, [1, 1, 1, 1, 2, 1, 0, 0, 1, 1,
                              2, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1])
        self.assertEqual(len(gl), 21)
        self.assertEqual(dgg.females, 3)
        self.assertEqual(dgg.males, 16)
        self.assertEqual(dgg.unknown, 2)

    def test_dame_genderguesser_guess_list(self):
        dgg = DameGenderGuesser()
        self.assertEqual(['male', 'male', 'male', 'male', 'male',
                          'male', 'female', 'female', 'male', 'male'],
                         dgg.guess_list(path="files/names/partial.csv",
                                        binary=False)[0:10])
        self.assertEqual([1, 1, 1, 1, 1, 1, 0, 0, 1, 1],
                         dgg.guess_list(path="files/names/partial.csv",
                                        binary=True)[0:10])

    def test_dame_genderguesser_accuracy(self):
        dgg = DameGenderGuesser()
        self.assertTrue(dgg.accuracy(path="files/names/partial.csv") >= 0.5)
