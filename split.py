# Importing all necessary libraries
from logging.config import valid_ident
import cv2
import os
import sys
import random
import argparse

def split_data():

    train_percent  = 92
    test_percent   = 4
    valid_percent  = 4

    images_path = os.path.join(opt.images,'')
    labels_path  = os.path.join(opt.labels,'')

    train_path  = os.path.join(opt.train_path,'')
    test_path   = os.path.join(opt.test_path,'')
    valid_path  = os.path.join(opt.valid_path,'')


    test_image_path = test_path+"images/"
    test_label_path = test_path+"labels/"
    valid_image_path = valid_path+"images/"
    valid_label_path = valid_path+"labels/"
    
    

    if not os.path.exists(images_path):
        print("Path do not exist: ",images_path)
        exit() 
    if not os.path.exists(labels_path):
        print("Path do not exist: ",labels_path)
        exit()  
    

    all_files = os.listdir(images_path)
    count = len(all_files)
    train_count = int(train_percent*count/100)
    test_count  = int(test_percent*count/100)
    valid_count = int(valid_percent*count/100)
    print("Count: ",count,"Train: ",train_count,"Test: ",test_count,"valid: ",valid_count)  


    valid_list = random.sample(all_files, valid_count)   
    for index in valid_list:
        os.replace(images_path+index, valid_image_path+index)
        label_file_name_wit_ext = index.rsplit( ".", 1 )[0]+".txt"
        os.replace(labels_path+label_file_name_wit_ext, valid_label_path+label_file_name_wit_ext)
        all_files.remove(index)

    test_list = random.sample(all_files, test_count)   
    for index in test_list:
        os.replace(images_path+index, test_image_path+index)
        label_file_name_wit_ext = index.rsplit( ".", 1 )[0]+".txt"
        os.replace(labels_path+label_file_name_wit_ext, test_label_path+label_file_name_wit_ext)
        all_files.remove(index)

   


    # while count > 0 and valid_count > 0 and test_count >0:
    #     index = random.randint(0, count-1) 
    #     if os.path.exists(images_path+all_files[index]):
    #         try:
    #             if valid_count > 0:
    #                 os.replace(images_path+all_files[index], valid_path+all_files[index])
    #                 os.replace(labels_path+all_label_files[index], valid_path+all_label_files[index])
    #                 valid_count = valid_count - 1
    #             elif test_count > 0:
    #                 os.replace(images_path+all_files[index], test_path+all_files[index])
    #                 os.replace(labels_path+all_label_files[index], test_path+all_label_files[index])
    #                 test_count = test_count - 1
    #             # elif train_count > 0:
    #             #     os.replace(images_path+all_files[index], "train/"+all_files[index])
    #             #     os.replace(labels_path+all_label_files[index], "train/"+all_label_files[index])
    #             #     train_count = train_count - 1
    #         except OSError:
    #             print ('Error: Unable to copy'+all_files[index])
    #     print("--done--")



                
def match_images_and_labels():
    images_path = os.path.join(opt.images,'')
    labels_path  = os.path.join(opt.labels,'')
    image_not_exist, label_not_exist = False,False
    for i in os.listdir(images_path):
        if not os.path.exists(labels_path+i):
            label_not_exist = True
            print("Label dont exist: ", i)
    print("--------------------------")
    for i in os.listdir(labels_path):
        if not os.path.exists(images_path+i):
            image_not_exist = True
            print("Image dont exist: ", i)
    
    if image_not_exist == True or label_not_exist == True:
        return False
    else:
        return True



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--images', type=str, default='images', help='image path')
    parser.add_argument('--labels', type=str, default='labels', help='image path')
    parser.add_argument('--train_path', type=str, default='train', help='train path')
    parser.add_argument('--test_path',  type=str, default='test', help='test path')
    parser.add_argument('--valid_path', type=str, default='valid', help='valid path')
    parser.add_argument('--model', type=str, default='yolo', help='Image Folder for specific model,')
    parser.add_argument('--check', action='store_true', help='save results to *.txt')
   # parser.add_argument('--test_percent', type=int, default="20", help='save results to *.txt')
   # parser.add_argument('--valid_percent', type=int,default="20" ,help='save results to *.txt')
    #parser.add_argument('--i', type=int, default=640, help='inference size (pixels)')
  
    opt = parser.parse_args()
    
    if opt.check is True:
        if match_images_and_labels() is True:
            split_data()
    else:
        split_data()

    
    