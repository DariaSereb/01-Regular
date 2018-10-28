#!/usr/bin/env python

import sys
import numpy as np

Matrix_l = []
Matrix_r = []
array_line = []
file_used = []

file = open(sys.argv[1], "r")

def file_used1(file):
    file = open(sys.argv[1], "r")
    lineCounter = 0

    for line in file:
       array_line.append(line)

       for letter in line:
           if letter.isalpha()== True:

               if letter not in file_used: file_used.append(letter)

       lineCounter = lineCounter + 1

    return file_used


file_used = file_used1(file)


for line in file:
   coefficient_array = []

   for letter in file_used:
       coefficient_array.append(0)

   line_split = (line.split("="))
   line_split[1] = line_split[1].strip("\n")
   constant = int(line_split[1].strip(" "))

   for index, letter in enumerate(line_split[0]):

        if (letter.isalpha() == True):
            coefficient = line_split[0][index-1]

            if letter != line_split[0][index]: coefficient_array.append(0)
            if coefficient == " ": coefficient = 1 
            if coefficient == "": coefficient = 1
            else: coefficient = int(coefficient)

            if line_split[0][index-2] == "-": coefficient = coefficient * -1
            for index1, variables in enumerate(file_used):
                if variables == line_split[0][index]: coefficient_array[index1] =(coefficient)

   Matrix_l.append(coefficient_array)
   Matrix_r.append(constant)

Matrix_l2 = np.array(Matrix_l)
Matrix_r2 = np.array(Matrix_r)

matrix_Rank = np.linalg.matrix_rank(Matrix_l2)
Matrix_r2 = (np.expand_dims(Matrix_r2, axis=1))
extendedMatrix = (np.hstack((Matrix_l2, Matrix_r2)))


try:
    results = np.linalg.solve(Matrix_l, Matrix_r)
    resultStr = "solution: "

    for index, item in enumerate(results):
        resultStr = resultStr + (file_used[index] + "=" + str(item) + ", ")
    resultStr = resultStr.strip(", ")
    print(resultStr)

except:

    if len(file_used) != len(Matrix_l2):
            spaceDim = len(file_used) - len(Matrix_l2)
            print("solution space dimension: " + str(spaceDim))

    if np.linalg.matrix_rank(extendedMatrix) != matrix_Rank:

            print("no solution")