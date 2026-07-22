from patterns.single import SinglePatternDetector
from patterns.double import DoublePatternDetector
from patterns.triple import TriplePatternDetector


class PatternEngine:

    def __init__(self):

        self.single = SinglePatternDetector()

        self.double = DoublePatternDetector()

        self.triple = TriplePatternDetector()

    def detect(self, candles):

        results = []

        results.extend(

            self.single.detect(candles)

        )

        results.extend(

            self.double.detect(candles)

        )

        results.extend(

            self.triple.detect(candles)

        )

        return results