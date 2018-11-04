import sys
import numpy as np

left_Matrix = []
right_Matrix = []
Arr_line = []
used_file = []

def used_fileFun(file):
    line_counter = 0

    for line in file:
       Arr_line.append(line)

       for letter in line:
           if letter.isalpha()== True:
               if letter not in used_file: used_file.append(letter)
       line_counter = line_counter + 1

    return used_file



file = open(sys.argv[1], "r")

used_file = used_fileFun(open(sys.argv[1], "r"))
for line in file:
   arr_coefficient = []

   for letter in used_file:
       arr_coefficient.append(0)
   line_split = (line.split("="))
   line_split[1] = line_split[1].strip("\n")
   constant = int(line_split[1].strip(" "))

   for index, letter in enumerate(line_split[0]):
        if (letter.isalpha() == True):
            i = -1
            coeffic = ""
            negate = False
            while True:
                curPos = line_split[0][index+i]
                if curPos == "" or curPos == "-" or curPos== " ":
                    if line_split[0][index+i-1] == "-": negate = True
                    break
                else:
                    coeffic =  curPos + coeffic
                i = i - 1
            if letter != line_split[0][index]: arr_coefficient.append(0)
            if coeffic == " " or coeffic == "": coeffic = 1
            if coeffic == "-": coeffic = -1

            else: coeffic = int(coeffic)

            if negate == True:
                coeffic = str(coeffic)
                coeffic = "-" + coeffic
                coeffic = int(coeffic)
            for index2, alfa in enumerate(used_file):

                if alfa == line_split[0][index]: arr_coefficient[index2] = (coeffic)
   left_Matrix.append(arr_coefficient)
   right_Matrix.append(constant)

left_MatrixN = np.array(left_Matrix)
right_MatrixN = np.array(right_Matrix)
matrixRank = np.linalg.matrix_rank(left_MatrixN)
right_MatrixN = (np.expand_dims(right_MatrixN, axis=1))

extended_matr = (np.hstack((left_MatrixN, right_MatrixN)))

try:
    results = np.linalg.solve(left_Matrix, right_Matrix)
    resultStr = "solution: "
    for index, item in enumerate(results):
        resultStr = resultStr + (used_file[index] + " = " + str(item) + ", ")
    resultStr = resultStr.strip(", ")
    print(resultStr)

except:

    if len(used_file) != len(left_MatrixN):
            spaceDim = len(used_file) - len(left_MatrixN)
            print("solution space dimension: " + str(spaceDim))

    if np.linalg.matrix_rank(extended_matr) != matrixRank:
         print("no solution")
