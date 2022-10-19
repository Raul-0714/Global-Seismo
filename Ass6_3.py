import math


def M_to_Mw(M):
    Mw = (2/3) * math.log(M,10) - 10.7
    print(f"Mw = {Mw:.1f}")


M = math.sqrt(11/2) * 10 ** 27
M_to_Mw(M)