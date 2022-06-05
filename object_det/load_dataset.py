import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

#resizing and converting to tensor
transform = transforms.transforms.Compose([transforms.Resize(128),
                                           transforms.ToTensor()])
#loading the train set
pascal_train = datasets.VOCSegmentation("pascal_train", year="2007", 
                                         image_set="train", 
                                         transforms= transform,
                                         download=True)

#Loading the test set
pascal_test = datasets.VOCSegmentation("pascal_test", year = "2007",
                                        image_set="test", 
                                        transforms=transform, 
                                        download=True)

print(pascal_train.masks[0])
#Loaders
train_loader = DataLoader(pascal_train, batch_size=64)
test_loader = DataLoader(pascal_test, batch_size=64)