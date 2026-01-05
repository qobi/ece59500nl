from gui import *
from distances import *
import nearest_neighbor_classifier
import medoid_classifier
import mean_classifier
import em
from numpy.linalg import eigh
from numpy import sqrt, sin, cos, arctan2, radians
import pickle

#\needswork
#  1. way to erase all
#  2. classify can't have unlabeled points
#  3. all can't have unlabeled points
#  4. linear_classifier_gui.py
#  5. two_layer_perceptron_gui.py

points = []
labels = []
ownerships = []
medoids = []
mixture_proportions = []
means = []
variances = []

distance = L2_vector(L2_scalar)

def redisplay():
    get_axes().clear()
    get_axes().clear()
    for i in range(len(points)):
        if labels[i]==-1:
            get_axes().plot([points[i][0]], [points[i][1]], "g+")
        elif labels[i]==0:
            get_axes().plot([points[i][0]], [points[i][1]], "r+")
        elif labels[i]==1:
            get_axes().plot([points[i][0]], [points[i][1]], "b+")
        else:
            raise RuntimeError("invalid label")
    if classifier()==0:
        pass
    elif classifier()==1:
        if len(medoids)==2:
            get_axes().plot([medoids[0][0]], [medoids[0][1]], "ro")
            get_axes().plot([medoids[1][0]], [medoids[1][1]], "bo")
    elif classifier()==2:
        if len(means)==2:
            get_axes().plot([means[0][0]], [means[0][1]], "ro")
            get_axes().plot([means[1][0]], [means[1][1]], "bo")
    elif classifier()==3:
        if len(means)==2:
            for j in range(2):
                ellipse_x = []
                ellipse_y = []
                w, v = eigh(variances[j])
                x0 = means[j][0]
                y0 = means[j][1]
                t0 = arctan2(variances[j][1, 0], w[0]-variances[j][1, 1])
                a = sqrt(2*w[0])
                b = sqrt(2*w[1])
                rxx = cos(t0)
                rxy = -sin(t0)
                ryx = -rxy
                ryy = rxx
                for l in range(37):
                    x = a*sin(radians(10*l))
                    y = b*cos(radians(10*l))
                    ellipse_x.append(rxx*x+rxy*y+x0)
                    ellipse_y.append(ryx*x+ryy*y+y0)
                if j==0:
                    color = "r"
                else:
                    color = "b"
                get_axes().plot(ellipse_x, ellipse_y, color)
    else:
        raise RuntimeError("invalid classifier")
    redraw()

def clear_command():
    global points, labels, ownerships
    global medoids, mixture_proportions, means, variances
    points = []
    labels = []
    ownerships = []
    medoids = []
    mixture_proportions = []
    means = []
    variances = []
    message("")
    get_axes().clear()
    redraw()

def random_labels_command():
    global labels, ownerships, medoids, mixture_proportions, means, variances
    if classifier()==0:
        labels = medoid_classifier.random_labels(points, 2)
        ownerships = [[1, 0] if label==0 else [0, 1] for label in labels]
    elif classifier()==1:
        labels = medoid_classifier.random_labels(points, 2)
        ownerships = [[1, 0] if label==0 else [0, 1] for label in labels]
    elif classifier()==2:
        labels = mean_classifier.random_labels(points, 2)
        ownerships = [[1, 0] if label==0 else [0, 1] for label in labels]
    elif classifier()==3:
        ownerships = em.random_labels(points, 2)
        labels = [0 if ownership[0]>ownership[1] else 1
                  for ownership in ownerships]
    else:
        raise RuntimeError("invalid classifier")
    medoids = []
    mixture_proportions = []
    means = []
    variances = []
    message("")
    redisplay()

def train_command():
    def internal():
        global medoids, mixture_proportions, means, variances
        if classifier()==0:
            raise RuntimeError("can't train nearest neighbor")
        elif classifier()==1:
            medoids = medoid_classifier.train(distance, points, labels)
            message("{:.3f}".format(
                medoid_classifier.cost(distance, points, labels, medoids)))
        elif classifier()==2:
            means = mean_classifier.train(points, labels)
            message("{:.3f}".format(mean_classifier.cost(points, labels, means)))
        elif classifier()==3:
            mixture_proportions, means, variances = em.train(points, ownerships)
            message("{:.3e}".format(
                em.likelihood(points, mixture_proportions, means, variances)))
        else:
            raise RuntimeError("invalid classifier")
        redisplay()
    if classifier()==0:
        message("Can't do this with nearest neighbor classifier")
    elif classifier()==1:
        if not medoid_classifier.all_labels(labels, 2):
            message("Missing class")
        elif not medoid_classifier.all_labeled(labels):
            message("Random labels first")
        else:
            message("Training")
            get_window().after(10, internal)
    elif classifier()==2:
        if not mean_classifier.all_labels(labels, 2):
            message("Missing class")
        elif not mean_classifier.all_labeled(labels):
            message("Random labels first")
        else:
            message("Training")
            get_window().after(10, internal)
    elif classifier()==3:
        if not em.all_labeled(ownerships):
            message("Random labels first")
        elif not em.all_labels(ownerships, 2):
            message("Missing class")
        else:
            message("Training")
            get_window().after(10, internal)
    else:
        raise RuntimeError("invalid classifier")

