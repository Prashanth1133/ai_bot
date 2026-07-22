from __future__ import annotations


class SignalPipeline:

    def __init__(

        self,

        generator,

        validator,

        ranking,

        registry,

    ):

        self.generator = generator

        self.validator = validator

        self.ranking = ranking

        self.registry = registry

    def process(
        self,
        predictions,
    ):

        signals = []

        for prediction in predictions:

            signal = self.generator.generate(
                prediction
            )

            if self.validator.validate(
                signal
            ):

                self.registry.update(
                    signal
                )

                signals.append(
                    signal
                )

        return self.ranking.rank(
            signals
        )