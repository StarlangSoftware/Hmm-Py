from Hmm.Hmm1 import Hmm1

if __name__ == '__main__':
    observed = [1, 1, 1, 1, 1, 1]
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
    hmm = Hmm1.Hmm1(states, observations, emittedSymbols)