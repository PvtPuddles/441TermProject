
import sys
import time
import os
from os.path import exists

from Matrix import Matrix
from BasicTest import testHeading

if __name__ == "__main__":

    size = 50
    steps = 3
    stepSize = 50

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

    for mat in range(steps):
        matrix = Matrix(size, size)
        for i in range(size):
            for j in range(size):
                matrix.data[i][j] = i + j

        startTime = time.time()

        result = matrix.multiply(matrix)

        endTime = time.time()
        file.write(f"{size}, {endTime - startTime}\n")
        print(f"Matrices (size {size}) finished in {endTime - startTime}")

        size = size + stepSize

    file.close()
