import os

from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_405_METHOD_NOT_ALLOWED
from django.test import TestCase
from django.core.management import call_command
from django.urls import reverse

from shop.models import *


class AbstractBaseTestClass:
    """ Abstract class for populating the database and getting URLs using Django reverse """

    @classmethod
    def setUpTestData(cls):
        test_data_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test_data/')
        call_command('populate_data', path=test_data_path)

    def get_url(self, date='2019-08-01'):
        return reverse('report_view', kwargs={'date': date})

    def get_response(self, date='2019-08-01'):
        return self.client.get(self.get_url(date))


class HTTPMethodTests(AbstractBaseTestClass, TestCase):
    """ Tests to confirm the correct HTTP responses are given for different requests """

    def test_invalid_url_returns_404_NOT_FOUND(self):
        url = '/shop/report/invalid_date'
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_valid_date_returns_200_OK(self):
        response = self.get_response()
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_patch_request_returns_405_METHOD_NOT_ALLOWED(self):
        response = self.client.patch(self.get_url())
        self.assertEqual(response.status_code, HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_request_returns_405_METHOD_NOT_ALLOWED(self):
        response = self.client.post(self.get_url())
        self.assertEqual(response.status_code, HTTP_405_METHOD_NOT_ALLOWED)

    def test_put_request_returns_405_METHOD_NOT_ALLOWED(self):
        response = self.client.put(self.get_url())
        self.assertEqual(response.status_code, HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_request_returns_405_METHOD_NOT_ALLOWED(self):
        response = self.client.delete(self.get_url())
        self.assertEqual(response.status_code, HTTP_405_METHOD_NOT_ALLOWED)


class DataValidationTests(AbstractBaseTestClass, TestCase):
    """ Tests to confirm the data has been read in correctly and the endpoint is returning correct values for the
    report """

    def test_data_populated(self):
        self.assertEqual(Order.objects.count(), 4)
        self.assertEqual(OrderLine.objects.count(), 4)
        self.assertEqual(Product.objects.count(), 3)
        self.assertEqual(Promotion.objects.count(), 3)
        self.assertEqual(ProductPromotion.objects.count(), 2)
        self.assertEqual(VendorCommission.objects.count(), 2)

    def test_item_total(self):
        response_data = self.get_response().json()
        self.assertEqual(response_data['items'], 25)

    def test_customer_total(self):
        response_data = self.get_response().json()
        self.assertEqual(response_data['customers'], 2)

    def test_discount_total(self):
        response_data = self.get_response().json()
        self.assertEqual(response_data['total_discount_amount'], 100)

    def test_average_discount(self):
        response_data = self.get_response().json()
        self.assertEqual(response_data['discount_rate_avg'], 0.04)

    def test_average_order_total(self):
        response_data = self.get_response().json()
        self.assertEqual(response_data['order_total_avg'], 910)

    def test_commission_total(self):
        response_data = self.get_response().json()
        self.assertEqual(response_data['commissions']['total'], 1365)

    def test_average_commissions(self):
        response_data = self.get_response().json()
        self.assertEqual(response_data['commissions']['order_average'], 455)

    def test_commission_total_per_promotion(self):
        response_data = self.get_response().json()
        promotions_results = {"1": 275, "2": 540}
        self.assertEqual(response_data['commissions']['promotions'], promotions_results)

    def test_no_data_report(self):
        response_data = self.get_response(date='2019-07-01').json()
        expected_response = {
            "customers": 0,
            "total_discount_amount": 0,
            "items": 0,
            "order_total_avg": 0,
            "discount_rate_avg": 0,
            "commissions": {
                "promotions": {},
                "total": 0,
                "order_average": 0
            }
        }
        self.assertEqual(response_data, expected_response)
