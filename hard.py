import random
from PIL import Image, ImageDraw, ImageFont
import os
import csv
import numpy as np

# Define multiple font paths
font_paths = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/home/arnavsharma/Arnav/Fonts/Quikhand.ttf",
    "/home/arnavsharma/Arnav/Fonts/SamsungOne-400.ttf"
]

def random_capitalize(word):
    return ''.join(c.upper() if random.random() > 0.5 else c.lower() for c in word)

def add_salt_and_pepper(image, amount=0.5):  # Increased to 50%
    output = np.array(image)
    height, width, channels = output.shape
    
    # Increased pixels to modify (50% of image)
    num_pixels = int(amount * width * height)
    
    # Add colored noise
    for _ in range(num_pixels):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        
        # More varied RGB values
        noise_type = random.random()
        if noise_type < 0.3:  # Bright colors
            r = random.randint(200, 255)
            g = random.randint(200, 255)
            b = random.randint(200, 255)
        elif noise_type < 0.6:  # Dark colors
            r = random.randint(0, 55)
            g = random.randint(0, 55)
            b = random.randint(0, 55)
        else:  # Random colored noise
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            
        output[y, x] = [r, g, b]
    
    return Image.fromarray(output.astype('uint8'))

output_dir = "hard_dataset"
image_dir = os.path.join(output_dir, 'images')
os.makedirs(image_dir, exist_ok=True)

with open('english_words_479k.txt', 'r') as file:
    valid_words = [word.strip() for word in file if word.strip().isalpha()]

selected_words = random.sample(valid_words, 1000)

csv_path = os.path.join(output_dir, 'labels.csv')
with open(csv_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Word', 'Image_Path'])
    
    for i, word in enumerate(selected_words):
        img = Image.new('RGB', (380, 60), color='white')
        draw = ImageDraw.Draw(img)
        
        font_path = random.choice(font_paths)
        font_size = random.randint(25, 35)
        font = ImageFont.truetype(font_path, font_size)
        
        display_word = random_capitalize(word)
        
        bbox = font.getbbox(display_word)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (300 - text_width) // 2
        y = (60 - text_height) // 2
        
        # Draw text
        draw.text((x,y), display_word, font=font, fill='black')
        
        # Add noise
        if random.random() > 0.5:
            img = add_salt_and_pepper(img, amount=random.uniform(0.01, 0.03))
        
        # Save image
        image_path = os.path.join('images', f'word_{i:04d}.png')
        img.save(os.path.join(output_dir, image_path))
        
        # Save original word in CSV
        writer.writerow([word.capitalize(), image_path])

print(f"Created {len(selected_words)} word-image pairs in {output_dir}/")