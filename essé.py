from collections import Counter
import copy
from pyts.transformation import PAA, SAX, StandardScaler
import numpy as np
import pandas as pd




file = open("E:\Robot data\Exemple.txt", "r")
element_matrix = []
tab_tmp = []
old_col, new_col = 1, 1

for line in file:
    # Spliting
    line_splt = line.split('          ')
    new_col = int(line_splt[0])
    # tab change
    if old_col != new_col:
        element_matrix.append(tab_tmp)
        tab_tmp = []
    # saving
    tab_tmp.append(float(line_splt[1]))
    old_col = new_col

# EOF
element_matrix.append(tab_tmp)
# FILE CLOSING
file.close()

########################### BEGINING ###########################

# file array transormation to numpy array
X = np.array(element_matrix) 

# standardscaler = StandardScaler(epsilon=1e-2)
# X_standardized = standardscaler.transform(X)

# paa = PAA(window_size=None, output_size=30, overlapping=True)
# X_paa = paa.transform(X_standardized)

print('END')