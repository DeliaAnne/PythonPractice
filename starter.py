import numpy as np
import sys

if __name__ == "__main__":
  lst1 = [5,10,0,200]
  result1 = []
  for each in lst1:
    result1.append(each+5)
  print(result1)

  lst2 = [1,2,3,'test', True, 3+2j]
  result2 = []
  for each in lst2:
    print(type(each))
    result2.append(str(each))
  print(type(result2))

  lst3 = [56,45,12,6]
  print(sys.getsizeof(lst3))

  arr = np.array(lst1)
  print(arr+5)

  arr2 = np.array(lst2)
  print(type(arr2[0]), type(arr2[4]), type(arr2[5]))

  arr3 = np.array(lst3)
  print(arr.nbytes)