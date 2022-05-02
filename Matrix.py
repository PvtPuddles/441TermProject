

class Matrix:

	def importData(self, data, rows=-1, columns=-1):
		self.data = data
		if rows == -1:
			self.rows = len(data)
		else:
			self.rows = rows
		if columns == -1:
			if self.rows > 0:
				self.columns = len(data[0])
			else:
				self.columns = 0
		else:
			self.columns = columns
		return self
	
	def makeMatrix(self, rows, columns):
		self.rows = rows
		self.columns = columns
		self.data=[]
		for _ in range(self.rows):
			col = []
			for _ in range(self.columns):
				col.append(0)
			self.data.append(col)
		return self

	def makeSubMatrix(self, rows, columns, reference, startRow, startCol):
		self.rows = rows
		self.columns = columns
		self.data=[]
		for i in range(self.rows):
			col = []
			for j in range(self.columns):
				col.append(reference[startRow + i][startCol + j])
			self.data.append(col)
		return self
	
	def __len__(self):
		return self.rows

	def __getitem__(self, key):
		return self.data[key]

	def __add__(self, other):
		if not self.rows == other.rows or not self.columns == other.columns:
			raise Exception("Incompatible matrices, addition failed")

		result = Matrix().makeMatrix(self.rows, self.columns)
		for i in range(self.rows):
			for j in range(self.columns):
				result[i][j] = self[i][j] + other[i][j]
		return result

	def __sub__(self, other):
		if not self.rows == other.rows or not self.columns == other.columns:
			raise Exception("Incompatible matrices, subtraction failed")

		result = Matrix().makeMatrix(self.rows, self.columns)
		for i in range(self.rows):
			for j in range(self.columns):
				result[i][j] = self[i][j] - other[i][j]
		return result

	# Basic matrix multiplication
	def BMM(self, other):
		if not self.columns == other.rows:
			raise Exception("Incompatible matrices, BMM failed")

		result = Matrix().makeMatrix(self.rows, other.columns)

		for i in range(0, result.rows):
			for j in range(0, result.columns):
				mul = 0
				for k in range(0, self.columns):
					a = self.data[i][k]
					b = other.data[k][j]
					mul = mul + a * b
				result.data[i][j] = mul

		return result

	def SAM(self, other):
		if self.rows != self.columns or other.rows != other.columns:
			raise Exception("Matrices must be square; SAM failed")
		if self.columns != other.rows:
			raise Exception("Incompatible matrices, SAM failed")
		
		if (self.rows == 1):
			result = Matrix().importData([[
				self[0][0] * other[0][0]
			]])
			return result

		# Check that matrix is a power of 2
		if (not (self.rows & (self.rows-1) == 0) and self.rows != 0):
			m = Matrix.__findNextPowerOf2(self.rows)
			# Deep copy of self and other (as to not modify their data)
			a = Matrix().importData([row[:] for row in self.data])
			a.expandMatrix(m, m)
			b = Matrix().importData([row[:] for row in other.data])
			b.expandMatrix(m, m)
		else:
			a = self
			b = other

		# Result matrix
		result = Matrix().makeMatrix(a.rows, a.columns)
		# Dimensions of sub-matrices
		k = a.rows // 2
		# Define and initialize sub-matrices (may be slow)
		ma11 = Matrix().makeSubMatrix(k, k, a, 0, 0)
		ma12 = Matrix().makeSubMatrix(k, k, a, 0, k)
		ma21 = Matrix().makeSubMatrix(k, k, a, k, 0)
		ma22 = Matrix().makeSubMatrix(k, k, a, k, k)
		mb11 = Matrix().makeSubMatrix(k, k, b, 0, 0)
		mb12 = Matrix().makeSubMatrix(k, k, b, 0, k)
		mb21 = Matrix().makeSubMatrix(k, k, b, k, 0)
		mb22 = Matrix().makeSubMatrix(k, k, b, k, k)
		# Define + initialize has a runtime of 8(k^2)
		# 	- Optimized to 7(k^2), but still a nasty amount of overhead
		# If this was programmed in c, we could simply move the pointers
		# 	for this to run in constant time

		p1 = ma11.SAM(mb12 - mb22)
		p2 = (ma11 + ma12).SAM(mb22)
		p3 = (ma21 + ma22).SAM(mb11)
		p4 = ma22.SAM(mb21 - mb11)
		p5 = (ma11 + ma22).SAM(mb11 + mb22)
		p6 = (ma12 - ma22).SAM(mb21 + mb22)
		p7 = (ma11 - ma21).SAM(mb11 + mb12)

		mr11 = (p5 + p4 + p6) - p2
		mr12 = p1 + p2
		mr21 = p3 + p4
		mr22 = (p5 + p1) - p3 - p7

		for i in range(k):
			for j in range(k):
				result[i][j] = mr11[i][j]
				result[i][j+k] = mr12[i][j]
				result[k+i][j] = mr21[i][j]
				result[k+i][k+j] = mr22[i][j]
		# Trim result back down to correct size
		result.rows = self.rows
		result.columns = self.columns
		result.data = [result[i][:result.columns] for i in range(result.rows)]

		return result


	def expandMatrix(self, rows, columns, *, fill = lambda i, j: 0):
		# Expand current columns to be taller
		for i in range(self.rows):
			for j in range(self.columns, columns):
				self[i].append(fill(i, j))

		# Add extra columns
		for i in range(self.rows, rows):
			column = []
			for j in range(columns):
				column.append(fill(i, j))
			self.data.append(column)
		self.rows = rows
		self.columns = columns
		return self

	@staticmethod
	def __findNextPowerOf2(n):
		#Bit manipulation stuff to find next power of 2 from n 
		n = n - 1

		n |= n >> 1
		n |= n >> 2
		n |= n >> 4
		n |= n >> 8
		n |= n >> 16

		return n + 1

	# Functions for pretty printing
	# -----------------------------

	# Gets witdh of the largest element in the matrix
	def getColumnWidth(self):
		width = 0
		for i in range(0, self.rows):
			for j in range(0, self.columns):
				if len(str(self.data[i][j])) > width:
					width = len(str(self.data[i][j]))
		return width

	# Gets total width of the matrix
	def getMatrixWidth(self):
		width = 2    			# | and |
		width = width + 1   	# padding before second |
		width = width + (self.getColumnWidth() + 1) * self.columns
		return width

	# Converts matrix data to pretty-array format for printing
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
		body = self.toArray()
		text = "\n"
		text = text.join(body)
		return text

	"""
	Pads the top + bottom of an array so that it displays nicely
	"""
	@staticmethod
	def padMatrixArray(matrix, width, targetHeight):
		if(len(matrix) < targetHeight):
			delta = int((targetHeight - len(matrix))/2)
			# Prepend blanks to top of array
			for _ in range(0, delta):
				matrix.insert(0, " " * width)
			# Append blanks to bottom of array
			for _ in range(len(matrix), targetHeight):
				matrix.append(" " * width)

		return matrix

	"""
	Prints the 3 provided matrices in the form
	matrix1 * matrix2 = resultMatrix
	~does not perform multiplacation~
	"""
	@staticmethod
	def printEquation(matrix1, matrix2, resultMatrix, *, symbol="*"):

		m1 = matrix1.toArray()
		m2 = matrix2.toArray()
		result = resultMatrix.toArray()

		height = max(matrix1.rows, matrix2.rows, resultMatrix.rows)

		# Pad matrices to line up nicely
		m1 = Matrix.padMatrixArray(m1, matrix1.getMatrixWidth(), height)
		m2 = Matrix.padMatrixArray(m2, matrix2.getMatrixWidth(), height)
		result = Matrix.padMatrixArray(result, resultMatrix.getMatrixWidth(), height)

		mid = int((height-1) // 2)
		for i in range(0, mid):
			print(f"{m1[i]}   {m2[i]}   {result[i]}")

		print(f"{m1[mid]} {symbol} {m2[mid]} = {result[mid]}")

		for i in range(mid + 1, height):
			print(f"{m1[i]}   {m2[i]}   {result[i]}")



