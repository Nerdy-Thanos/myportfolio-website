import os
import base64
import io
from PIL import Image
from cv2 import cvtColor, COLOR_RGB2BGR
from numpy import array, mean


def clean_output():
    path = "src/webapp/static/output/"
    files = os.listdir(path)
    for file in files:
        if os.path.exists(path + file):
            os.remove(path + file)

def readb64(base64_string):
    idx = base64_string.find('base64,')
    base64_string  = base64_string[idx+7:]

    sbuf = io.BytesIO()

    sbuf.write(base64.b64decode(base64_string, ' /'))
    pimg = Image.open(sbuf)

    return cvtColor(array(pimg), COLOR_RGB2BGR)

def moving_average(x):
    return mean(x)


