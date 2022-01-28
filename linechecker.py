lineCounter = 0
with open("main.py") as file:
    for line in file.read().splitlines():
        if line != "":
            lineCounter += 1

print(lineCounter)