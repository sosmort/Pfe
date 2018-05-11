from collections import Counter
import copy

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pyts.transformation import PAA, SAX, StandardScaler
from pyts.visualization import plot_paa, plot_sax, plot_ts

# file PATH
handle = open("E:\Robot data\lp1.data.txt", "r")

# CONSTANT
OCCURENCE_NUM = 88

########################### FUNCTIONS ###########################
def merge_key(dico, level1):
    new_dico = dict()
    tab = []
    for key in dico:
        tab.append(key)
    
    for i in range(len(tab)):
        for j in range(len(level1)):
            new_dico[tab[i] + level1[j]] = 0

    return new_dico

def car_counting(x_sax, dico):
    for line in x_sax:
        for key in dico:
            counter = line.count(key)
            dico[key] += counter

def minimum_support(dico, min_sup):
    for key in dico.keys():
        if dico[key] < min_sup:
            dico.pop(key)
########################### BEGINING ###########################
file_array = []
matrix_array = []
array = []
level1 = []
for line in handle:
    """
    [0] : contain a matrix description
    The rest are a third column matrix
    """
    # if is a matrix description line
    if line=='normal\n'or line=='collision\n' or line=='obstruction\n' or line=='fr_collision\n':
        # add a array in file array
        file_array.append(matrix_array)
        matrix_array = []
        
        
        
        matrix_array.append(line[0:-1])

    elif line == "\n" :
        pass

    # if is a matrix row
    else :
        tab = line.split('\t')
        matrix_array.append(int (tab[3]))


handle.close()
print(matrix_array)

# file array transormation to numpy array
file_array_bis = []
for arr in file_array:
    file_array_bis.append(arr[1:])

file_array_bis = file_array_bis[1:]

X = np.array(file_array_bis)

#normalization of datset
standardscaler = StandardScaler(epsilon=1e-2)
X_standardized = standardscaler.transform(X)


#plot_standardscaler(X[0])

# check
# for line in X_standardized:
#     print np.std(line)

paa = PAA(window_size=None, output_size=5, overlapping=True)
X_paa = paa.transform(X_standardized)
#print X_paa[1]

plt.show(plot_paa(X_standardized[0], window_size=None, output_size=8, overlapping=True, marker='o'))

#m= int(input("ecriver un nbr de symboles: "))
# m2= int(input("nbr de raw: "))
sax = SAX(n_bins=5, quantiles='gaussian')
X_sax = sax.transform(X_paa)

#plt.show(plot_sax(X_paa, n_bins=4, quantiles='gaussian'))


"""
TODO 05/04/2018 at 14:11
"""
# 1 - Read the characters
car_dic = dict()
while True:
    car_read = str(raw_input('Please, enter the character (0 else) : '))
    if car_read == '0':
        break
    
    car_dic[car_read] = 0
    level1.append(car_read)

min_support = float(raw_input('Please, enter the minimum support : '))
a_priory_tab = {}
########### GEN ###########
level_dict = dict()
while True:
    # 1 - count
    car_counting(X_sax, car_dic)
    # print(car_dic)
    # 2 - occurence dividing
    for key in car_dic:
        level_dict[key] = car_dic[key]/88.0
    print(level_dict)
    # 3 - minimum support deleting
    a_priory_tab = copy.deepcopy(level_dict)
    minimum_support(level_dict, min_support)
    print "*****************************************"
    #print(level_dict)

    if len(level_dict) <= 0:
        break
    else:
        # 4 - merge
        car_dic = merge_key(level_dict, level1)
        print(level_dict)
        level_dict = {}
    raw_input('continue : ')

# Printing the last element
print('The last tab \n')
print(a_priory_tab)