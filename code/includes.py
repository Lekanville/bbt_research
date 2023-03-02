#Algorithm for getting all users from singe index
def get_users(grouped_data):
    usershat = []
    for key in grouped_data.index:
        if key not in usershat:
            usershat.append(key)
    return usershat

#Algorithm for setting up matrix for plots
def matrix_generator(total, cols):
    #total-total umber of the matrix
    #cols-the number of columns
    a=0
    i=0
    j=0
    inc = []
    while a < total:
        x = [i,j]
        a += 1
        if (a % cols) == 0:
            i += 1
            j = 0
        else:
            i = i
            j += 1
        inc.append(x)
    return inc