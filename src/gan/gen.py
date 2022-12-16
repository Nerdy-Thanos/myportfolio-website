import torch
from pytorch_pretrained_gans import make_gan
import torchvision.transforms as T
import cv2
from numpy import array
from PIL import Image

def generate_image():
    G = make_gan(gan_type='biggan')  # -> nn.Module
    y = G.sample_class(batch_size=1)  # -> torch.Size([1, 1000])
    z = G.sample_latent(batch_size=1)  # -> torch.Size([1, 128])
    x = G(z=z, y=y)
    x = x.detach().cpu()
    img_trans = torch.squeeze(x, dim=0)
    transform = T.ToPILImage()
    img = transform(img_trans)
    img_col = cv2.cvtColor(array(img), cv2.COLOR_RGB2GRAY)
    image = Image.fromarray(img_col)

    return image


