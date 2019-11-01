#Array is the special variable which can hold more than one value at a time
#Python has no built in support for arrays. Python lists are used for this purpose instead
arr = [1,3,5,7, 'test', 'test1']
print(arr)
print('---------------')
print('Finding Length')
print(len(arr))

print('---------------')
print('remove all elements from array we use "clear" function')
arr.clear()
print(arr)

print('---------------')
print('Add an element in the end of the array we use "append" function')
arr.append(2)
print(arr)


print('---------------')
print('to return a copy of a list we use "copy" function')
arr1 = arr.copy()
print(arr1)


print('---------------')
print('to return a number of elements with specified value we use "count" function')
arr1 = arr.count(2)
print(arr1)


print('---------------')
print('Iterating Arrays')
for elem in arr:
    print(elem)

print('---------------')
print('Sorting Arrays')
#Sort function can be used only on the numeric indexed array
numericArray = [2,88,23,5,77,33,46,24];
numericArray.sort()
print(numericArray)
