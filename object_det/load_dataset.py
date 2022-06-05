import torch
from torchvision import datasets

pascal_train = datasets.VOCSegmentation("pascal", year= "2012", image_set= "train", download=True)