import requests
import datetime

DOWNLOAD_DIR="download"

# Read locations from file.
f = open("locations.csv", "r")
location_keys = f.readline().rstrip().split(",")
location_titles = f.readline().rstrip().split(",")
f.close()

# Read "pollen" from file.
f = open("pollen.csv", "r")
pollen = f.readline().split(",")
f.close()

# HTTP GET data from server.
# Download each location one-by-one.
baseurl = "https://epin-scientific.eu/api/measurements"

fromdate = 1573063038
todate = int(datetime.datetime.now(tz=datetime.timezone.utc).timestamp())
for i in range(len(location_keys)):
    location_key = location_keys[i]
    location_title = location_titles[i]
    params = {
        "from": fromdate,
        "to": todate,
        "locations": location_key,
        "pollen": ",".join(pollen)
    }
    r = requests.get(baseurl, params=params)
    if r.status_code != 200:
        print("----")
        print("Can not read data for location: " + location_key)
        print("URL: " + r.url)
        print("Status-Code: " + r.status_code)
        print("----")
        continue

    print("Loaded data for location: " + location_key)
    print("Size: " + str(len(r.text)))

    # Write to file.
    filename = location_key + "_" + location_title + ".json"
    content = r.text
    with open(DOWNLOAD_DIR + "/" + filename, "w") as jsonfile:
        jsonfile.write(content)
print("Done!")