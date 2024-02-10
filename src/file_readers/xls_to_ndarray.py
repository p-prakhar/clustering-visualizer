# TODO
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA

def read_xls(filename, reduce_dimensionality=True, n_components=3):
    # Load the workbook
    data = pd.read_excel(filename)
    # Convert the data into a numpy array
    data = np.array(data)
    
    
    data = PCA(n_components=n_components).fit_transform(data)

    return data

if __name__ == "__main__":
    # Print the type of the input
    Y = read_xls('sample.xlsx', sheet_name='Sheet1', header=True, reduce_dimensionality=False)
    
    # Debug
    # Print type of Y
    print(type(Y))
    # Print shape of Y
    print(Y.shape)
    # Print first 5 rows of Y
    print(Y[:5])
