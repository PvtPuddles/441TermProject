
import sys
import time
import os
from os.path import exists

from Matrix import Matrix
from Sam import SMatrixTools
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

    print(f"Testing matrices from n={size} to n={(steps-1)*stepSize + size}")

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
    file.close()

    loadingBarSize = 20

    loadingBar = " " * loadingBarSize
    print(f"Multiplying matrices... [{loadingBar}]", end="\r")

    matrixTools = SMatrixTools()


    matrix = Matrix(size, size)
    for i in range(size):
        for j in range(size):
            matrix.data[i][j] = i + j
    for mat in range(steps):
        # Analysis of Basic Multiplication
        startTime = time.time()
        result = matrix.multiply(matrix)
        endTime = time.time()
        basicTime = endTime - startTime

        # Analysis of Straussen's
        _matrix = matrixTools.padMatrix(matrix, len(matrix))

        startTime = time.time()
        result = matrixTools.multiply(_matrix, _matrix, len(_matrix))
        endTime = time.time()
        SAMTime = endTime - startTime

        # _result = Matrix(len(result), len(result[0]))
        # _result.data = result
        # print(_result)

        # Analysis of SAMk
        startTime = time.time()
        # result = matrix.SAMk(matrix)
        endTime = time.time()
        SAMkTime = endTime - startTime

        file = open("RunTimeResults/" + fileName, 'a')
        file.write(f"{size}, {size * size}, {basicTime}, {SAMTime}, {SAMkTime}\n")
        file.close()

        progress = int(mat / steps * loadingBarSize)
        loadingBar = "█" * progress + " " * (steps - progress)
        print(f"Multiplying matrices... [{loadingBar}]", end="\r")

        if mat < steps-1:
            # Expand the old matrix (rather than make a new one)
            # Much faster so that tests can run longer
            newSize = size + stepSize
            # Expand current columns to be taller
            for i in range(size):
                for j in range(size, newSize):
                    matrix[i].append(i+j)
            # Add extra columns
            for i in range(size, newSize):
                column = []
                for j in range(newSize):
                    column.append(i + j)
                matrix.data.append(column)
            matrix.rows = newSize
            matrix.columns = newSize
            size = newSize
    
    loadingBar = "█" * loadingBarSize
    print(f"Multiplying matrices... [{loadingBar}]")

    file.close()
