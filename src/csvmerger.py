import os
bases = ['volume01']
cwd = os.getcwd()
paths = [os.path.join(cwd, p) for p in bases]
list_subfolders_with_paths = [for path in paths f.path for f in os.scandir(path) if f.is_dir()]
print(list_subfolders_with_paths)

