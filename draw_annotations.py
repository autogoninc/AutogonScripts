#!pip install Pillow requests
 
import requests
from PIL import Image, ImageDraw
from io import BytesIO

def draw_annotations(image_url, annotations):
    # Download the image from the URL
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))

    # Create a drawing object
    draw = ImageDraw.Draw(img)

    # Define a list of distinct colors for annotations
    colors = ["red", "blue", "green" "orange", "purple", "pink", "yellow"]

    # Loop through each annotation
    for annotation in annotations:
        # Extract annotation parameters
        x, y, w, h = annotation['bbx']['x'], annotation['bbx']['y'], annotation['bbx']['w'], annotation['bbx']['h']
        label_name = annotation['lbl']
        label_id = annotation['lbl_id']
        confidence = annotation['conf']

        # Use a distinct color for each annotation
        color = colors[int(label_id) % len(colors)]
        
        # Draw the bounding box with colored background
        draw.rectangle([x, y, x + w, y + h], outline=color, width=2)

        # Get the size of the text
        text = f"{label_name} ({confidence:.2f})"
        text_width, text_height = draw.textsize(text)

        # Draw a black rectangle as background for the text
        draw.rectangle([x, y - text_height, x + text_width, y], fill=color)

        # Annotate with label name and confidence (white text)
        draw.text((x, y - text_height), text, fill="white")

    # Display the image (optional)
    img.show()

    # Save the modified image
    img.save('draw_annotations_ouput.jpeg')
    
    return img

if __name__ == '__main__':
	# Example usage
	image_url = "https://storage.autogon.ai/ef577ec5-f44a-4c2b-b880-294181b1fdb1.jpg"
	
	annotations = [
            {
                "lbl_id": 0.0,
                "lbl": "lift",
                "bbx": {
                    "x": 226.5530242919922,
                    "y": 274.2731628417969,
                    "w": 89.49031066894531,
                    "h": 193.92218017578125
                },
                "conf": 0.46340733766555786
            },
            {
                "lbl_id": 1.0,
                "lbl": "dock",
                "bbx": {
                    "x": 426.13006591796875,
                    "y": 274.5406188964844,
                    "w": 101.56939697265625,
                    "h": 190.98287963867188
                },
                "conf": 0.3851676881313324
            },
            {
                "lbl_id": 1.0,
                "lbl": "dock",
                "bbx": {
                    "x": 234.36944580078125,
                    "y": 275.2978210449219,
                    "w": 113.89996337890625,
                    "h": 180.27481079101562
                },
                "conf": 0.3135426640510559
            },
            {
                "lbl_id": 0.0,
                "lbl": "lift",
                "bbx": {
                    "x": 297.27581787109375,
                    "y": 326.2178955078125,
                    "w": 49.801361083984375,
                    "h": 117.59588623046875
                },
                "conf": 0.30581697821617126
            }
        ]
	
	draw_annotations(image_url, annotations)

