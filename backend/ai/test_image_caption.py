# test_image_caption.py

from image_caption import generate_image_caption
import os

if __name__ == "__main__":
    image_path = os.path.abspath("../data/images/1200px-Normal_posteroanterior_(PA)_chest_radiograph_(X-ray).jpg")
    caption = generate_image_caption(image_path)
    print("\n📝 Caption:", caption)
