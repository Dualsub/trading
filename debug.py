import random
import common
import datetime
import math

def gen_rand_stock():
    # Gen random name
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    sym_len = random.randint(3, 5)
    symbol = ""
    for _ in range(sym_len):
        idx = random.randint(0, len(letters) - 1)
        symbol += letters[idx]

    buy_price = math.exp(random.random()*4 - 4) * 1000.0 + 10

    return symbol, buy_price