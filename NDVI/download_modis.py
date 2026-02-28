import earthaccess


earthaccess.login()


results = earthaccess.search_data(
    short_name="MOD13Q1",
    version="061",
    granule_name="MOD13Q1.A2026033.h11v05.061.2026051100652.hdf",
    cloud_hosted=True
)

print("Found:", len(results), "results")


files = earthaccess.download(results)

print("Downloaded files:")
print(files)