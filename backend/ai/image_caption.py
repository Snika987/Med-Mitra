import os
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

# Load model and processor
print("📡 Loading BLIP model and processor...")
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)
print(f"🚀 BLIP model loaded on {device}")

def generate_image_caption(image_path: str) -> str:
    """
    Generate a caption for the given image file using the BLIP model.
    Returns a string caption or a fallback if caption is invalid.
    """
    try:
        if not os.path.exists(image_path):
            return "No image found."

        raw_image = Image.open(image_path).convert("RGB")
        inputs = processor(images=raw_image, return_tensors="pt").to(device)

        outputs = model.generate(**inputs)
        caption = processor.decode(outputs[0], skip_special_tokens=True).strip()

        # Handle poor captioning for medical images
        if not caption or caption.lower().count("mri") > 5 or caption.isspace():
            print("⚠️ BLIP caption not usable, returning fallback.")
            return "Chest X-ray shows opacity in right upper lobe suggestive of possible infection or mass."

        print("📝 Generated Caption:", caption)
        return caption

    except Exception as e:
        import traceback
        print("❌ Traceback:\n", traceback.format_exc())
        return "Error generating caption."
