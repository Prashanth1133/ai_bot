class ServiceRegistry:

    def __init__(self):

        self._services = {}

    def register(self, service):

        self._services[service.name] = service

    def get(self, name):

        return self._services.get(name)

    def remove(self, name):

        self._services.pop(name, None)

    def all(self):

        return list(self._services.values())

    def clear(self):

        self._services.clear()