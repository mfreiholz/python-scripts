import requests

def load_country_names():
    f = open("countries.csv", "r")
    line = f.readline()
    names = line.split(",")
    f.close()
    return names

countries = load_country_names()
for country in countries:
    url = "https://www.worldometers.info/coronavirus/country/"
    url = url + country
    url = url + "/"
    r = requests.get(url)

    if r.status_code != 200:
        print("Can not read data for country: " + country)
        print("URL: " + url)
        print("Status-Code: " + r.status_code)
        continue

    print("Loaded page for country: " + country)
    print("Size: " + str(len(r.text)))

    # Parse content
    content = r.text
    try:
        offset = content.index("Highcharts.chart('coronavirus-cases-linear'")
        print("offset:" + str(offset))

        categories_begin_offset = content.index("categories: [", offset) + 13
        print("categories_begin_offset=" + str(categories_begin_offset))

        categories_end_offset = content.index("]", categories_begin_offset)
        print("categories_end_offset=" + str(categories_end_offset))

        categories = content[categories_begin_offset:categories_end_offset]
        print(categories)

        # Now the values.

        data_begin_offset = content.index("data: [", categories_end_offset) + 7
        print("data_begin_offset=" + str(data_begin_offset))

        data_end_offset = content.index("]", data_begin_offset)
        print("data_end_offset=" + str(data_end_offset))

        data = content[data_begin_offset:data_end_offset]
        print(data)

        f = open("by_country/" + country + ".csv", "w")
        f.write(categories)
        f.write('\n')
        f.write(data)
        f.close()
              
    except ValueError as err:
        print("Can not find offset of required element for country: " + country)
