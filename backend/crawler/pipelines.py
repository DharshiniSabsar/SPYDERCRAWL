from db.mongo import MongoDB
import requests

class MongoPipeline:
    def open_spider(self, spider):
        self.db = MongoDB()

    def process_item(self, item, spider):
        item = dict(item)

        image_urls = item.get("images", [])
        image_ids = []

        for i, url in enumerate(image_urls):
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    image_id = self.db.store_image(
                        response.content,
                        filename=f"{item.get('vendor')}_{i}.jpg"
                    )
                    image_ids.append(str(image_id))
            except Exception:
                continue

        # Replace URLs with stored IDs
        item["image_ids"] = image_ids
        item.pop("images", None)

        self.db.insert_raw(item)
        return item