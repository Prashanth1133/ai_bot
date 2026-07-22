class SmartMoneyTracker:

    def __init__(self):

        self.wallets = set()

    def add_wallet(self,

                   address):

        self.wallets.add(address)

    def is_smart_money(self,

                       address):

        return address in self.wallets