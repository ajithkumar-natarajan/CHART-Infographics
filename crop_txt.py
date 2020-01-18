#!/usr/bin/env python3

import sys
import argparse
import json
import cv2
import datetime
import os
import fnmatch

def parse_args():
	parser = argparse.ArgumentParser(description="Crop text portion from plots based on bounding boxes in associated JSON")
	parser.add_argument(
		"--json-path",
		type=str,
		default="./jsons/1685.json",
		help="path to the json"
	)
	parser.add_argument(
		"--plot-path",
		type=str,
		default="./plots/1685.png",
		help="path to the plot"
	)
	now = datetime.datetime.today()
	nTime = now.strftime("%d-%m-%Y-%H-%M-%S")
	parser.add_argument(
		"--result-saving-dir",
		dest="rs_dir",
		type=str,
		default=nTime,
		help="directory to which cropped images are saved"
	)
	args = parser.parse_args()
	return args

args = parse_args()

in_json_file = args.json_path
in_im_file = args.plot_path


in_obj = json.load(open(in_json_file))
img = cv2.imread(in_im_file, 1)

# coords_file = open('/home/ajithkumar/Desktop/text-detection-ctpn/data/res/img.txt', 'r')

# img = cv2.imread("/home/ajithkumar/Desktop/text-detection-ctpn/data/demo/img.png")
# now = datetime.datetime.today()
# nTime = now.strftime("%d-%m-%Y-%H-%M-%S")
loc = './cropped_imgs/'
dest = os.path.join(loc+args.rs_dir)
if not os.path.exists(dest):
	os.makedirs(dest) #creat dest dir
# count = len(fnmatch.filter(os.listdir(dest), '*.png'))
count = in_im_file[in_im_file.find('/')+1:in_im_file.find('.')]
cnt = 0

for text_block_2_op in in_obj['task2']['output']['text_blocks']:
	if(text_block_2_op['text']!=""):
		bb = text_block_2_op['bb']
		
		# cropped_img = img[int(coords[1]):int(coords[5]), int(coords[0]):int(coords[2])]
		cropped_img = img[int(bb['y0']):int(bb['y0'] + bb['height']), int(bb['x0']):int(bb['x0'] + bb['width'])]

		# cv2.imwrite("cropped_img_"+str(count)+".png", cropped_img)
		cv2.imwrite(os.path.join(dest, "cropped_img_"+str(count)+"_"+str(cnt)+".png"), cropped_img)

	cnt += 1

print("Done")