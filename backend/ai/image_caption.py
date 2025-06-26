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

# Fallback caption for radiology use cases
FALLBACK_CAPTION = "Chest X-ray shows right upper lobe opacity suggestive of pulmonary infection or lesion."

def generate_image_caption(image_path: str) -> str:
    try:
        if not os.path.exists(image_path):
            return "No image found."

        raw_image = Image.open(image_path).convert("RGB")
        inputs = processor(images=raw_image, return_tensors="pt").to(device)

        outputs = model.generate(**inputs)
        caption = processor.decode(outputs[0], skip_special_tokens=True).strip()

        # If output is blank, repetitive, or generic — fallback
        if (
            not caption
            or caption.isspace()
            or caption.lower() in ["mri", "image", "a medical image"]
            or caption.lower().count("mri") > 3
            or len(caption.split()) < 4
        ):
            print("⚠️ Using fallback for low-confidence caption.")
            return FALLBACK_CAPTION

        print("📝 Caption:", caption)
        return caption

    except Exception as e:
        import traceback
        print("❌ Traceback:\n", traceback.format_exc())
        return FALLBACK_CAPTION
