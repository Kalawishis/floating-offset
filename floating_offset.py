"""
(Add variable length bit vectors)
(Add metaclass structure)
(Consider renaming "floating-offset" notation)
(Find use for ABC(0, 0)

Python library for the implementation of floating-offset numbers
These are of the form A*B^(1/C), where A is a signed integer in two's
complement form, B is an unsigned integer, and C is a signed integer
in two's complement form. This allows for the representation of a
surprising amount of integers, rational numbers and irrational numbers.

The number is represented by a bit vector in the ABC class. The
length of the vector is currently 64-bit, but that will change
later. The ABC constructor takes two arguments representing
offsets inside the bit vector which delineate the values A, B,
and C. For example, ABC(12, 57) will make it so that the A value
is composed of the first 12 bits, the B value is composed of the
next 45 bits (12 to 57), and the C value is composed of the final
7 bits (57 to 64).

If 0 bits are allocated towards an A, B, or C value, that value is
treated as being equal to 1. This allows the ABC notation to
represent all manner of number forms. For example, ABC(64, 64) gives
all bits to the A value and is essentially a signed long long.
ABC(0, 64) gives all bits to the B value and is essentially an unsigned
long long. ABC(0, 0) gives all bits to the C value, but since A and B
are 1 the number is going to be 1 no matter what (in other words, doing
this is pointless at the moment). 

Rational numbers can be easily represented by simply making C equal to
negative 1. This will have the effect of making A the numerator and B
the denominator. Irrational numbers are created by setting C to a value
other than 1, which would give roots. For example, sqrt(2)/2 can be
represented with A = 1, B = 2, and C = -2. This is 1*2^(1/-2) which is
1/sqrt(2) which is sqrt(2)/2. Setting C = 0 gives NaN. 

Example code:

X_Type = ABC(32, 48) #x_type a class for floating-offsets with those specific offsets
Y_Type = ABC(16, 32) #see above

x0 = X_Type(a_val = 42) #keyword argument for initial value of A: default 1
                        #same behavior and implementation for b_val, c_val
x1 = X_Type(a_val = 43)
y0 = Y_Type(a_val = 42)
x2 = X_Type(b_val = 42) 

x0 == x1 #false
x0 + 1 == x1 #true
x0 == y0 #error, comparing w/ different offsets is a type error,
         #even if numerically the same
x0*x1 == x1*x0 #true (always follows commutativity, associativity, general rules of
                arithmetic as defined mathematically by the operations)
x0 + x1 - x0 == x1 #true
x0 == x2 #true, x numerically equals w although they were constructed differently


In due time all operations will be listed.

It's important to note that ABCs with different offsets are not
different instances of the same class, they are different classes
themselves. This will become apparent when ABC becomes a metaclass
and I define U64, Rational, Complex, etc. as instances of that metaclass
(remember, instances of a metaclass are classes and types in their
own right).
"""

BASE_VECTOR = [0]*64

class ABC(type):
    def __init__(self, ab_offset, bc_offset, val = 0):
            
