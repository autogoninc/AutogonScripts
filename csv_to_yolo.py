import pandas as pd
from PIL import Image
import os
import shutil
import ast

# folder path 
folder_path = r"C:\Users\...."

# Check if the folder exists
if os.path.exists(folder_path) and os.path.isdir(folder_path):
    # Create the 'labels', and 'images' directories if they don't exist
    os.makedirs("labels", exist_ok=True)
    os.makedirs("images", exist_ok=True)
  

    # Iterate through files in the folder
    for filename in os.listdir(folder_path):
        # Check if the file has the specified extension
        if filename.endswith(".csv"):
            # Construct the full file path
            file_path = os.path.join(folder_path, filename)

            # Load the CSV data
            data = pd.read_csv(file_path, sep=',')

            # Get unique label names and create a list
            unique_labels = list(data["image_type"].unique())

            # Create a dictionary to map label names to their indices
            label_to_index =  {'active_tb': 0, 'latent_tb': 1}

            # Get image dimensions once outside the loop
            image_name = data.iloc[0]["fname"]  # Assuming at least one row is present
            image = Image.open(os.path.join(folder_path, "images", image_name))
            image_width, image_height = image.size

            # Iterate through each row in the CSV
            for index, row in data.iterrows():
                image_name = row["fname"]
                tb_type = row["tb_type"]
                label = ["active_tb", "latent_tb"]

                # Try to convert string representation of dictionary to an actual dictionary
                try:
                    bbox_dict = ast.literal_eval(row["bbox"]) if isinstance(row["bbox"], str) else row["bbox"]
                except (SyntaxError, ValueError) as e:
                    print(f"Error in row {index + 1} - {e}: {row['bbox']}")
                    continue

                # Access 'xmin' and 'ymin' only if bbox_dict is a dictionary
                if isinstance(bbox_dict, dict):
                    x = bbox_dict.get("xmin")
                    y = bbox_dict.get("ymin")
                    w = bbox_dict.get("width")
                    h = bbox_dict.get("height")

                    # Convert bounding box coordinates to YOLO format (normalized coordinates)
                    x_center = (x + w  / 2) / image_width
                    y_center = (y + h / 2) / image_height
                    width_normalized = w / image_width
                    height_normalized = h / image_height

                    # Create the label text in YOLO format using the label index
                    label_index = label.index(tb_type)
                    label_text = f"{label_index} {x_center} {y_center} {width_normalized} {height_normalized}\n"

                    # Write the label text to a file in the 'labels' directory
                    with open(
                        os.path.join("labels", os.path.splitext(image_name)[0] + ".txt"), "a"
                    ) as f:
                        f.write(label_text)

                    # Copy the image to the 'images' directory
                    source_image_path = os.path.join(folder_path, "images", image_name)
                    destination_image_path = os.path.join("images", image_name)
                    shutil.copyfile(source_image_path, destination_image_path)

            print("Label files and images copied successfully!")
            print("Unique label names:", unique_labels)

else:
    print(f"Error: Folder not found at {folder_path}")
