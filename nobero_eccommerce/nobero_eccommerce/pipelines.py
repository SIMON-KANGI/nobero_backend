# pipelines.py
from scrapy.exceptions import DropItem
from scraper.models import Product, SKU

class DjangoPipeline:
    def process_item(self, item, spider):
        # Check if the item is a dictionary
        if isinstance(item, dict):
            # Extract product data
            product_data = item
            # Update or create a product entry in the database
            product, created = Product.objects.update_or_create(
                url=product_data.get('url'),
                defaults={
                    "category": product_data.get('category'),
                    "title": product_data.get('title'),
                    "price": product_data.get('price'),
                    "MRP": product_data.get('MRP'),
                    "last_7_day_sale": product_data.get('last_7_day_sale'),
                    "fit": product_data.get('fit'),
                    "fabric": product_data.get('fabric'),
                    "neck": product_data.get('neck'),
                    "sleeve": product_data.get('sleeve'),
                    "pattern": product_data.get('pattern'),
                    "length": product_data.get('length'),
                    "description": product_data.get('description'),
                }
            )

            # Handle SKUs
            for sku_data in product_data.get('available_skus', []):
                sku, _ = SKU.objects.get_or_create(color=sku_data['color'], size=sku_data['size'])
                product.available_skus.add(sku)
            
            # Save product with its SKUs
            product.save()
        else:
            # Drop items that are not dictionaries
            raise DropItem(f"Invalid item format: {item}")

        return item
