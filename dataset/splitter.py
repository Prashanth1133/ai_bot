from __future__ import annotations


class DatasetSplitter:

    def split(

        self,

        features,

        labels,

        train=0.7,

        validation=0.15,

    ):

        n = len(features)

        train_end = int(n * train)

        validation_end = int(

            n * (train + validation)

        )

        return {

            "train": (

                features[:train_end],

                labels[:train_end],

            ),

            "validation": (

                features[

                    train_end:validation_end

                ],

                labels[

                    train_end:validation_end

                ],

            ),

            "test": (

                features[validation_end:],

                labels[validation_end:],

            ),

        }