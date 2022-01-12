

def split_list(arr, wanted_parts=1):
    """ Разбить список на подсписки """
    arrs = []
    while len(arr) > wanted_parts:
        pice = arr[:wanted_parts]
        arrs.append(pice)
        arr = arr[wanted_parts:]
    arrs.append(arr)
    return arrs
