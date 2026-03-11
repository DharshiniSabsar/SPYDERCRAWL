def send_alert(record):
    level = record.get("threat_level", "UNKNOWN")
    title = record.get("title", "Untitled")

    if level == "HIGH":
        print("🚨 ALERT: High-risk bio-hacking listing detected")
        print("   →", title)

    elif level == "MEDIUM":
        print("⚠️ WARNING: Medium-risk listing detected")
        print("   →", title)

    elif level == "LOW":
        print("ℹ️ INFO: Low-risk listing detected")
        print("   →", title)

    else:
        print("❓ UNKNOWN threat level")
        print("   →", title)
