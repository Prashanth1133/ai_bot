from datetime import datetime

from live.services.service_state import ServiceState


class ServiceManager:

    def __init__(self, registry):

        self.registry = registry

    def start(self, name):

        service = self.registry.get(name)

        if service is None:
            return

        service.state = ServiceState.RUNNING

        service.started_at = datetime.utcnow()

    def stop(self, name):

        service = self.registry.get(name)

        if service is None:
            return

        service.state = ServiceState.STOPPED

        service.stopped_at = datetime.utcnow()

    def state(self, name):

        service = self.registry.get(name)

        if service is None:
            return None

        return service.state