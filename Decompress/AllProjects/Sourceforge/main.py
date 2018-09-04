
from scrapy import cmdline

if __name__ == '__main__':
    #cmdline.execute("scrapy crawl OschinaSpider".split())
    cmdline.execute("scrapy crawl sourceforge".split())
    #cmdline.execute("scrapy runspider ./spiders/GolangSpider.py".split())
