from sklearn import datasets
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt
import numpy as np

def random_data(num_samples,num_clusters,num_features):
    X, y = make_blobs(n_samples= num_samples, centers=num_clusters, n_features=num_features,random_state=0)
#     plt.scatter(X[:, 0], X[:, 1], marker="o", c=y, s=25, edgecolor="k")
#     plt.show()
    # convert to numpy array
    res = np.array(X)
    return res