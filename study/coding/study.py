def trans(c):
    return c*9/5+32


def trans_lam(c): return c*9/5+32


for t in (22.6, 25.8, 27.3, 29.8):
    print(t, "C : ", trans_lam(t), "F")
