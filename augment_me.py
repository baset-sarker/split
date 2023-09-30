import cv2
import numpy as np
import random


def show_result(shifted_image, adjusted_annotations):
    # Display the annotated image with the adjusted annotations
    for annotation in adjusted_annotations:
        class_id, x_center, y_center, width, height = map(float, annotation.split())
        x1 = int((x_center - width / 2) * shifted_image.shape[1])
        y1 = int((y_center - height / 2) * shifted_image.shape[0])
        x2 = int((x_center + width / 2) * shifted_image.shape[1])
        y2 = int((y_center + height / 2) * shifted_image.shape[0])
        cv2.rectangle(shifted_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.imshow('Annotated Image', shifted_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def save_image_and_annotation(image_path,anootaion_path,shifted_image, adjusted_annotations):
    random_init = random.randint(0, 100000)
    image_path = image_path.replace('.png', f'_{random_init}.png')
    anootaion_path = anootaion_path.replace('.txt', f'_{random_init}.txt')

    # Save the modified image
    cv2.imwrite(image_path, shifted_image)
    # Save the adjusted YOLO annotations to a text file
    with open(anootaion_path, 'w') as modified_annotation_file:
        for adjusted_annotation in adjusted_annotations:
            modified_annotation_file.write(adjusted_annotation + '\n')
    print('image and annotation saved')


# Shift by 10% of the image height, adjust as needed
def vertical_shift(image_path, annotation_file_path, shift_amount_vertical = 0.1,is_show_result = False):
    # Load the image
    image = cv2.imread(image_path)

    # Load YOLO annotations from a text file
    # Assuming the annotation format is: class_id, x_center, y_center, width, height, one annotation per line
    with open(annotation_file_path, 'r') as annotation_file:
        annotations = [line.strip() for line in annotation_file.readlines()]

    # Calculate the shift in pixels
    shift_pixels_vertical = int(shift_amount_vertical * image.shape[0])

    # Apply the vertical shift to the entire image
    shifted_image = np.roll(image, shift_pixels_vertical, axis=0)

    # Adjust all YOLO annotations with the new image position
    adjusted_annotations = []
    for annotation in annotations:
        class_id, x_center, y_center, width, height = map(float, annotation.split())
        adjusted_y_center = (y_center + shift_amount_vertical) if (y_center + shift_amount_vertical) < 1.0 else (y_center + shift_amount_vertical - 1.0)
        adjusted_annotation = f'{int(class_id)} {x_center:.6f} {adjusted_y_center:.6f} {width:.6f} {height:.6f}'
        adjusted_annotations.append(adjusted_annotation)
    
    if is_show_result:
        show_result(shifted_image, adjusted_annotations)

    save_image_and_annotation(image_path,annotation_file_path,shifted_image, adjusted_annotations)
    
    return shifted_image, adjusted_annotations



def horizontal_shift(image_path, annotation_file_path, shift_amount_horizontal = 0.1,is_show_result = False):
    # Load the image
    image = cv2.imread(image_path)

    # Load YOLO annotations from a text file
    # Assuming the annotation format is: class_id, x_center, y_center, width, height, one annotation per line
    with open(annotation_file_path, 'r') as annotation_file:
        annotations = [line.strip() for line in annotation_file.readlines()]

    # Calculate the shift in pixels
    shift_pixels_horizontal = int(shift_amount_horizontal * image.shape[1])

    # Apply the horizontal shift to the entire image
    shifted_image = np.roll(image, shift_pixels_horizontal, axis=1)

    # Adjust all YOLO annotations with the new image position
    adjusted_annotations = []
    for annotation in annotations:
        class_id, x_center, y_center, width, height = map(float, annotation.split())
        adjusted_x_center = (x_center + shift_amount_horizontal) if (x_center + shift_amount_horizontal) < 1.0 else (x_center + shift_amount_horizontal - 1.0)
        adjusted_annotation = f'{int(class_id)} {adjusted_x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}'
        adjusted_annotations.append(adjusted_annotation)

    if is_show_result:
        show_result(shifted_image, adjusted_annotations)

    save_image_and_annotation(image_path,annotation_file_path,shifted_image, adjusted_annotations)
    
    return shifted_image, adjusted_annotations


# get parse arg from command line
import argparse
parser = argparse.ArgumentParser(description='Augment dataset')
parser.add_argument('--source', type=str, default='', help='Source directory')

args = parser.parse_args()
source = args.source


# get all image and annotation path
import glob
image_paths = glob.glob(source + '/*.png')
count = len(image_paths)

for image_path in image_paths:
    annotation_path = image_path.replace('.png','.txt')
    scale = 0.02
    for i in range(5):
        vertical_shift(image_path, annotation_path, shift_amount_vertical = scale,is_show_result = False)
        horizontal_shift(image_path, annotation_path, shift_amount_horizontal =scale,is_show_result = False)
        scale = scale+0.02
        print(scale,"count:",count)
    count = count-1


