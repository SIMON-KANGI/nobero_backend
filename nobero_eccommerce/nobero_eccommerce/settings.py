import sys
import os
import django
from pathlib import Path

from shutil import which
# Path to your scraper directory
SCRAPER_DIR = Path('/home/simon/nobero/nobero_api/scraper')
if str(SCRAPER_DIR) not in sys.path:
    sys.path.append(str(SCRAPER_DIR))

# Path to your Django project
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nobero_eccommerce.settings')
django.setup()

# Scrapy settings
ITEM_PIPELINES = {
    'nobero_eccommerce.pipelines.DjangoPipeline': 300,  # Correct the pipeline path here
}



BOT_NAME = "nobero_eccommerce"

SPIDER_MODULES = ["nobero_eccommerce.spiders"]
NEWSPIDER_MODULE = "nobero_eccommerce.spiders"

ROBOTSTXT_OBEY = True
##selenium settings
SELENIUM_DRIVER_NAME = 'chrome'
SELENIUM_DRIVER_EXECUTABLE_PATH = which('chromedriver')
SELENIUM_DRIVER_ARGUMENTS = ['--headless']  # '--headless' if using a headless browser

DOWNLOADER_MIDDLEWARES = {
    'scrapy_selenium.SeleniumMiddleware': 800,
}

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
