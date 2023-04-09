import unittest

from Tests.block_test import *
from Tests.bloom_filter_test import *
from Tests.ecc_test import *
from Tests.field_element_test import *
from Tests.helper_test import *
from Tests.merkle_block_test import *
from Tests.merkle_tree_test import *
from Tests.network_test import *
from Tests.op_test import *
from Tests.point_test import *
from Tests.private_key_test import *
from Tests.s256_test import *
from Tests.script_test import *
from Tests.signature_test import *
from Tests.tx_test import *

unittest.main()

# Run particular test
# def run(test):
#     suite = TestSuite()
#     suite.addTest(test)
#     TextTestRunner().run(suite)
