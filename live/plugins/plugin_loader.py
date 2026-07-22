from datetime import datetime

from live.plugins.plugin_state import PluginState


class PluginLoader:

    def load(self, plugin):

        plugin.state = PluginState.LOADED

        plugin.loaded_at = datetime.utcnow()

        return plugin

    def unload(self, plugin):

        plugin.state = PluginState.UNLOADED

        return plugin