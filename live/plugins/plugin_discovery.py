from pathlib import Path


class PluginDiscovery:

    def discover(self, directory):

        plugins = []

        root = Path(directory)

        if not root.exists():

            return plugins

        for item in root.iterdir():

            if item.is_dir():

                plugins.append(item.name)

        return plugins