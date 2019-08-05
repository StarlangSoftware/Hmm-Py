class HmmState(object):

    def __init__(self, state: object, emissionProbabilities: dict):
        self.state = state
        self.emissionProbabilities = emissionProbabilities

    def getState(self) -> object:
        return self.state

    def getEmitProb(self, symbol: object) -> float:
        if symbol in self.emissionProbabilities:
            return self.emissionProbabilities[symbol]
        else:
            return 0.0