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

#thrown when a_val, b_val, or c_val is too large
class Overflow_Exception(Exception):
    pass

#thrown when offsets given to ABC are impossible to implement
class Bad_Offsets_Exception(Exeption):
    pass

"""
This is a simple metaclass used for the purpose of modifying the behavior of type.
This metaclass allows floating-offset numbers to check compatibility using the
"==" operator and ensures type consistency. Two floating-offset numbers are of the
same type if they have the same offsets, so type(floating_offset1) == type(floating_offset2)
is enforced by this metaclass.
"""
class Equality_Meta(type):
    def __eq__(self, other):
        return self.offsets_string == other.offsets_string

"""
This is a namespace for the methods that will be contained within any instance of
an object that is created from an instance of the ABC metaclass. These methods are
called using the following form: "x": lambda self, ...: ABC_Methods.y(self, ...),
where x is the name of the method in the object and y is the name of the method in
the ABC_Methods namespace.
"""
class ABC_Methods:

    NO_EXTREMES = (0, 0)
    
    #returns the lowest and highest values a signed integer with a bit vector having
    #the given length can take, in the tuple form (minimum value, maximum value)
    def signed_extremes(length):
        if length == 0:
            return NO_EXTREMES
        return (-(2**(length - 1)), 2**(length - 1) - 1)

    #returns the lowest and highest values an unsigned integer with a bit vector having
    #the given length can take, in the tuple form (minimum value, maximum value)
    def unsigned_extremes(length):
        if length == 0:
            return NO_EXTREMES
        return (0, 2**length - 1)

    #implementation of __init__ for floating-offset numbers
    def construct(self, a_val = 1, b_val = 1, c_val = 1):
        if not (a_extrema[0] <= a_val <= a_extrema[1] and
                b_extrema[0] <= b_val <= b_extrema[1] and
                c_extrema[0] <= c_val <= c_extrema[1]):
            raise Overflow_Exception()
        self.a_val = 1 if a_len == 0 else a_val
        self.b_val = 1 if b_len == 0 else b_val
        self.c_val = 1 if c_len == 0 else c_val
        self.compose()

    #modifies internal bit_vector to reflect appropriate a, b, and c values
    def compose(self):
        a_bitstring = list(bin(self.a_val))[2:]
        b_bitstring = list(bin(self.b_val))[2:]
        c_bitstring = list(bin(self.c_val))[2:]
        self.bit_vector[offset1 - len(a_bitstring):offset1] = a_bitstring
        self.bit_vector[offset2 - len(b_bitstring):offset2] = b_bitstring
        self.bit_vector[len(base_vector) - len(c_bitstring):] = c_bitstring
      
"""
This is a class factory whose instances are types for floating-offset numbers. All work
is done in the new constructor, which initializes fields and methods for the class to
give to its instances. Method definitions are given in the ABC_Methods namespace.
"""
def ABC(name, offset0, offset1, vector_size = 64):
        if not 0 <= offset0 <= offset1 <= vector_size:
            raise Bad_Offsets_Exception()
        return Equality_Meta(name, (), {"offset0": offset0,
                                        "offset1": offset1,
                                        "offsets_string": str(offset0) + ':' + str(offset1),
                                        "a_len": offset0,
                                        "b_len": offset1 - offset0,
                                        "c_len": vector_size - offset1,
                                        "a_extrema": ABC_Methods.signed_extremes(a_len),
                                        "b_extrema": ABC_Methods.unsigned_extremes(b_len),
                                        "c_extrema": ABC_Methods.signed_extremes(c_len),
                                        "bit_vector": [0]*vector_size})


            
