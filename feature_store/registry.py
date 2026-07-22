class FeatureRegistry:

    def __init__(self):

        self.sources = {}

    def register(

        self,

        name,

        publisher

    ):

        self.sources[name] = publisher

    def publishers(self):

        return self.sources