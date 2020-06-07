import cv2
import  os
from pathlib import Path
import numpy as np

if __name__ == "__main__":
    print("path_files(path) /npath= Location of folder where your images are as a raw string r'location'")

def path_files(path):
    paths = []
    folders = Path(path)
    for folder in folders.iterdir():
        for file in folder.iterdir():
            paths.append(str(file))
    find_duplicate_hash(paths)

def dhash(image, hashsize= 8):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized= cv2.resize(gray, (hashsize  + 1, hashsize))
    diff= resized[: , 1:] > resized[: , :-1]
    return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])

def find_duplicate_hash(paths):
    hashes = {}
    for imagepath in paths:
        image = cv2.imread(imagepath)
        h = dhash(image)
        p= hashes.get(h , [])
        p.append(imagepath)
        hashes[h] = p
    print("0 to view duplicates.\n1 to remove duplicates.")
    view_or_remove_duplicate(int(input()) , hashes)

def view_or_remove_duplicate(val, hashes):
    for (h , hashpath) in hashes.items():
        
        if len(hashpath) > 1:
            
            if val== 0:
                montage = None
                
                for p in hashpath:
                    image = cv2.imread(p)
                    image = cv2.resize(image, (300, 300))
                    
                    if montage is None:
                        montage = image
                    else: 
                        montage = np.hstack([montage , image])
                        
                print(f"[INFO] hash: {h}")
                cv2.imshow("Montage" , montage)
                cv2.waitKey(0)
            else:
                for p in hashpath[1:]:
                    os.remove(p)
