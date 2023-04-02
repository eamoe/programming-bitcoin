from Helper.helper import (
    hash256
)

class Tx:

    def __init__(self, version, tx_ins, tx_outs, locktime, testnet=False):
        self.version = version
        self.tx_ins = tx_ins
        self.tx_outs = tx_outs
        self.locktime = locktime
        # Define the network the transaction is on to be able to validate it fully
        self.testnet = testnet

    def __repr__(self):
        tx_ins = ''
        for tx_in in self.tx_ins:
            tx_ins += tx_in.__repr__() + '\n'
        tx_outs = ''
        for tx_out in self.tx_outs:
            tx_outs += tx_out.__repr__() + '\n'
        return 'tx: {}\nversion: {}\ntx_ins:\n{}tx_outs:\n{}locktime: {}'.format(
            self.id(),
            self.version,
            tx_ins,
            tx_outs,
            self.locktime,
        )
    
    def id(self):
        # Human-readable hexadecimal of the transaction hash
        return self.hash().hex()
    
    def hash(self):
        # Binary hash of the legacy serialization
        return hash256(self.serialize())[::-1]
    
    # This method has to be a class method as the serialization will return a new instance of a Tx object
    @classmethod
    def parse(cls, stream):
        # The read method allows to parse on the fly so that it will not need to wait on I/O
        serialized_version = stream.read(4)
