# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from pymongo import MongoClient
import gridfs


class PokySpiderPipeline(object):
    db = MongoClient().poky
    fs = gridfs.GridFS(db)

    def process_item(self, item, spider):
        fid = self.fs.put(item['body'])
        documents = self.db.documents
        links = item['links']
        linkids = []
        for link in links:
            document = documents.find_one({'url': link})
            if document is None:
                document = {'url': link}
                document_id = documents.insert(document)
            else:
                document_id = document['_id']
            linkids.append(document_id)

        url = item["url"]
        document = documents.find_one({'url': url})
        if document is None:
            document = {}
        document['url'] = url
        document['links'] = linkids
        document['text'] = item['text']
        document['body'] = fid
        documents.save(document)

        return item
