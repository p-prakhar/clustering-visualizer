
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.decomposition import PCA

from itertools import cycle
import shutil

color_list = ['#FF0000', '#00008b', '#00FF00', '#FFFF00', '#8B008B', '#B8860B', '#2E2E2E', '#1C1C1C', '#8B2500', '#4B0082', '#A52A2A', '#8B5F65', '#4F4F4F', '#556B2F', '#800000', '#000080', '#008080', '#FF7F50', '#FFD700', '#4B0082', '#BDB76B', '#8B668B', '#32CD32', '#9932CC',
              '#8B4726', '#8B668B', '#FA8072', '#8B3A3A', '#8B6969', '#40E0D0', '#EE82EE', '#F5DEB3', '#7FFFD4', '#F0FFFF', '#F5F5DC', '#7FFF00', '#6495ED', '#DC143C', '#00008B', '#008B8B', '#B8860B', '#696969', '#006400', '#BDB76B', '#8B008B', '#556B2F', '#FF8C00', '#9932CC', '#8B0000', '#E9967A']


class AffinityPropagation():
    global A, R, S

    def similarity(self, xi, xj):
        return -((xi - xj)**2).sum()

    def create_matrices(self):
        S = np.zeros((x.shape[0], x.shape[0]))
        R = np.array(S)
        A = np.array(S)
        # compute similarity for every data point.
        for i in range(x.shape[0]):
            for k in range(x.shape[0]):
                S[i, k] = self.similarity(x[i], x[k])

        return A, R, S

    global R
    # R = create_matrices()

    def update_r(self, damping=0.9):
        global R
        v = S + A
        rows = np.arange(x.shape[0])
        # We only compare the current point to all other points,
        # so the diagonal can be filled with -infinity
        np.fill_diagonal(v, -np.inf)

        # max values
        idx_max = np.argmax(v, axis=1)
        first_max = v[rows, idx_max]

        # Second max values. For every column where k is the max value.
        v[rows, idx_max] = -np.inf
        second_max = v[rows, np.argmax(v, axis=1)]

        # Broadcast the maximum value per row over all the columns per row.
        max_matrix = np.zeros_like(R) + first_max[:, None]
        max_matrix[rows, idx_max] = second_max

        new_val = S - max_matrix

        R = R * damping + (1 - damping) * new_val

    global A

    def update_a(self, damping=0.9):
        global A
        k_k_idx = np.arange(x.shape[0])
        # set a(i, k)
        a = np.array(R)
        a[a < 0] = 0
        np.fill_diagonal(a, 0)
        a = a.sum(axis=0)  # columnwise sum
        a = a + R[k_k_idx, k_k_idx]

        # broadcasting of columns 'r(k, k) + sum(max(0, r(i', k))) to rows.
        a = np.ones(A.shape) * a

        # For every column k, subtract the positive value of k.
        # This value is included in the sum and shouldn't be
        a -= np.clip(R, 0, np.inf)
        a[a > 0] = 0

        # set(a(k, k))
        w = np.array(R)
        np.fill_diagonal(w, 0)

        w[w < 0] = 0

        a[k_k_idx, k_k_idx] = w.sum(axis=0)  # column wise sum
        A = A * damping + (1 - damping) * a

    def plot_iteration(self, A, R, iteration):
        fig = plt.figure(figsize=(12, 6))
        sol = A + R
        # every data point i chooses the maximum index k
        labels = np.argmax(sol, axis=1)
        exemplars = np.unique(labels)

        colors = dict(zip(exemplars, cycle('bgrcmyk')))
        if(len(x[0]) == 3):
            ax = plt.axes(projection="3d")
            
        for i in range(len(labels)):
            if len(x[0]) == 2:
                X = x[i][0]
                Y = x[i][1]

                if i in exemplars:
                    exemplar = i
                    edge = 'k'
                    ms = 10
                else:
                    exemplar = labels[i]
                    ms = 3
                    edge = None
                    plt.plot([X, x[exemplar][0]], [
                             Y, x[exemplar][1]], c=colors[exemplar])
                plt.plot(X, Y, 'o', markersize=ms,
                         markeredgecolor=edge, c=colors[exemplar])
            if len(x[0]) == 3:
                X = x[i][0]
                Y = x[i][1]
                Z = x[i][2]
                if i in exemplars:
                    exemplar = i
                    edge = 'k'
                    ms = 10
                else:
                    exemplar = labels[i]
                    ms = 3
                    edge = None
                    ax.plot([X, x[exemplar][0]], [Y, x[exemplar][1]],
                            [Z, x[exemplar][2]], c=colors[exemplar])
                ax.plot(X, Y, Z, 'o', markersize=ms,
                        markeredgecolor=edge, c=colors[exemplar])
        # plt.title('Number of exemplars:' + str(len(exemplars)) +
        #           ' in iteration' + str(iteration))
        plt.savefig('Outputs/AffinityPropogations/output' +
                    str(iteration)+".png")
        plt.clf()
        plt.close()
        return fig, labels, exemplars

    # In[50]:

    def __init__(self, X, damp=0.7, max_iters=100):
        global x
        x = X
        damping = float(damp)
        iterations = int(max_iters)
        global A
        global R
        global S
        A, R, S = self.create_matrices()
        preference = np.median(S)
        np.fill_diagonal(S, preference)
        # damping = 0.5

        figures = []
        last_sol = np.ones(A.shape)
        last_exemplars = np.array([])

        c = 0
        last_i = 0
        conv_iter = 0
        for i in range(iterations):
            self.update_r(damping)
            self.update_a(damping)

            sol = A + R

            exemplars = np.unique(np.argmax(sol, axis=1))

            # if last_exemplars.size != exemplars.size or np.all(last_exemplars != exemplars):

            fig, labels, exemplars = self.plot_iteration(A, R, i)
            figures.append(fig)
            last_i = i

            if (last_exemplars.size != exemplars.size or np.all(last_exemplars != exemplars)):
                conv_iter = 0
            else:
                conv_iter = conv_iter + 1

            if (conv_iter == 5):
                break
            if np.allclose(last_sol, sol):
                break

            last_sol = sol
            last_exemplars = exemplars


def call_affinity(dataset, damping_factor, max_iterations):
    shutil.rmtree("Outputs/AffinityPropogations")
    os.mkdir("Outputs/AffinityPropogations")

    AffinityPropagation(dataset, damping_factor, max_iterations)
    print("Affinity Propogation Clustering completed successfully!")
