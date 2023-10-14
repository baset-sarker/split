import argparse
import os
import random
import cv2
import numpy as np


def random_flip(cropped_object):
    # Randomly determine whether to flip horizontally (left to right)
    flip_horizontal = random.choice([True, False])

    # Randomly determine whether to flip vertically (up to down)
    flip_vertical = random.choice([True, False])

    # choose flip_horizontal or flip_vertical randomly


    # Create a copy of the cropped object for adjustments
    flipped_object = cropped_object.copy()

    # Apply horizontal flip if chosen
    if flip_horizontal:
        flipped_object = cv2.flip(flipped_object, 1)

    # Apply vertical flip if chosen
    if flip_vertical:
        flipped_object = cv2.flip(flipped_object, 0)
    
    return flipped_object

def brightness_contrast(cropped_object):
    # Define the range for random brightness and contrast adjustments
    #brightness_range = (-50, 50)  # Range of brightness adjustment in pixels
    #contrast_range = (0.5, 1.5)   # Range of contrast adjustment (0.5 = reduced contrast, 1.5 = increased contrast)

    brightness_range = (-1, 20)  # Range of brightness adjustment in pixels
    contrast_range = (0.9, 1.5)   # Range of contrast adjustment (0.5 = reduced contrast, 1.5 = increased contrast)

    # Generate random values for brightness and contrast
    brightness = random.randint(brightness_range[0], brightness_range[1])
    contrast = random.uniform(contrast_range[0], contrast_range[1])

    # Create a copy of the cropped object for adjustments
    adjusted_object = cropped_object.copy()

    # Apply brightness and contrast adjustments
    adjusted_object = cv2.convertScaleAbs(adjusted_object, alpha=contrast, beta=brightness)
    return adjusted_object



def zoom_image(cropped_object):

    #zoom_factor = random.uniform(0.8, 1.2)
    zoom_factor = random.uniform(0.9, 1.3)

    # Get the dimensions of the cropped object
    cropped_height, cropped_width, _ = cropped_object.shape

    # Calculate the new dimensions for the zoomed object
    new_height = int(cropped_height * zoom_factor)
    new_width = int(cropped_width * zoom_factor)

    # Ensure that the new dimensions are greater than zero
    if new_height <= 0 or new_width <= 0:
        # Handle the case where the zoom factor is too extreme
        new_height = 1  # Set a minimum height
        new_width = 1   # Set a minimum width

    # Resize the cropped object to the new dimensions
    zoomed_object = cv2.resize(cropped_object, (new_width, new_height))

    # Crop to match the original size if necessary
    if new_height > cropped_height:
        y_offset = random.randint(0, new_height - cropped_height)
        x_offset = random.randint(0, new_width - cropped_width)
        zoomed_object = zoomed_object[y_offset:y_offset + cropped_height, x_offset:x_offset + cropped_width]    
    
    return zoomed_object



