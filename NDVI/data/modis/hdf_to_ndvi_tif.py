import numpy as np
import rasterio
from rasterio.transform import from_origin
from rasterio.crs import CRS
from pyhdf.SD import SD, SDC
import re

HDF_FILE = "MOD13Q1.A2024001.h11v05.061.2024022132913.hdf" 
OUT_TIF  = "ndvi_out.tif"

NDVI_SDS = "250m 16 days NDVI"  

MODIS_SIN = CRS.from_string("+proj=sinu +R=6371007.181 +nadgrids=@null +wktext")

def parse_point(struct_meta: str, key: str):
    m = re.search(rf"{re.escape(key)}=\(\s*([-\d\.]+)\s*,\s*([-\d\.]+)\s*\)", struct_meta)
    if not m:
        return None
    return float(m.group(1)), float(m.group(2))

hdf = SD(HDF_FILE, SDC.READ)


datasets = hdf.datasets()
if NDVI_SDS not in datasets:
    print("NDVI SDS name not found. Available datasets include:")
    for name in list(datasets.keys())[:50]:
        print(" -", name)
    raise SystemExit(1)

sds = hdf.select(NDVI_SDS)
arr = sds.get().astype(np.float32)

attrs = sds.attributes()
fill = attrs.get("_FillValue", None)
scale = float(attrs.get("scale_factor", 0.0001))  
offset = float(attrs.get("add_offset", 0.0))

if fill is not None:
    arr = np.where(arr == fill, np.nan, arr)


arr = (arr - offset) * scale
arr = np.where((arr < -1.2) | (arr > 1.2), np.nan, arr)

# Pull tile bounds from metadata so the GeoTIFF is georeferenced
meta = hdf.attributes().get("StructMetadata.0", "")
ul = parse_point(meta, "UpperLeftPointMtrs")
lr = parse_point(meta, "LowerRightMtrs")
if ul is None or lr is None:
    raise RuntimeError("Could not read UpperLeftPointMtrs/LowerRightMtrs from StructMetadata.0")

ulx, uly = ul
lrx, lry = lr

h, w = arr.shape
px_w = (lrx - ulx) / w
px_h = (uly - lry) / h
transform = from_origin(ulx, uly, px_w, px_h)

with rasterio.open(
    OUT_TIF,
    "w",
    driver="GTiff",
    height=h,
    width=w,
    count=1,
    dtype="float32",
    crs=MODIS_SIN,
    transform=transform,
    nodata=np.nan,
    compress="deflate",
) as dst:
    dst.write(arr.astype(np.float32), 1)

print("✅ Wrote:", OUT_TIF)
print("NDVI min/max:", np.nanmin(arr), np.nanmax(arr))