from Hmm import HmmState
from DataStructure import CounterHashMap
import math


class Hmm(object):

    def calculatePi(self, observations: list):
        pass

    def calculateTransitionProbabilities(self, observations: list):
        pass

    def viterbi(self, s: list) -> list:
        pass

    def __init__(self, states: dict, observations: list, emittedSymbols: list):
        i = 0
        self.stateCount = len(states)
        self.states = []
        self.stateIndexes = {}
        for state in states:
            self.stateIndexes[state] = i
            i = i + 1
        self.calculatePi(observations)
        for state in states:
            emissionProbabilities = self.calculateEmissionProbabilities(state, observations, emittedSymbols)
            self.states.append(HmmState.HmmState(state, emissionProbabilities))
        self.calculateTransitionProbabilities(observations)

    def calculateEmissionProbabilities(self, state: object,  observations: list, emittedSymbols: list) -> dict:
        counts = CounterHashMap.CounterHashMap()
        emissionProbabilities = {}
        for i in range(len(observations)):
            for j in range(len(observations[i])):
                currentState = observations[i][j]
                currentSymbol = emittedSymbols[i][j]
                if currentState == state:
                    counts.put(currentSymbol)
        total = counts.sumOfCounts()
        for symbol in counts:
            emissionProbabilities[symbol] = counts[symbol] / total
        return emissionProbabilities

    def safeLog(self, x: float) -> float:
        if x <= 0:
            return -1000
        else:
            return math.log(x)