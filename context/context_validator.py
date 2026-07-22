class ContextValidator:

    REQUIRED = (

        "market",

        "orderflow",

        "indicators",

    )

    @classmethod
    def validate(

        cls,

        snapshot,

    ):

        for name in cls.REQUIRED:

            if getattr(snapshot, name) is None:

                return False

        return True