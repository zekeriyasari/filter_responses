def f1(x, a1=1, b1=2.):
    return x * a1 * b1


def f2(x, a2=1, b2=2.):
    return x * a2 * b2


cont = ((f1, {'a1': (0, 1), 'b1': (0, 2)}),
        (f2, {'a2': (0, 1), 'b2': (0, 10)}))

for pair in cont:
    func, param = pair
    print(func)
    print(param)
