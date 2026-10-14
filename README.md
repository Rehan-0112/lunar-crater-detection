# Lunar Crater Detection System (LCDS)

Crater detection on Chandrayaan-2 TMC-2 ortho images. Guide: Dr. Balachandra Pujari (SCMS, SPPU).

## Status (work in progress)
- Environment: WSL2 Ubuntu 24.04, Python 3.11, PyTorch (CPU), rasterio, OpenCV
- First tile: ch2_tmc_ndn_20250217T0120183473_d_oth_d18 (6,416 x 162,392 px, about 5 m/px, sun incidence 55.2 deg)
- About 39% of the strip is empty (zero) pixels; 2,072 clean 512x512 tiles extracted
- Hand-labelling a small set of 256x256 patches (boxes, one class: crater) as a test set
- Reviewing the NASA-IBM Lunar Foundation Model (trained on LROC, untested on TMC-2)

## Scripts
- src/tile_scan.py: per-tile empty-pixel fraction
- src/make_tiles.py: clean tiles to 8-bit PNG with one shared brightness range

Data is not stored in this repo.
