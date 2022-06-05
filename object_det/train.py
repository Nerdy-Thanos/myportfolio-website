import imp
import torch
import torchvision
import torch.optim as optim
import base_model
from base_model import Model

device = torch.device('mps' if torch.torch.has_mps else 'cpu')
model = Model.make_model()

model.to(device)

print(model)
print(device)