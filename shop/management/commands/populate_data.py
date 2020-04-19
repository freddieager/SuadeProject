import logging
import os
import csv
from collections import OrderedDict

from django.core.management.base import BaseCommand

from shop import models

DEFAULT_DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../sample_data/')
models_csv_mapping = OrderedDict([(models.Product, 'products.csv'),
                                  (models.Promotion, 'promotions.csv'),
                                  (models.ProductPromotion, 'product_promotions.csv'),
                                  (models.VendorCommission, 'commissions.csv'),
                                  (models.Order, 'orders.csv'),
                                  (models.OrderLine, 'order_lines.csv')])


class Command(BaseCommand):
    help = " Populates the database with data from csvs. The path to the directory the data is stored in can be passed " \
           "as an argument, otherwise it will default to 'shop/sample_data/' "

    def add_arguments(self, parser):
        parser.add_argument('-p', '--path', type=str, help="Specify the data directory")

    def handle(self, *args, **options):
        data_path = options.get('path')
        if not data_path:
            data_path = DEFAULT_DATA_PATH
        for model, csv_name in models_csv_mapping.items():
            with open(os.path.join(data_path, csv_name)) as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    model.objects.create(**row)
