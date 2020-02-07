class HmmState(object):

    emissionProbabilities: dict
    state: object

    """
    A constructor of HmmState class which takes a State and emission probabilities as inputs and
    initializes corresponding class variable with these inputs.

    PARAMETERS
    ----------
    state : object
        Data for this state.
    emissionProbabilities : dict
        Emission probabilities for this state
    """
    def __init__(self, state: object, emissionProbabilities: dict):
        self.state = state
        self.emissionProbabilities = emissionProbabilities

    """
    Accessor method for the state variable.

    RETURNS
    -------
    object
        state variable.
    """
    def getState(self) -> object:
        return self.state

    """
    getEmitProb method returns the emission probability for a specific symbol.

    PARAMETERS
    ----------
    symbol : object 
        Symbol for which the emission probability will be get.
        
    RETURNS
    -------
    float
        Emission probability for a specific symbol.
    """
    def getEmitProb(self, symbol: object) -> float:
        if symbol in self.emissionProbabilities:
            return self.emissionProbabilities[symbol]
        else:
            return 0.0
