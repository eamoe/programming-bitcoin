import unittest

from Tests.FieldElement_test import *
from Tests.Point_test import *
from Tests.S256_test import *
from Tests.helper_test import *
from Tests.Tx_test import *
from Tests.script_test import *
from Tests.Signature_test import *
from Tests.PrivateKey_test import *
from Tests.ecc_test import *

unittest.main()

# Run particular test
# def run(test):
#     suite = TestSuite()
#     suite.addTest(test)
#     TextTestRunner().run(suite)
