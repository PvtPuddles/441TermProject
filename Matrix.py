

class Matrix:

	def __init__(self, rows, columns):
		self.rows = rows
		self.columns = columns
		self.data=[]
		for i in range(self.rows):
		    col = []
		    for j in range(self.columns):
		        col.append(0)
		    self.data.append(col)

    # Functions for pretty printing
	def getColumnWidth(self):
		width = 0
		for i in range(0, self.rows):
			for j in range(0, self.columns):
				if len(str(self.data[i][j])) > width:
					width = len(str(self.data[i][j]))
		return width

	def getMatrixWidth(self):
		width = 2    			# | and |
		width = width + 1   	# padding before second |
		width = width + (self.getColumnWidth() + 1) * self.columns
		return width

	def multiply(self, other):
		if not self.columns == other.rows:
			raise Exception("Incompatible matrices, multiplication failed")

		result = Matrix(self.rows, other.columns)

		for i in range(0, result.rows):
			for j in range(0, result.columns):
				mul = 0
				for k in range(0, self.columns):
					a = self.data[i][k]
					b = other.data[k][j]
					mul = mul + a * b
				result.data[i][j] = mul

		return result


	def toArray(self):
		width = self.getColumnWidth()
		body = []

		for i in range(self.rows):
			if self.rows == 1:
				symbols = ("│", "│")
			elif i == 0:
				symbols = ("┌", "┐")
			elif i == self.rows - 1:
				symbols = ("└", "┘")
			else:
				symbols = ("│", "│")

			line = symbols[0]
			for j in range(self.columns):
				line = line + f" {self.data[i][j]:<{width}}"
			line = line + " " + symbols[1]
			body.append(line)

		return body

	def __str__(self):

		body = self.toArray();
		text = "\n"
		text = text.join(body)

		return text

	@staticmethod
	def padMatrixArray(matrix, width, targetHeight):
		if(len(matrix) < targetHeight):
			delta = int((targetHeight - len(matrix))/2)
			# Prepend blanks
			for i in range(0, delta):
				matrix.insert(0, " " * width)
			# Append blanks
			for i in range(len(matrix), targetHeight):
				matrix.append(" " * width)

		return matrix

	@staticmethod
	def printMultiply(matrix1, matrix2, resultMatrix):

		m1 = matrix1.toArray()
		m2 = matrix2.toArray()
		result = resultMatrix.toArray()

		height = max(matrix1.rows, matrix2.rows)

		# Pad matrices to line up nicely
		m1 = Matrix.padMatrixArray(m1, matrix1.getMatrixWidth(), height)
		m2 = Matrix.padMatrixArray(m2, matrix2.getMatrixWidth(), height)
		result = Matrix.padMatrixArray(result, resultMatrix.getMatrixWidth(), height)
		
		# if(len(m2) < height):
		# 	delta = int((height - len(m2))/2)
		# 	for i in range(0, delta):
		# 		m2.insert(0, " " * matrix2.getColumnWidth())

		for i in range(0, int(height / 2)):
			print(f"{m1[i]}   {m2[i]}   {result[i]}")

		mid = int(height / 2)
		print(f"{m1[mid]} * {m2[mid]} = {result[mid]}")

		for i in range(int(height / 2) + 1, height):
			print(f"{m1[i]}   {m2[i]}   {result[i]}")



