from collections import defaultdict


class SessionMetrics:

    def __init__(self):

        self.connections = defaultdict(int)

        self.disconnections = defaultdict(int)

    def connected(self, name):

        self.connections[name] += 1

    def disconnected(self, name):

        self.disconnections[name] += 1

    def statistics(self):

        return {

            "connections": dict(
                self.connections
            ),

            "disconnections": dict(
                self.disconnections
            ),

        }