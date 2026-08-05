for record in raw_records:
    description = record.get("description", "")
    image_ids = record.get("image_ids", [])   # ✅ from DB

    # --- TEXT THREAT ---
    text_threat = classify_threat(description)

    # --- IMAGE THREAT ---
    image_threats = []

    for img_id in image_ids:
        image = load_image_from_db(img_id)
        if image:
            image_threats.append(
                classify_image_from_pil(image)
            )

    # --- FUSION ---
    all_levels = [text_threat] + image_threats

    if "HIGH" in all_levels:
        final_threat = "HIGH"
    elif "MEDIUM" in all_levels:
        final_threat = "MEDIUM"
    else:
        final_threat = "LOW"

    processed = {
        "title": record.get("title"),
        "vendor": record.get("vendor"),
        "price": record.get("price"),
        "url": record.get("url"),
        "description": description,
        "image_ids": image_ids,   # ✅ keep IDs
        "threat_level": final_threat,
    }

    db.insert_processed(processed)