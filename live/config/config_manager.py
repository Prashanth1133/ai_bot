from live.config.config_entry import ConfigEntry


class ConfigManager:

    def __init__(self, registry):

        self.registry = registry

    def add(

        self,

        key,

        value,

        source,

        description="",

    ):

        entry = ConfigEntry(

            key=key,

            value=value,

            source=source,

            description=description,

        )

        self.registry.register(entry)

        return entry

    def get(

        self,

        key,

        default=None,

    ):

        entry = self.registry.get(key)

        if entry is None:

            return default

        return entry.value

    def update(

        self,

        key,

        value,

    ):

        self.registry.set(

            key,

            value,

        )