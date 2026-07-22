class ConfigValidator:

    def validate(

        self,

        required_keys,

        configuration,

    ):

        missing = []

        for key in required_keys:

            if key not in configuration:

                missing.append(key)

        return missing