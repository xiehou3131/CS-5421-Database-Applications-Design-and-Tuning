import unittest
from prover import Prover

class TestStringMethods(unittest.TestCase):

    def test_axiom1(self):
        # Proof in PPT slide 19 out of 50
        p = Prover(["A", "B", "C", "D"])
        p.set_goal([["C"], ["A","B"]])

        p.we_know_that([["A"], ["B"]])
        p.we_know_that([["C"], ["A"]])

        p.augmentation([["A", "C"], ["A", "B", "C"]], 1, ["A", "C"])
        p.augmentation([["C"], ["A", "C"]], 2, ["C"])
        p.transitivity([["C"], ["A", "B", "C"]], 3, 4)
        p.reflexivity([["A", "B", "C"], ["A", "B"]], 6)
        p.transitivity([["C"], ["A","B"]], 6, 5)
        
        p.print_context()
        self.assertTrue(p.finished())


    def test_axiom2(self):
        # Proof in PPT slide 19 out of 50 (Different way)
        p = Prover(["A", "B", "C", "D"])
        p.set_goal([["C"], ["A","B"]])

        p.we_know_that([["A"], ["B"]])
        p.we_know_that([["C"], ["A"]])

        p.augmentation([["C"], ["A", "C"]], 2, ["C"])
        p.transitivity([["A", "C"], ["A", "B"]], 1, 2)
        p.augmentation([["A", "C"], ["A", "B"]], 4, "A")
        p.transitivity([["C"], ["A", "B"]], 5, 3)
        p.print_context()
        self.assertTrue(p.finished())


if __name__ == '__main__':
    unittest.main()