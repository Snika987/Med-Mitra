import os
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

# Load model + processor only once at module level
print("📡 Loading BLIP model and processor...")
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)
print(f"🚀 BLIP model loaded on {device}")

def generate_image_caption(image_path: str) -> str:
    """
    Generate a caption for the given image file using the BLIP model.
    Returns a string caption or error message.
    """
    try:
        if not os.path.exists(image_path):
            return f"❌ Error: File not found: {image_path}"

        raw_image = Image.open(image_path).convert("RGB")
        inputs = processor(images=raw_image, return_tensors="pt").to(device)

        outputs = model.generate(**inputs)
        caption = processor.decode(outputs[0], skip_special_tokens=True)
        return caption

    except Exception as e:
        import traceback
        print("❌ Traceback:\n", traceback.format_exc())
        return f"❌ Error: {str(e)}"
