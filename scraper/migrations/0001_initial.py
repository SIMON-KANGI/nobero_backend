# Generated by Django 5.1 on 2024-08-21 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SKU',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=100)),
                ('size', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(default='Uncategorized', max_length=255)),
                ('url', models.URLField(default='Unknown', unique=True)),
                ('title', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('MRP', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('img', models.URLField(blank=True, null=True)),
                ('last_7_day_sale', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('fit', models.CharField(default='Unknown', max_length=100)),
                ('fabric', models.CharField(default='Unknown', max_length=100)),
                ('neck', models.CharField(default='Unknown', max_length=100)),
                ('sleeve', models.CharField(default='Unknown', max_length=100)),
                ('pattern', models.CharField(default='Unknown', max_length=100)),
                ('length', models.CharField(default='Unknown', max_length=100)),
                ('description', models.TextField()),
                ('available_skus', models.ManyToManyField(related_name='products', to='scraper.sku')),
            ],
        ),
    ]
