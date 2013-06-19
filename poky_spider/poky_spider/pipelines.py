# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html


class PokySpiderPipeline(object):

    def process_item(self, item, spider):
        # store links (forward and reverse)
        # build reverse table
        return item
