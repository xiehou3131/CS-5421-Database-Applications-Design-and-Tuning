import random
from tqdm import tqdm
import unittest
from prover import Prover


class TestStringMethods(unittest.TestCase):
    def test_axiom1(self):
        # Proof in PPT slide 19 out of 50
        p = Prover(["A", "B", "C", "D"])
        p.set_goal([["C"], ["A", "B"]])

        self.assertTrue(p.we_know_that([["A"], ["B"]]))
        self.assertTrue(p.we_know_that([["C"], ["A"]]))
        self.assertTrue(p.augmentation([["A", "C"], ["A", "B", "C"]], 1, ["A", "C"]))
        self.assertTrue(p.augmentation([["C"], ["A", "C"]], 2, ["C"]))
        self.assertTrue(p.transitivity([["C"], ["A", "B", "C"]], 3, 4))
        self.assertTrue(p.reflexivity([["A", "B", "C"], ["A", "B"]]))
        self.assertTrue(p.transitivity([["C"], ["A", "B"]], 6, 5))

        p.print_procedure()
        self.assertTrue(p.finished())

    def test_axiom2(self):
        # Proof in PPT slide 19 out of 50 (Different way)
        p = Prover(["A", "B", "C", "D"])
        p.set_goal([["C"], ["A", "B"]])

        self.assertTrue(p.we_know_that([["A"], ["B"]]))  # step 1
        self.assertTrue(p.we_know_that([["C"], ["A"]]))  # step 2
        self.assertTrue(p.augmentation([["C"], ["A", "C"]], 2, ["C"]))  # step 3
        self.assertFalse(
            p.transitivity([["A", "C"], ["A", "B"]], 1, 2)
        )  # step 4, failed
        self.assertTrue(p.transitivity([["C"], ["B"]], 1, 2))  # step 4, ok
        self.assertTrue(p.augmentation([["A", "C"], ["A", "B"]], 4, "A"))  # step 5
        self.assertTrue(p.transitivity([["C"], ["A", "B"]], 5, 3))  # step 6

        p.print_procedure()
        self.assertTrue(p.finished())

    def test_union_rule(self):
        for _ in range(1000):
            NATTR = random.randint(10, 100)
            R = []
            for i in range(NATTR):
                R.append(f"A{i}")

            X = set(random.sample(list(R), random.randint(1, NATTR)))
            Y = set(random.sample(list(R), random.randint(1, NATTR)))
            Z = set(random.sample(list(R), random.randint(1, NATTR)))

            p = Prover(R)
            p.set_goal([X, Y.union(Z)])

            p.we_know_that([X, Y])  # step 1
            p.we_know_that([X, Z])  # step 2
            p.augmentation([X, X.union(Y)], 1, X) # step 3
            p.augmentation([X.union(Y), Y.union(Z)], 2, Y)  # step 4
            p.transitivity([X, Y.union(Z)], 3, 4)  # step 5

            # p.print_procedure()
            self.assertTrue(p.finished())

    def test_decomposition_rule(self):
        for _ in range(1000):
            NATTR = random.randint(10, 100)
            R = []
            for i in range(NATTR):
                R.append(f"A{i}")

            X = set(random.sample(list(R), random.randint(1, NATTR)))
            Y = set(random.sample(list(R), random.randint(1, NATTR)))
            Z = set(random.sample(list(Y), random.randint(1, len(Y))))

            p = Prover(R)
            p.set_goal([X, Z])

            p.we_know_that([X, Y])  # step 1
            p.reflexivity([Y, Z])  # step 2
            p.transitivity([X, Z], 1, 2)  # step 3

            # p.print_procedure()
            self.assertTrue(p.finished())


if __name__ == "__main__":
    unittest.main()
