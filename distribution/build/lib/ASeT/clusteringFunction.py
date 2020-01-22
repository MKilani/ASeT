import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth


def clusteringFunction (listToCluster):

    reshapedList = np.reshape(listToCluster, (-1, 1))

    ms = MeanShift(bandwidth=None, bin_seeding=True)
    ms.fit(reshapedList)
    labels = list(ms.labels_)

    return labels

