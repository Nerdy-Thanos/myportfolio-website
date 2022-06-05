from torch.utils.data import DataLoader
from torchvision import datasets, transforms

class Pascal(object):
    def __init__(self) -> None:
        pass

    #Function to load and 
    def get_data():
        #resizing and converting to tensor
        transform = transforms.transforms.Compose([transforms.Resize(128),
                                                transforms.ToTensor()])
        #loading the train set
        pascal_train = datasets.VOCDetection("pascal_train", year="2007", 
                                                image_set="train", 
                                                transforms= transform,
                                                download=True)
        #Loading the test set
        pascal_test = datasets.VOCDetection("pascal_test", year = "2007",
                                                image_set="test", 
                                                transforms=transform, 
                                                download=True)
        #Loaders
        train_loader = DataLoader(pascal_train, batch_size=64)
        test_loader = DataLoader(pascal_test, batch_size=64)

        return train_loader, test_loader
