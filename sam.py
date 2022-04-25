import unittest

class SMatrixTools:

    def __initMatrix(self, n) -> list:
            resultMatrix = []
            for i in range(n):
                column = []
                for j in range(n):
                    column.append(0)
                resultMatrix.append(column)
            return resultMatrix

    def __add(self, m1, m2, n) -> list:
        addedMatrix = self.__initMatrix(n)
        for i in range(n):
            for j in range(n):
                addedMatrix[i][j] = m1[i][j] + m2[i][j]
        return addedMatrix

    def __subtract(self, m1, m2, n) -> list:
        addedMatrix = self.__initMatrix(n)
        for i in range(n):
            for j in range(n):
                addedMatrix[i][j] = m1[i][j] - m2[i][j]
        return addedMatrix

    def __findNextPowerOf2(self, n):
        #Bit manipulation stuff to find next power of 2 from n 
        n = n - 1
    
        n |= n >> 1
        n |= n >> 2
        n |= n >> 4
        n |= n >> 8
        n |= n >> 16
    
        return n + 1


    def padMatrix(self, matrix, n) -> list:
        if (not (n & (n-1) == 0) and n != 0):
            m = self.__findNextPowerOf2(n)
            temp = self.__initMatrix(m)
            for i in range(n):
                for j in range(n):
                    temp[i][j] = matrix[i][j]
            return temp
        else:
            return matrix


    
    def multiply(self, m1, m2, n) -> list:
        if (len(m1) != len(m2)):            
            raise RuntimeError('Matrix sizes do not match')    
        else:
            if (n == 1):
                result = self.__initMatrix(1)
                result[0][0]  = m1[0][0] * m2[0][0]
                return result
            
            #Result matrix
            result = self.__initMatrix(n)
            #Dimension of sub-matrices
            k = n // 2
            #Initialize and define sub-matrices
            ma11 = self.__initMatrix(k)
            ma12 = self.__initMatrix(k)
            ma21 = self.__initMatrix(k)
            ma22 = self.__initMatrix(k)
            mb11 = self.__initMatrix(k)
            mb12 = self.__initMatrix(k)
            mb21 = self.__initMatrix(k)
            mb22 = self.__initMatrix(k)

            for i in range(k):
                for j in range(k):
                    ma11[i][j] = m1[i][j]
                    ma12[i][j] = m1[i][k+j]
                    ma21[i][j] = m1[k+i][j]
                    ma22[i][j] = m1[k+i][k+j]
                    mb11[i][j] = m2[i][j]
                    mb12[i][j] = m2[i][k+j]
                    mb21[i][j] = m2[k+i][j]
                    mb22[i][j] = m2[k+i][k+j]
            
            p1 = self.multiply(ma11, self.__subtract(mb12, mb22, k), k)
            p2 = self.multiply(self.__add(ma11, ma12, k), mb22, k)
            p3 = self.multiply(self.__add(ma21, ma22, k), mb11, k)
            p4 = self.multiply(ma22, self.__subtract(mb21, mb11, k), k)
            p5 = self.multiply(self.__add(ma11, ma22, k), self.__add(mb11, mb22, k), k)
            p6 = self.multiply(self.__subtract(ma12, ma22, k), self.__add(mb21, mb22, k), k)
            p7 = self.multiply(self.__subtract(ma11, ma21, k), self.__add(mb11, mb12, k), k)

            mr11 = self.__subtract(self.__add(self.__add(p5, p4, k), p6, k), p2, k)
            mr12 = self.__add(p1, p2, k)
            mr21 = self.__add(p3, p4, k)
            mr22 = self.__subtract(self.__subtract(self.__add(p5, p1, k), p3, k), p7, k)

            for i in range(k):
                for j in range(k):
                    result[i][j] = mr11[i][j]
                    result[i][j+k] = mr12[i][j]
                    result[k+i][j] = mr21[i][j]
                    result[k+i][k+j] = mr22[i][j]
            return result

