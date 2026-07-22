class WalkForwardValidation:

    def __init__(

        self,

        train,

        test,

    ):

        self.train = train

        self.test = test

    def generate(

        self,

        data,

    ):

        n = len(data)

        start = 0

        while start + self.train + self.test < n:

            train = data[

                start:

                start + self.train

            ]

            test = data[

                start + self.train:

                start + self.train + self.test

            ]

            yield train, test

            start += self.test