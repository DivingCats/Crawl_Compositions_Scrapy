from scrapy import cmdline
cmdline.execute("scrapy crawl myspider_redis".split())
# cmdline.execute("scrapy crawl basic --nolog".split())