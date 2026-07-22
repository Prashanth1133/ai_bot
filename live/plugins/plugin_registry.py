class PluginRegistry:

    def __init__(self):

        self._plugins = {}

    def register(self, plugin):

        self._plugins[plugin.name] = plugin

    def unregister(self, name):

        self._plugins.pop(name, None)

    def get(self, name):

        return self._plugins.get(name)

    def plugins(self):

        return list(self._plugins.values())

    def clear(self):

        self._plugins.clear()