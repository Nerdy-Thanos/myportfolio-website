import torch
from pytorch_pretrained_gans import make_gan
import torchvision.transforms as T

def generate_image():
    G = make_gan(gan_type='biggan')  # -> nn.Module
    y = G.sample_class(batch_size=1)  # -> torch.Size([1, 1000])
    z = G.sample_latent(batch_size=1)  # -> torch.Size([1, 128])
    x = G(z=z, y=y)
    x = x.detach().cpu()
    img_trans = torch.squeeze(x, dim=0)
    transform = T.ToPILImage()
    img = transform(img_trans)
    return img


