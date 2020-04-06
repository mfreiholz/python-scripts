from os import listdir
from os.path import isfile, join

def file_list(path):
    return [f for f in listdir(path) if isfile(join(path, f))]

# List of all available country data files.
BY_COUNTRY_DIR = "by_country"
files = file_list(BY_COUNTRY_DIR + "/")
print("Available data files by country: " + str(len(files)))

# Load header from first file.
f = open(BY_COUNTRY_DIR + "/" + files[0], "r")
global_header = f.readline()
f.close()

combined_file = open("combined.csv", "w")
combined_file.write("\"country\",")
combined_file.write(global_header)

for file in files:
    f = open(BY_COUNTRY_DIR + "/" + file, "r")
    header = f.readline()
    data = f.readline()
    f.close()
    if header != global_header:
        print("Header of country is different (skip): " + file)
        continue
    
    combined_file.write(file[:file.index(".")] + ",")
    combined_file.write(data)
    combined_file.write('\n')
combined_file.close()
