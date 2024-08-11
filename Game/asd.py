def a(**kwargs):
    return kwargs['a'] + kwargs['b'] + kwargs['c']

print(a(a=2, b=3, c=4))