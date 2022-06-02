import torch
from torch.nn import functional
import platform

#Checking platform and device
print(platform.platform())
print(torch.has_mps)