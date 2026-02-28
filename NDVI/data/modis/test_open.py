from pyhdf.SD import SD, SDC
import numpy as np

path = "data/2026-02-28-deb59e/MOD13Q1.A2026017.h07v05.061.2026034010251.hdf"

hdf = SD(path, SDC.READ)


ndvi = hdf.select("250m 16 days NDVI")


ndvi_data = ndvi.get()

print("Shape:", ndvi_data.shape)
print("Raw min:", np.min(ndvi_data))
print("Raw max:", np.max(ndvi_data))


ndvi_scaled = ndvi_data * 0.0001

print("Scaled min:", np.min(ndvi_scaled))
print("Scaled max:", np.max(ndvi_scaled))