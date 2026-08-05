import torch
from PIL import Image
import requests
from transformers import CLIPProcessor, CLIPModel

MODEL_NAME = "openai/clip-vit-base-patch32"

print("🔄 Loading CLIP model...")

model = CLIPModel.from_pretrained(MODEL_NAME)
processor = CLIPProcessor.from_pretrained(MODEL_NAME)

model.eval()

print("✅ CLIP model loaded")


LABELS = [
    "laboratory experiment",
    "genetic engineering",
    "biohacking setup",
    "medical research",
    "dangerous biological experiment",
    "normal daily activity"
]


# ---------------- BASIC CLASSIFIER ----------------
def classify_image_from_pil(image):
    inputs = processor(
        text=LABELS,
        images=image,
        return_tensors="pt",
        padding=True
    )

    with torch.no_grad():
        outputs = model(**inputs)

    probs = outputs.logits_per_image.softmax(dim=1)[0]
    label = LABELS[probs.argmax().item()]

    if "dangerous" in label or "biohacking" in label:
        return "HIGH"
    elif "lab" in label or "genetic" in label:
        return "MEDIUM"
    return "LOW"


# ---------------- NEW: WITH REASON + CONFIDENCE ----------------
def classify_image_with_reason(image):
    try:
        inputs = processor(
            text=LABELS,
            images=image,
            return_tensors="pt",
            padding=True
        )

        with torch.no_grad():
            outputs = model(**inputs)

        probs = outputs.logits_per_image.softmax(dim=1)[0]

        best_idx = probs.argmax().item()
        label = LABELS[best_idx]
        confidence = probs[best_idx].item()

        if "dangerous" in label or "biohacking" in label:
            threat = "HIGH"
        elif "lab" in label or "genetic" in label:
            threat = "MEDIUM"
        else:
            threat = "LOW"

        return threat, label, confidence

    except Exception as e:
        raise RuntimeError(f"Classification failed: {e}")