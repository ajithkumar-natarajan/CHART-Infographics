import os
from shutil import copyfile


for each_file in os.listdir('/home/ajithkumar/Desktop/Data_subset/plots'):
#	files_list = list()
#	files_list.append(each_file)
#	split_files_list = list()
#	split_files_list.append(each_file.split('.')[0])
#	print(split_files_list)
	copyfile('/media/ajithkumar/Softwares & Others/CUBS/train_json_gt/json_gt/'+str(each_file.split('.')[0])+'.json', '/home/ajithkumar/Desktop/Data_subset/jsons/'+str(each_file.split('.')[0])+'.json')

print("Completed successfully")
