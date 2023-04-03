import random
from tqdm import tqdm
import unittest
from prover import Prover


class TestStringMethods(unittest.TestCase):
    def test_axiom1(self):
        # Proof in PPT slide 19 out of 50
        p = Prover(["A", "B", "C", "D"])
        p.set_goal([["C"], ["A", "B"]], "fd")

        self.assertTrue(p.we_know_that([["A"], ["B"]], "fd"), p.errmsg)
        self.assertTrue(p.we_know_that([["C"], ["A"]], "fd"), p.errmsg)
        self.assertTrue(p.augmentation([["A", "C"], ["A", "B", "C"]], 1, ["A", "C"], "fd"), p.errmsg)
        self.assertTrue(p.augmentation([["C"], ["A", "C"]], 2, ["C"], "fd"), p.errmsg)
        self.assertTrue(p.transitivity([["C"], ["A", "B", "C"]], 3, 4), p.errmsg)
        self.assertTrue(p.reflexivity([["A", "B", "C"], ["A", "B"]]), p.errmsg)
        self.assertTrue(p.transitivity([["C"], ["A", "B"]], 6, 5), p.errmsg)

        p.print_procedure()
        self.assertTrue(p.finished())

    def test_axiom1_mvd(self):
        p = Prover(["A", "B", "C", "D"])
        p.set_goal([["C"], ["B"]], "mvd")

        self.assertTrue(p.we_know_that([["A"], ["B"]], "fd"), p.errmsg)
        self.assertTrue(p.we_know_that([["C"], ["A"]], "fd"), p.errmsg)
        self.assertTrue(p.mv_replication([["A"], ["B"]], 1), p.errmsg)
        self.assertTrue(p.mv_replication([["C"], ["A"]], 2), p.errmsg)
        self.assertTrue(p.augmentation([["A", "C"], ["A", "B", "C"]], 1, ["A", "C"], "fd"), p.errmsg)
        self.assertTrue(p.augmentation([["A", "C"], ["A", "B", "C"]], 3, ["A", "C"], "mvd"), p.errmsg)
        self.assertTrue(p.augmentation([["C"], ["A", "C"]], 2, ["C"], "fd"), p.errmsg)
        self.assertTrue(p.augmentation([["C"], ["A", "C"]], 4, ["C"], "mvd"), p.errmsg)
        self.assertTrue(p.transitivity([["C"], ["A", "B", "C"]], 7,5), p.errmsg)
        self.assertTrue(p.mv_transitivity([["C"], ["B"]], 8, 6), p.errmsg)
        
        p.print_procedure()
        self.assertTrue(p.finished())

    def test_axiom2(self):
        # Proof in PPT slide 19 out of 50 (Different way)
        p = Prover(["A", "B", "C", "D"])
        p.set_goal([["C"], ["A", "B"]], "fd")

        self.assertTrue(p.we_know_that([["A"], ["B"]], "fd"))  # step 1
        self.assertTrue(p.we_know_that([["C"], ["A"]], "fd"))  # step 2
        self.assertTrue(p.augmentation([["C"], ["A", "C"]], 2, ["C"], "fd"))  # step 3
        self.assertFalse(
            p.transitivity([["A", "C"], ["A", "B"]], 1, 2)
        )  # step 4, failed
        self.assertTrue(p.transitivity([["C"], ["B"]], 1, 2))  # step 4, ok
        self.assertTrue(p.augmentation([["A", "C"], ["A", "B"]], 4, "A", "fd"))  # step 5
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
            p.set_goal([X, Y.union(Z)], "fd")

            p.we_know_that([X, Y], "fd")  # step 1
            p.we_know_that([X, Z], "fd")  # step 2
            p.augmentation([X, X.union(Y)], 1, X, "fd")  # step 3
            p.augmentation([X.union(Y), Y.union(Z)], 2, Y, "fd")  # step 4
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
            p.set_goal([X, Z], "fd")

            p.we_know_that([X, Y], "fd")  # step 1
            p.reflexivity([Y, Z])  # step 2
            p.transitivity([X, Z], 1, 2)  # step 3

            # p.print_procedure()
            self.assertTrue(p.finished())


if __name__ == "__main__":
    unittest.main()
