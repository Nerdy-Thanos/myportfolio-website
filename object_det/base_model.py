import torch
import platform
from torchvision import models

#Checking platform and device
print(platform.platform())
print(torch.has_mps)

#Loading pre-trained fasterRCNN model
class Model(object):

    def __init__(self) -> None:
        pass
    
    def make_model():
        model = models.detection.fasterrcnn_resnet50_fpn(pretrained=False, 
                                                num_classes=20, 
                                                progress=True,
                                                pretrained_backbone=True)
        return model


        
        



         