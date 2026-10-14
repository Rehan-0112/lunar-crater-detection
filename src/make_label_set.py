import os, glob, random
import cv2
random.seed(1)
files = sorted(glob.glob(os.path.expanduser("~/lcds/data/tiles/*.png")))
out = os.path.expanduser("~/lcds/data/label_256")
for f in random.sample(files, 5):
    img = cv2.imread(f, cv2.IMREAD_GRAYSCALE)
    base = os.path.splitext(os.path.basename(f))[0]
    for i, (r, c) in enumerate([(0, 0), (0, 256), (256, 0), (256, 256)]):
        cv2.imwrite(os.path.join(out, f"{base}_q{i}.png"), img[r:r+256, c:c+256])
print("saved", len(os.listdir(out)), "patches to", out)
