import os
import numpy as np
from PIL import Image

def are_images_similar(img1, img2, threshold=5):
    """
    Compare two images if they are the same, give a threshold value to allow small difference due to image compression
    """
    img1 = img1.convert('RGB')
    img2 = img2.convert('RGB')

    array1 = np.array(img1, dtype=np.int32)
    array2 = np.array(img2, dtype=np.int32)
    
    # calculate the difference
    diff = np.abs(array1 - array2)
    
    # sum of the difference
    num_different_pixels = np.sum(np.any(diff > threshold, axis=2))
    return num_different_pixels == 0  # if the difference is smaller than threshold, take two images as same

def remove_repeated_images(input_folder, threshold=5):
    """
    remove repeated images, allow small difference, only save one
    """
    image_files = sorted([f for f in os.listdir(input_folder) if f.endswith(('jpg', 'png', 'jpeg'))])

    if len(image_files) == 0:
        print("on image in folder")
        return

    prev_image = Image.open(os.path.join(input_folder, image_files[0]))
    prev_image = prev_image.convert('RGB') 
    print(f"save: {image_files[0]}")

    for image_file in image_files[1:]:
        current_image_path = os.path.join(input_folder, image_file)
        current_image = Image.open(current_image_path)
        current_image = current_image.convert('RGB') 

        # if same, remove it
        if are_images_similar(prev_image, current_image, threshold=threshold):
            os.remove(current_image_path)
        else:
            prev_image = current_image

input_folder = 'path to images folder'
remove_repeated_images(input_folder, threshold=20)