class TestMatrixInternalMethods(unittest.TestCase):
    def testInit(self):
        matrixTools = SMatrixTools()
        initializedMatrix = matrixTools._SMatrixTools__initMatrix(4)
        expectedMatrix = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.assertListEqual(initializedMatrix, expectedMatrix)

    def testInit2(self):
        matrixTools = SMatrixTools()
        initializedMatrix = matrixTools._SMatrixTools__initMatrix(2)
        expectedMatrix = [
            [0, 0],
            [0, 0]
        ]
        self.assertListEqual(initializedMatrix, expectedMatrix)

    def testInit3(self):
        matrixTools = SMatrixTools()
        initializedMatrix = matrixTools._SMatrixTools__initMatrix(3)
        expectedMatrix = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        self.assertListEqual(initializedMatrix, expectedMatrix)

    def testInit4(self):
        matrixTools = SMatrixTools()
        initializedMatrix = matrixTools._SMatrixTools__initMatrix(0)
        expectedMatrix = []
        self.assertListEqual(initializedMatrix, expectedMatrix)

    def testInit5(self):
        matrixTools = SMatrixTools()
        initializedMatrix = matrixTools._SMatrixTools__initMatrix(1)
        expectedMatrix = [
            [0]
        ]
        self.assertListEqual(initializedMatrix, expectedMatrix)
    
    def testAdd(self):
        matrixTools = SMatrixTools()
        matrix1 = [
            [1, 2],
            [3, 4]
        ]
        matrix2 = [
            [0, 0],
            [0, 0]
        ]
        addedMatrix = matrixTools._SMatrixTools__add(matrix1, matrix2, 2)
        expectedMatrix = [
            [1, 2],
            [3, 4]
        ]
        self.assertListEqual(addedMatrix, expectedMatrix)
    def testSubtract(self):
        matrixTools = SMatrixTools()
        matrix1 = [
            [1, 2],
            [3, 4]
        ]
        matrix2 = [
            [1, 2],
            [3, 4]
        ]
        addedMatrix = matrixTools._SMatrixTools__subtract(matrix1, matrix2, 2)
        expectedMatrix = [
            [0, 0],
            [0, 0]
        ]
        self.assertListEqual(addedMatrix, expectedMatrix)

class TestMatrixMultiplication(unittest.TestCase): 
    def testMultiply(self):
        matrixTools = SMatrixTools()
        matrix1 = [
            [1, 2],
            [3, 4]
        ]
        matrix2 = [
            [1, 2],
            [3, 4]
        ]
        matrix1 = matrixTools.padMatrix(matrix1, 2)
        matrix2 = matrixTools.padMatrix(matrix2, 2)
        multiplied = matrixTools.multiply(matrix1, matrix2, 2)
        expectedMatrix = [
            [7, 10],
            [15, 22]
        ]
        self.assertListEqual(multiplied, expectedMatrix)
    def testMultiply1(self):
        matrixTools = SMatrixTools()
        matrix1 = [
            [1, 2],
            [3, 4],
            [5, 6]
        ]
        matrix2 = [
            [1, 2],
            [3, 4]
        ]
        matrix1 = matrixTools.padMatrix(matrix1, 2)
        matrix2 = matrixTools.padMatrix(matrix2, 2)
        with self.assertRaises(RuntimeError):
            matrixTools.multiply(matrix1, matrix2, 2)
    def testMultiply3(self):
        matrixTools = SMatrixTools()
        matrix1 = [
            [1, 2, 3, 4],
            [3, 4, 5, 6],
            [5, 6, 7, 8],
            [5, 6, 7, 9]
        ]
        matrix2 = [
            [100, 50, 69, 70],
            [33, 45, 51, 90],
            [11, 77, 1000, 69],
            [11, 77, 1000, 15]
        ]
        matrix1 = matrixTools.padMatrix(matrix1, 4)
        matrix2 = matrixTools.padMatrix(matrix2, 4)
        multiplied = matrixTools.multiply(matrix1, matrix2, 4)
        expectedMatrix = [
            [243, 679, 7171, 517],
            [553, 1177, 11411, 1005],
            [863, 1675, 15651, 1493],
            [874, 1752, 16651, 1508]
        ]
      
        self.assertListEqual(multiplied, expectedMatrix)
    def testMultiply4(self):
        matrixTools = SMatrixTools()
        matrix1 = [
            [1, 2, 3],
            [3, 4, 5],
            [5, 6, 7]
        ]
        matrix2 = [
            [100, 50, 69],
            [33, 45, 51],
            [11, 77, 1000]
        ]
        matrix1 = matrixTools.padMatrix(matrix1, 3)
        matrix2 = matrixTools.padMatrix(matrix2, 3)
        multiplied = matrixTools.multiply(matrix1, matrix2, 4)
        expectedMatrix = [
            [199, 371, 3171, 0],
            [487, 715, 5411, 0],
            [775, 1059, 7651, 0],
            [0, 0, 0, 0]

        ]
        self.assertListEqual(multiplied, expectedMatrix)

    

if __name__ == '__main__':
    unittest.main()





        

        
