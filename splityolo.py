#!/usr/bin/env python
import os
import shutil
import random
import argparse

# Function to copy files and organize them into subdirectories.
def copy_and_organize_files(file_pairs, destination_directory,noremove):
    # Define subdirectories for images and labels.
    image_subdir = "images"
    label_subdir = "labels"
    image_dir = os.path.join(destination_directory, image_subdir)
    label_dir = os.path.join(destination_directory, label_subdir)

    if noremove:
        os.makedirs(image_dir, exist_ok=True)
        os.makedirs(label_dir, exist_ok=True)

    for image, text in file_pairs:
        shutil.copy(os.path.join(source_directory, image), os.path.join(image_dir, image))
        shutil.copy(os.path.join(source_directory, text), os.path.join(label_dir, text))


def create_directories(output_directory,no_remove):
     # Create output directories for train, test, and valid sets.
    train_directory = os.path.join(output_directory, "train")
    test_directory = os.path.join(output_directory, "test")
    valid_directory = os.path.join(output_directory, "valid")

    if no_remove:
        # Remove the train, test, and valid directories if they exist.
        if os.path.exists(train_directory):
            shutil.rmtree(train_directory)
        if os.path.exists(test_directory):
            shutil.rmtree(test_directory)
        if os.path.exists(valid_directory):
            shutil.rmtree(valid_directory)

    # Create the train, test, and valid directories again.
    os.makedirs(train_directory, exist_ok=True)
    os.makedirs(test_directory, exist_ok=True)
    os.makedirs(valid_directory, exist_ok=True)

    return train_directory, test_directory, valid_directory


def find_paired_and_unpaired_files():
    # Dictionary to store pairs of files.
    file_pairs = []
    # List to store unpaired files.
    unpaired_files = []
    # List all files in the source directory.
    files = os.listdir(source_directory)

    # Iterate through the files and group .txt and .png files by name.
    for file in files:
        #file_path = os.path.join(source_directory, file)
        if file.endswith(".png") or file.endswith(".jpg"):
            
            txt_file = file.replace(".png", ".txt") if file.endswith(".png") else file.replace(".jpg", ".txt")

            if txt_file in files:
                #txt_path = os.path.join(source_directory, txt_file)
                file_pairs.append((file, txt_file))
            else:
                unpaired_files.append(file)
        elif file.endswith(".txt"):
            png_file = file.replace(".txt", ".png")
            if png_file not in files:
                unpaired_files.append(file)

    return file_pairs, unpaired_files

if __name__ == '__main__':
    # Create an ArgumentParser object.
    parser = argparse.ArgumentParser(description="Organize and split files into train, test, and valid directories.")
    parser.add_argument("--source",required=True, help="Path to the source directory containing .txt and .png files")
    parser.add_argument("--dest", type=str, default=".", help="destination folder path")
    parser.add_argument("--check", action="store_true", help="Check for unpaired .png or .txt files without pairs")
    parser.add_argument("--ratio",nargs='+',type=int,default=[80,10,10], help="Train test valid ratio")
    parser.add_argument("--noremove", action="store_true", help="Do not remove existing train, test, and valid directories")

    # Parse the command-line arguments.
    args = parser.parse_args()
    # Get the source directory from the parsed arguments.
    source_directory = args.source
    output_directory = args.dest
    noremove = args.noremove
    train_ratio, test_ratio, valid_ratio = args.ratio[0]/100, args.ratio[1]/100, args.ratio[2]/100
    
    if train_ratio + test_ratio + valid_ratio != 1:
        print("train, test, valid ratios must sum to 100")
        exit()


    file_pairs, unpaired_files = find_paired_and_unpaired_files()
    

    # If --check flag is provided, print unpaired files and exit.
    if args.check:
        if unpaired_files:
            print("unpaired .png and .txt files without pairs:")
            for unpaired_file in unpaired_files:
                print(unpaired_file)
        else:
            print("No unpaired files found.")
        exit()


    train_directory, test_directory, valid_directory = create_directories(output_directory,noremove)

    # Shuffle the file pairs if you want to randomize the split.
    random.shuffle(file_pairs)



    # Calculate split indices.
    total_files = len(file_pairs)
    train_split = int(total_files * train_ratio)
    test_split = int(total_files * (train_ratio + test_ratio))


    # Copy files to their respective directories and organize them.
    copy_and_organize_files(file_pairs[:train_split], train_directory,noremove)
    copy_and_organize_files(file_pairs[train_split:test_split], test_directory,noremove)
    copy_and_organize_files(file_pairs[test_split:], valid_directory,noremove)

    print("Train count:",len(file_pairs[:train_split]))
    print("Test count:",len(file_pairs[train_split:test_split]))
    print("Valid count:",len(file_pairs[test_split:]))
    print("Data split and files copied successfully.")
