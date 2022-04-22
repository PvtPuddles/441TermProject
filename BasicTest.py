
from Matrix import Matrix

def testHeading(text, m1, m2, m3):

	text = f"┫ {text} ┣"

	textSize = m1.getMatrixWidth() + m2.getMatrixWidth() + m3.getMatrixWidth()
	textSize = textSize + 6				# Operators
	fillSize = textSize - len(text)

	text = "━" * int(fillSize/2) + text + "━" * (fillSize - int(fillSize/2))

	text = f"\033[1m{text}\033[0m"  	# Bold text

	return text

def doTest1():
	matrix1 = Matrix(1, 3)
	matrix1.data = [
		[1, 2, 3]
	]

	matrix2 = Matrix(3, 1)
	matrix2.data = [
		[4], [5], [6]
	]

	result = matrix1.multiply(matrix2)

	print(testHeading("TEST ONE", 
		matrix1, matrix2, result))

	Matrix.printMultiply(matrix1, matrix2, result)

def doTest2():

	matrix1 = Matrix(3, 1)
	matrix1.data = [
		[4], [5], [6]
	]

	matrix2 = Matrix(1, 3)
	matrix2.data = [
		[1, 2, 3]
	]

	result = matrix1.multiply(matrix2)

	print(testHeading("TEST TWO", 
		matrix1, matrix2, result))

	Matrix.printMultiply(matrix1, matrix2, result)

def doTest3():
	matrix1 = Matrix(2, 3)
	matrix1.data = [
		[1, 2, 3], 
		[4, 5, 6]
	]

	matrix2 = Matrix(3, 2)
	matrix2.data = [
		[7, 8], 
		[9, 10],
		[11, 12]
	]

	result = matrix1.multiply(matrix2)

	print(testHeading("TEST THREE", 
		matrix1, matrix2, result))

	Matrix.printMultiply(matrix1, matrix2, result)


def doTest4():

	matrix1 = Matrix(5, 7)
	for i in range(matrix1.rows):
		for j in range(matrix1.columns):
			matrix1.data[i][j] = (i+1) * (j+1)

	matrix2 = Matrix(7, 3)
	for i in range(matrix2.rows):
		for j in range(matrix2.columns):
			matrix2.data[i][j] = i + j

	result = matrix1.multiply(matrix2)

	
	print(testHeading("TEST FOUR", 
		matrix1, matrix2, result))

	Matrix.printMultiply(matrix1, matrix2, result)



if __name__ == "__main__":

	doTest1()

	doTest2()

	doTest3()

	doTest4()

