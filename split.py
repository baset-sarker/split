import os
import shutil
import random
import argparse

# Function to copy files and organize them into subdirectories.
def copy_and_organize_files(file_pairs, destination_directory):
    image_dir = os.path.join(destination_directory, image_subdir)
    label_dir = os.path.join(destination_directory, label_subdir)

    os.makedirs(image_dir, exist_ok=True)
    os.makedirs(label_dir, exist_ok=True)

    for image, text in file_pairs:
        shutil.copy(os.path.join(source_directory, image), os.path.join(image_dir, image))
        shutil.copy(os.path.join(source_directory, text), os.path.join(label_dir, text))

if __name__ == '__main__':
    # Create an ArgumentParser object.
    parser = argparse.ArgumentParser(description="Organize and split files into train, test, and valid directories.")
    parser.add_argument("--source", help="Path to the source directory containing .txt and .png files")
    parser.add_argument("--dest", type=str, default=".", help="destination folder path")
    parser.add_argument("--check", action="store_true", help="Check for unpaired .png or .txt files without pairs")

    # Parse the command-line arguments.
    args = parser.parse_args()

    # Get the source directory from the parsed arguments.
    source_directory = args.source
    output_directory = args.dest


    # Define subdirectories for images and labels.
    image_subdir = "images"
    label_subdir = "labels"


    # List all files in the source directory.
    files = os.listdir(source_directory)

    # Dictionary to store pairs of files.
    file_pairs = []

    # List to store unpaired files.
    unpaired_files = []

    # Iterate through the files and group .txt and .png files by name.
    for file in files:
        file_path = os.path.join(source_directory, file)
        if file.endswith(".png"):
            txt_file = file.replace(".png", ".txt")
            if txt_file in files:
                #txt_path = os.path.join(source_directory, txt_file)
                file_pairs.append((file, txt_file))
            else:
                unpaired_files.append(file)
        elif file.endswith(".txt"):
            png_file = file.replace(".txt", ".png")
            if png_file not in files:
                unpaired_files.append(file)

    # If --check flag is provided, print unpaired files and exit.
    if args.check:
        if unpaired_files:
            print("unpaired .png and .txt files without pairs:")
            for unpaired_file in unpaired_files:
                print(unpaired_file)
        else:
            print("No unpaired files found.")
        exit()


     # Create output directories for train, test, and valid sets.
    output_directory = output_directory
    train_directory = os.path.join(output_directory, "train")
    test_directory = os.path.join(output_directory, "test")
    valid_directory = os.path.join(output_directory, "valid")

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

    # Shuffle the file pairs if you want to randomize the split.
    random.shuffle(file_pairs)

    # Define the split ratios (adjust as needed).
    train_ratio = 0.8
    test_ratio = 0.1
    valid_ratio = 0.1

    # Calculate split indices.
    total_files = len(file_pairs)
    train_split = int(total_files * train_ratio)
    test_split = int(total_files * (train_ratio + test_ratio))

    # Copy files to their respective directories and organize them.
    copy_and_organize_files(file_pairs[:train_split], train_directory)
    copy_and_organize_files(file_pairs[train_split:test_split], test_directory)
    copy_and_organize_files(file_pairs[test_split:], valid_directory)

    print("Data split and files copied successfully.")
