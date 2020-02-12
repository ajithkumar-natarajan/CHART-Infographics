#!/usr/bin/env python3

import argparse
import os
import datetime


def parse_args():
	parser = argparse.ArgumentParser(description="Crop text portion from plots based on bounding boxes in associated JSON and deskew them")
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

os.chmod("./crop_txt.py", 0o755)
args = parse_args()

file_list = os.listdir('./plots/')
for file in file_list:
	print(file[0:-4])
	# print("./crop_txt.py --json-path jsons/"+file[0:-4]+".json"+" --plot-path plots/"+file+".png --result-saving-dir "+args.rs_dir)
	os.system("./crop_txt.py --json-path jsons/"+file[0:-4]+".json"+" --plot-path plots/"+file+" --result-saving-dir "+args.rs_dir)

os.chmod("./deskew_imgs.py", 0o755)
os.system("./deskew_imgs.py --image-dir "+args.rs_dir)