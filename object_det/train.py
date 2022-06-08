from cgi import test
from matplotlib.pyplot import cla
import torch
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.optim as optim
import load_data
import load_dataset
from base_model import Model
import time
from torchvision import transforms

#Skip SSL checks
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

classes = ["background",
			"aeroplane",
			"bicycle",
			"bird",
			"boat",
			"bottle",
			"bus",
			"car",
			"cat",
			"chair",
			"cow",
			"diningtable",
			"dog",
			"horse",
			"motorbike",
			"person",
			"pottedplant",
			"sheep",
			"sofa",
			"train",
			"tvmonitor"]

device = torch.device('mps' if torch.torch.has_mps else 'cpu')
model = Model.make_model()

model.to(device)

#print(model)
#print(device)

#Apply transformations
train_DS = load_data.ObjectDetectionDataset(img_path="object_det/pascal_train/VOCdevkit/VOC2007/JPEGImages",
											annot_path="object_det/pascal_train/VOCdevkit/VOC2007/Annotations/",
											classes=classes, transform=transforms.ToTensor())
test_DS = load_data.ObjectDetectionDataset(img_path="object_det/pascal_test/VOCdevkit/VOC2007/JPEGImages",
										   annot_path="object_det/pascal_test/VOCdevkit/VOC2007/Annotations/",
										   classes=classes, transform= transforms.ToTensor())
print("train_samples: ",len(train_DS))
print(type(train_DS))

#Defining the loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.0001)

# calculate steps per epoch for training and test set
trainSteps = len(train_DS) // 64
testSteps = len(test_DS) // 64
# initialize a dictionary to store training history
H = {"train_loss": [], "test_loss": []}
train_loader = DataLoader(train_DS, 64)#, collate_fn=train_DS.collate_fn)
print(type(train_loader))
test_loader = DataLoader(test_DS, 64)#,collate_fn= test_DS.collate_fn)
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
	for i, (imgs, boxes, labels) in enumerate(train_loader):
		# send the input to the device
		imgs = imgs.to(device)
		boxes = [b.to(device) for b in boxes]
		labels = [l.to(device) for l in labels]
		# perform a forward pass and calculate the training loss
		pred_locs, pred_scores = model(imgs)
		loss = criterion(pred_locs, pred_scores, boxes, labels)
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
		for j, (t_img, t_box, t_labels) in enumerate(test_loader):
			# send the input to the device
			t_img = t_img.to(device)
			t_box = [tb.to(device) for tb in t_box]
			t_labels = [tl.to(device) for tl in t_labels]
			# make the predictions and calculate the validation loss
			t_locs, t_scores = model(t_img)
			totalTestLoss += criterion(t_locs, t_scores, t_box, t_labels)
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