import os

def rename_images(input_folder):
    """
    rename images in order
    """
    image_files = sorted([f for f in os.listdir(input_folder) if f.endswith(('jpg', 'png', 'jpeg'))])

    if len(image_files) == 0:
        print("no image in folder")
        return

    for i, image_file in enumerate(image_files):
        old_path = os.path.join(input_folder, image_file)
        new_filename = f"a_frame_{i:03d}.jpg"
        new_path = os.path.join(input_folder, new_filename)
        
        # if exist, skip
        if os.path.exists(new_path):
            print(f"file {new_filename} exist, skip rename")
            continue
        
        os.rename(old_path, new_path)
        print(f"rename: {image_file} -> {new_filename}")

# 用法
input_folder = 'path to image folder'
rename_images(input_folder)