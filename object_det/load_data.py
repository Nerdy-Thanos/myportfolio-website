from matplotlib.transforms import Transform
import torch
import os
from torch.utils.data import Dataset
from torchvision import transforms
import cv2
from xml.etree import ElementTree as et
import numpy as np
import glob
from PIL import Image


class ObjectDetectionDataset(Dataset):
	def __init__(self, img_path, annot_path, classes, transform = None):
		self.img_path = img_path
		self.anno_path = annot_path
		self.classes = classes
		self.transform = transform

		self.images = [os.listdir(self.img_path)]
		self.allimgs = [i for i in glob.glob(f"{self.img_path}/*")]
		self.anno = [f for f in glob.glob(f"{self.anno_path}/*")]

	def __getitem__(self, index):
		#Loading the images and annotations
		
		img = Image.open(self.allimgs[index])
		print(type(img))
		
		annot = et.parse(self.anno[index])
		boxes = []
		labels = []
		root = annot.getroot()

		for child in root.findall('object'):
			#fetching the labels and bounding boxes
			labels.append(self.classes.index(child.find('name').text))
			# xmin = left corner x-coordinates
			xmin = int(child.find('bndbox').find('xmin').text)
			# xmax = right corner x-coordinates
			xmax = int(child.find('bndbox').find('xmax').text)
			# ymin = left corner y-coordinates
			ymin = int(child.find('bndbox').find('ymin').text)
			# ymax = right corner y-coordinates
			ymax = int(child.find('bndbox').find('ymax').text)
			boxes.append([xmin, ymin, xmax, ymax])
		

		transformations = transforms.ToTensor()
		#applying the transformation
		image = self.transform(img)
		boxes = self.transform(boxes) 
		labels = self.transform(labels)
		return (image, boxes, labels)

	def __len__(self):
		return len(self.images)
	
	def collate_fn(self, batch):
		"""
		Since each image may have a different number of objects, we need a collate function (to be passed to the DataLoader).
		This describes how to combine these tensors of different sizes. We use lists.
		Note: this need not be defined in this Class, can be standalone.
		:param batch: an iterable of N sets from __getitem__()
		:return: a tensor of images, lists of varying-size tensors of bounding boxes, labels, and difficulties
		"""

		images = []
		boxes = []
		labels = []

		for b in batch:
			images.append(b[0])
			boxes.append(b[1])
			labels.append(b[2])
		images = torch.stack(images, dim=0)

		return images, boxes, labels


