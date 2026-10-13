import os, csv, random
import numpy as np
import rasterio, cv2
from rasterio.windows import Window

SRC = os.path.expanduser("~/lcds/data/raw/tmc_tiled.tif")
CSV = os.path.expanduser("~/lcds/outputs/tile_scan.csv")
OUT = os.path.expanduser("~/lcds/data/tiles")
SHEET = os.path.expanduser("~/lcds/outputs/sample_tiles.png")
TILE = 512
MAX_ZERO = 0.0

os.makedirs(OUT, exist_ok=True)
keep = []
with open(CSV) as f:
    for row in csv.DictReader(f):
        if float(row["zero_fraction"]) <= MAX_ZERO:
            keep.append((int(row["row"]), int(row["col"])))
print("tiles kept:", len(keep))

random.seed(0)
with rasterio.open(SRC) as src:
    def read(r, c):
        return src.read(1, window=Window(c, r, TILE, TILE))

    # one brightness range for ALL tiles, so they stay comparable
    vals = []
    for r, c in random.sample(keep, min(200, len(keep))):
        t = read(r, c)
        vals.append(t[t > 0])
    lo, hi = np.percentile(np.concatenate(vals), [1, 99])
    print("scaling range (raw values):", lo, hi)

    def to8(t):
        x = np.clip((t.astype(np.float32) - lo) / (hi - lo), 0, 1) * 254 + 1
        x[t == 0] = 0
        return x.astype(np.uint8)

    for i, (r, c) in enumerate(keep):
        cv2.imwrite(os.path.join(OUT, f"tile_r{r}_c{c}.png"), to8(read(r, c)))
        if i % 200 == 0:
            print("saved", i, "of", len(keep))

    picks = random.sample(keep, 9)
    imgs = [to8(read(r, c)) for r, c in picks]
    grid = np.vstack([np.hstack(imgs[i:i + 3]) for i in (0, 3, 6)])
    cv2.imwrite(SHEET, grid)
    print("sample sheet:", SHEET)
