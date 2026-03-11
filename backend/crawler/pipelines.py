from db.mongo import MongoDB

class MongoPipeline:
    def open_spider(self, spider):
        self.db = MongoDB()

    def process_item(self, item, spider):
        self.db.insert_raw(dict(item))
        return item
