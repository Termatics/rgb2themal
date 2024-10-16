from PIL import Image
import os

input_dir = '/Users/zhengtonglin/Termatics/Karlsruhe Dataset/A/val'

target_size = (640, 512)

for filename in os.listdir(input_dir):
    if filename.endswith('.jpg'):
        try:
            img = Image.open(os.path.join(input_dir, filename))

            img_resized = img.resize(target_size, Image.BILINEAR)

            img_resized.save(os.path.join(input_dir, filename))
        except Exception as e:
            print(f"can't resize {filename}, error: {e}")

