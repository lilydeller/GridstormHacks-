import earthaccess

# Login
earthaccess.login()

# Search by date + tile instead of exact granule name
results = earthaccess.search_data(
    short_name="MOD13Q1",
    version="061",
    temporal=("2026-02-01", "2026-02-10"),  
    bounding_box=(-125, 30, -65, 50),  # continental US
    cloud_hosted=True,
)

print("Found:", len(results), "results")

if len(results) > 0:
    files = earthaccess.download(results[:1])  
    print("Downloaded files:")
    print(files)
else:
    print("No results found.")