def all_command():
    resolution = 50
    scale = 1.0/resolution
    for y in range(resolution+1):
        for x in range(resolution+1):
            if classifier()== 0:
                label = nearest_neighbor_classifier.classify(
                    [scale*x, scale*y], distance, points, labels)
            elif classifier()==1:
                label = medoid_classifier.classify(
                    [scale*x, scale*y], distance, medoids)
            elif classifier()==2:
                label = mean_classifier.classify([scale*x, scale*y], means)
            elif classifier()==3:
                ownership = em.classify(
                    [scale*x, scale*y], mixture_proportions, means, variances)
                label = 0 if ownership[0]>ownership[1] else 1
            else:
                raise RuntimeError("invalid classifier")
            if label==0:
                get_axes().plot([scale*x], [scale*y], "r.")
            else:
                get_axes().plot([scale*x], [scale*y], "b.")
    redraw()

def load_command():
    global points, labels, ownerships
    global medoids, mixture_proportions, means, variances
    f = open("data.pkl", "rb")
    (points, labels, ownerships, medoids, mixture_proportions, means, variances
     ) = pickle.load(f)
    f.close()
    message("")
    redisplay()

def save_command():
    f = open("data.pkl", "wb")
    pickle.dump((points, labels, ownerships,
                 medoids, mixture_proportions, means, variances),
                f)
    f.close()

def reclassify_all_command():
    def internal():
        global labels, ownerships
        if classifier()==0:
            raise RuntimeError("can't reclassify_all nearest neighbor")
        elif classifier()==1:
            labels = medoid_classifier.reclassify_all(distance, points, medoids)
            ownerships = [[1, 0] if label==0 else [0, 1] for label in labels]
            message("{:.3f}".format(
                medoid_classifier.cost(distance, points, labels, medoids)))
        elif classifier()==2:
            labels = mean_classifier.reclassify_all(points, means)
            ownerships = [[1, 0] if label==0 else [0, 1] for label in labels]
            message("{:.3f}".format(mean_classifier.cost(points, labels, means)))
        elif classifier()==3:
            ownerships = em.reclassify_all(
                points, mixture_proportions, means, variances)
            labels = [0 if ownership[0]>ownership[1] else 1
                      for ownership in ownerships]
            message("{:.3e}".format(
                em.likelihood(points, mixture_proportions, means, variances)))
        else:
            raise RuntimeError("invalid classifier")
        redisplay()
    if classifier()==0:
        message("Can't do this with nearest neighbor classifier")
    elif classifier()==1:
        if len(medoids)==0:
            message("Train first")
        else:
            message("Reclassifying all")
            get_window().after(10, internal)
    elif classifier()==2:
        if len(means)==0:
            message("Train first")
        else:
            message("Reclassifying all")
            get_window().after(10, internal)
    elif classifier()==3:
        if len(means)==0:
            message("Train first")
        else:
            message("Reclassifying all")
            get_window().after(10, internal)
    else:
        raise RuntimeError("invalid classifier")

def loop_command():
    infinity = float("inf")
    def internal(last):
        global labels, ownerships
        global medoids, mixture_proportions, means, variances
        if classifier()==0:
            raise RuntimeError("can't loop nearest neighbor")
        elif classifier()==1:
            medoids = medoid_classifier.train(distance, points, labels)
            labels = medoid_classifier.reclassify_all(distance, points, medoids)
            ownerships = [[1, 0] if label==0 else [0, 1] for label in labels]
            this_cost = medoid_classifier.cost(distance, points, labels, medoids)
            message("{:.3f}".format(this_cost))
            redisplay()
            if this_cost<last:
                get_window().after(500, lambda: internal(this_cost))
            else:
                message("Done")
        elif classifier()==2:
            means = mean_classifier.train(points, labels)
            labels = mean_classifier.reclassify_all(points, means)
            ownerships = [[1, 0] if label==0 else [0, 1] for label in labels]
            this_cost = mean_classifier.cost(points, labels, means)
            message("{:.3f}".format(this_cost))
            redisplay()
            if this_cost<last:
                get_window().after(500, lambda: internal(this_cost))
            else:
                message("Done")
        elif classifier()==3:
            mixture_proportions, means, variances = em.train(points, ownerships)
            ownerships = em.reclassify_all(
                points, mixture_proportions, means, variances)
            labels = [0 if ownership[0]>ownership[1] else 1
                      for ownership in ownerships]
            this_likelihood = em.likelihood(
                points, mixture_proportions, means, variances)
            message("{:.3e}".format(this_likelihood))
            redisplay()
            if (last==-infinity or (this_likelihood-last)/last>1e-3):
                get_window().after(500, lambda: internal(this_likelihood))
            else:
                message("Done")
        else:
            raise RuntimeError("invalid classifier")
    if classifier()==0:
        message("Can't do this with nearest neighbor classifier")
    elif classifier()==1:
        if not medoid_classifier.all_labeled(labels):
            message("Random labels first")
        elif not medoid_classifier.all_labels(labels, 2):
            message("Missing class")
        else:
            infinity = float("inf")
            internal(infinity)
    elif classifier()==2:
        if not mean_classifier.all_labeled(labels):
            message("Random labels first")
        elif not mean_classifier.all_labels(labels, 2):
            message("Missing class")
        else:
            infinity = float("inf")
            internal(infinity)
    elif classifier()==3:
        if not em.all_labeled(ownerships):
            message("Random labels first")
        elif not em.all_labels(ownerships, 2):
            message("Missing class")
        else:
            internal(-infinity)
    else:
        raise RuntimeError("invalid classifier")

