import json


class FeatureSerializer:

    def serialize(

        self,

        record

    ):

        return json.dumps(

            record.features

        )