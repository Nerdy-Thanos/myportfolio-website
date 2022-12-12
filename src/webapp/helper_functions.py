import os


def clean_output():
    path = "src/webapp/static/output/"
    files = os.listdir(path)
    for file in files:
        if os.path.exists(path + file):
            os.remove(path + file)
