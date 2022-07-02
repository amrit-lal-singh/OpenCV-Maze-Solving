import cv2 as cv
import numpy as np
import random

matrix=np.full((100,100,3),255)
#print(matrix.show())
x_start=random.randrange(0,matrix.shape[0])
x_end=random.randrange(0,matrix.shape[0])
y_start=random.randrange(0,matrix.shape[1])
y_end=random.randrange(0,matrix.shape[1])
matrix[x_start,y_start]=125
matrix[x_end,y_end]=125

for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        prob=random.random()
        if prob>=0.2 and prob<=0.3:
            if (i!=x_start and j!=y_start) or (i!=x_end and j!=y_end):
                matrix[i,j]=0

cv.namedWindow('Maze',cv.WINDOW_NORMAL)
cv.imshow('Maze',matrix.astype(np.uint8))
cv.waitKey(0)
cv.destroyAllWindows()