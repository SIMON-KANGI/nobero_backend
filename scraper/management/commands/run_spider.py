# scraper/management/commands/run_spider.py

from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
# from nobero_eccommerce.spiders.noberospider import NoberoSpider
from nobero_eccommerce.nobero_eccommerce.spiders.noberospider import NoberoSpider


class Command(BaseCommand):
    help = 'Runs the Scrapy spider and saves the scraped data to the database'

    def handle(self, *args, **kwargs):
        process = CrawlerProcess(get_project_settings())
        process.crawl(NoberoSpider)  
        process.start()
