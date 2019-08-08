import Hmm
from Math import Vector
from Math import Matrix


class Hmm2(Hmm):

    def __init__(self, states: dict, observations: list, emittedSymbols: list):
        super().__init__(states, observations, emittedSymbols)

    def calculatePi(self, observations: list):
        self.pi = Matrix.Matrix(self.stateCount, self.stateCount)
        for observation in observations:
            first = self.stateIndexes[observation[0]]
            second = self.stateIndexes[observation[1]]
            self.pi.increment(first, second)
        self.pi.columnWiseNormalize()

    def calculateTransitionProbabilities(self, observations: list):
        self.transitionProbabilities = Matrix.Matrix(self.stateCount * self.stateCount, self.stateCount)
        for current in observations:
            for j in range(len(current) - 1):
                fromIndex1 = self.stateIndexes[current[j]]
                fromIndex2 = self.stateIndexes[current[j + 1]]
                toIndex = self.stateIndexes[current[j + 2]]
                self.transitionProbabilities.increment(fromIndex1 * self.stateCount + fromIndex2, toIndex)
        self.transitionProbabilities.columnWiseNormalize()

    def logOfColumn(self, column: int) -> Vector:
        result = Vector.Vector()
        for i in range(self.stateCount):
            result.add(self.safeLog(self.transitionProbabilities.getValue(i * self.stateCount + column // self.stateCount, column % self.stateCount)))
        return result

    def viterbi(self, s: list) -> list:
        result = []
        sequenceLength = len(s)
        gamma = Matrix.Matrix(sequenceLength, self.stateCount * self.stateCount)
        phi = Matrix.Matrix(sequenceLength, self.stateCount * self.stateCount)
        qs = Vector.Vector()
        qs.initAllSame(sequenceLength, 0)
        emission1 = s[0]
        emission2 = s[1]
        for i in range(self.stateCount):
            for j in range(self.stateCount):
                observationLikelihood = self.states[i].getEmitProb(emission1) * self.states[j].getEmitProb(emission2)
                gamma.setValue(1, i * self.stateCount + j, self.safeLog(self.pi.getValue(i, j)) + self.safeLog(observationLikelihood))
        for t in range (1, sequenceLength):
            emission = s[t]
            for j in range(self.stateCount * self.stateCount):
                current = self.logOfColumn(j)
                previous = gamma.getRowVector(t - 1).skipVector(self.stateCount, j // self.stateCount)
                current.add(previous)
                maxIndex = current.maxIndex()
                observationLikelihood = self.states[j % self.stateCount].getEmitProb(emission)
                gamma.setValue(t, j, current.getValue(maxIndex) + self.safeLog(observationLikelihood))
                phi.setValue(t, j, maxIndex * self.stateCount + j // self.stateCount)
        qs.setValue(sequenceLength - 1, gamma.getRowVector(sequenceLength - 1).maxIndex())
        result.insert(0, self.states[qs.getValue(sequenceLength - 1) % self.stateCount].getState())
        for i in range(sequenceLength - 2, 0, -1):
            qs.setValue(i, phi.getValue(i + 1, qs.getValue(i + 1)))
            result.insert(0, self.states[qs.getValue(i) % self.stateCount].getState())
        result.insert(0, self.states[qs.getValue(1) // self.stateCount].getState())
        return result