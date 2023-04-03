from Helper.helper import (
    hash256,
    little_endian_to_int
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
    def parse(cls, s, testnet=False):
        # The read method allows to parse on the fly so that it will not need to wait on I/O
        version = little_endian_to_int(s.read(4))
        return cls(version, None, None, None, testnet=testnet)




# tag::source1[]
class Tx:

    def __init__(self, version, tx_ins, tx_outs, locktime, testnet=False):
        self.version = version
        self.tx_ins = tx_ins  # <1>
        self.tx_outs = tx_outs
        self.locktime = locktime
        self.testnet = testnet  # <2>

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

    def id(self):  # <3>
        '''Human-readable hexadecimal of the transaction hash'''
        return self.hash().hex()

    def hash(self):  # <4>
        '''Binary hash of the legacy serialization'''
        return hash256(self.serialize())[::-1]
    # end::source1[]

    @classmethod
    def parse(cls, s, testnet=False):
        '''Takes a byte stream and parses the transaction at the start
        return a Tx object
        '''
        # s.read(n) will return n bytes
        # version is an integer in 4 bytes, little-endian
        # num_inputs is a varint, use read_varint(s)
        # parse num_inputs number of TxIns
        # num_outputs is a varint, use read_varint(s)
        # parse num_outputs number of TxOuts
        # locktime is an integer in 4 bytes, little-endian
        # return an instance of the class (see __init__ for args)
        version = little_endian_to_int(s.read(4))
        return cls(version, None, None, None, testnet=testnet)

    # tag::source6[]
    def serialize(self):
        '''Returns the byte serialization of the transaction'''
        result = int_to_little_endian(self.version, 4)
        result += encode_varint(len(self.tx_ins))
        for tx_in in self.tx_ins:
            result += tx_in.serialize()
        result += encode_varint(len(self.tx_outs))
        for tx_out in self.tx_outs:
            result += tx_out.serialize()
        result += int_to_little_endian(self.locktime, 4)
        return result
    # end::source6[]

    def fee(self):
        '''Returns the fee of this transaction in satoshi'''
        # initialize input sum and output sum
        # use TxIn.value() to sum up the input amounts
        # use TxOut.amount to sum up the output amounts
        # fee is input sum - output sum
        raise NotImplementedError


# tag::source2[]
class TxIn:
    def __init__(self, prev_tx, prev_index, script_sig=None, sequence=0xffffffff):
        self.prev_tx = prev_tx
        self.prev_index = prev_index
        if script_sig is None:  # <1>
            self.script_sig = Script()
        else:
            self.script_sig = script_sig
        self.sequence = sequence

    def __repr__(self):
        return '{}:{}'.format(
            self.prev_tx.hex(),
            self.prev_index,
        )
    # end::source2[]

    @classmethod
    def parse(cls, s):
        '''Takes a byte stream and parses the tx_input at the start
        return a TxIn object
        '''
        # prev_tx is 32 bytes, little endian
        # prev_index is an integer in 4 bytes, little endian
        # use Script.parse to get the ScriptSig
        # sequence is an integer in 4 bytes, little-endian
        # return an instance of the class (see __init__ for args)
        raise NotImplementedError

    # tag::source5[]
    def serialize(self):
        '''Returns the byte serialization of the transaction input'''
        result = self.prev_tx[::-1]
        result += int_to_little_endian(self.prev_index, 4)
        result += self.script_sig.serialize()
        result += int_to_little_endian(self.sequence, 4)
        return result
    # end::source5[]

    # tag::source8[]
    def fetch_tx(self, testnet=False):
        return TxFetcher.fetch(self.prev_tx.hex(), testnet=testnet)

    def value(self, testnet=False):
        '''Get the output value by looking up the tx hash.
        Returns the amount in satoshi.
        '''
        tx = self.fetch_tx(testnet=testnet)
        return tx.tx_outs[self.prev_index].amount

    def script_pubkey(self, testnet=False):
        '''Get the ScriptPubKey by looking up the tx hash.
        Returns a Script object.
        '''
        tx = self.fetch_tx(testnet=testnet)
        return tx.tx_outs[self.prev_index].script_pubkey
    # end::source8[]


# tag::source3[]
class TxOut:

    def __init__(self, amount, script_pubkey):
        self.amount = amount
        self.script_pubkey = script_pubkey

    def __repr__(self):
        return '{}:{}'.format(self.amount, self.script_pubkey)
    # end::source3[]

    @classmethod
    def parse(cls, s):
        '''Takes a byte stream and parses the tx_output at the start
        return a TxOut object
        '''
        # amount is an integer in 8 bytes, little endian
        # use Script.parse to get the ScriptPubKey
        # return an instance of the class (see __init__ for args)
        raise NotImplementedError

    # tag::source4[]
    def serialize(self):  # <1>
        '''Returns the byte serialization of the transaction output'''
        result = int_to_little_endian(self.amount, 8)
        result += self.script_pubkey.serialize()
        return result
    # end::source4[]
