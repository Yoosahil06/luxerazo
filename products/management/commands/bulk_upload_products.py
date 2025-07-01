import csv
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from products.models import Product, Brand, Category, ProductVariant
from decimal import Decimal

class Command(BaseCommand):
    help = 'Bulk upload products from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                created_count = 0
                error_count = 0
                
                for row in reader:
                    try:
                        # Get or create brand
                        brand_name = row.get('brand', '').strip()
                        if brand_name:
                            brand, _ = Brand.objects.get_or_create(
                                name=brand_name,
                                defaults={'slug': slugify(brand_name)}
                            )
                        else:
                            self.stdout.write(
                                self.style.WARNING(f'No brand specified for product: {row.get("name", "Unknown")}')
                            )
                            continue

                        # Get or create category
                        category_name = row.get('category', '').strip()
                        if category_name:
                            category, _ = Category.objects.get_or_create(
                                name=category_name,
                                defaults={'slug': slugify(category_name)}
                            )
                        else:
                            self.stdout.write(
                                self.style.WARNING(f'No category specified for product: {row.get("name", "Unknown")}')
                            )
                            continue

                        # Create product
                        product_name = row.get('name', '').strip()
                        if not product_name:
                            self.stdout.write(
                                self.style.WARNING('Product name is required')
                            )
                            error_count += 1
                            continue

                        # Check if product already exists
                        if Product.objects.filter(name=product_name, brand=brand).exists():
                            self.stdout.write(
                                self.style.WARNING(f'Product already exists: {product_name}')
                            )
                            continue

                        product = Product.objects.create(
                            name=product_name,
                            slug=slugify(product_name),
                            brand=brand,
                            category=category,
                            description=row.get('description', ''),
                            price_in_usd=Decimal(row.get('price', '0')),
                            discount_percent=Decimal(row.get('discount_percent', '0')),
                            stock_quantity=int(row.get('stock_quantity', '0')),
                            authenticity=row.get('authenticity', 'original'),
                            materials=row.get('materials', ''),
                            dimensions=row.get('dimensions', ''),
                            care_instructions=row.get('care_instructions', ''),
                            story=row.get('story', ''),
                            gender=row.get('gender', 'Unisex'),
                            is_active=row.get('is_active', 'True').lower() == 'true',
                            is_featured=row.get('is_featured', 'False').lower() == 'true',
                            meta_title=row.get('meta_title', ''),
                            meta_description=row.get('meta_description', ''),
                        )

                        # Create variants if specified
                        variant_name = row.get('variant_name', '').strip()
                        if variant_name:
                            ProductVariant.objects.create(
                                product=product,
                                name=variant_name,
                                sku=row.get('variant_sku', f'{product.slug}-{slugify(variant_name)}'),
                                price_adjustment=Decimal(row.get('variant_price_adjustment', '0')),
                                stock_quantity=int(row.get('variant_stock_quantity', '0')),
                                color=row.get('variant_color', ''),
                                material=row.get('variant_material', ''),
                                size=row.get('variant_size', ''),
                                weight=row.get('variant_weight', ''),
                            )

                        created_count += 1
                        self.stdout.write(f'Created product: {product_name}')

                    except Exception as e:
                        error_count += 1
                        self.stdout.write(
                            self.style.ERROR(f'Error creating product {row.get("name", "Unknown")}: {str(e)}')
                        )

                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created {created_count} products. {error_count} errors.')
                )

        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'File not found: {csv_file}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error reading CSV file: {str(e)}')
            )
