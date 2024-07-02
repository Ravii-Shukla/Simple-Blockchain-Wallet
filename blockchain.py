import uuid

class Wallet:
    def __init__(self):
        self.address = str(uuid.uuid4())
        self.balance = 100  # Initial balance for testing

class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
