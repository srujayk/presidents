from os import walk
f = []
path = "./data"
for (dirpath, dirnames, filenames) in walk(path):
    f.extend(filenames)

final_files = []

for i in range(len(f)):
    if f[i] != '.DS_Store':
        final_files.append(f[i])

for file in final_files:
    print(file)
