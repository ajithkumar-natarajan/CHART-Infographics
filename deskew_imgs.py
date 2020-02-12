#!/usr/bin/env python3

import argparse
import cv2
import os, fnmatch
import numpy as np
from math import atan2,degrees
import matplotlib.pyplot as plt
import imutils

def parse_args():
	parser = argparse.ArgumentParser(description="Location of images to be deskewed")
	parser.add_argument(
		"--image-dir",
		dest="im_dir",
		type=str,
		help="directory in which cropped images are present"
	)
	args = parser.parse_args()
	return args

def imshow_components(labels, midpoints, file_name):
	# Map component labels to hue val
	label_hue = np.uint8(179*labels/np.max(labels))
	blank_ch = 255*np.ones_like(label_hue)
	labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])

	# cvt to BGR for display
	labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)

	# set bg label to black
	labeled_img[label_hue==0] = 1

	# cv2.imshow(file_name, labeled_img)
	# cv2.imshow("cc", labeled_img)
	# cv2.waitKey()

	color = (250, 169, 160)
	# print(labeled_img.shape)
	for midpoint in midpoints:
		# print(midpoint[1], midpoint[0])
		labeled_img[midpoint[1], midpoint[0]] = color
	# cv2.imshow("labeled_img", labeled_img)
	# cv2.waitKey()


def calculate_angle(midpoints):
	print("midpoints", midpoints)
	angles = list()
	midpoints_count = len(midpoints)
	# for i in range (0, midpoints_count-1):
	# 	x_diff = abs(midpoints[i+1][1] - midpoints[i][1])
	# 	y_diff = abs(midpoints[i+1][0] - midpoints[i][0])
	# 	angles.append(degrees(atan2(y_diff, x_diff)))

	# print(angles)
	for i in range (0, midpoints_count):
		for j in range(i+1, midpoints_count):
			x_diff = abs(midpoints[i][0] - midpoints[j][0])
			y_diff = abs(midpoints[i][1] - midpoints[j][1])
			# print("diffs", y_diff, x_diff, degrees(atan2(y_diff, x_diff)))
			angles.append(degrees(atan2(y_diff, x_diff)))

	return (angles)


def get_histogram_stats(angles):
	counts, bins, bars = plt.hist(angles, bins=[0,10,20,30,40,50,60,70,80,90])
	# print(counts, bins, bars)
	# plt.show()
	return counts, bins, bars


def rotateImage(image, angle, borderValue=(255,255,255)):
	# grab the dimensions of the image and then determine the
	# center
	(h, w) = image.shape[:2]
	(cX, cY) = (w / 2, h / 2)
	# grab the rotation matrix (applying the negative of the
	# angle to rotate clockwise), then grab the sine and cosine
	# (i.e., the rotation components of the matrix)
	M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
	cos = np.abs(M[0, 0])
	sin = np.abs(M[0, 1])
	# compute the new bounding dimensions of the image
	nW = int((h * sin) + (w * cos))
	nH = int((h * cos) + (w * sin))
	# adjust the rotation matrix to take into account translation
	M[0, 2] += (nW / 2) - cX
	M[1, 2] += (nH / 2) - cY
	# perform the actual rotation and return the image
	return cv2.warpAffine(image, M, (nW, nH), borderValue=borderValue)

args = parse_args()
im_dir = args.im_dir
cropped_imgs_loc = "./cropped_imgs/"+im_dir
cropped_imgs_list = fnmatch.filter(os.listdir(cropped_imgs_loc), '*.png')


for file in cropped_imgs_list:
	img = cv2.imread(os.path.join(cropped_imgs_loc, file), 0)
	kernel = np.ones((1, 1), np.uint8)

	# print(img.shape)

	# Threshold it so it becomes binary
	ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)
	thresh = 255-thresh
	# cv2.imshow("thresh", thresh)
	# cv2.waitKey()
	
	img_eroded = cv2.erode(thresh, kernel, iterations=1)
	# img_eroded = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
	
	# You need to choose 4 or 8 for connectivity type
	connectivity = 4
	CC_output = cv2.connectedComponentsWithStats(img_eroded, connectivity, cv2.CV_32S)
	
	# cv2.imshow("img_eroded", img_eroded)
	# cv2.waitKey()

	# print(index for index in img if(index != 255))
	# print(CC_output[2])
	# print(type(CC_output[2]))
	CC_shape = CC_output[2].shape
	# print(CC_output[2][0][2])
	midpoints = list()
	for i in range(1, CC_shape[0]):
		if(CC_output[2][i][4]>8):
			midpoints.append((int(CC_output[2][i][0]+CC_output[2][i][2]/2), int(CC_output[2][i][1]+CC_output[2][i][3]/2)))
		# print(CC_output[2][i][3])
		# print("area- ", CC_output[2][i][4])

	# print(midpoints)


	imshow_components(CC_output[1], midpoints, file)
	angles = calculate_angle(midpoints)
	counts, bins, bars = get_histogram_stats(angles)
	angle_to_rotate_max = list(counts).index(max(counts))
	if(len(angles)!=0):
		angle_to_rotate_cnt = 0
		angle_to_rotate_sum = 0
		for angle in angles:
			if(angle>=angle_to_rotate_max*10 and angle<=angle_to_rotate_max*10+10):
				angle_to_rotate_sum += angle
				angle_to_rotate_cnt += 1
		angle_to_rotate = angle_to_rotate_sum/angle_to_rotate_cnt
	else:
		angle_to_rotate = 0
	# angle_to_rotate = (list(counts).index(max(counts))*10+5)
	# print(angles)
	# print(list(counts).index(max(counts)))
	print(angle_to_rotate)
	h, c = img.shape
	if not os.path.exists(cropped_imgs_loc+"/rotated"):
		os.makedirs(cropped_imgs_loc+"/rotated")
	if(angle_to_rotate<80):
		# if(h>c and CC_output[0] != 2):
		# 	cv2.imwrite(cropped_imgs_loc+"/rotated/rotated_"+file, rotateImage(img, 90-angle_to_rotate, borderValue=(255,255,255)))
		# else:
		# 	cv2.imwrite(cropped_imgs_loc+"/rotated/rotated_"+file, rotateImage
		# 	(img, angle_to_rotate, borderValue=(255,255,255)))
		cv2.imwrite(cropped_imgs_loc+"/rotated/rotated_"+file, rotateImage
			(img, angle_to_rotate, borderValue=(255,255,255)))
			
	else:
		cv2.imwrite(cropped_imgs_loc+"/rotated/rotated_"+file, img)
	print(file)
	print(counts)
	# print()
	# cv2.imwrite("/home/ajithkumar/Documents/CUBS/Data_subset/rotated_1.png", rotateImage(img, 13.794))
	# print(img.shape)
	print()