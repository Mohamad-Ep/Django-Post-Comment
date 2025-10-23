import random
# _______________________________________________________

def get_random_code(num):
    num1 = num-1
    return random.randint((10**num1),((10**num)-1))
# _______________________________________________________