import torch.nn as nn


class DirectionHead(nn.Module):

    def __init__(

        self,

        hidden

    ):

        super().__init__()

        self.fc = nn.Linear(

            hidden,

            3

        )

    def forward(self, x):

        return self.fc(x[:, -1])


class ConfidenceHead(nn.Module):

    def __init__(

        self,

        hidden

    ):

        super().__init__()

        self.fc = nn.Linear(

            hidden,

            1

        )

    def forward(self, x):

        return self.fc(x[:, -1])


class RiskHead(nn.Module):

    def __init__(

        self,

        hidden

    ):

        super().__init__()

        self.fc = nn.Linear(

            hidden,

            2

        )

    def forward(self, x):

        return self.fc(x[:, -1])