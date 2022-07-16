import os
import re
data_dir = "pashto_demo.txt"
save_path = "pashto.txt"


with open(data_dir, "r", encoding= "utf-8") as file:
    for id, line in enumerate(file.readlines(), start=1):
        line = line.strip("\n")
        # remove all the " characters in each line.
        line = re.sub('["]', '', line)
        # we only need the odd or even lines to get the english text.
        if id % 2:
            print(id, line + "$", end= " ")
        # here we got the pashto text.
        else:
            print(line)

