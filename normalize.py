def lcm(x, y):
   if x > y:
       z = x
   else:
       z = y
   while(True):
       if((z % x == 0) and (z % y == 0)):
           lcm = z
           break
       z += 1
   return lcm
def norm(A,B,C):
    if C==1:
        A=A*B
        B=1
        print(str(A) + " * (" + str(B) + ")^1/" + str(C))
        return;
    coeff = 0
    c_isneg=False
    if C<0:
        c_isneg=True
        C=abs(C)

    tempB=B
    while(tempB%C ==0):
        coeff+=1
        tempB=tempB//C
    coeff = (coeff//C) * C
    if coeff ==0:
        coeff =1
    B=B//coeff
    if B==1:
        C=1
    if c_isneg:
        x=A
        y=coeff
        while y != 0:
            #get gcd(A,coeff)
            #gcd will be x
            (x, y) = (y, x % y)
        A=A//x
        B=((coeff//x)**C)*B
        #coeff = coeff//x

        C=-C
    else:
        A=A*coeff
    print(str(A) + " * (" + str(B) + ")^1/" + str(C))


def multiply(A1,B1,C1,A2,B2,C2):
    if C1==C2:
        A=A1*A2
        B=B1*B2
        C=C1
        norm(A,B,C)
    if (C1<0 and C2<0) or (C1>0 and C2>0):
        is_C_neg = False
        if C1<0:
            is_C_neg = True
            C1=abs(C1)
            C2=abs(C2)
        l = lcm(C1,C2)
        B1 = B1 ** (l//C1)
        B2 = B2 ** (l//C2)
        C=l
        B=B1*B2
        A=A1*A2
        if is_C_neg:
            C=-C
        norm(A,B,C)
    else:
        print("cannot multiply cleanly (there are fractions in form of radicals)")


multiply(1,5,3,1,2,2)
