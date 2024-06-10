from PyQt6 import  uic
from PyQt6.QtWidgets import QApplication, QFileDialog,QMainWindow
from PyQt6.QtGui import QPixmap


import sys
from pathlib import Path
import cv2 as cv
import numpy as np
import tempfile

import controller.ui_controller as ui
import model.image_filter as image_filter

class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('ui/app.ui', self)

        self.hasSelect = False
        self.image_origin_path = ""
        self.hasResult = False

        #menu
        self.select_image_menu.triggered.connect(self.select_image)
        self.save_image_menu.triggered.connect(self.save_image)
        self.kernel_convolution_menu.triggered.connect(self.kernel_convolution)
        self.gaussian_menu.triggered.connect(self.gaussian_blur)
        self.median_menu.triggered.connect(self.median_blur)
        self.sharpen_menu.triggered.connect(self.sharpening)
        self.bilateral_menu.triggered.connect(self.bilateral_blur)
        self.sobel_menu.triggered.connect(self.edge_detection_sobel)
        self.canny_menu.triggered.connect(self.edge_detection_canny)


        #button
        self.kernel_convolution_btn.clicked.connect(self.kernel_convolution)
        self.gaussian_btn.clicked.connect(self.gaussian_blur)
        self.median_btn.clicked.connect(self.median_blur)
        self.sharpen_btn.clicked.connect(self.sharpening)
        self.bilateral_btn.clicked.connect(self.bilateral_blur)
        self.sobel.clicked.connect(self.edge_detection_sobel)
        self.canny.clicked.connect(self.edge_detection_canny)

        self.show()

    def select_image(self):
        filename, ok = QFileDialog.getOpenFileName(
            self,
            "Select a File", 
            r"D:/", 
            "Images (*.png *.jpg *.jpeg)"
        )
        if filename:
            path = Path(filename)
            self.img_data = ui.image_frame.setUpPixmap(self,str(path),900,700)
            self.image.setPixmap(self.img_data)
            self.image_origin_path = filename
            self.hasSelect = True
    
    #blur
    def kernel_convolution(self):
        if not self.hasSelect:
            ui.message.alert(self,message="Please choose image first!")
        else:
            output = image_filter.blur_operation.kernel_convolution(self,str(self.image_origin_path))

            self.img_data = ui.image_frame.openCVtoPixmap(self,output,900,700)
            self.image.setPixmap(self.img_data)
            self.hasResult = True

    def gaussian_blur(self):
        if not self.hasSelect:
            ui.message.alert(self,message="Please choose image first!")
        else:
            output = image_filter.blur_operation.gaussian_blur(self,str(self.image_origin_path))
            
            self.img_data = ui.image_frame.openCVtoPixmap(self,output,900,700)
            self.image.setPixmap(self.img_data)
            self.hasResult = True

    def median_blur(self):
        if not self.hasSelect:
            ui.message.alert(self,message="Please choose image first!")
        else:
            output = image_filter.blur_operation.median_blur(self,str(self.image_origin_path))

            self.img_data = ui.image_frame.openCVtoPixmap(self,output,900,700)
            self.image.setPixmap(self.img_data)
            self.hasResult = True

    def sharpening(self):
        if not self.hasSelect:
            ui.message.alert(self,message="Please choose image first!")
        else:
            output = image_filter.blur_operation.sharpening(self,str(self.image_origin_path))

            self.img_data = ui.image_frame.openCVtoPixmap(self,output,900,700)
            self.image.setPixmap(self.img_data)
            self.hasResult = True
        
    def bilateral_blur(self):
        if not self.hasSelect:
            ui.message.alert(self,message="Please choose image first!")
        else:
            output = image_filter.blur_operation.bilateral_blur(self,str(self.image_origin_path))

            self.img_data = ui.image_frame.openCVtoPixmap(self,output,900,700)
            self.image.setPixmap(self.img_data)
            self.hasResult = True

    #edge detection
    def edge_detection_sobel(self):
        if self.image_origin_path == "" :
            ui.message.alert(self,message= "please choose image first!")
        else:
            img = cv.imread(self.image_origin_path)
            img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            img_blur = cv.GaussianBlur(img_gray,(3,3),0)


            grad_x = cv.Sobel(img_blur, cv.CV_64F, 1, 0)
            grad_y = cv.Sobel(img_blur, cv.CV_64F, 0, 1)
            grad = np.sqrt(grad_x**2 + grad_y**2)
            output = (grad * 255 / grad.max()).astype(np.uint8)

            temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)

                
            cv.imwrite(temp_file.name,output)

            self.img_data = ui.image_frame.setUpPixmap(self,temp_file.name,900,700)
            self.image.setPixmap(self.img_data)
            self.hasResult = True

    def edge_detection_canny(self):
        if self.image_origin_path == "" :
            ui.message.alert(self,message= "please choose image first!")
        else:
            img = cv.imread(self.image_origin_path)
            img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            img_blur = cv.GaussianBlur(img_gray,(3,3),0)

            output = cv.Canny(image=img_blur, threshold1=100, threshold2=200)

            temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)

                
            cv.imwrite(temp_file.name,output)

            self.img_data = ui.image_frame.setUpPixmap(self,temp_file.name,900,700)
            self.image.setPixmap(self.img_data)
            self.hasResult = True

    
    def save_image(self):
        if not self.hasResult :
            ui.message.alert(self,message="no result generate yet!")
        else:
            ui.button_control.save_image(self,img_data=self.img_data)

app = QApplication(sys.argv)
window = Ui()
app.exec()
