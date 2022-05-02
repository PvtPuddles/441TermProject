
import sys
import time
import os
from os.path import exists

from Matrix import Matrix
from BasicTest import testHeading

if __name__ == "__main__":
    mode = "add"

    size = 2
    steps = 3
    stepSize = 3
    trials = 3

    if(len(sys.argv) > 1):
        for i in range(1, len(sys.argv)):
            if sys.argv[i] == "size" and len(sys.argv) > i + 1:
                size = int(sys.argv[i + 1])
            elif sys.argv[i] == "steps" and len(sys.argv) > i + 1:
                steps = int(sys.argv[i + 1])
            elif sys.argv[i] == "stepSize" and len(sys.argv) > i + 1:
                stepSize = int(sys.argv[i + 1])
            elif sys.argv[i] == "trials" and len(sys.argv) > i + 1:
                trials = int(sys.argv[i + 1])
            elif sys.argv[i] == "mode" and len(sys.argv) > i + 1:
                mode = sys.argv[i + 1]
            
    maxSize = 0
    if mode == "mul":
        maxSize = size * stepSize ** (steps - 1)
    elif mode == "add":
        maxSize = (steps-1)*stepSize + size

    if not exists("RunTimeResults/"):
        os.mkdir("RunTimeResults")

    print(f"Testing matrices from n={size} to n={maxSize}")

    fileName = f"run_times_{size}_to_{maxSize}"
    numString = ""
    num = 0
    while(exists("RunTimeResults/" + fileName + numString + ".csv")):
        num = num + 1
        numString = f"({num})"
    fileName = fileName + numString

    fileName = fileName + ".csv"

    file = open("RunTimeResults/" + fileName, 'w')
    file.write("Matrix Size, Elements")
    for trial in range(trials):
        file.write(f", BMM{trial}")
    for trial in range(trials):
        file.write(f", SAM{trial}")
    file.write("\n")
    file.close()

    loadingBarSize = 20

    loadingBar = " " * loadingBarSize
    print(f"Multiplying matrices... [{loadingBar}] (0/{steps}) ", end="\r")

    matrix = Matrix()
    data = []
    for i in range(size):
        column = []
        for j in range(size):
            column.append(i + j)
        data.append(column)
    matrix.importData(data)
    for step in range(steps):
        file = open("RunTimeResults/" + fileName, "a")
        file.write(f"{size}, {size ** 2}")

        progress = int(step / steps * loadingBarSize)
        loadingBar = "█" * progress + " " * (loadingBarSize - progress)
        print(f"Multiplying matrices... [{loadingBar}] ({step}/{steps})    ", end="\r")

        for _ in range(trials):
            # Analysis of Basic Multiplication
            startTime = time.time()
            result = matrix.BMM(matrix)
            endTime = time.time()
            basicTime = endTime - startTime
            file.write(f", {basicTime}")

        # Analysis of Straussen's
        for _ in range(trials):
            startTime = time.time()
            result = matrix.SAM(matrix)
            endTime = time.time()
            SAMTime = endTime - startTime
            file.write(f", {SAMTime}")

        # # Analysis of SAMk
        # for _ in range(trials):
        #     startTime = time.time()
        #     result = matrix.SAMk(matrix)
        #     endTime = time.time()
        #     SAMkTime = endTime - startTime
        #     file.write(f", {SAMkTime}")

        file.write("\n")

        if step < steps-1:
            # Expand the old matrix (rather than make a new one)
            # Much faster so that tests can run longer
            if mode == "mul":
                newSize = size * stepSize
            elif mode == "add":
                newSize = size + stepSize
            matrix.expandMatrix(newSize, newSize, fill=(lambda i, j: i + j))
            size = newSize
    
    loadingBar = "█" * loadingBarSize
    print(f"Multiplying matrices... [{loadingBar}] ({steps}/{steps})\a      ")

    file.close()
