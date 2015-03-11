import os

path = os.getcwd()
print(path)
dir,name  = os.path.split(path)
print('dir' + dir)
print('name' + name)
if os.path.isdir(path):
    for dir , dirNames , fileNames in os.walk(path):
        print(dir)