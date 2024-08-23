import scrapy
from bs4 import BeautifulSoup
from scraper.models import Product, SKU
import re
from scrapy_selenium import SeleniumRequest

class NoberoSpider(scrapy.Spider):
    name = 'nobero'
    allowed_domains = ['nobero.com']
    start_urls = [
        'https://nobero.com/collections/mens-oversized-tees',
        'https://nobero.com/collections/fashion-joggers-men',
        'https://nobero.com/collections/best-selling-co-ord-sets'
        
        
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):
        # Parse the main collection page
        self.logger.info('Parsing collection page: %s', response.url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract product links
        product_links = [a['href'] for a in soup.select('a.product_link') if a.has_attr('href')]
        self.logger.info(f'Found {len(product_links)} product links')

        # Follow each product link
        for link in product_links:
            full_link = response.urljoin(link)
            yield scrapy.Request(full_link, callback=self.parse_product)

        # Follow pagination link if available
        next_page = soup.select_one('a.pagination__next')
        if next_page and next_page.has_attr('href'):
            next_page_url = response.urljoin(next_page['href'])
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_product(self, response):
        # Parse individual product page
        self.logger.info('Parsing product page: %s', response.url)
        soup = BeautifulSoup(response.text, 'html.parser')

       
        category_element = soup.select_one('h1.list-title')
        category = category_element.get_text(strip=True) if category_element else 'Unknown'

        self.logger.info(f'Extracted category: {category}')

        # Extract image URL
        img_element = soup.select_one('img.image-placeholder-bg')
        img_url = img_element.get('src', '') or img_element.get('srcset', '').split()[0] if img_element else 'No Image'
        img_url = response.urljoin(img_url) if img_url != 'No Image' else img_url

        # Extract price and MRP
        price = self.extract_price(soup.select_one('#variant-price'))
        mrp = self.extract_price(soup.select_one('span.line-through'))

        # Extract product details
        product_data = {
            "category": category,
            "title": soup.select_one('h1.product-title').get_text(strip=True) if soup.select_one('h1.product-title') else 'No Title',
            "price": price,
            "MRP": mrp,
            "img": img_url,
            "last_7_day_sale": self.extract_sale(soup.select_one('div.price-drop')),
            "fit": self.extract_detail(soup.select_one('div.product-details span[data-fit]')),
            "fabric": self.extract_detail(soup.select_one('div.product-details span[data-fabric]')),
            "neck": self.extract_detail(soup.select_one('div.product-details span[data-neck]')),
            "sleeve": self.extract_detail(soup.select_one('div.product-details span[data-sleeve]')),
            "pattern": self.extract_detail(soup.select_one('div.product-details span[data-pattern]')),
            "length": self.extract_detail(soup.select_one('div.product-details span[data-length]')),
            "description": "\n".join(p.get_text(strip=True) for p in soup.select('div.product-description p')) or 'No Description'
        }

        # Create or update product record in the database
        product, created = Product.objects.get_or_create(url=response.url, defaults=product_data)
        if created:
            self.logger.info(f'Created new product: {product.title}')
        else:
            self.logger.info(f'Updated existing product: {product.title}')

        # Handle SKUs (colors and sizes)
        self.handle_skus(soup, product)

        product.save()
        self.logger.info(f'Saved product with URL: {response.url}')


#if the price is a string convert to float
    def extract_price(self, element):
        """ Extract price from element and convert to float. """
        if element:
            price_text = element.get_text(strip=True)
            price_clean = re.sub(r'[^\d.]', '', price_text)
            try:                                             
                return float(price_clean)
            except ValueError:
                self.logger.error(f'Invalid price format: {price_clean}')
        return 0.00

    def extract_sale(self, element):
        """ Extract sale price and convert to float. """
        if element:
            sale_text = element.get_text(strip=True)
            sale_clean = re.sub(r'[^\d.]', '', sale_text)
            try:
                return float(sale_clean)
            except ValueError:
                self.logger.error(f'Invalid sale price format: {sale_clean}')
        return 0.00
#extract the product details
    def extract_detail(self, element):
        """ Extract product detail if available, otherwise return 'Unknown'. """
        return element.get_text(strip=True) if element else 'Unknown'

    def handle_skus(self, soup, product):
        """ Handle SKU creation and association. """
        colors = [option.get_text(strip=True) for option in soup.select('span.color-label')]
        for color in colors:
            sizes = [size.get_text(strip=True) for size in soup.select('label.size-select')]
            for size in sizes:
                sku, _ = SKU.objects.get_or_create(color=color, size=size)
                product.available_skus.add(sku)