def lookup(x, y):
    d = infinity
    j = -1
    for i in range(len(points)):
        if distance(points[i], [x, y])<d:
            d = distance(points[i], [x, y])
            j = i
    return j

def click(x, y):
    message("")
    if mode()==0:
        points.append([x, y])
        labels.append(-1)
        ownerships.append([0, 0])
        get_axes().plot([x], [y], "g+")
        redraw()
    elif mode()==1:
        points.append([x, y])
        labels.append(0)
        ownerships.append([1, 0])
        get_axes().plot([x], [y], "r+")
        redraw()
    elif mode()==2:
        points.append([x, y])
        labels.append(1)
        ownerships.append([0, 1])
        get_axes().plot([x], [y], "b+")
        redraw()
    elif mode()==3:
        j = lookup(x, y)
        if j==-1:
            message("No data")
        else:
            labels[j] = -1
            ownerships[j] = [0, 0]
        redisplay()
    elif mode()==4:
        j = lookup(x, y)
        if j==-1:
            message("No data")
        else:
            labels[j] = 0
            ownerships[j] = [1, 0]
        redisplay()
    elif mode()==5:
        j = lookup(x, y)
        if j==-1:
            message("No data")
        else:
            labels[j] = 1
            ownerships[j] = [0, 1]
        redisplay()
    elif mode()==6:
        j = lookup(x, y)
        if j==-1:
            message("No data")
        else:
            del points[j]
            del labels[j]
            del ownerships[j]
        redisplay()
    elif mode()==7:
        if len(points)==0:
            message("No data")
        else:
            if classifier()== 0:
                label = nearest_neighbor_classifier.classify(
                    [x, y], distance, points, labels)
                if label==0:
                    message("Red")
                elif label==1:
                    message("Blue")
            elif classifier()==1:
                if len(medoids)==0:
                    message("Train first")
                else:
                    label = medoid_classifier.classify([x, y], distance, medoids)
                    if label==0:
                        message("Red")
                    elif label==1:
                        message("Blue")
            elif classifier()==2:
                if len(means)==0:
                    message("Train first")
                else:
                    label = mean_classifier.classify([x, y], means)
                    if label==0:
                        message("Red")
                    elif label==1:
                        message("Blue")
            elif classifier()==3:
                if len(means)==0:
                    message("Train first")
                else:
                    label = em.classify(
                        [x, y], mixture_proportions, means, variances)
                    message(
                        "Red: {:.3f}, Blue: {:.3f}".format(label[0], label[1]))
            else:
                raise RuntimeError("invalid classifier")
    else:
        raise RuntimeError("invalid mode")

mode = add_radio_button_group([[0, 0, "Unlabeled", 0],
                               [0, 1, "Red", 1],
                               [0, 2, "Blue", 2],
                               [0, 3, "Unlabel", 3],
                               [0, 4, "Reden", 4],
                               [0, 5, "Bluen", 5],
                               [0, 6, "Delete", 6],
                               [0, 7, "Classify", 7]],
                              lambda: False)
classifier = add_radio_button_group([[1, 0, "Nearest", 0],
                                     [1, 1, "Medoid", 1],
                                     [1, 2, "Mean", 2],
                                     [1, 3, "Gaussian", 3]],
                                    lambda: False)
add_button(2, 0, "Clear", clear_command, nothing)
add_button(2, 1, "Random labels", random_labels_command, nothing)
add_button(2, 2, "Train", train_command, nothing)
add_button(2, 3, "Reclassify all", reclassify_all_command, nothing)
add_button(2, 4, "Loop", loop_command, nothing)
add_button(2, 5, "All", all_command, nothing)
add_button(2, 6, "Load", load_command, nothing)
add_button(2, 7, "Save", save_command, nothing)
add_button(2, 8, "Exit", done, nothing)
message = add_message(3, 0, 9)
add_click(click)
start_fixed_size_matplotlib(7, 7, 4, 9)
