li1 = [False, False, False, False, False, False, True, False, True, False, True]
li2 = [False, False, False, False, False, False, False, True, False, True, True]




def shift_left(li):
    li.append(False)
    del li[0]

def shift_right(li):
    li=[False]+li
    del li[len(li)-1]



def russian_peasant_signed(li1,li2):
    is_neg=False
    if li1[0]=True:
        is_neg=True
        li1 = invert(li1)
    if li2[0]=True:
        is_neg=False
        li2 = invert(li2)
    else:
        is_neg=True


    while (li2>0):
        if (li2[len(li2)-1] == True):
            res=addition(res,li1)

        li1 = shift_left(li1)
        li2 = shift_right(li2)

    if is_neg:
        res = invert(res)
    return res


def russian_peasant_unsigned(li1,li2):
    while (li2>0):
        if (li2[len(li2)-1] == True):
            res=addition(res,li1)

        li1 = shift_left(li1)
        li2 = shift_right(li2)
    return res


def divide_unsigned(divisor,dividend):
    divisor_index=len(divisor)-1
    dividend_shift=0
    while (divisor[divisor_index]!=True):
        divisor_index-=1
        dividend_shift+=1
    for i in (0,dividend_shift):
        shift_left(dividend)

    Q;
    while 1:
        t= difference(divisor,dividend)
        if t>=0:
            Q=Q+[True]
            divisor=t
        else:
            break
        shift_left(divisor)
        shift_left(dividend)
    for i in (0,dividend_shift):
        shift_right(Q)
    return Q
