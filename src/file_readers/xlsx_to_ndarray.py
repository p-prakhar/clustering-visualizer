import numpy as np
import openpyxl
from sklearn.decomposition import PCA
import pandas as pd

def read_xlsx(filename, sheet_name=None, header=False, reduce_dimensionality=True, n_components=3):
    # Load the workbook
    # workbook = openpyxl.load_workbook(filename)
    
    # # Get the active worksheet if sheet_name is not provided
    # if sheet_name is None:
    #     worksheet = workbook.active
    # else:
    #     worksheet = workbook[sheet_name]

    # data = []

    # # Iterate through the rows of the worksheet
    # for row in worksheet.iter_rows(values_only=True):
    #     # Add the row to the data list
    #     data.append(row)

    # if header:
    #     data = data[1:]

    # Convert the data into a numpy array
    data = pd.read_excel(filename)
    data = np.array(data)
    
    if reduce_dimensionality:
        data = PCA(n_components=min(len(data[0]),n_components)).fit_transform(data)

    return data

if __name__ == "__main__":
    # Print the type of the input
    Y = read_xlsx('file_readers/sample.xlsx', sheet_name='Sheet1', header=True, reduce_dimensionality=False)
    
    # Debug
    # Print type of Y
    print(type(Y))
    # Print shape of Y
    print(Y.shape)
    # Print first 5 rows of Y
    print(Y[:5])

