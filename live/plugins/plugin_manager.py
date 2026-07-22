from live.plugins.plugin_loader import PluginLoader
from live.plugins.plugin_state import PluginState


class PluginManager:

    def __init__(self, registry):

        self.registry = registry

        self.loader = PluginLoader()

    def load(self, name):

        plugin = self.registry.get(name)

        if plugin is None:

            return None

        return self.loader.load(plugin)

    def unload(self, name):

        plugin = self.registry.get(name)

        if plugin is None:

            return None

        return self.loader.unload(plugin)

    def enable(self, name):

        plugin = self.registry.get(name)

        if plugin:

            plugin.enabled = True

            plugin.state = PluginState.RUNNING

    def disable(self, name):

        plugin = self.registry.get(name)

        if plugin:

            plugin.enabled = False

            plugin.state = PluginState.DISABLED