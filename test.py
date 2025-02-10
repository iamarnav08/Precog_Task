import random
from PIL import Image, ImageDraw, ImageFont
import os
import csv

output_dir = "test_dataset"
image_dir = os.path.join(output_dir, 'images')
os.makedirs(image_dir, exist_ok=True)

# Use os.path.join to navigate to the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
file_path = os.path.join(parent_dir, 'english_words_479k.txt')

with open(file_path, 'r') as file:
    valid_words = [word.strip() for word in file if word.strip().isalpha()]

selected_words = random.sample(valid_words, 1000)
word_pairs = [(word, word.capitalize()) for word in selected_words]

font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
font = ImageFont.truetype(font_path, 20)

csv_path = os.path.join(output_dir, 'labels.csv')
with open(csv_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Word', 'Image_Path'])
    
    for i, word in enumerate(selected_words):
        img = Image.new('RGB', (200, 200), color='white')
        draw = ImageDraw.Draw(img)

        # Center text
        bbox = font.getbbox(word)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (300 - text_width) // 2
        y = (60 - text_height) // 2
        
        draw.text((x,y), word.capitalize(), font=font, fill='black')
        
        image_path = os.path.join('images', f'word_{i:04d}.png')
        img.save(os.path.join(output_dir, image_path))
        
        writer.writerow([word.capitalize(), image_path])

print(f"Created {len(selected_words)} word-image pairs in {output_dir}/")