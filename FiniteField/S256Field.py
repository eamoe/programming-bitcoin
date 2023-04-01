from FiniteField.FieldElement import *

import constants

# Redefine FieldElement class for working with secp256k1 curve
class S256Field(FieldElement):

    # Subclassing the FieldElement class in order not to pass in P all the time
    def __init__(self, num, prime=None):
        super().__init__(num=num, prime=constants.P)

    def __repr__(self):
        # Display a 256-bit number consistently by filling 64 characters to see any leading zeros
        return '{:x}'.format(self.num).zfill(64)

    # tag::source2[]
    def sqrt(self):
        return self**((constants.P + 1) // 4)
    # end::source2[]
