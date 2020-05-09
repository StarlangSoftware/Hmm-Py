import unittest

from Hmm.Hmm1 import Hmm1


class Hmm1Test(unittest.TestCase):

    def test_viterbi(self):
        states = {"HOT", "COLD"}
        observations = [["HOT", "HOT", "HOT"],
                        ["HOT", "COLD", "COLD", "COLD"],
                        ["HOT", "COLD", "HOT", "COLD"],
                        ["COLD", "COLD", "COLD", "HOT", "HOT"],
                        ["COLD", "HOT", "HOT", "COLD", "COLD"]]
        emittedSymbols = [[3, 2, 3],
                          [2, 2, 1, 1],
                          [3, 1, 2, 1],
                          [3, 1, 2, 2, 3],
                          [1, 2, 3, 2, 1]]
        hmm = Hmm1(states, observations, emittedSymbols)
        observed = [1, 1, 1, 1, 1, 1]
        observedStates = hmm.viterbi(observed)
        self.assertEqual("COLD", observedStates[0])
        self.assertEqual("COLD", observedStates[1])
        self.assertEqual("COLD", observedStates[2])
        self.assertEqual("COLD", observedStates[3])
        self.assertEqual("COLD", observedStates[4])
        self.assertEqual("COLD", observedStates[5])
        observed = [1, 2, 3, 3, 2, 1]
        observedStates = hmm.viterbi(observed)
        self.assertEqual("COLD", observedStates[0])
        self.assertEqual("HOT", observedStates[1])
        self.assertEqual("HOT", observedStates[2])
        self.assertEqual("HOT", observedStates[3])
        self.assertEqual("HOT", observedStates[4])
        self.assertEqual("COLD", observedStates[5])
        observed = [3, 3, 3, 3, 3, 3]
        observedStates = hmm.viterbi(observed)
        self.assertEqual("HOT", observedStates[0])
        self.assertEqual("HOT", observedStates[1])
        self.assertEqual("HOT", observedStates[2])
        self.assertEqual("HOT", observedStates[3])
        self.assertEqual("HOT", observedStates[4])
        self.assertEqual("HOT", observedStates[5])


if __name__ == '__main__':
    unittest.main()
