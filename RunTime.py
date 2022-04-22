
import sys
import time
import os
from os.path import exists

from Matrix import Matrix
from BasicTest import testHeading

if __name__ == "__main__":

    size = 10
    steps = 20
    stepSize = 10

    if(len(sys.argv) > 1):
        for i in range(1, len(sys.argv)):
            if sys.argv[i] == "startSize" and len(sys.argv) > i + 1:
                size = int(sys.argv[i + 1])
            elif sys.argv[i] == "steps" and len(sys.argv) > i + 1:
                steps = int(sys.argv[i + 1])
            elif sys.argv[i] == "stepSize" and len(sys.argv) > i + 1:
                stepSize = int(sys.argv[i + 1])

    if not exists("RunTimeResults/"):
        os.mkdir("RunTimeResults")

    fileName = f"run_times_{size}_to_{(steps-1)*stepSize + size}"
    numString = ""
    num = 0
    while(exists("RunTimeResults/" + fileName + numString + ".csv")):
        num = num + 1
        numString = f"({num})"
    fileName = fileName + numString

    fileName = fileName + ".csv"

    file = open("RunTimeResults/" + fileName, 'w')
    file.write("Matrix Size, Elements, Basic Multiply, SAM, SAMk\n")

    loadingBarSize = 20

    loadingBar = " " * loadingBarSize
    print(f"[{loadingBar}]", end="\r")

    for mat in range(steps):
        matrix = Matrix(size, size)
        for i in range(size):
            for j in range(size):
                matrix.data[i][j] = i + j

        # Analysis of Basic Multiplication
        startTime = time.time()
        result = matrix.multiply(matrix)
        endTime = time.time()
        basicTime = endTime - startTime

        # Analysis of Straussen's
        startTime = time.time()
        # result = matrix.SAM(matrix)
        endTime = time.time()
        SAMTime = endTime - startTime

        # Analysis of SAMk
        startTime = time.time()
        # result = matrix.SAMk(matrix)
        endTime = time.time()
        SAMkTime = endTime - startTime

        file.write(f"{size}, {size * size}, {basicTime}, {SAMTime}, {SAMkTime}\n")

        progress = int(mat / steps * loadingBarSize)
        loadingBar = "█" * progress + " " * (steps - progress)
        print(f"[{loadingBar}]", end="\r")
        size = size + stepSize
    
    loadingBar = "█" * loadingBarSize
    print(f"[{loadingBar}]")

    file.close()
