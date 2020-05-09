from Hmm.Hmm import Hmm
from Math.Vector import Vector
from Math.Matrix import Matrix


class Hmm2(Hmm):

    __pi: Matrix

    def __init__(self, states: set, observations: list, emittedSymbols: list):
        """
        A constructor of Hmm2 class which takes a Set of states, an array of observations (which also
        consists of an array of states) and an array of instances (which also consists of an array of emitted symbols).
        The constructor calls its super method to calculate the emission probabilities for those states.

        PARAMETERS
        ----------
        states : set
            A Set of states, consisting of all possible states for this problem.
        observations : list
            An array of instances, where each instance consists of an array of states.
        emittedSymbols : list
            An array of instances, where each instance consists of an array of symbols.
        """
        super().__init__(states, observations, emittedSymbols)

    def calculatePi(self, observations: list):
        """
        calculatePi calculates the prior probability matrix (initial probabilities for each state combinations)
        from a set of observations. For each observation, the function extracts the first and second states in
        that observation.  Normalizing the counts of the pair of states returns us the prior probabilities for each
        pair of states.

        PARAMETERS
        ----------
        observations : list
            A set of observations used to calculate the prior probabilities.
        """
        self.__pi = Matrix(self.stateCount, self.stateCount)
        for observation in observations:
            first = self.stateIndexes[observation[0]]
            second = self.stateIndexes[observation[1]]
            self.__pi.increment(first, second)
        self.__pi.columnWiseNormalize()

    def calculateTransitionProbabilities(self, observations: list):
        """
        calculateTransitionProbabilities calculates the transition probabilities matrix from each state to another
        state. For each observation and for each transition in each observation, the function gets the states.
        Normalizing the counts of the three of states returns us the transition probabilities.

        PARAMETERS
        ----------
        observations : list
            A set of observations used to calculate the transition probabilities.
        """
        self.transitionProbabilities = Matrix(self.stateCount * self.stateCount, self.stateCount)
        for current in observations:
            for j in range(len(current) - 2):
                fromIndex1 = self.stateIndexes[current[j]]
                fromIndex2 = self.stateIndexes[current[j + 1]]
                toIndex = self.stateIndexes[current[j + 2]]
                self.transitionProbabilities.increment(fromIndex1 * self.stateCount + fromIndex2, toIndex)
        self.transitionProbabilities.columnWiseNormalize()

    def __logOfColumn(self, column: int) -> Vector:
        """
        logOfColumn calculates the logarithm of each value in a specific column in the transition probability matrix.

        PARAMETERS
        ----------
        column : int
            Column index of the transition probability matrix.

        RETURNS
        -------
        Vector
            A vector consisting of the logarithm of each value in the column in the transition probability matrix.
        """
        result = Vector()
        for i in range(self.stateCount):
            result.add(self.safeLog(self.transitionProbabilities.getValue(i * self.stateCount + column
                                                                          // self.stateCount, column %
                                                                          self.stateCount)))
        return result

    def viterbi(self, s: list) -> list:
        """
        viterbi calculates the most probable state sequence for a set of observed symbols.

        PARAMETERS
        ----------
        s : list
            A set of observed symbols.

        RETURNS
        -------
        list
            The most probable state sequence as an {@link ArrayList}.
        """
        result = []
        sequenceLength = len(s)
        gamma = Matrix(sequenceLength, self.stateCount * self.stateCount)
        phi = Matrix(sequenceLength, self.stateCount * self.stateCount)
        qs = Vector(sequenceLength, 0)
        emission1 = s[0]
        emission2 = s[1]
        for i in range(self.stateCount):
            for j in range(self.stateCount):
                observationLikelihood = self.states[i].getEmitProb(emission1) * self.states[j].getEmitProb(emission2)
                gamma.setValue(1, i * self.stateCount + j, self.safeLog(self.__pi.getValue(i, j)) +
                               self.safeLog(observationLikelihood))
        for t in range(2, sequenceLength):
            emission = s[t]
            for j in range(self.stateCount * self.stateCount):
                current = self.__logOfColumn(j)
                previous = gamma.getRowVector(t - 1).skipVector(self.stateCount, j // self.stateCount)
                current.addVector(previous)
                maxIndex = current.maxIndex()
                observationLikelihood = self.states[j % self.stateCount].getEmitProb(emission)
                gamma.setValue(t, j, current.getValue(maxIndex) + self.safeLog(observationLikelihood))
                phi.setValue(t, j, maxIndex * self.stateCount + j // self.stateCount)
        qs.setValue(sequenceLength - 1, gamma.getRowVector(sequenceLength - 1).maxIndex())
        result.insert(0, self.states[int(qs.getValue(sequenceLength - 1)) % self.stateCount].getState())
        for i in range(sequenceLength - 2, 0, -1):
            qs.setValue(i, phi.getValue(i + 1, int(qs.getValue(i + 1))))
            result.insert(0, self.states[int(qs.getValue(i)) % self.stateCount].getState())
        result.insert(0, self.states[int(qs.getValue(1)) // self.stateCount].getState())
        return result
