from PIL import Image
import os

# Define input and output directories
input_folder = r"C:\Users\..."
output_folder = r"C:\Users\..."

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Loop through files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".bmp"):
        # Create file paths
        input_bmp = os.path.join(input_folder, filename)
        output_jpg = os.path.join(output_folder, os.path.splitext(filename)[0] + ".jpg")
        
        # Open the BMP image and save as JPEG in the output folder
        with Image.open(input_bmp) as img:
            img.save(output_jpg, "JPEG")

        print(f"Converted {filename} to {os.path.basename(output_jpg)}")

print("Conversion completed.")
