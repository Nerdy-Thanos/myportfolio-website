import torch
from torch.nn import functional
import platform
from torchvision import datasets

#Checking platform and device
print(platform.platform())
print(torch.has_mps)

#Creating the model class
class BaseModel(object):
    def __init__(self) -> None:
         