#lambda is a function that can take any number of arguments but return only one expression

x = lambda a: a+20
print(x(2))

def testLambda(n):
    return lambda a:a*n
doubler = testLambda(2)
print(doubler(5))