def process_crop(source , destination,image_name,func='zoom'):
    print("Working on",image_name)

    annotation_name = image_name.split('.')[0]+'.txt' 
    # join the path 
    image_path = os.path.join(source,image_name)
    annotation_file = os.path.join(source,annotation_name)

    
    # Load the original image
    original_image = cv2.imread(image_path)
    # Get the height and width of the original image
    height, width, _ = original_image.shape

    lines = []
    # Parse the YOLO annotation file to get the bounding box coordinates
    with open(annotation_file, 'r') as annotation_file:
        lines = annotation_file.readlines()


    for line in lines:
        class_id, x_center, y_center, bbox_width, bbox_height = map(float, line.strip().split())
        
        # Convert YOLO coordinates to absolute coordinates
        x_center *= width
        y_center *= height
        bbox_width *= width
        bbox_height *= height
        
        # Calculate bounding box coordinates
        x1 = int(x_center - (bbox_width / 2))
        y1 = int(y_center - (bbox_height / 2))
        x2 = int(x_center + (bbox_width / 2))
        y2 = int(y_center + (bbox_height / 2))


        # Crop the object from the original image
        #cropped_object = original_image[y1:y2, x1:x2]
        cropped_object1 = original_image[y1-5:y2+5, x1-5:x2+5]

        # Load the destination image
        destination_image = original_image.copy()


        # Define the number of times to paste the cropped object
        num_pastes = 250  # You can change this to the desired number

        # Create a list to store YOLO annotation for each pasted object
        annotations = []

        # Create a list to store non-overlapping positions
        non_overlapping_positions = []

        # Iterate through positions and paste the cropped object
        for i in range(num_pastes):
            while True:

                try:

                    func = random.choice(['zoom','flip','brightness'])
                    if func == 'zoom':
                        cropped_object = zoom_image(cropped_object1)
                    elif func == 'flip':
                        cropped_object = random_flip(cropped_object1)
                    elif func == 'brightness':
                        cropped_object = brightness_contrast(cropped_object1)
                    else:
                        print('Invalid function')
                        break

      
                    # Randomize the destination positions
                    destination_x = random.randint(10, destination_image.shape[1] - cropped_object.shape[1] - 50)
                    destination_y = random.randint(10, destination_image.shape[0] - cropped_object.shape[0] - 50)


                    # Ensure that the cropped object fits within the available space
                    if (destination_x + cropped_object.shape[1] <= destination_image.shape[1] and
                        destination_y + cropped_object.shape[0] <= destination_image.shape[0]):
                        pass
                    else:
                        break
                    
                    # Check if the destination position overlaps with existing positions
                    overlapping = False
                    for pos in non_overlapping_positions:
                        x1, y1, x2, y2 = pos
                        if (
                            destination_x < x2 and
                            destination_x + cropped_object.shape[1] > x1 and
                            destination_y < y2 and
                            destination_y + cropped_object.shape[0] > y1
                        ):
                            overlapping = True
                            break
                    
                    if not overlapping:
                        # Paste the rotated object into the destination image
                        destination_image[destination_y:destination_y + cropped_object.shape[0],
                                        destination_x:destination_x + cropped_object.shape[1]] = cropped_object

                        # Update YOLO annotation coordinates for the current object
                        new_x_center = (destination_x + destination_x + cropped_object.shape[1]) / (2 * destination_image.shape[1])
                        new_y_center = (destination_y + destination_y + cropped_object.shape[0]) / (2 * destination_image.shape[0])
                        # subtract 10 because we added 10 pixels to the cropped object
                        new_width = ((destination_x + cropped_object.shape[1] - destination_x)-10) / destination_image.shape[1]
                        new_height = ((destination_y + cropped_object.shape[0] - destination_y)-10) / destination_image.shape[0]

                        annotations.append(f"{class_id} {new_x_center} {new_y_center} {new_width} {new_height}")

                        # Add the current position to the non-overlapping positions list
                        non_overlapping_positions.append((destination_x, destination_y, destination_x + cropped_object.shape[1], destination_y + cropped_object.shape[0]))

                        break
                except Exception as e:
                    print(e)


        # modify the image name and annotation name add random number at the end
        random_number = random.randint(0,1000000)
        annotation_name = image_name.split('.')[0] + '_'+str(random_number)+'.txt'
        image_name = image_name.split('.')[0] + '_'+str(random_number)+'.png'
        
        dest_image_path = os.path.join(destination,image_name)
        dest_annoation_file = os.path.join(destination,annotation_name)

        # Save the modified image
        cv2.imwrite(dest_image_path, destination_image)

        # append original annotation
        for line in lines:
            annotations.append(line.strip())

        # Save the YOLO annotations for the modified objects
        with open(dest_annoation_file, 'w') as modified_annotation_file:
            for annotation in annotations:
                modified_annotation_file.write(annotation + '\n')   

    # end of lines in annotation file    




if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser(description='Crop and rotate an object from an image')
    #directory = '/home/rohit/Downloads/13_09_23_18_49_00_283341_15cms_4mm_fixed_320_688'
    parser.add_argument('source', type=str, help='Directory containing the images and annotations')
    parser.add_argument('destination', type=str, help='Directory to save the modified images and annotations')

    args = parser.parse_args()
    source = args.source
    destination = args.destination

    for image_name in os.listdir(source):
        if image_name.endswith('.png'):
            process_crop(source,destination,image_name,func='zoom')
            process_crop(source,destination,image_name,func='flip')
            process_crop(source,destination,image_name,func='brightness')
            print('Done for image {}'.format(image_name))
    
