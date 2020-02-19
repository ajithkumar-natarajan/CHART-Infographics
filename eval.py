import jellyfish
import argparse
import pytesseract
import json
from PIL import Image
import os


def parse_args():
	parser = argparse.ArgumentParser(description="Location of cropped images")
	parser.add_argument(
		"--image-dir",
		dest="im_dir",
		type=str,
		help="directory in which cropped images are present"
	)
	args = parser.parse_args()
	return args

def find(gt_text, ch):
	return [i for i, char in enumerate(gt_text) if char == ch]

args = parse_args()
im_dir = args.im_dir
rotated_imgs_loc = "./cropped_imgs/"+im_dir+"/rotated/"
# rotated_imgs_loc = "./cropped_imgs/"+im_dir+"/"
rotated_imgs_list = os.listdir(rotated_imgs_loc)
count = 1
error = 0
for img in rotated_imgs_list:
	loc = find(img, '_')
	# print(img)
	# print('./jsons/'+img[loc[-2]+1:loc[-1]]+'.json')
	obj = json.load(open('./jsons/'+img[loc[-2]+1:loc[-1]]+'.json'))
	# print(img[loc[-1]+1:img.find('.')])
	gt_text = obj['task2']['output']['text_blocks'][int(img[loc[-1]+1:img.find('.')])]['text']
	im = Image.open(rotated_imgs_loc+img)
	op_text = pytesseract.image_to_string(im, config='-l eng+equ+grc --oem 3 --psm 6')
	# print(gt_text)
	# print(op_text)
	# print(jellyfish.levenshtein_distance(op_text, gt_text))
	error += jellyfish.levenshtein_distance(op_text, gt_text)/len(gt_text)
	error_percent = error/count
	# print(error, error_percent, count)
	print(count)
	count += 1
	# if(count == 5):
		# break
print(error, error_percent)
