import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel

MODEL_NAME = "nlpaueb/sec-bert-base"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)
model.eval()

# --- Threat anchor texts (domain knowledge) ---
THREAT_PROFILES = {
    "HIGH": [
        "illegal biohacking",
        "black market crispr",
        "rogue biolab",
        "illicit genetic modification",
        "gain of function research",
        "underground biotech trade",
    ],
    "MEDIUM": [
        "biohacking tools",
        "genetic engineering kits",
        "synthetic biology experiments",
        "nootropic compounds",
    ],
    "LOW": [
        "academic biotechnology research",
        "health optimization",
        "longevity studies",
        "bioinformatics research",
    ],
}

def embed(text: str) -> torch.Tensor:
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )
    with torch.no_grad():
        output = model(**inputs).last_hidden_state[:, 0, :]
    return F.normalize(output, dim=1)

# --- Precompute anchor embeddings ---
ANCHOR_EMBEDS = {
    level: torch.mean(
        torch.cat([embed(t) for t in texts]),
        dim=0,
        keepdim=True,
    )
    for level, texts in THREAT_PROFILES.items()
}

def classify_threat(text: str) -> str:
    if not text or len(text.strip()) < 20:
        return "LOW"

    text_emb = embed(text)

    scores = {
        level: F.cosine_similarity(text_emb, anchor_emb).item()
        for level, anchor_emb in ANCHOR_EMBEDS.items()
    }

    return max(scores, key=scores.get)


