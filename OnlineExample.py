import numpy as np
import pandas as pd
# List of Tuples
matrix = [(10, 56, 17),
          (np.NaN, 23, 11),
          (49, 36, 55),
          (75, np.NaN, 34),
          (89, 21, 44)
          ]
# Create a DataFrame
abc = pd.DataFrame(matrix, index=list('abcde'), columns=list('xyz'))
 
# output
print(abc)

maxValues = abc.max()
 
print(maxValues)

maxValues = abc.max(axis=1)
print(maxValues)