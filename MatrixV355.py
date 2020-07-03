import random


class Matrix(object):
    def __init__(self, matrix=None):
        if matrix is None:
            matrix = [[]]
        self.matrix = matrix
        if self.check_matrix() is True:
            self.columns = len(matrix[0])
            self.rows = len(matrix)
        else:
            raise NameError('The rows of the matrix must be equal in size')

    def check_matrix(self):
        check = True
        for i in range(len(self.matrix) - 1):
            if len(self.matrix[i]) != len(self.matrix[i + 1]):
                check = False
        return check

    @staticmethod
    def generate_matrix(i, j, c):
        return Matrix([[c for m in range(j)] for n in range(i)])

    @staticmethod
    def random_matrix(i, j, a, b):
        return Matrix([[random.randint(a, b) for m in range(j)] for n in range(i)])

    @staticmethod
    def get_unit_matrix(i):
        supmatrix = Matrix.generate_matrix(i, i, 0)
        for i in range(i):
            supmatrix.matrix[i][i] = 1
        return supmatrix

    def size(self):
        return self.rows, self.columns

    def copy(self):
        return Matrix([[self.matrix[i][j] for j in range(self.columns)] for i in range(self.rows)])

    def get_value(self, i, j):
        return self.matrix[i][j]

    def get_row(self, i):
        return Matrix([self.matrix[i]])

    def get_column(self, j):
        supmatrix = []
        for i in range(self.rows):
            supmatrix.append([self.get_value(i, j)])
        return Matrix(supmatrix)

    def extend_horizontally(self, other_matrix):
        if self.rows == other_matrix.rows:
            for i in range(self.rows):
                self.add_column(other_matrix.get_column(i))
            return Matrix(self.matrix)

    def extended_horizontally(self, other_matrix):
        supmatrix = self.copy()
        supmatrix.extend_horizontally(other_matrix)
        return supmatrix

    def extend_vertically(self, other_matrix):
        if self.columns == other_matrix.columns:
            for i in range(self.columns):
                self.add_row(other_matrix.get_row(i))
            return self

    def extended_vertically(self, other_matrix):
        supmatrix = self.copy()
        supmatrix.extend_vertically(other_matrix)
        return supmatrix

    def remove_column(self, j):
        for i in range(self.rows):
            del self.matrix[i][j]
        return self

    def removed_column(self, j):
        supmatrix = self.copy()
        return supmatrix.remove_column(j)

    def remove_row(self, i):
        del self.matrix[i]
        return self.matrix

    def removed_row(self, i):
        supmatrix = self.copy()
        return supmatrix.remove_row(i)

    def add_column(self, column_matrix):
        if column_matrix.columns == 1 and column_matrix.rows == self.rows:
            for i in range(self.rows):
                self.matrix[i].append(column_matrix.matrix[i][0])
            return self
        else:
            return

    def add_row(self, row_matrix):
        if row_matrix.rows == 1 and row_matrix.columns == self.columns:
            self.matrix.append(row_matrix.matrix[0])
            return self
        else:
            return

    def overwrite_column(self, j, column_matrix):
        if column_matrix.columns == 1 and column_matrix.rows == self.rows:
            for i in range(self.rows):
                self.matrix[i][j] = column_matrix.matrix[i][0]
            return self
        else:
            return

    def overwrite_row(self, i, row_matrix):
        if row_matrix.rows == 1 and self.columns == row_matrix.columns:
            self.matrix[i] = row_matrix.matrix[0]
            return self
        else:
            return

    def sum_column_values(self, j):
        count = 0
        for i in range(self.rows):
            count += self.matrix[i][j]
        return count

    def add(self, other):
        if self.rows == other.rows and self.columns == other.columns:
            supmatrix = self.generate_matrix(self.rows, self.columns, 0)
            for i in range(self.rows):
                for j in range(self.columns):
                    supmatrix.matrix[i][j] = self.matrix[i][j] + other.matrix[i][j]
            return supmatrix
        else:
            return

    def scaler(self, c):
        supmatrix = self.copy()
        for i in range(self.rows):
            for j in range(self.columns):
                supmatrix.matrix[i][j] *= c
        return supmatrix

    def column_multiply(self, column_matrix):
        if column_matrix.columns == 1 and column_matrix.rows == self.columns:
            supmatrix = self.generate_matrix(self.rows, 1, 0)
            for i in range(self.columns):
                supmatrix = supmatrix.add(self.get_column(i).scaler(column_matrix.matrix[i][0]))
            return supmatrix
        else:
            return

    def sum_row_values(self, i):
        count = 0
        for j in range(self.rows):
            count += self.matrix[i][j]
        return count

    def multiply(self, other):
        if self.columns == other.rows:
            supmatrix = self.generate_matrix(self.rows, other.columns, 0)
            for i in range(other.columns):
                supmatrix.overwrite_column(i, self.column_multiply(other.get_column(i)))
            return supmatrix
        else:
            return

    def power(self, x):
        if self.columns == self.rows and type(x) == int:
            supmatrix = self.copy()
            for i in range(x - 1):
                supmatrix = supmatrix.multiply(self)
            return supmatrix
        else:
            return

    def row_operation(self, i1, op1, i2, op2, i3):
        if op2 == 1:
            return self.overwrite_row(i3, self.get_row(i1).scaler(op1).add(self.get_row(i2)))
        elif op2 == 0:
            return self.overwrite_row(i3, self.get_row(i1).scaler(op1))
        else:
            return self.overwrite_row(i3, self.get_row(i1).scaler(op1).add(self.get_row(i2).scaler(op2)))

    def reduce(self):
        for i in range(self.rows - 1):
            for n in range(i + 1, self.rows):
                for j in range(self.columns):
                    if self.matrix[i][j] != 0:
                        self.row_operation(i, -(self.matrix[n][j] / self.matrix[i][j]), n, 1, n)
                        break
        return self

    def full_reduce(self):
        for i in range(self.rows):
            for n in range(self.rows):
                if n != i:
                    for j in range(self.columns):
                        if self.matrix[i][j] != 0:
                            self.row_operation(i, -(self.matrix[n][j] / self.matrix[i][j]), n, 1, n)
                            break
        if self.rows < self.columns:
            for i in range(self.rows):
                for j in range(self.columns):
                    if self.matrix[i][j] != 0:
                        self.row_operation(i, 1 / self.matrix[i][j], i, 0, i)
                        break
        else:
            for i in range(self.columns):
                for j in range(self.rows):
                    if self.matrix[i][j] != 0:
                        self.row_operation(i, 1 / self.matrix[i][j], i, 0, i)
                        break
        return self

    def reduced(self):
        supmatrix = self.copy()
        return supmatrix.reduce()

    def full_reduced(self):
        supmatrix = self.copy()
        return supmatrix.full_reduce()

    def rank(self):
        supmatrix = self.full_reduced()
        rank = 0
        for i in range(supmatrix.rows):
            for j in range(supmatrix.columns):
                if supmatrix.matrix[i][j] != 0:
                    rank += 1
                    break
        return rank

    def det(self):
        if self.rows == self.columns and self.rows == self.rank():
            supmatrix = self.reduced()
            det = 1
            for i in range(self.rows):
                det *= supmatrix.matrix[i][i]
            if det is None:
                return 0
            else:
                return det

    def invert(self):
        if self.rows == self.columns and self.rows == self.rank():
            self.extend_horizontally(self.get_unit_matrix(self.rows)).full_reduce()
            for j in range(self.rows):
                self.remove_column(0)
            return self

    def inverted(self):
        supmatrix = self.copy()
        return supmatrix.invert()

    def __str__(self):
        for i in range(len(self.matrix)):
            print(self.matrix[i])
        return str(self.rows) + ' X ' + str(self.columns)
