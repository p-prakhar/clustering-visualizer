import copy
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.decomposition import PCA
import shutil

color_list = ['#FF0000', '#00008b', '#00FF00', '#FFFF00', '#8B008B', '#B8860B', '#2E2E2E', '#1C1C1C', '#8B2500', '#4B0082', '#A52A2A', '#8B5F65', '#4F4F4F', '#556B2F', '#800000', '#000080', '#008080', '#FF7F50', '#FFD700', '#4B0082', '#BDB76B', '#8B668B', '#32CD32', '#9932CC',
              '#8B4726', '#8B668B', '#FA8072', '#8B3A3A', '#8B6969', '#40E0D0', '#EE82EE', '#F5DEB3', '#7FFFD4', '#F0FFFF', '#F5F5DC', '#7FFF00', '#6495ED', '#DC143C', '#00008B', '#008B8B', '#B8860B', '#696969', '#006400', '#BDB76B', '#8B008B', '#556B2F', '#FF8C00', '#9932CC', '#8B0000', '#E9967A']


def kmeans(X, K, max_iters=100):
    # Initialize centroids randomly

    # centroids = X[np.random.choice(X.shape[0], K, replace=False), :]
    n_samples = len(X)
    idx = np.random.randint(n_samples)
    centroids = np.zeros((K, len(X[0])))
    centroids[0] = X[idx]

    # Step 2: Choose the remaining centroids using K-means++ algorithm
    for i in range(1, K):
        # Compute the distance from each data point to the nearest centroid
        distances = np.zeros(n_samples)
        for j in range(n_samples):
            distances[j] = np.min(np.sum((X[j] - centroids[:i]) ** 2, axis=1))

        # Choose the next centroid randomly with probability proportional to distance^2
        probabilities = distances ** 2 / np.sum(distances ** 2)
        idx = np.random.choice(n_samples, p=probabilities)
        centroids[i] = X[idx]
    labels = np.zeros(X.shape[0], dtype=int)
    all_centroids = []
    all_labels = []
    # Run iterations until convergence or maximum iterations are reached
    for i in range(max_iters):
        # Assign each data point to the closest centroid
        dists = np.sqrt(((X - centroids[:, np.newaxis])**2).sum(axis=2))
        labels = np.argmin(dists, axis=0)

        # Update centroids based on the mean of the data points in each cluster
        for k in range(K):
            centroids[k] = X[labels == k].mean(axis=0)
        all_centroids.append(copy.deepcopy(centroids))
        all_labels.append(labels[:])
#         plt.scatter(centroids[:, 0], centroids[:, 1], marker='*', s=100, c='r')
#         plt.show()
    return all_centroids, all_labels


def call_kmeans(dataset, num_clusters=3, max_iters=100):
    # os.chdir("..")
    shutil.rmtree("Outputs/Kmeans")
    os.mkdir("Outputs/Kmeans")
    all_centroids, all_labels = kmeans(dataset, num_clusters, max_iters)
    for i in range(100):
        if i != 0 and np.array_equal(all_centroids[i], all_centroids[i-1]) and np.array_equal(all_labels[i], all_labels[i-1]):
            break
        centroids = all_centroids[i]
        labels = all_labels[i]

    #     plt.scatter(Y[:, 0], Y[:, 1], c=labels)
    #     plt.scatter(centroids[:, 0], centroids[:, 1], marker='*', s=200, c='r',cmap=pylab.cm.gist_rainbow)
        colormap = [color_list[i] for i in labels]
        if len(dataset[0]) == 3:
            ax = plt.axes(projection="3d")
            ax.scatter(dataset[:, 0], dataset[:, 1], dataset[:, 2], c=colormap)
            ax.scatter(centroids[:, 0], centroids[:, 1],
                       centroids[:, 2], marker='*', s=200, c='r')
        else:
            plt.scatter(dataset[:, 0], dataset[:, 1], c=colormap)
            plt.scatter(centroids[:, 0], centroids[:, 1],
                        marker='*', s=200, c='r')
        plt.savefig('Outputs/Kmeans/output'+str(i)+".png")
        plt.clf()

    print("Kmeans Clustering Completed Successfully!")
