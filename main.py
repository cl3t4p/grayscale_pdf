from pdf2image import convert_from_path
import os
import sys
import cv2
import numpy as np

if len(sys.argv) != 2:
    print("Usage: python main.py <path to pdf>")
    sys.exit(1)

images = convert_from_path(sys.argv[1],thread_count=4,dpi=500)

lenght_images = len(images)

for i, image in enumerate(images):
    image.save(f'temp/page_{i}.png', 'PNG')

#free up spce removing images
del images

for i in range(lenght_images):
    print(f"Processing page {i}")
    image = cv2.imread(f'temp/page_{i}.png')
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Threshold the image to create a binary image (black text on white background)
    _, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
    
    # Invert the binary image (white text on black background)
    binary_inv = cv2.bitwise_not(binary)
    
    # Remove the horizontal lines from the binary image
    
    # Save the processed image
    cv2.imwrite(f'temp/processed_page_{i}.png', binary_inv)
    # remove old image
    os.remove(f'temp/page_{i}.png')
    
from PIL import Image

# List of processed image file paths
processed_images = [f'temp/processed_page_{i}.png' for i in range(lenght_images)]

# Open images and convert to PDF
image_list = [Image.open(img).convert('RGB') for img in processed_images]
image_list[0].save('output.pdf', save_all=True, append_images=image_list[1:])
