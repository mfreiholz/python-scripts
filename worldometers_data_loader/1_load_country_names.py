import requests
import re

def unify(seq):
    checked = []
    for e in seq:
        if e not in checked:
            checked.append(e)
    return checked

url = "https://www.worldometers.info/coronavirus/"
r = requests.get(url)
content = r.text

matches = re.findall(r"href\=\"\/coronavirus\/country\/([^\/]+)", content)
countries = unify(matches)

print("Write " + str(len(countries)) + " unique country names to file.")

f = open("countries.csv", "w")
first = True
for c in countries:
    if first:
        first = False
        f.write(c)
    else:
        f.write(",")
        f.write(c)
f.write('\n')
f.close()
