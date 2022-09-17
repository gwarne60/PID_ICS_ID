#https://pbpython.com/python-word-template.html
#Import opencv for shape recognition
import cv2
#Import numpy for array manipulation
import numpy as np
#Import matplotlib for plotting
import matplotlib.pyplot as plt
#Import pandas for data manipulation
import pandas as pd
#Import os for file manipulation
import os
#Import sys for system manipulation
import sys
#Import re for regular expressions
import re
#Import datetime for date manipulation
import datetime

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
class ShapeDetector:
	def __init__(self):
		pass
	def detect(self, c):
		# initialize the shape name and approximate the contour
		shape = "unidentified"
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.04 * peri, True)
		# if the shape is a triangle, it will have 3 vertices
		if len(approx) == 3:
			shape = "triangle"
		# if the shape has 4 vertices, it is either a square or
		# a rectangle
		elif len(approx) == 4:
			# compute the bounding box of the contour and use the
			# bounding box to compute the aspect ratio
			(x, y, w, h) = cv2.boundingRect(approx)
			ar = w / float(h)
			# a square will have an aspect ratio that is approximately
			# equal to one, otherwise, the shape is a rectangle
			shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
		# if the shape is a pentagon, it will have 5 vertices
		elif len(approx) == 5:
			shape = "pentagon"
		# otherwise, we assume the shape is a circle
		else:
			shape = "circle"
		# return the name of the shape
		return shape


#Define a function called "PreProcess" which is intended to take an image and convert it to grayscale, blur it, and threshold it
def PreProcess(image):
    #Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #Blur the image
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    #Threshold the image
    thresh=cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    #thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY)[1]
    return thresh

#Set the path to the image
root = tk.Tk()
root.withdraw()
messagebox.showinfo("FHX Parser", "Please select the input pdf image")
file_path = filedialog.askopenfilename()

#Break the image into a grid of 256x256 pixel images , with 50% overlap horizontally and vertically
#Load the image
image = cv2.imread(file_path)
#Get the height and width of the image
(h, w) = image.shape[:2]
#Set the number of rows and columns
rows = 4
cols = 4
#Set the cell width and height
cellW = int(w / cols)
cellH = int(h / rows)
#Set the overlap
overlap = 0.5
#Set the horizontal and vertical overlap
overlapW = int(cellW * overlap)
overlapH = int(cellH * overlap)
#Set the number of horizontal and vertical cells
numX = int((w - overlapW) / (cellW - overlapW))
numY = int((h - overlapH) / (cellH - overlapH))
#Set the number of cells
numCells = numX * numY

#Create a list to hold the images
images = []
#Loop over the rows
for y in range(0, numY):
    print(y)
    #Loop over the columns
    for x in range(0, numX):
        #Get the starting and ending coordinates of the current cell
        startX = int(x * (cellW - overlapW))
        startY = int(y * (cellH - overlapH))
        endX = int(startX + cellW)
        endY = int(startY + cellH)
        #print(startX, startY, endX, endY)
        #Add the cell to the list of images
        images.append(image[startY:endY, startX:endX])

        #Export the images to a folder
        #Create a folder to hold the images in the root
        folder = os.path.join(os.path.dirname(file_path), 'images')
        #If the folder does not exist, create it
        if not os.path.exists(folder):
            os.makedirs(folder)
        #Create a list of the images
        image_list = images
        #print(len(image_list))
        #Loop over the images
for i in range(len(image_list)):
    #Get the image
    image = image_list[i]
    #Get the image name
    image_name = 'image_' + str(i) + '.png'
    #Get the image path
    image_path = os.path.join(folder, image_name)
    #Save the image
    cv2.imwrite(image_path, image)


#Loop through the images in image_path, and highlight +label shapes
for i in range(len(image_list)):
    print(i)
    image = image_list[i]
    #Preprocess the image
    thresh = PreProcess(image)
    #Find contours in the thresholded image
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    #Initialize the shape detector
    sd = ShapeDetector()
    #Loop over the contours
    for c in cnts:
        #Compute the center of the contour
        M = cv2.moments(c)
        #Check if M["m00"] is not zero - prevents ShapeDetector from erroring out if no shapes in image
        if M["m00"] != 0:
            cX = int((M["m10"] / M["m00"]) * 1)
            cY = int((M["m01"] / M["m00"]) * 1)
            #Detect the shape of the contour and label the contour
            shape = sd.detect(c)
            #Draw the contour and center of the shape on the image
            cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
            cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    #Export the images to a folder
    #Create a folder to hold the images in the root
    folder3 = os.path.join(os.path.dirname(file_path), 'images_3')
    #If the folder does not exist, create it
    if not os.path.exists(folder3):
        os.makedirs(folder3)
    #Create a list of the images
    image_list3 = images
    #print(len(image_list))
    #Loop over the images
    for i in range(len(image_list3)):
        #Get the image
        image = image_list3[i]
        #Get the image name
        image_name = 'image_' + str(i) + '.png'
        #Get the image path
        image_path = os.path.join(folder3, image_name)
        #Save the image
        cv2.imwrite(image_path, image)





