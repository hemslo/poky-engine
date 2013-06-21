poky-engine
===========

A simple search engine in python using Tornado, Scrapy, Redis and MongoDB


Requirements
------------

`Redis <http://redis.io/topics/quickstart>`_

`MongoDB <http://www.mongodb.org/downloads>`_

Installation
------------

    pip install tornado Scrapy redis pymongo jieba stemming

Run
---

Crawl

    cd /path/to/poky_spider

    scrapy crawl PokySpider url  # defautl start url is http://www.seu.edu.cn

Build inverse table

    cd /path/to/indexer

    python InverseTable.py

Compute PageRank

    cd /path/to/indexer

    python PageRank.py

Run Web Server

    python app.py  # default url is http://localhost:8888

Help
----

    python app.py --help
