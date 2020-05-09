import json
import csv
import datetime
import ntpath
from os import listdir
from os.path import isfile, join

JSON_DIR="rki_esri_portal_data_converter/json"
CSV_DIR="rki_esri_portal_data_converter/csv"

def json2dict(jsonfilepath):
    # Load JSON.
    obj = {}
    with open(jsonfilepath, "r") as f:
        file_data = f.read()
        obj = json.loads(file_data)
    
    # Create unique date headers.
    dateDict = dict()
    for e in obj["features"]:
        ts = e["attributes"]["Meldedatum"]
        ts = datetime.datetime.fromtimestamp(ts / 1000, tz=datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        num = e["attributes"]["AnzahlFall"]
        if not ts in dateDict:
            dateDict[ts] = 0
        dateDict[ts] = dateDict[ts] + num
    return dateDict


def json2csv(jsonfilepath, csvfilepath):
    dateDict = json2dict(jsonfilepath)
    # Create CSV from dict.
    # ROW#0 -> Dates
    # ROW#1 -> Dayly Numbers
    # ROW#2 -> Accumulated
    with open(csvfilepath, "w", newline='') as csvfile:
        w = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # ROW#0
        w.writerow(dateDict.keys())
        # ROW#1
        w.writerow(dateDict.values())
        # ROW#2
        count = 0
        row = []
        for v in dateDict.values():
            count = count + v
            row.append(count)
        w.writerow(row)

def file_list(path):
    return [f for f in listdir(path) if isfile(join(path, f))]

def run_onefileperregion():
    files = file_list(JSON_DIR)
    print("Found JSON files: " + str(len(files)))
    for file in files:
        print("Work on: " + file)
        jsonfilepath = JSON_DIR + "/" + file
        csvfilepath = CSV_DIR + "/" + file + ".csv"
        json2csv(jsonfilepath, csvfilepath)
        print("Done")

def run_onebigfile():
    # Will hold all data.
    region2dict = dict()
    bigdict = dict()

    # Load all dicts from JSON.
    files = file_list(JSON_DIR)
    for file in files:
        jsonfilepath = JSON_DIR + "/" + file
        datedict = json2dict(jsonfilepath)
        region2dict[file] = datedict

    # Sum all dicts.
    for rdict in region2dict.values():
        count = 0
        for date in rdict:
            value = rdict[date]
            count = count + value
            rdict[date] = count

    # Collect all available dates from all files.
    for region in region2dict:
        regiondict = region2dict[region]
        for date in regiondict:
            if not date in bigdict:
                bigdict[date] = []

    #print(bigdict.keys())
    #print(region2dict)

    # Fill bigdict with data from all regions (empty values if missing)
    # for region in region2dict:
    #     regiondict = region2dict[region]
    #     for date in bigdict:
    #         value = ""
    #         if date in regiondict:
    #             value = regiondict[date]
    #         bigdict[date].append(value)

    # CSV
    csvfilepath = CSV_DIR + "/Summary.csv"
    with open(csvfilepath, "w", newline='') as csvfile:
        w = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        regions = region2dict.keys()

        header = ["REGION"]
        for date in bigdict:
            header.append(date)
        w.writerow(header)

        for region in regions:
            row = []
            row.append(region)
            for date in bigdict:
                value = ""
                if region in region2dict:
                    if date in region2dict[region]:
                        value = region2dict[region][date]
                row.append(value)
            w.writerow(row)







## MAIN
#run_onefileperregion()
run_onebigfile()