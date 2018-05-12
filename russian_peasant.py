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


