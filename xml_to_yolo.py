import os
import xml.etree.ElementTree as ET


def convert_to_yolo(image_width, image_height, box):
    label, xmin, ymin, xmax, ymax = box

    # Calculate YOLO normalized coordinates
    x_center = (xmin + xmax) / (2.0 * image_width)
    y_center = (ymin + ymax) / (2.0 * image_height)
    width_normalized = (xmax - xmin) / image_width
    height_normalized = (ymax - ymin) / image_height

    return f"{label} {x_center} {y_center} {width_normalized} {height_normalized}"

def process_image(image_element, labels_folder):
    try:
        # Extract relevant information from the image tag
        image_name = image_element.get("name")
        image_width = int(image_element.get("width"))
        image_height = int(image_element.get("height"))

        # Extract bounding box information
        boxes = []
        for box in image_element.findall(".//box"):
            label = 0
            xmin = float(box.get("xtl"))
            ymin = float(box.get("ytl"))
            xmax = float(box.get("xbr"))
            ymax = float(box.get("ybr"))

            # Append the bounding box information to the list
            boxes.append((label, xmin, ymin, xmax, ymax))

        # Check if there are bounding boxes for the image
        if boxes:
            # Create a .txt file for the image in the 'labels' folder
            output_file_path = os.path.join(labels_folder, os.path.splitext(os.path.basename(image_name))[0] + ".txt")
            with open(output_file_path, "w") as f:
                for box in boxes:
                    yolo_annotation = convert_to_yolo(image_width, image_height, box)
                    f.write(yolo_annotation + "\n")

            print(f"Created {output_file_path}")

    except Exception as e:
        print(f"Error processing image {image_name}: {e}")


def convert_xml_to_yolo(xml_file, labels_folder):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Process each image tag separately
        for image_element in root.findall(".//image"):
            process_image(image_element, labels_folder)

    except Exception as e:
        print(f"Error processing XML file {xml_file}: {e}")

def convert_xmls_to_yolo(xml_folder, labels_folder):
    os.makedirs(labels_folder, exist_ok=True)
    
    for xml_file in os.listdir(xml_folder):
        if xml_file.endswith(".xml"):
            xml_path = os.path.join(xml_folder, xml_file)
            convert_xml_to_yolo(xml_path, labels_folder)

# Example usage
# folder path to the xml file
xml_folder_path = r"C:\Users\...."
# folder path to where to put the .txt file.
label_folder_path = r"C:\Users\...\labels"
convert_xmls_to_yolo(xml_folder_path, label_folder_path)
