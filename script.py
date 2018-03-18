import matplotlib.pyplot as plt
import numpy as np
from pyts.transformation import StandardScaler
from pyts.visualization import plot_ts

# file PATH
handle = open("E:\Robot data\lp1.data.txt", "r")

file_array = []
matrix_array = []
array = []
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

# Representation begin :

#Normalization of the array
"""
def normalization():
    
   
    for f in file_array:
        #average
        avg = np.mean(f[1:])
      
        #X
        tab1 = f[1:]
        
        #n
        #lenght=len(tab1)
        
        #ecart type = (X - average) / n
        ec= np.std(tab1)
        ecartype= (tab1-avg)/ec
        
        m=np.mean(ecartype)
        print m
        
     
#print normalization()

m= int(input("ecriver un valeur: "))
n=15//m


i=1
j=0
while(i<15):
    j=i+n
    
    for line in file_array:z
        mn=np.mean(line[i:j])
        print mn
        
       
   
    print("-------------------")
    i=j
    


 
    

#print k[1:]
"""

# file array transormation
file_array_bis = []
for arr in file_array:
    file_array_bis.append(arr[1:])

file_array_bis = file_array_bis[1:]

X = np.array(file_array_bis)

standardscaler = StandardScaler(epsilon=1e-2)
X_standardized = standardscaler.transform(X)

for line in X_standardized:
    print np.mean(line)

plot_ts(X[0])