from FieldElement import FieldElement
from Point import Point
import constants
# print(constants.N * constants.G)
from helper import run
from FieldElement_test import *

from Point import *

a = Point(-1, -1, 5, 7)
a2 = a + a

a = FieldElement(3, 4)
print(a)

run(FieldElementTest("test_ne"))


prime = 223
a = FieldElement(num=0, prime=prime)
b = FieldElement(num=7, prime=prime)
x1 = FieldElement(num=192, prime=prime)
y1 = FieldElement(num=105, prime=prime)
x2 = FieldElement(num=17, prime=prime)
y2 = FieldElement(num=56, prime=prime)
p1 = Point(x1, y1, a, b)
p2 = Point(x2, y2, a, b)
print(p1 + p2)
