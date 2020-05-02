def generator1():
    print('g11')
    yield 1
    print('g12')
    t = yield 2
    print('g13')
    yield 3
    return t


def generator2():
    g1 = generator1()
    print('g21')
    yield from g1


g2 = generator2()
print(next(g2))
print(next(g2))
print(next(g2))
