
from Matrix import Matrix
from Sam import SMatrixTools

def testHeading(text, m1, m2, m3):

	text = f"┫ {text} ┣"

	textSize = m1.getMatrixWidth() + m2.getMatrixWidth() + m3.getMatrixWidth()
	textSize = textSize + 6				# Operators
	fillSize = textSize - len(text)

	text = "━" * int(fillSize/2) + text + "━" * (fillSize - int(fillSize/2))

	text = f"\033[1m{text}\033[0m"  	# Bold text

	return text

def doTest1():
	matrix1 = Matrix()
	matrix1.importData([
		[1, 2, 3]
	])

	matrix2 = Matrix()
	matrix2.importData([
		[4], [5], [6]
	])

	result = matrix1.BMM(matrix2)

	print(testHeading("BMM TEST ONE", 
		matrix1, matrix2, result))

	Matrix.printEquation(matrix1, matrix2, result)

def doTest2():

	matrix1 = Matrix()
	matrix1.importData([
		[4], [5], [6]
	])

	matrix2 = Matrix()
	matrix2.importData([
		[1, 2, 3]
	])

	result = matrix1.BMM(matrix2)

	print(testHeading("BMM TEST TWO", 
		matrix1, matrix2, result))

	Matrix.printEquation(matrix1, matrix2, result)

def doTest3():
	matrix1 = Matrix()
	matrix1.importData([
		[1, 2, 3], 
		[4, 5, 6]
	])

	matrix2 = Matrix()
	matrix2.importData([
		[7, 8], 
		[9, 10],
		[11, 12]
	])

	result = matrix1.BMM(matrix2)

	print(testHeading("BMM TEST THREE", 
		matrix1, matrix2, result))

	Matrix.printEquation(matrix1, matrix2, result)


def doTest4():
	matrix1 = Matrix()
	data = []
	for i in range(5):
		column = []
		for j in range(7):
			column.append((i+1) * (j+1))
		data.append(column)
	matrix1.importData(data.copy())

	matrix2 = Matrix()
	data = []
	for i in range(7):
		column = []
		for j in range(3):
			column.append(i + j)
		data.append(column)
	matrix2.importData(data.copy())

	result = matrix1.BMM(matrix2)

	
	print(testHeading("BMM TEST FOUR", 
		matrix1, matrix2, result))

	Matrix.printEquation(matrix1, matrix2, result)

def doBMMTests():
	doTest1()
	doTest2()
	doTest3()
	doTest4()

def doSAM1():
	matrix1 = Matrix().importData([
		[1, 2],
		[3, 4]
	])

	matrix2 = Matrix().importData([
		[5, 6],
		[7, 8]
	])

	resultBMM = matrix1.BMM(matrix2)

	print(testHeading("SAM TEST ONE", 
		matrix1, matrix2, resultBMM))

	print("BMM:")
	Matrix.printEquation(matrix1, matrix2, resultBMM)
	print("SAM:")
	resultSAM = matrix1.SAM(matrix2)
	Matrix.printEquation(matrix1, matrix2, resultSAM)

def doSAM2():
	matrix1 = Matrix().importData([
		[1, 2, 3],
		[3, 4, 5],
		[5, 6, 7]
	])

	matrix2 = Matrix().importData([
		[5, 6, 7],
		[7, 8, 9],
		[9, 10, 11]
	])

	resultBMM = matrix1.BMM(matrix2)

	print(testHeading("SAM TEST TWO", 
		matrix1, matrix2, resultBMM))

	print("BMM:")
	Matrix.printEquation(matrix1, matrix2, resultBMM)
	print("SAM:")
	resultSAM = matrix1.SAM(matrix2)
	Matrix.printEquation(matrix1, matrix2, resultSAM)

def doSAM3():
	matrix1 = Matrix().importData([
		[1, 2, 3, 4, 5],
		[3, 4, 5, 6, 7],
		[5, 6, 7, 8, 9],
		[7, 8, 9, 10, 11],
		[9, 10, 11, 12, 13]
	])

	matrix2 = Matrix().importData([
		[5, 6, 7, 8, 9],
		[7, 8, 9, 10, 11],
		[9, 10, 11, 12, 13],
		[11, 12, 13, 14, 15],
		[13, 14, 15, 16, 17]
	])

	resultBMM = matrix1.BMM(matrix2)

	print(testHeading("SAM TEST THREE", 
		matrix1, matrix2, resultBMM))

	print("BMM:")
	Matrix.printEquation(matrix1, matrix2, resultBMM)
	print("SAM:")
	resultSAM = matrix1.SAM(matrix2)
	Matrix.printEquation(matrix1, matrix2, resultSAM)

def doSAMTests():
	doSAM1()
	doSAM2()
	doSAM3()

if __name__ == "__main__":

	# doBMMTests()

	doSAMTests()


