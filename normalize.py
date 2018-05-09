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

    while(B%C ==0):
        coeff+=1
        B=B//C
    coeff = (coeff//C) * C
    if coeff ==0:
        coeff =1
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

norm(-6,48,-2)
