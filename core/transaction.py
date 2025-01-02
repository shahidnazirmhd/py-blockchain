from dataclasses import dataclass
from collections import OrderedDict

@dataclass
class Transaction:
    sender: str
    recipient: str
    amount: float

    def to_ordered_dict(self):
        return OrderedDict([
            ('sender', self.sender),
            ('recipient', self.recipient),
            ('amount', self.amount)
        ])
    

