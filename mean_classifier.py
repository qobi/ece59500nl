from distances import *
import random
from functools import reduce

def distance(p1, p2):
    return (p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1])

def vplus(p1, p2):
    return [p1[0]+p2[0], p1[1]+p2[1]]

def ktimesv(k, p):
    return [k*p[0], k*p[1]]

def random_labels(points, k):
    return [random.randint(0, k-1) for point in points]

def points_with_label(label, points, labels):
    result = []
    for i in range(len(points)):
        if labels[i]==label:
            result.append(points[i])
    return result

def mean(points):
    return ktimesv(1.0/len(points), reduce(vplus, points, [0, 0]))

def train(points, labels):
    k = 0
    for i in range(len(points)):
        if labels[i]>k:
            k = labels[i]+1
    return [mean(points_with_label(j, points, labels)) for j in range(k)]

infinity = float("inf")

def classify(point, means):
    best_distance = infinity
    best_label = -1
    for j in range(len(means)):
        d = distance(point, means[j])
        if d<best_distance:
            best_distance = d
            best_label = j
    return best_label

def reclassify_all(points, means):
    return [classify(point, means) for point in points]

def cost(points, labels, means):
    return sum([sum([distance(point, means[j])
                     for point in points_with_label(j, points, labels)],)
                for j in range(len(means))])

def all_labeled(labels):
    for label in labels:
        if label==-1:
            return False
    return True

def all_labels(labels, k):
    for j in range(k):
        if len(points_with_label(j, labels, labels))==0:
            return False
    return True
