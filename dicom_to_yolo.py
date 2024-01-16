import pandas as pd
import numpy as np
from PIL import Image
import pydicom
import os

folder_path = r"D:\train_images"

# Check if the folder exists
if os.path.exists(folder_path) and os.path.isdir(folder_path):
    # Create the 'labels' and 'images' directories if they don't exist
    os.makedirs("labels", exist_ok=True)
    os.makedirs("images", exist_ok=True)

    # Read the CSV file
    df = pd.read_csv(os.path.join(folder_path, "train_bounding_boxes.csv"))

    # Iterate over the rows of the CSV file
    for index, row in df.iterrows():
        # Get the StudyInstanceUID and the slice_number
        study_instance_uid = row["StudyInstanceUID"]
        slice_number = row["slice_number"]

        # Get the bounding box coordinates
        x = row["x"]
        y = row["y"]
        width = row["width"]
        height = row["height"]

        class_index = 0  # Only one class, Fractured

        # Open the corresponding study_instance_uid folder and get the image corresponding to the slice_number.dcm
        image_path = os.path.join(folder_path, study_instance_uid, f"{slice_number}.dcm")
        
        # Read the DICOM image
        dicom = pydicom.dcmread(image_path)

        new_image = dicom.pixel_array.astype(float)

        scaled_image = (np.maximum(new_image, 0) / new_image.max()) * 255.0

        scaled_image = np.uint8(scaled_image)

        final_image = Image.fromarray(scaled_image)

        # Save the image in the 'images' folder as jpg
        final_image.save(os.path.join("images", f"{study_instance_uid}_{slice_number}.jpg"))

        # Get the image dimensions
        image_width, image_height = final_image.size

        # Convert bounding box coordinates to YOLO format (normalized coordinates)
        x_center = (x + width / 2) / image_width
        y_center = (y + height / 2) / image_height
        width_normalized = width / image_width
        height_normalized = height / image_height

        # Create the label text in YOLO format
        label_text = f"{class_index} {x_center} {y_center} {width_normalized} {height_normalized}\n"

        # Save the label file in the 'labels' folder
        with open(os.path.join("labels", f"{study_instance_uid}_{slice_number}.txt"), "a") as f:
            f.write(label_text)

print("Label files and images copied successfully!")
