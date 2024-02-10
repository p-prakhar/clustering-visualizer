import csv
import numpy as np
from sklearn.decomposition import PCA
import pandas as pd

def read_csv(filename, header=True, reduce_dimensionality=True, n_components=3):

    data = []
    if header:
        data = pd.read_csv(filename,header=1)
        print("Header was given")
    else:
        print("No header was given")
        data =  pd.read_csv(filename, header=0)

    data = np.array(data)
    
    if reduce_dimensionality:
        data = PCA(n_components=min(n_components,len(data[0]))).fit_transform(data)

    return data

if __name__ == "__main__":
    # print the type of the input
    Y = read_csv('Mall_Customers.csv', header=True, reduce_dimensionality=False)
    # debug
    # print type of Y
    print(type(Y))
    # print shape of Y
    print(Y.shape)
    # print first 5 rows of Y
    print(Y[:5])

