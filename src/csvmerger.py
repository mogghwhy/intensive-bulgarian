import os
import glob
bases = ['volume01']
cwd = os.getcwd()
paths = [os.path.join(cwd, p) for p in bases]
list_subfolders_with_paths = []
for p in paths:
    list_subfolders_with_paths += [f.path for f in os.scandir(p) if f.is_dir()]
#print(list_subfolders_with_paths)
files = []
for item in list_subfolders_with_paths:
    files += glob.glob(os.path.join(item, "*.txt"))
print(files)

