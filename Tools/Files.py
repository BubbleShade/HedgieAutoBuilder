import os

def newFileOfName(directory : str, name : str):
    with os.scandir(directory) as entries:
        paths = map(lambda entry: entry.path, filter(lambda entry : entry.is_file(),entries))
        nameWithoutExtension, extension = name.split(".")

        if(not directory+name in paths): return name
        a = 0            
        for i in range(500):
            newName = nameWithoutExtension+f" ({i})"+ "."+extension
            if(not directory+newName in paths): return newName
        return "error"
