import json
import csv
import datetime
from os import listdir
from os.path import isfile, join

def compare_arrays(a, b):
    if len(a) != len(b):
        return False
    for i in range(len(a)):
        if a[i] != b[i]:
            return False
    return True

def write_json_to_csv(obj, filename):
    if len(obj["measurements"]) <= 0:
        return False

    # Header from "pollen" names.
    pollen_names = []
    for e in obj["measurements"]:
        pollen_names.append(e["polle"])

    # Write CSV.
    with open(filename, "w", newline='') as csvfile:
        w = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # Master Header
        # Create header from first data-set datetime values ("from").
        header = []
        header.append("POLLE")
        header.append("LOCATION")
        firstdata = obj["measurements"][0]["data"]
        for data in firstdata:
            header.append(datetime.datetime.fromtimestamp(data["from"], tz=datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S"))
        w.writerow(header)

        # Values with custom header for validation.
        for e in obj["measurements"]:
            # Validate data-set by header-comparison.
            rowheader = []
            rowheader.append("POLLE")
            rowheader.append("LOCATION")
            rowfirstdata = e["data"]
            for data in firstdata:
                rowheader.append(datetime.datetime.fromtimestamp(data["from"], tz=datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S"))
            if not (rowheader == header):
                print("HEADER DOESNT MATCH!" + filename)
                continue
            
            rowdata = []
            rowdata.append(e["polle"])
            rowdata.append(e["location"])
            for data in e["data"]:
                rowdata.append(data["value"])
            w.writerow(rowdata)
    return True


def file_list(path):
    return [f for f in listdir(path) if isfile(join(path, f))]

## MAIN

files = file_list("download/")
print("Available data files: " + str(len(files)))

for filename in files:
    try:
        # Load data from file.
        f = open("download/" + filename, "r")
        src_file_data = f.read()
        f.close()

        # Parse JSON data.
        obj = json.loads(src_file_data)
        if not write_json_to_csv(obj, "output/" + filename + ".csv"):
            printf("No measurements in: " + filename)
    except:
        print("No data for: " + filename)


#            rowheader.append("location")
#            rowheader.append(datetime.datetime.fromtimestamp(data["from"], tz=datetime.timezone.utc).strftime("%Y-%m-%d"))
#            if not compare_arrays(header, rowheader):
#                print("not matching date in row: " + e["polle"])
#                continue



