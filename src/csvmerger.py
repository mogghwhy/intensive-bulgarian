import os
cwd = os.getcwd()
path = cwd
list_subfolders_with_paths = [f.path for f in os.scandir(path) if f.is_dir()]
print(list_subfolders_with_paths)
print(f"cwd {cwd}")
