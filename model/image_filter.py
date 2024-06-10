import cv2 as cv
import numpy as np


class blur_operation :
    def kernel_convolution(self,path):
        image = cv.imread(path)
        kernel = np.ones((5, 5), np.float32) / 25
        output = cv.filter2D(src=image, ddepth=-1, kernel=kernel)

        return output

    def gaussian_blur(self,path):
        image = cv.imread(path)
        output = cv.GaussianBlur(src=image, ksize=(5,5),sigmaX=0, sigmaY=0)

        return output
            

    def median_blur(self,path):
        image = cv.imread(path)
        output = cv.medianBlur(src=image, ksize=5)

        return output

    def sharpening(self,path):
        image = cv.imread(path)
        kernel = np.array([ [0, -1,  0],
                            [-1,  5, -1],
                            [0, -1,  0]])
        output = cv.filter2D(src=image, ddepth=-1, kernel=kernel)

        return output
        
    def bilateral_blur(self,path):
        image = cv.imread(path)
        output = cv.bilateralFilter(src=image, d=9, sigmaColor=75, sigmaSpace=75)

        return output