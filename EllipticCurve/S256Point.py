from FiniteField.S256Field import *
from EllipticCurve.Point import *
from Helper.helper import encode_base58_checksum, hash160
import constants

# Redefine Point class for working with secp256k1 curve
class S256Point(Point):

    def __init__(self, x, y, a=None, b=None):
        a, b = S256Field(constants.A), S256Field(constants.B)
        if type(x) == int:
            super().__init__(x=S256Field(x), y=S256Field(y), a=a, b=b)
        # If point is initialized with the point at infinity,
        # it needs to let x and y through directly instead of using the S256Field class
        else:
            super().__init__(x=x, y=y, a=a, b=b)

    def __repr__(self):
        if self.x is None:
            return 'S256Point(infinity)'
        else:
            return 'S256Point({}, {})'.format(self.x, self.y)

    def __rmul__(self, coefficient):
        # Mod by n because nG = 0
        coef = coefficient % constants.N
        return super().__rmul__(coef)


    def verify(self, z, sig):
        # By Fermat's Little Theorem, 1/s = pow(s, N-2, N)
        s_inv = pow(sig.s, constants.N - 2, constants.N)
        # u = z / s
        u = z * s_inv % constants.N
        # v = r / s
        v = sig.r * s_inv % constants.N
        # u*G + v*P should have as the x coordinate, r
        total = u * constants.G + v * self
        return total.x.num == sig.r

    def sec(self, compressed=True):
        '''returns the binary version of the SEC format'''
        if compressed:
            if self.y.num % 2 == 0:
                return b'\x02' + self.x.num.to_bytes(32, 'big')
            else:
                return b'\x03' + self.x.num.to_bytes(32, 'big')
        else:
            return b'\x04' + self.x.num.to_bytes(32, 'big') + \
                self.y.num.to_bytes(32, 'big')
 
    def hash160(self, compressed=True):
        return hash160(self.sec(compressed))

    def address(self, compressed=True, testnet=False):
        '''Returns the address string'''
        h160 = self.hash160(compressed)
        if testnet:
            prefix = b'\x6f'
        else:
            prefix = b'\x00'
        return encode_base58_checksum(prefix + h160)
    
    @classmethod
    def parse(self, sec_bin):
        '''returns a Point object from a SEC binary (not hex)'''
        if sec_bin[0] == 4:
            x = int.from_bytes(sec_bin[1:33], 'big')
            y = int.from_bytes(sec_bin[33:65], 'big')
            return S256Point(x=x, y=y)
        # The evenness of the y coordinate is given in the first byte
        is_even = sec_bin[0] == 2
        x = S256Field(int.from_bytes(sec_bin[1:], 'big'))
        # right side of the equation y^2 = x^3 + 7
        alpha = x**3 + S256Field(constants.B)
        # solve for left side
        beta = alpha.sqrt()
        if beta.num % 2 == 0:
            even_beta = beta
            odd_beta = S256Field(constants.P - beta.num)
        else:
            even_beta = S256Field(constants.P - beta.num)
            odd_beta = beta
        if is_even:
            return S256Point(x, even_beta)
        else:
            return S256Point(x, odd_beta)
