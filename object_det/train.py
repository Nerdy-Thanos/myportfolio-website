import imp
import torch
import torchvision
import torch.nn as nn
import torch.optim as optim
from load_dataset import get_data
from base_model import Model
import time

#Skip SSL checks
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

device = torch.device('mps' if torch.torch.has_mps else 'cpu')
model = Model.make_model()

model.to(device)

print(model)
print(device)

train_loader, test_loader = get_data()

#Defining the loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.0001)

# calculate steps per epoch for training and test set
trainSteps = len(train_loader) // 64
testSteps = len(test_loader) // 64
# initialize a dictionary to store training history
H = {"train_loss": [], "test_loss": []}
#Defining the Training loop
# loop over epochs
print("[INFO] training the network...")
startTime = time.time()
for e in range(50):
	# set the model in training mode
	model.train()
	# initialize the total training and validation loss
	totalTrainLoss = 0
	totalTestLoss = 0
	# loop over the training set
	for x, y in train_loader:
		# send the input to the device
		x, y = x.to(device), y.to(device)
		# perform a forward pass and calculate the training loss
		pred = model(x)
		loss = criterion(pred, y)
		# first, zero out any previously accumulated gradients, then
		# perform backpropagation, and then update model parameters
		optimizer.zero_grad()
		loss.backward()
		optimizer.step()
		# add the loss to the total training loss so far
		totalTrainLoss += loss
	# switch off autograd
	with torch.no_grad():
		# set the model in evaluation mode
		model.eval()
		# loop over the validation set
		for x, y in test_loader:
			# send the input to the device
			x, y = x.to(device), y.to(device)
			# make the predictions and calculate the validation loss
			pred = model(x)
			totalTestLoss += criterion(pred, y)
	# calculate the average training and validation loss
	avgTrainLoss = totalTrainLoss / trainSteps
	avgTestLoss = totalTestLoss / testSteps
	# update our training history
	H["train_loss"].append(avgTrainLoss.cpu().detach().numpy())
	H["test_loss"].append(avgTestLoss.cpu().detach().numpy())
	# print the model training and validation information
	print("[INFO] EPOCH: {}/{}".format(e + 1, 50))
	print("Train loss: {:.6f}, Test loss: {:.4f}".format(
		avgTrainLoss, avgTestLoss))
# display the total time needed to perform the training
endTime = time.time()
print("[INFO] total time taken to train the model: {:.2f}s".format(
	endTime - startTime))