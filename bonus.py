import random
from PIL import Image, ImageDraw, ImageFont
import os
import csv
import numpy as np

# Define font paths
font_paths = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/home/arnavsharma/Arnav/Fonts/Quikhand.ttf",
    "/home/arnavsharma/Arnav/Fonts/SamsungOne-400.ttf"
]

def random_capitalize(word):
    """Randomly capitalize letters in a word"""
    return ''.join(c.upper() if random.random() > 0.5 else c.lower() for c in word)

def add_salt_and_pepper(image, amount=0.5):
    output = np.array(image)
    height, width, channels = output.shape
    num_pixels = int(amount * width * height)
    
    for _ in range(num_pixels):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        
        noise_type = random.random()
        if noise_type < 0.3:  # Bright colors
            r, g, b = [random.randint(200, 255) for _ in range(3)]
        elif noise_type < 0.6:  # Dark colors
            r, g, b = [random.randint(0, 55) for _ in range(3)]
        else:  # Random colors
            r, g, b = [random.randint(0, 255) for _ in range(3)]
            
        output[y, x] = [r, g, b]
    
    return Image.fromarray(output.astype('uint8'))

def create_word_image(word, bg_color):
    # Set background color
    bg_rgb = (255,0,0) if bg_color == 'red' else (0,255,0)
    img = Image.new('RGB', (400, 100), color=bg_rgb)
    draw = ImageDraw.Draw(img)
    
    # Apply transformations
    display_word = word[::-1] if bg_color == 'red' else word  # Reverse if red
    display_word = random_capitalize(display_word)  # Random capitalization
    
    # Setup font
    font_path = random.choice(font_paths)
    font_size = random.randint(30, 40)
    font = ImageFont.truetype(font_path, font_size)
    
    # Center text
    bbox = font.getbbox(display_word)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (400 - text_width) // 2
    y = (100 - text_height) // 2
    
    # Draw text and add noise
    draw.text((x, y), display_word, font=font, fill='black')
    if random.random() > 0.5:
        img = add_salt_and_pepper(img, amount=random.uniform(0.2, 0.4))
    
    return img

# Setup directories
output_dir = "bonus_dataset"
image_dir = os.path.join(output_dir, 'images')
os.makedirs(image_dir, exist_ok=True)

# Read words
with open('english_words_479k.txt', 'r') as file:
    valid_words = [word.strip() for word in file if word.strip().isalpha()]

# Select random words
selected_words = random.sample(valid_words, 1000)

# Generate dataset
csv_path = os.path.join(output_dir, 'labels.csv')
with open(csv_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Word', 'Image_Path'])
    
    for i, word in enumerate(selected_words):
        bg_color = random.choice(['red', 'green'])
        img = create_word_image(word, bg_color)
        
        # Save image
        image_path = os.path.join('images', f'word_{i:04d}.png')
        img.save(os.path.join(output_dir, image_path))
        
        # Save original word in CSV (not reversed)
        writer.writerow([word.capitalize(), image_path])

print(f"Created {len(selected_words)} word-image pairs in {output_dir}/")