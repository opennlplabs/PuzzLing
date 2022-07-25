import os
data_dir = "pashto.txt"



with open(data_dir, "r", encoding= "utf-8") as file:
    for line in file.readlines():
        line = line.strip("\n")
        print(line.split("$")[1])
