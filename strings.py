#strings
#strings are a sequence of characters which are includes in single or double quotes
stringVar = 'string'
#or
stringVar1 = "string"
stringVar2 = 'This is special property of escaping the string\''
print(stringVar)
print(stringVar1)
print(stringVar2)

#string formatting in python
programmingLanguage = 'Python'
print("{} is a great programming language".format(programmingLanguage))

#string operations
#string.upper
print("python".upper())
#lower
print("PYTHON".lower())
#replace
print("python programming is easy".replace('easy', 'powerful'))
#slice
print("python programming is easy"[0:10])
#len
print(len("python programming is easy"))
