import os, csv
import numpy as np
import rasterio
from rasterio.windows import Window

SRC = os.path.expanduser("~/lcds/data/raw/tmc_tiled.tif")
OUT_CSV = os.path.expanduser("~/lcds/outputs/tile_scan.csv")
TILE = 512

rows = []
total_zero = 0
total_px = 0

with rasterio.open(SRC) as src:
    H, W = src.height, src.width
    print("image size:", W, "x", H)
    for r in range(0, H - TILE + 1, TILE):
        band = src.read(1, window=Window(0, r, W, TILE))
        total_zero += int((band == 0).sum())
        total_px += band.size
        for c in range(0, W - TILE + 1, TILE):
            t = band[:, c:c + TILE]
            rows.append((r, c, float((t == 0).mean())))
        if (r // TILE) % 50 == 0:
            print("row", r, "of", H)

with open(OUT_CSV, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["row", "col", "zero_fraction"])
    w.writerows(rows)

zf = np.array([x[2] for x in rows])
print("Overall zero fraction:", round(total_zero / total_px, 3))
print("Total tiles:", len(rows))
for cut in (0.0, 0.1, 0.2, 0.3, 0.5):
    print("tiles with zero fraction <=", cut, ":", int((zf <= cut).sum()))
