import torch
from torch.autograd import Variable
import torch.nn as nn
import numpy as np

def create_xor_dataset(size):
    dataset = {}
    dataset["features"] = np.random.randint(2, size=[size, 2])
    labels = np.array([(dataset["features"][i, 0] and
			(not dataset["features"][i, 1])) or
		       (dataset["features"][i,1 ] and
			(not dataset["features"][i, 0])) for i in range(size)])
    dataset["labels"] = np.zeros([size, 2])
    for i in range(size):
	dataset["labels"][i, labels[i]] = 1
    return dataset

def test(network, kind, dataset):
    network.eval()
    classifier_correct = 0
    N =	 dataset["features"].shape[0]
    features = torch.FloatTensor(dataset["features"])
    labels = torch.LongTensor(dataset["labels"])
    for i in range(N):
	features_ground_truth = features[i].unsqueeze(0).cuda()
	classifier_prediction = network.forward(features_ground_truth)
	classifier_ground_truth = dataset["labels"][i].argmax()
	max_val, max_ind = torch.max(classifier_prediction, 1)
	if classifier_ground_truth == max_ind.cpu().numpy()[0]:
	    classifier_correct += 1.0
    print "accuracy on %s set %2.1f%%"%(kind, 100*classifier_correct/N)
    network.train()

def train(network,
	  criterion,
	  iterations,
	  batch_size,
	  learning_rate,
	  training_set,
	  test_set):
    training_set_size = training_set["features"].shape[0]
    number_of_features = training_set["features"].shape[1]
    network.train()
    test(network, "training", training_set)
    test(network, "test", test_set)
    for i in range(iterations):
	n_samples = 0
	loss = 0
	#rng_state = np.random.get_state()
	#np.random.shuffle(training_set["features"])
	#np.random.set_state(rng_state)
	#np.random.shuffle(training_set["labels"])
	while n_samples<training_set_size:
	    st = n_samples
	    ed = min(n_samples+batch_size, training_set_size)
	    sz = ed-st+1
	    features = torch.FloatTensor(training_set["features"][st:ed])
	    classes = torch.FloatTensor(training_set["labels"][st:ed])
	    features = Variable(features.cuda())
	    classes = Variable(classes.cuda())
	    prediction = network.forward(features)
	    grad_criterion = criterion(prediction, classes)
	    grad_criterion.backward()
	    for W in network.parameters():
		W.data = W.data-learning_rate*W.grad.data
	    loss += grad_criterion.cpu().detach().numpy()
	    n_samples += batch_size
	print "iteration %s loss %f"%(i, loss)
    test(network, "training", training_set)
    test(network, "test", test_set)

def mlp(number_of_features, number_of_hidden, number_of_classes):
    network = nn.Sequential(
	nn.Linear(number_of_features, number_of_hidden),
	nn.ReLU(),
	nn.Linear(number_of_hidden, number_of_classes),
	nn.Softmax(dim=1))
    return network.cuda()

def run():
    network = mlp(2, 10, 2)
    criterion = nn.MSELoss()
    iterations = 10
    batch_size = 50
    learning_rate = 0.1
    training_set = create_xor_dataset(1000)
    test_set = create_xor_dataset(100)
    train(network,
          criterion,
          iterations,
          batch_size,
          learning_rate,
          training_set,
          test_set)

run()
