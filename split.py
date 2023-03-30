# Importing all necessary libraries
from logging.config import valid_ident
import os
import sys
import random
import argparse
import shutil

# compare two array and take the common element
def compare_array(arr1,arr2):
    arr3 = [value for value in arr1 if value in arr2]
    return arr3

def create_directories_if_not_exist(train_path,test_path,valid_path):
    if not os.path.exists(train_path):
        os.mkdir(train_path)
    if not os.path.exists(test_path):
        os.mkdir(test_path)
    if not os.path.exists(valid_path):
        os.mkdir(valid_path)

    if not os.path.exists(train_path+"images/"):
        os.mkdir(train_path+"images/")
    if not os.path.exists(train_path+"labels/"):
        os.mkdir(train_path+"labels/")

    if not os.path.exists(test_path+"images/"):
        os.mkdir(test_path+"images/")
    if not os.path.exists(test_path+"labels/"):
        os.mkdir(test_path+"labels/")

    if not os.path.exists(valid_path+"images/"):
        os.mkdir(valid_path+"images/")
    if not os.path.exists(valid_path+"labels/"):
        os.mkdir(valid_path+"labels/")

# split the data into train and test and validation
def split_data():

    train_percent  = 80
    test_percent   = 10
    valid_percent  = 10

    images_path = os.path.join(opt.images,'')
    labels_path  = os.path.join(opt.labels,'')

    train_path  = os.path.join(opt.train_path,'')
    test_path   = os.path.join(opt.test_path,'')
    valid_path  = os.path.join(opt.valid_path,'')


    test_image_path = test_path+"images/"
    test_label_path = test_path+"labels/"
    valid_image_path = valid_path+"images/"
    valid_label_path = valid_path+"labels/"
    train_image_path = train_path+"images/"
    train_label_path = train_path+"labels/"

    

    if not os.path.exists(images_path):
        print("Path do not exist: ",images_path)
        exit() 
    if not os.path.exists(labels_path):
        print("Path do not exist: ",labels_path)
        exit()  
    

    image_path_list = os.listdir(images_path)
    label_path_list = os.listdir(labels_path)
    image_path_list_without_ext = [s.strip('.jpg') for s in image_path_list]
    label_path_list_without_ext = [s.strip('.txt') for s in label_path_list] 

    all_files = compare_array(image_path_list_without_ext,label_path_list_without_ext)
    count = len(all_files)
    train_count = int(train_percent*count/100)
    test_count  = int(test_percent*count/100)
    valid_count = int(valid_percent*count/100)
    print("Count: ",count,"Train: ",train_count,"Test: ",test_count,"valid: ",valid_count)  


    create_directories_if_not_exist(train_path,test_path,valid_path)

    valid_list = random.sample(all_files, valid_count)
    print("valid_count",len(valid_list)) 
    for im in valid_list:
        label_file_name_wit_ext = im+".txt"
        image_file_name_wit_ext = im+".jpg"
        shutil.copyfile(images_path+image_file_name_wit_ext, valid_image_path+image_file_name_wit_ext)
        shutil.copyfile(labels_path+label_file_name_wit_ext, valid_label_path+label_file_name_wit_ext)
        all_files.remove(im)


    test_list = random.sample(all_files, test_count)  
    print("valid_count",len(valid_list))  
    for im in test_list:
        image_file_name_wit_ext = im+".jpg"
        label_file_name_wit_ext = im+".txt"
        shutil.copyfile(images_path+image_file_name_wit_ext, test_image_path+image_file_name_wit_ext)
        shutil.copyfile(labels_path+label_file_name_wit_ext, test_label_path+label_file_name_wit_ext)
        all_files.remove(im)

    print("train_file_count: ",len(all_files))
    for im in all_files:
        image_file_name_wit_ext = im+".jpg"
        label_file_name_wit_ext = im+".txt"
        shutil.copyfile(images_path+image_file_name_wit_ext, train_image_path+image_file_name_wit_ext)
        shutil.copyfile(labels_path+label_file_name_wit_ext, train_label_path+label_file_name_wit_ext)
        #all_files.remove(im)


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

    
    
