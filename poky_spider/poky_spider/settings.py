# Scrapy settings for poky_spider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'poky_spider'

SPIDER_MODULES = ['poky_spider.spiders']
NEWSPIDER_MODULE = 'poky_spider.spiders'
DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleFifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.FifoMemoryQueue'
ITEM_PIPELINES = [
    'poky_spider.pipelines.PokySpiderPipeline',
]
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'poky_spider (+http://www.yourdomain.com)'
