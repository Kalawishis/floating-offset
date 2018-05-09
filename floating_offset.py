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
The ordering is big-endian.

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
class OverflowException(Exception):
    pass

#thrown when offsets given to ABC are impossible to implement
class BadOffsetsException(Exception):
    pass

#thrown when two floating-offset numbers have incompatible types
class TypeMismatchException(Exception):
    pass

"""
This is a simple metaclass used for the purpose of modifying the behavior of type.
This metaclass allows floating-offset numbers to check compatibility using the
"==" operator and ensures type consistency. Two floating-offset numbers are of the
same type if they have the same offsets, so type(floating_offset1) == type(floating_offset2)
is enforced by this metaclass.
"""
class EqualityMeta(type):
    def __eq__(self, other):
        return self.offsets_string == other.offsets_string

"""
This is a namespace for the methods that will be contained within any instance of
an object that is created from an instance of the ABC metaclass. These methods are
called using the following form: "x": lambda self, ...: ABC_Methods.y(self, ...),
where x is the name of the method in the object and y is the name of the method in
the ABC_Methods namespace.
"""
class ABCMethods:

    NO_EXTREMES = (1, 1)
    MAPPING = {True: "1", False: "0"}
    ANTI_MAPPING = {"1": True, "0": False}
    
    #returns the lowest and highest values a signed integer with a bit vector having
    #the given length can take, in the tuple form (minimum value, maximum value)
    def signed_extremes(length):
        if length == 0:
            return ABCMethods.NO_EXTREMES
        return (-(2**(length - 1)), 2**(length - 1) - 1)

    #returns the lowest and highest values an unsigned integer with a bit vector having
    #the given length can take, in the tuple form (minimum value, maximum value)
    def unsigned_extremes(length):
        if length == 0:
            return ABCMethods.NO_EXTREMES
        return (0, 2**length - 1)

    #implementation of __init__ for floating-offset numbers
    def construct(self, a_val, b_val, c_val):
        self.bit_vector = [False]*self.vector_size  
        if not (self.a_extrema[0] <= a_val <= self.a_extrema[1] and
                self.b_extrema[0] <= b_val <= self.b_extrema[1] and
                self.c_extrema[0] <= c_val <= self.c_extrema[1]):
            raise OverflowException()

        #modification of internal bit_vector to match passed_in values
        if self.a_len != 0:
            a_bitstring = [ABCMethods.ANTI_MAPPING[bit] for bit in list(bin(a_val))[2:]]
            self.bit_vector[self.offset0 - len(a_bitstring):self.offset0] = a_bitstring
        if self.b_len != 0:
            b_bitstring = [ABCMethods.ANTI_MAPPING[bit] for bit in list(bin(b_val))[2:]]
            self.bit_vector[self.offset1 - len(b_bitstring):self.offset1] = b_bitstring
        if self.c_len != 0:
            c_bitstring = [ABCMethods.ANTI_MAPPING[bit] for bit in list(bin(c_val))[2:]]
            self.bit_vector[len(self.bit_vector) - len(c_bitstring):] = c_bitstring

    #implementation of | operator
    def bitwise_or(self, other):
        if type(self) != type(other):
            raise TypeMismatchException()
        result = type(self)()
        for bit_index in range(len(self.bit_vector)):
            result.bit_vector[bit_index] = self.bit_vector[bit_index] or other.bit_vector[bit_index]
        return result

    #implementation of & operator
    def bitwise_and(self, other):
        if type(self) != type(other):
            raise TypeMismatchException()
        result = type(self)()
        for bit_index in range(len(self.bit_vector)):
            result.bit_vector[bit_index] = self.bit_vector[bit_index] and other.bit_vector[bit_index]
        return result

    #implementation of ^ operator
    def bitwise_xor(self, other):
        if type(self) != type(other):
            raise TypeMismatchException()
        result = type(self)()
        for bit_index in range(len(self.bit_vector)):
            result.bit_vector[bit_index] = self.bit_vector[bit_index] ^ other.bit_vector[bit_index]
        return result

    #implementation of ~ operator
    def bitwise_not(self):
        result = type(self)()
        for bit_index in range(len(self.bit_vector)):
            result.bit_vector[bit_index] = not self.bit_vector[bit_index]
        return result

    #implementation of == operator
    def equals(self, other):
        #normalize?
        if type(self) != type(other):
            raise TypeMismatchException()
        for bit_index in range(len(self.bit_vector):
            if self.bit_vector[bit_index] != other.bit_vector[bit_index]:
                return False
        return True

    #the decimal value of the floating-offset number
    def represent(self):
        #print("a_extrema", self.a_extrema[0])
        #computation of signed A value
        if self.a_len == 0:
            a_val = 1
        else:
            if self.bit_vector[0] == True:
                #print("ran?")
                a_val = self.a_extrema[0]
            else:
                a_val = 0
            if self.a_len > 1:
                a_val += int("".join([ABCMethods.MAPPING[bit] for bit in self.bit_vector[1:self.offset0]]), 2)
        #print("a_val represent", a_val)

        #computation of unsigned B value (simpler)
        b_val = 1 if self.b_len == 0 else int("".join([ABCMethods.MAPPING[bit] for bit in self.bit_vector[self.offset0:self.offset1]]), 2)

        #computation of signed C value
        if self.c_len == 0:
            c_val = 1
        else:
            if self.bit_vector[self.offset1] == True:
                c_val = self.c_extrema[0]
            else:
                c_val = 0
            if self.c_len > 1:
                c_val += int("".join([ABCMethods.MAPPING[bit] for bit in self.bit_vector[self.offset1 + 1:]]), 2)

        return str(a_val*b_val**(1/c_val))

"""
This is a class factory whose instances are types for floating-offset numbers. All work
is done in the new constructor, which initializes fields and methods for the class to
give to its instances. Method definitions are given in the ABC_Methods namespace.
"""
def ABC(name, offset0, offset1, vector_size = 64):
        if not 0 <= offset0 <= offset1 <= vector_size:
            raise BadOffsetsException()
        return EqualityMeta(name, (),  {#fields
                                        "offset0": offset0,
                                        "offset1": offset1,
                                        "offsets_string": str(offset0) + ':' + str(offset1) + ':' + str(vector_size),
                                        "a_len": offset0,
                                        "b_len": offset1 - offset0,
                                        "c_len": vector_size - offset1,
                                        "a_extrema": ABCMethods.signed_extremes(offset0),
                                        "b_extrema": ABCMethods.unsigned_extremes(offset1 - offset0),
                                        "c_extrema": ABCMethods.signed_extremes(vector_size - offset1),
                                        "vector_size": vector_size,
                                        #methods
                                        "__init__": lambda self, a_val = 1, b_val = 1, c_val = 1: ABCMethods.construct(self, a_val, b_val, c_val),
                                        "__or__": lambda self, other: ABCMethods.bitwise_or(self, other),
                                        "__and__": lambda self, other: ABCMethods.bitwise_and(self, other),
                                        "__xor__": lambda self, other: ABCMethods.bitwise_xor(self, other),
                                        "__invert__": lambda self: ABCMethods.bitwise_not(self),
                                        "__str__": lambda self: ABCMethods.represent(self)})

#TESTS
    
#floating-offset classes
print("floating offset classes being constructed")
I64 = ABC("Signed 64-Bit Integer", 64, 64)
U64 = ABC("Unsigned 64-Bit Integer", 0, 64)
print()

#floating-offset numbers
print("floating-offset numbers being constructed")
i0 = I64(56)
i1 = I64(25)
u0 = U64(b_val = 10)
u1 = U64(b_val = 20)

#bitwise operations
print("bitwise operations")
i2 = ~i0
i3 = i0&i1
i4 = i0|i1
i5 = i0^i1
u2 = ~u0
u3 = u0&u1
u4 = u0|u1
u5 = u0^u1
print()

print("printing values")
print("i0", i0)
print("i1", i1)
print("i2", i2)
print("i3", i3)
print("i4", i4)
print("i5", i5)

print("u0", u0)
print("u1", u1)
print("u2", u2)
print("u3", u3)
print("u4", u4)
print("u5", u5)
print()

            
