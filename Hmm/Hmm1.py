from Hmm.Hmm import Hmm
from Math.Vector import Vector
from Math.Matrix import Matrix


class Hmm1(Hmm):

    __pi: Vector

    def __init__(self,
                 states: set,
                 observations: list,
                 emittedSymbols: list):
        """
        A constructor of Hmm1 class which takes a Set of states, an array of observations (which also
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
        calculatePi calculates the prior probability vector (initial probabilities for each state) from a set of
        observations. For each observation, the function extracts the first state in that observation. Normalizing the
        counts of the states returns us the prior probabilities for each state.

        PARAMETERS
        ----------
        observations : list
            A set of observations used to calculate the prior probabilities.
        """
        self.__pi = Vector()
        self.__pi.initAllSame(self.state_count, 0.0)
        for observation in observations:
            index = self.state_indexes[observation[0]]
            self.__pi.addValue(index, 1.0)
        self.__pi.l1Normalize()

    def calculateTransitionProbabilities(self, observations: list):
        """
        calculateTransitionProbabilities calculates the transition probabilities matrix from each state to another
        state. For each observation and for each transition in each observation, the function gets the states.
        Normalizing the counts of the pair of states returns us the transition probabilities.

        PARAMETERS
        ----------
        observations : list
            A set of observations used to calculate the transition probabilities.
        """
        self.transition_probabilities = Matrix(self.state_count, self.state_count)
        for current in observations:
            for j in range(len(current) - 1):
                from_index = self.state_indexes[current[j]]
                to_index = self.state_indexes[current[j + 1]]
                self.transition_probabilities.increment(from_index, to_index)
        self.transition_probabilities.columnWiseNormalize()

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
        for i in range(self.state_count):
            result.add(self.safeLog(self.transition_probabilities.getValue(i, column)))
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
        sequence_length = len(s)
        gamma = Matrix(sequence_length, self.state_count)
        phi = Matrix(sequence_length, self.state_count)
        qs = Vector(sequence_length, 0)
        emission = s[0]
        for i in range(self.state_count):
            observation_likelihood = self.states[i].getEmitProb(emission)
            gamma.setValue(0, i, self.safeLog(self.__pi.getValue(i)) + self.safeLog(observation_likelihood))
        for t in range(1, sequence_length):
            emission = s[t]
            for j in range(self.state_count):
                temp_array = self.__logOfColumn(j)
                temp_array.addVector(gamma.getRowVector(t - 1))
                max_index = temp_array.maxIndex()
                observation_likelihood = self.states[j].getEmitProb(emission)
                gamma.setValue(t, j, temp_array.getValue(max_index) + self.safeLog(observation_likelihood))
                phi.setValue(t, j, max_index)
        qs.setValue(sequence_length - 1, gamma.getRowVector(sequence_length - 1).maxIndex())
        result.insert(0, self.states[int(qs.getValue(sequence_length - 1))].getState())
        for i in range(sequence_length - 2, -1, -1):
            qs.setValue(i, phi.getValue(i + 1, int(qs.getValue(i + 1))))
            result.insert(0, self.states[int(qs.getValue(i))].getState())
        return result

    def __repr__(self):
        return f"{self.__pi} {self.transition_probabilities} {self.states}"
