import Hmm
from Math import Vector
from Math import Matrix


class Hmm1(Hmm):

    def __init__(self, states: dict, observations: list, emittedSymbols: list):
        super().__init__(states, observations, emittedSymbols)

    def calculatePi(self, observations: list):
        self.pi = Vector.Vector()
        self.pi.initAllSame(self.stateCount, 0.0)
        for observation in observations:
            index = self.stateIndexes[observation[0]]
            self.pi.addValue(index, 1.0)
        self.pi.l1Normalize()

    def calculateTransitionProbabilities(self, observations: list):
        self.transitionProbabilities = Matrix.Matrix(self.stateCount, self.stateCount)
        for current in observations:
            for j in range(len(current) - 1):
                fromIndex = self.stateIndexes[current[j]]
                toIndex = self.stateIndexes[current[j + 1]]
                self.transitionProbabilities.increment(fromIndex, toIndex)
        self.transitionProbabilities.columnWiseNormalize()

    def logOfColumn(self, column: int) -> Vector:
        result = Vector.Vector()
        for i in range(self.stateCount):
            result.add(self.safeLog(self.transitionProbabilities.getValue(i, column)))
        return result

    def viterbi(self, s: list) -> list:
        result = []
        sequenceLength = len(s)
        gamma = Matrix.Matrix(sequenceLength, self.stateCount)
        phi = Matrix.Matrix(sequenceLength, self.stateCount)
        qs = Vector.Vector()
        qs.initAllSame(sequenceLength, 0)
        emission = s[0]
        for i in range(self.stateCount):
            observationLikelihood = self.states[i].getEmitProb(emission)
            gamma.setValue(0, i, self.safeLog(self.pi.getValue(i)) + self.safeLog(observationLikelihood))
        for t in range (1, sequenceLength):
            emission = s[t]
            for j in range(self.stateCount):
                tempArray = self.logOfColumn(j)
                tempArray.add(gamma.getRowVector(t - 1))
                maxIndex = tempArray.maxIndex()
                observationLikelihood = self.states[j].getEmitProb(emission)
                gamma.setValue(t, j, tempArray.getValue(maxIndex) + self.safeLog(observationLikelihood))
                phi.setValue(t, j, maxIndex)
        qs.setValue(sequenceLength - 1, gamma.getRowVector(sequenceLength - 1).maxIndex())
        result.insert(0, self.states[qs.getValue(sequenceLength - 1)].getState())
        for i in range(sequenceLength - 2, -1, -1):
            qs.setValue(i, phi.getValue(i + 1, qs.getValue(i + 1)))
            result.insert(0, self.states[qs.getValue(i)].getState())
        return result
