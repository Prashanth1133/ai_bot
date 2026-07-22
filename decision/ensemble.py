from decision.confidence_engine import ConfidenceEngine
from decision.voting import VotingEngine


class EnsembleEngine:

    def __init__(self):

        self.confidence = ConfidenceEngine()

        self.voting = VotingEngine()

    def evaluate(

        self,

        signal,

    ):

        signal.side = self.voting.vote(signal)

        signal.confidence = self.confidence.calculate(signal)

        return signal